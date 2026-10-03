# Validation notes

Checked on 29 September 2026.

This is a maintainer test summary, not a security certification or a guarantee of live source availability.

## What was checked

| Check | Observed result |
| --- | --- |
| Format and safety-documentation checks | 128 local assertions passed across eight skills |
| Example inputs | All eight JSON examples passed validation against the saved published input schemas, with no unknown input keys |
| Installation | skills CLI 1.7.0 found and installed all eight skills into an isolated local project for Codex |
| Installed contents | All eight installed SKILL.md files matched their source files |
| Existing-export use | Two independently executed assistant walkthroughs for Reviews and Trends, plus six maintainer-run local data walkthroughs and a separate content review |
| Cost and production changes | No Actor runs, builds, proxy traffic or paid model API calls; no live Actor code, schema or pricing changes |

The installer used a local source folder, --copy and project scope, with telemetry disabled. The GitHub download path and every supported assistant were not separately installed or tested. The skills themselves contain documentation only, with no bundled executables or install hooks.

The format check follows the current [Agent Skills specification](https://agentskills.io/specification), including its compatibility field.

## Existing-export cases

All inputs for these checks were explicitly synthetic, not customer records or new source collections.

| Skill | Cases exercised |
| --- | --- |
| App reviews | Exact duplicates, edited and newly observed reviews, unresolved identity, missing rating, invalid date and absent run report |
| Google Trends | Non-timeline rows, incomplete intervals, exact duplicates, invalid timestamps, null versus zero, incompatible contexts and untrusted query text |
| Map Your Show | Duplicate deliveries, separate events with the same company name, multiple booths, category-only details and directory absence versus business closure |
| Shopify reviews | Provider-aware identity, grouped reviews about another product, ratings-only feedback, unknown attribution and formula-leading text |
| Google News | Duplicate article identities, matching headlines from different publishers, unresolved links, missing dates and snippet-only evidence |
| Pinterest | Duplicate pins, unknown destinations, source attribution, missing counts versus zero and saves versus views |
| Google Hotels | Different stay dates and currencies, nightly versus total prices, unknown room equivalence and missing quotes |
| TikTok Shop | Long string IDs, repeated products, unavailable versus unknown stock, missing prices, shipping and source-selected review previews |

Embedded requests to run paid tools, reveal credentials, download media or make purchases were treated as data. No such action occurred. This bounded offline exercise does not establish resistance to every prompt injection.

## Important limits

- These checks validate the documented local workflows and example inputs, not the current operation of the commercial scrapers.
- Fresh collection, authentication, server-side spending enforcement, rate limits and restart behaviour were not exercised in this skills release.
- The handmade Pinterest and TikTok fixtures used simplified link-field aliases. Their analysis is an incomplete-import case, not proof of production output-schema compatibility.
- Some Shopify fixture rows lacked grouping metadata. Their exact product attribution remained unknown or caveated.
- Trends duplicate handling and missing request provenance required explicit conservative choices: flag exact duplicates, do not average conflicts, and do not claim a common normalisation merely from matching country/time labels.
- A missing run report means coverage is unconfirmed. Map Your Show and Shopify use SUMMARY; the other six Actors use RUN_REPORT.
- No claim is made that these skills improve search ranking, will be selected automatically, or behave identically in every assistant.

## Published Actor references

These input-schema and documentation versions were inspected when preparing the skills:

| Actor | Build |
| --- | --- |
| App Store & Google Play Reviews | 0.3.19 |
| Google Trends | 0.3.12 |
| Map Your Show exhibitors | 0.2.10 |
| Shopify reviews | 0.4.10 |
| Google News | 0.2.16 |
| Pinterest | 0.1.10 |
| Google Hotels | 0.1.16 |
| TikTok Shop | 0.1.16 |

Before fresh collection, check the current Actor schema and Pricing tab and obtain an explicit positive spending cap. Installing a free skill does not make an Actor run free.



## Threads addition (2026-10-01)

The original eight-skill checks above remain historical checks of those eight skills. The new `apify-cleanscrape-threads-research` skill is a separate addition.

- Its example input passed the Threads Actor normalizer.
- Current Agent Skills specification checks passed for frontmatter keys, YAML types, field lengths, directory/name matching and a non-empty body.
- The bundled `quick_validate.py` rejects the `compatibility` key. The current specification explicitly permits that key; a specification-aligned check passed without modifying the installed validator. See https://agentskills.io/specification.
- Cost approval, positive spending limits, credential handling, untrusted source text, partial results and experimental replies are covered explicitly.
- Threads uses `SUMMARY` and `REPORT`, with `RECOVERY_POSTS` where relevant. Do not apply other Actors' report-key assumptions to it.
- A real NASA example saved 20 unique posts with 20 settled billing events. Five blank captions were link-only posts with preserved link previews. The run stopped at its configured spending cap.
- The public Actor and all three example pages returned HTTP 200 with the expected titles. A fresh run of the public 20-post example on build 0.1.7 saved 20 unique posts with 20 billing events, a valid CSV export and the corrected report.
- These checks validate the skill format, documented input and released Actor. They are not an end-to-end installation or execution test in every assistant client.

## Likee addition (2026-10-03)

The checks above remain historical checks of the earlier skills. The new `apify-cleanscrape-likee-research` skill is a separate addition.

- Its example input passed the Likee Actor normalizer (`videos`, maximum 10).
- Agent Skills specification checks passed for frontmatter keys, name format and directory match, description length (380 characters), compatibility length and a non-empty body.
- Cost approval, positive spending limits, credential handling, untrusted captions and comments, commenter names and partial results are covered explicitly.
- Likee uses `SUMMARY` and `REPORT`. Do not apply other Actors' report-key assumptions to it.
- A real run on build 0.1.10 saved 40 comments from a video on Likee's official US account; 22 of the 40 were written in Russian (one more in Tajik, also in Cyrillic). That sample is the source of the audience-language example.
- These checks validate the skill format, documented input and released Actor. They are not an end-to-end installation or execution test in every assistant client.

## Tennis addition (2026-10-03)

The checks above remain historical checks of the earlier skills. The new `apify-cleanscrape-tennis-research` skill is a separate addition.

- Its example input passed the Tennis Actor normalizer (one target, maximum 500, statistics on, ATP and WTA).
- Agent Skills specification checks passed for frontmatter keys, name format and directory match, description length (347 characters), compatibility length and a non-empty body.
- Cost approval, positive spending limits, credential handling, untrusted source text and partial results are covered explicitly.
- Tennis uses `SUMMARY` and `REPORT`. Do not apply other Actors' report-key assumptions to it.
- A real run of the public Wimbledon 2025 example saved 478 singles matches, all with full statistics. Summed over the seven men's main-draw matches each, Sinner held 93 of 99 service games and faced 23 break points; Alcaraz held 118 of 133 and faced 57. That run is the source of the aggregation example.
- These checks validate the skill format, documented input and released Actor. They are not an end-to-end installation or execution test in every assistant client.
