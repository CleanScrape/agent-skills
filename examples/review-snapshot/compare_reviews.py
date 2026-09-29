"""Compare two local CleanScrape app-review exports. Python 3.10+, stdlib only.

No network, credentials, AI calls, telemetry or source-file changes.
"""

import argparse
import csv
import html
import json
import math
from collections import Counter
from pathlib import Path


MAX_BYTES = 50 * 1024 * 1024
MAX_ROWS = 200_000
FIELDS = ("rating", "title", "text", "date", "appVersion",
          "developerReply", "developerReplyDate")
KEY_FIELDS = ("source", "appId", "country", "language", "reviewId")
NOTES = [
    "Coverage is unknown: these files alone do not establish collection completeness.",
    "Newly observed does not mean newly published. Missing from the later sample does not mean deleted.",
    "Ratings describe unambiguous, identifiable reviews in these samples, not an app's overall Store rating.",
    "Missing identity and conflicting duplicate IDs are excluded rather than guessed.",
    "Country is the requested storefront; language is the requested language, not detected reviewer language.",
    "Apple review dates can be update times. This tool does not infer release effects or sentiment themes.",
    "Compare exports collected with the same app, country, language, sort and limits; those settings are not all recoverable from rows.",
]


def atom(value):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        return None
    text = str(value).strip()
    return text or None


def identity(row):
    source = (atom(row.get("source")) or "").lower()
    app = atom(row.get("appId"))
    country = (atom(row.get("country")) or "").lower()
    review = atom(row.get("reviewId"))
    language = atom(row.get("language"))
    if source not in ("app_store", "google_play") or not app or not review:
        return None
    if len(country) != 2 or not country.isascii() or not country.isalpha():
        return None
    # None stays distinct from an explicitly supplied language such as "unknown".
    return source, app, country, language.lower() if language else None, review


