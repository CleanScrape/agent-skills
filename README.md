# CleanScrape agent skills

Practical guides for turning web data into useful comparisons, shortlists and research.

These skills give an AI assistant the inputs, field definitions and analysis steps it needs to work with CleanScrape's Apify Actors. Start with an existing export at no collection cost, or use your own Apify account when you need fresh data.

**The skills are free. Live Apify runs are billed separately.** Installing a skill does not start a run, create a schedule or send data to CleanScrape.

## Choose a task

Eight focused skills, one for each CleanScrape Actor. Use the one that fits the task rather than installing everything by default.

| Task | Skill | What you get |
| --- | --- | --- |
| Compare iOS and Android feedback | [App review comparison](skills/apify-cleanscrape-app-reviews/SKILL.md) | Ratings by store, evidence-backed themes and clearly labelled coverage |
| Research seasonal search interest | [Google Trends research](skills/apify-cleanscrape-google-trends/SKILL.md) | A comparable timeline, a chart-ready table and an explanation of what the scores mean |
| Map Your Show exhibitor research | [Map Your Show exhibitor research](skills/apify-cleanscrape-exhibitor-research/SKILL.md) | Sourced shortlists and careful interpretation of directory changes |
| Shopify product-review research | [Shopify product-review research](skills/apify-cleanscrape-shopify-reviews/SKILL.md) | Judge.me and Okendo feedback with product-group attribution |
| Google News and publisher-feed research | [Google News and publisher-feed research](skills/apify-cleanscrape-news-research/SKILL.md) | A sourced brief with link status and coverage notes |
| Pinterest content and destination research | [Pinterest content and destination research](skills/apify-cleanscrape-pinterest-research/SKILL.md) | Content themes and destination-domain tables |
| Google Hotels stay and offer comparison | [Google Hotels stay and offer comparison](skills/apify-cleanscrape-hotel-comparison/SKILL.md) | Same-stay hotel and provider-offer comparisons |
| TikTok Shop product comparison | [TikTok Shop product comparison](skills/apify-cleanscrape-tiktok-shop/SKILL.md) | US product and variant comparisons with source caveats |

These are instructions for a compatible assistant, not a hosted dashboard or an automatic monitoring service. Your assistant performs the analysis using tools you have enabled.

## Install

