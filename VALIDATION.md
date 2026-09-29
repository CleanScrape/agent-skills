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