def rating(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    try:
        number = float(value)
    except (ValueError, OverflowError):
        return None
    if math.isfinite(number) and number.is_integer() and 1 <= number <= 5:
        return int(number)
    return None


def payload(row):
    result = {field: row.get(field) for field in FIELDS}
    parsed = rating(result["rating"])
    if parsed is not None:
        result["rating"] = parsed
    return result


def key_order(key):
    return tuple("" if part is None else part for part in key)


def reference(key):
    return dict(zip(KEY_FIELDS, key))


def index_rows(rows):
    if not isinstance(rows, list) or len(rows) > MAX_ROWS:
        raise ValueError("Use a JSON array with at most 200,000 review objects.")
    records, seen, conflicts = {}, {}, set()
    unresolved = duplicates = 0
    for position, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise ValueError(f"Row {position} is not a review object.")
        key = identity(row)
        if key is None:
            unresolved += 1
            continue
        value = payload(row)
        fingerprint = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
        variants = seen.setdefault(key, set())
        if fingerprint in variants:
            duplicates += 1
        variants.add(fingerprint)
        if len(variants) > 1:
            conflicts.add(key)
            records.pop(key, None)
        elif key not in conflicts:
            records[key] = value
    return {"records": records, "conflicts": conflicts, "rows": len(rows),
            "unresolved_rows": unresolved, "duplicate_rows": duplicates}


def summarise(index):
    groups = {}
    for key, row in index["records"].items():
        group = key[:4]
        bucket = groups.setdefault(group, {"reviews": 0, "ratings": Counter(), "invalid_ratings": 0})
        bucket["reviews"] += 1
        number = rating(row["rating"])
        if number is None:
            bucket["invalid_ratings"] += 1
        else:
            bucket["ratings"][number] += 1
    result = []
    for key in sorted(groups, key=key_order):
        bucket = groups[key]
        counts = bucket["ratings"]
        valid = sum(counts.values())
        low = counts[1] + counts[2]
        result.append({**dict(zip(KEY_FIELDS[:4], key)), "reviews": bucket["reviews"],
                       "valid_ratings": valid, "invalid_ratings": bucket["invalid_ratings"],
                       "star_counts": {str(i): counts[i] for i in range(1, 6)},
                       "low_ratings": low, "low_rating_share": low / valid if valid else None})
    return {"input_rows": index["rows"], "identified_reviews": len(index["records"]),
            "unresolved_rows": index["unresolved_rows"],
            "repeated_equivalent_rows": index["duplicate_rows"],
            "conflicting_keys": len(index["conflicts"]), "groups": result}


def compare(before, after, synthetic=False):
    left, right = index_rows(before), index_rows(after)
    ambiguous = left["conflicts"] | right["conflicts"]
    old, new = left["records"], right["records"]
    changes = []
    counts = Counter()
    for key in sorted((set(old) | set(new)) - ambiguous, key=key_order):
        fields = []
        if key not in old:
            status = "newly_observed"
        elif key not in new:
            status = "missing_from_later_sample"
        else:
            fields = [f for f in FIELDS if old[key][f] != new[key][f]]
            status = "changed" if fields else "unchanged"
        counts[status] += 1
        if status != "unchanged":
            changes.append({**reference(key), "status": status, "changed_fields": fields,
                            "before_rating": rating(old[key]["rating"]) if key in old else None,
                            "after_rating": rating(new[key]["rating"]) if key in new else None})
    return {"format_version": 1, "synthetic_example": synthetic, "coverage": "unknown",
            "before": summarise(left), "after": summarise(right),
            "counts": {s: counts[s] for s in ("newly_observed", "changed", "unchanged", "missing_from_later_sample")},
            "ambiguous_keys_excluded_from_comparison": len(ambiguous),
            "ambiguous_keys": [reference(k) for k in sorted(ambiguous, key=key_order)],
            "changes": changes, "notes": NOTES}


def reject_constant(value):
    raise ValueError(f"Non-standard JSON number {value}; export valid JSON first.")


def load_rows(path):
    with path.open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Each input must be 50 MiB or smaller.")
    return json.loads(data.decode("utf-8-sig"), parse_constant=reject_constant)


def md(value):
    text = html.escape("unknown" if value is None else str(value)).replace("\n", " ").replace("\r", " ")
    for char in ("\\", "`", "*", "_", "[", "]", "|", "!"):
        text = text.replace(char, "\\" + char)
    return text


def markdown(report):
    lines = ["# App review snapshot comparison", ""]
    if report["synthetic_example"]:
        lines += ["**Synthetic demonstration. Not real app feedback or evidence of customer demand.**", ""]
    lines += ["Two saved exports, compared locally. No fresh collection or model call.", "", "## What changed", ""]
    for label, count in report["counts"].items():
        lines.append(f"- {label.replace('_', ' ').capitalize()}: {count}")
    lines += [f"- Ambiguous keys excluded from comparison: {report['ambiguous_keys_excluded_from_comparison']}", ""]
    for name in ("before", "after"):
        sample = report[name]
        lines += [f"## {name.capitalize()} sample", "",
                  f"{sample['input_rows']} rows; {sample['identified_reviews']} identifiable, unambiguous reviews.", "",
                  f"Unresolved rows: {sample['unresolved_rows']}. Repeated equivalent rows: {sample['repeated_equivalent_rows']}. Conflicting keys: {sample['conflicting_keys']}.", "",
                  "| Store | App | Country | Request language | Reviews | Valid ratings | 1-2 stars | Share of valid ratings |",
                  "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |"]
        for g in sample["groups"]:
            share = "n/a" if g["low_rating_share"] is None else f"{g['low_rating_share']:.1%}"
            cells = [g["source"], g["appId"], g["country"], g["language"], g["reviews"], g["valid_ratings"], g["low_ratings"], share]
            lines.append("| " + " | ".join(md(c) for c in cells) + " |")
        lines.append("")
    lines += ["## Read this before drawing conclusions", ""] + ["- " + note for note in report["notes"]]
    lines += ["", "`changes.csv` contains IDs and changed field names, not reviewer names or review text.",
              "Keep the source files private and inspect the identified records before deciding what to do.", ""]
    return "\n".join(lines)


def csv_cell(value):
    text = "" if value is None else str(value)
    # Neutralise formula prefixes, including those hidden behind whitespace.
    if text.lstrip().startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r", "\n")):
        return "'" + text
    return text


def write_report(report, out):
    out.mkdir(parents=True, exist_ok=False)
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    (out / "report.md").write_text(markdown(report), encoding="utf-8")
    columns = (*KEY_FIELDS, "status", "changed_fields", "before_rating", "after_rating")
    with (out / "changes.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for item in report["changes"]:
            row = {**item, "changed_fields": ", ".join(item["changed_fields"])}
            writer.writerow({key: csv_cell(value) for key, value in row.items()})


def demo_rows():
    common = {"source": "google_play", "appId": "demo.app", "country": "us", "language": "en"}
    a = {**common, "reviewId": "demo-a", "rating": 2, "text": "Synthetic example: sign-in failed."}
    b = {**common, "reviewId": "demo-b", "rating": 5, "text": "Synthetic example: worked well."}
    c = {**common, "reviewId": "demo-c", "rating": 1, "text": "Synthetic example: download failed."}
    d = {"source": "app_store", "appId": "demo-ios", "country": "us", "language": None,
         "reviewId": "demo-d", "rating": 4, "text": "Synthetic example: useful."}
    return [a, a.copy(), b, d], [{**a, "rating": 4, "text": "Synthetic example: sign-in now works."}, c, d]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path, nargs="?")
    parser.add_argument("after", type=Path, nargs="?")
    parser.add_argument("--out", type=Path, required=True, help="New output directory; existing directories are never overwritten.")
    parser.add_argument("--demo", action="store_true", help="Use tiny synthetic examples instead of real files.")
    args = parser.parse_args(argv)
    if args.demo and (args.before or args.after):
        parser.error("Use --demo without input files.")
    if not args.demo and (args.before is None or args.after is None):
        parser.error("Provide before.json and after.json, or use --demo.")
    try:
        before, after = demo_rows() if args.demo else (load_rows(args.before), load_rows(args.after))
        report = compare(before, after, synthetic=args.demo)
        write_report(report, args.out)
    except (OSError, ValueError, UnicodeError, RecursionError) as error:
        parser.exit(2, f"Cannot create report: {error}\n")
    print(f"Created report.md, report.json and changes.csv in {args.out}")


if __name__ == "__main__":
    main()
