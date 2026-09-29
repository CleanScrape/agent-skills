# What changed in your app reviews?

Compare two saved App Store / Google Play review exports without starting another scrape. This small Python script finds newly observed IDs, changed fields and reviews missing from the later sample. It also shows rating counts separately for each store, app, country and requested language.

**Free, local, no API key.** Python 3.10 or newer, with no packages to install, network requests, AI model calls or telemetry. It does not change your source files. The script and its tests are MIT licensed.

## Try the example

Download this folder, open a terminal in it, and run:

```bash
python compare_reviews.py --demo --out demo-report
```

The demonstration is explicitly synthetic. You should get one newly observed review, one changed review, one unchanged review and one missing from the later sample. A repeated row is counted once. This is a way to try the workflow, not real feedback about an app.

Open `demo-report/report.md` for the readable summary. `report.json` has the full counts, and `changes.csv` lists the affected IDs and changed field names. Use a new output folder for each run; existing folders are never overwritten.

## Use your own exports

1. In your completed Apify run, export the dataset as **JSON**, with all fields. Use two saved exports of the same app and collection settings. No new run is needed if you already have both files.
2. Keep the files on your computer as `before.json` and `after.json`. Do not upload review collections or API tokens to a public repository.
3. Run:

```bash
python compare_reviews.py before.json after.json --out review-comparison
```

On Windows, `py` can be used instead of `python` if that is your installed Python command. Inputs must be JSON arrays, at most 50 MiB and 200,000 rows each. CSV input is not supported: JSON preserves IDs, nulls and review text more reliably.

The expected fields are the [CleanScrape app-review export](https://apify.com/cleanscrape/app-store-reviews-scraper): `source`, `appId`, `country`, `language`, `reviewId`, `rating`, `title`, `text`, `date`, `appVersion`, `developerReply` and `developerReplyDate`. Extra fields are ignored. Other providers can work if you explicitly map their fields to this format; this script does not guess mappings.

## Read the result correctly

| Result | What it tells you |
| --- | --- |
| Newly observed | An identifiable review is in the later file but not the earlier one. It may have been published earlier. |
| Changed | The same ID and request context has a different rating, text, title, date, app version or developer reply. The changed fields are listed. |
| Missing from later sample | The later file does not contain that ID. It is **not evidence of deletion**. |
| Unresolved | A row lacks a usable source, app ID, country or review ID. It is excluded, not matched by similar text. |
| Conflicting key | One file has different review payloads under the same identity. That key is excluded from the comparison. |

Identity includes source, app ID, country, request language and review ID. A missing language remains distinct from a supplied language. Ratings accept only whole values from 1 to 5. The low-rating share uses valid ratings from identifiable, unambiguous reviews, not every input row. A zero denominator is shown as `n/a`, never zero percent.

Your two exports still need comparable collection settings. Different sorting, limits or time windows can produce a different sample without any change in customer sentiment. The script cannot recover all those settings or establish completeness from the rows, so coverage is always labelled unknown. Check the original `RUN_REPORT` yourself. Apple's review timestamp can reflect an edit rather than original publication.

For a product-team review, inspect the changed IDs and read the matching comments in your private source files. Then use the [app-review skill](../../skills/apify-cleanscrape-app-reviews/SKILL.md) if you want an assistant to group recurring issues with evidence. The deterministic script itself does not label sentiment or invent themes.

## Privacy and safety

Generated files contain IDs, rating aggregates and changed field names, not reviewer names or full review text. Treat the report as private nonetheless. Spreadsheet formula prefixes are neutralised in `changes.csv`; import ID columns as text to preserve long numeric IDs. The JSON report preserves the IDs without spreadsheet escaping.

No schedule or alert is created. Repeating the analysis of saved files is free; collecting new reviews through Apify is a separate paid action. Your chosen assistant may also have usage charges.

## Run the checks

```bash
python -m unittest -v test_compare_reviews.py
```

The suite uses synthetic fixtures only. It checks identity separation, ambiguous duplicates, edits, missing IDs, invalid ratings, privacy, safe output and complete command-line runs. It does not test live scraping or claim to measure customer demand.

Maintained by [CleanScrape](https://apify.com/cleanscrape). We earn revenue from the paid Actor linked above; this local example is free and has no affiliate links. For a reproducible problem, [open an issue](https://github.com/CleanScrape/agent-skills/issues) with a small synthetic example, not private customer data.