Use an assistant that supports the [Agent Skills format](https://agentskills.io/specification). With the [skills CLI](https://skills.sh/docs):

```bash
npx skills add CleanScrape/agent-skills --skill apify-cleanscrape-app-reviews
npx skills add CleanScrape/agent-skills --skill apify-cleanscrape-google-trends
npx skills add CleanScrape/agent-skills --list
```

Review the skill before installing. Each skill is self-contained in its own folder; there are no bundled executables, install hooks or third-party dependencies. The optional installer has its own software requirements and telemetry policy. You can instead download the folder and use your assistant's documented local-skill installation method.

Installation makes the skill available to that assistant. It does not automatically add CleanScrape to every AI service or guarantee that an assistant will select it.

## Try it without a new scrape

Export an existing Actor dataset as JSON and keep it locally. Include its `RUN_REPORT` if you have it.

Then ask:

> Use the app-review skill with these existing exports only. Compare the ratings and recurring complaints on iOS and Android. Do not start a new run.

Or:

> Use the Google Trends skill with this export. Compare the two search terms, leave out incomplete intervals and prepare a chart-ready table. Do not collect new data.

No Apify token is needed to analyse local exports. Your assistant may have its own usage charges; this repository does not require an additional AI subscription or model API.

Do not put private exports, reviewer details, API tokens or signed download links in a public repository or issue.

## A local example you can run without an assistant

[Compare two app-review snapshots](examples/review-snapshot/README.md) with a small Python script. It reports newly observed reviews, changed fields and ratings by store, without a token, model call or network request. A synthetic demonstration and offline tests are included. The optional script lives outside the skill folders and is not installed with a skill.

## When you need fresh data

The assistant should show the proposed inputs, current pricing and a spending limit before starting. It must use your own authorised Apify connection or `APIFY_TOKEN` environment variable. It must not quietly run extra Actors, increase the budget or create recurring jobs.

Examples to adapt:

> Compare recent reviews of my app on iOS and Android in the United States. Start by showing the inputs and cost for up to 20 reviews per store.

> Compare iced coffee and cold brew in the United States over the past 12 months. Use timeline data only and show me the likely cost before collecting it.

### What a small job costs

Reference base rates checked on 29 September 2026, before subscription discounts:

| Actor | Base event prices | Example at 1 GB memory |
| --- | --- | --- |
| App Store & Google Play Reviews | $0.20 per 1,000 delivered reviews + $0.01 startup per allocated GB, minimum one | 40 delivered reviews: $0.018 |
| Google Trends | $3 per 1,000 delivered rows + $0.05 startup per allocated GB, minimum one | 104 delivered timeline rows: $0.362 |

These are calculations, not promised output counts. Trends bills one term at one timestamp as one timeline row. Other selected sections add rows. Startup can be charged even if no data is returned. Check the Actor's current Pricing tab before running; the skills do not grant free scraping or subsidised access.

## How the analysis stays useful

- Every summary states what was collected, what is missing and which filters were applied.
- App-review findings refer back to source review IDs where available. They do not treat a small sample as every customer's opinion.
- Apple review dates can be update dates, and its recent public feed is not a complete history.
- Google Trends scores measure relative search interest, not search counts or sales.
- A successful run is not enough: the assistant also checks the run report for partial, empty or failed sections.
- Existing exports stay unchanged. Any cleaned tables, charts or summaries are separate analysis outputs.

## Guides for tutorials and evaluations

The [demo kit](guides/demo-kit/README.md) brings together a free app-review comparison, a Google Trends decision guide, example inputs and short walkthrough outlines. It explains when a free native export is enough and when a paid Actor may help.

## Watch the workflow

[App-review demo](https://www.youtube.com/watch?v=WpWDcEdP3Rs) shows collection and export using Spotify as an example. [Google Trends demo](https://www.youtube.com/watch?v=GBEaKKHMJKs) compares two coffee-related terms.

The videos demonstrate the Actors, not a recording of these agent skills being executed.

## More CleanScrape tools

| Tool | Starting point |
| --- | --- |
| [App Store & Google Play Reviews](https://apify.com/cleanscrape/app-store-reviews-scraper) | App links and a review limit |
| [Google Trends](https://apify.com/cleanscrape/google-trends-scraper) | Search terms, country and time range |
| [Map Your Show exhibitors](https://apify.com/cleanscrape/event-exhibitor-monitor) | A supported event directory |
| [Shopify product reviews](https://apify.com/cleanscrape/shopify-reviews-scraper) | Product links using supported Judge.me or Okendo integrations |
| [Google News](https://apify.com/cleanscrape/google-news-scraper) | News queries or supported feed inputs |
| [Pinterest](https://apify.com/cleanscrape/pinterest-scraper) | Supported search or pin inputs |
| [Google Hotels](https://apify.com/cleanscrape/google-hotels-scraper) | Destination and stay details |
| [TikTok Shop products](https://apify.com/cleanscrape/tiktok-shop-product-scraper) | US-market product searches or supported product links |

Each tool now has a focused skill in this repository. The table at the top links to the individual instructions. Each Store page documents the current inputs, coverage, examples and pricing.

## Support and scope

For skill instructions, [open a GitHub issue](https://github.com/CleanScrape/agent-skills/issues). For an Actor run, use that Actor's Issues tab or email [contact.cleanscrape@gmail.com](mailto:contact.cleanscrape@gmail.com). Include the expected result and a non-sensitive example, never a token.

The skills were prepared against published Actor schemas and documentation. Local format, example-input and installation checks and export-only walkthroughs are documented in [Validation](VALIDATION.md). No fresh cloud scrape is part of this skills release. Local checks do not establish live source availability or identical behaviour across every assistant.

**Disclosure:** CleanScrape builds the paid Actors linked here and earns revenue from their use. These links contain no affiliate or referral codes. The skills are original MIT-licensed documentation; the commercial Actors and third-party data are not covered by that licence. CleanScrape is independent of Apple, Google, Apify and the other platforms named here.

[Apify](https://apify.com/cleanscrape) | [Tutorials](https://dev.to/cleanscrape) | [YouTube](https://www.youtube.com/@CleanScrapeTools)
