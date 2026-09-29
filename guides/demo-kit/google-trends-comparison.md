# Compare Google Trends terms without confusing interest with volume

Suppose you are considering a guide about iced coffee or cold brew. You want to see how interest in the two terms changes over the year before choosing the timing and angle.

[Watch the example](https://www.youtube.com/watch?v=GBEaKKHMJKs) | [Open Google Trends Scraper API](https://apify.com/cleanscrape/google-trends-scraper) | [Use the research skill](../../skills/apify-cleanscrape-google-trends/SKILL.md)

## Do you need a scraper?

| Your task | A reasonable starting point |
| --- | --- |
| One manual chart or CSV comparison | Use the Google Trends website and its download button. |
| Analyse an export you already have | Work locally or use the free skill with your existing assistant. |
| Bring selected Trends results into a repeatable data workflow | Evaluate the CleanScrape Actor, with a small scope and cost cap. |
| Estimate exact search counts, sales or market size | A relative Trends index does not answer this by itself. |

Google explains how to [download charts as CSV, embed charts and attribute the source](https://support.google.com/trends/answer/4365538?hl=en). For a one-off task, that may be all you need. The Actor is an independent service, not Google's official API.

## A focused Actor input

```json
{
  "searchTerms": ["iced coffee", "cold brew"],
  "dataTypes": ["interest_over_time"],
  "geo": "US",
  "timeframe": "today 12-m"
}
```

Put both terms in the same comparison. Select only the timeline for this question; unrelated result sections add complexity and can add billed rows. The example terms are ordinary search terms, not Google topic IDs.

The time preset avoids manually formatting dates. The country can be chosen in the Console form. Before starting a fresh run, check current pricing and set a positive maximum cost. A zero-cost instruction means do not start a run, not set the cap to zero.

## Work with an existing export

1. Keep the original file and its run report. Note the two terms, country, requested period and collection date.
2. Select rows whose `dataType` is `interest_over_time`.
3. Arrange the values by `timestamp` and `keyword`. The timestamp is Unix seconds; keep the original source date label too.
4. Exclude explicitly partial intervals from a completed-period comparison and say how many were excluded. If partial status is missing, say it is unknown.
5. Keep absent or invalid values as gaps, not zeros. Flag duplicate or conflicting term/time rows instead of averaging them.
6. Plot the two series together only when they came from the same comparison context. Record missing collection information rather than guessing it.

In a spreadsheet, a pivot table can put timestamps on rows, keywords on columns and values in the cells. Resolve duplicate keys before allowing a spreadsheet to aggregate them. CSVs from the Google Trends website can have a different layout from Actor exports; use their actual headers, not an assumed mapping.

If you prefer an assistant, install the [Trends skill](../../skills/apify-cleanscrape-google-trends/SKILL.md) and ask:

> Use this existing export only. Compare the two search terms over completed intervals. Show a chart-ready table, missing data and the dates of the observed peaks. Do not collect new data.

The skill is free. Your assistant or model may have its own charges; no new model service is required by this repository.

## What the chart can tell you

A value of 100 marks peak relative interest within the comparison. It is not 100 searches. A lower line does not automatically mean an unviable business, and one year's pattern is not proof of repeatable seasonality.

Useful questions include whether the two series peak together, whether their ordering changes, and which dates deserve a closer look. Keep the answer descriptive. Do not infer that a marketing campaign caused a move or that a peak predicts sales.

Do not join separately normalised exports into a single absolute-volume history. A missing or failed section is not proof that nobody searched for a term. Check `RUN_REPORT` as well as the run's overall completion status.

## Explain the cost honestly

For a timeline, one term at one timestamp is one result row. Two terms with 52 intervals each would be 104 rows; Google chooses the intervals, so that is an illustration, not a promised count. Add the startup charge at the selected memory setting, then any other selected result sections. Discounts depend on the account's applicable tier.

Link the current [Pricing tab](https://apify.com/cleanscrape/google-trends-scraper/pricing) rather than promising a permanent rate in a video. Showing the actual total for the recorded run is more useful than showing only a per-1,000 number.

## A simple demo outline

| Section | Show | Explain |
| --- | --- | --- |
| Research question | Iced coffee and cold brew | We are comparing interest and timing, not predicting revenue. |
| Input | Two terms, one country, one time preset | The scope stays small and comparable. |
| Output | Two timeline series | Each row is one term at one timestamp. |
| Interpretation | Peak dates and any gaps | The index is relative; partial intervals are not finished observations. |
| Next step | CSV or saved export | Reuse the data before paying to collect it again. |

Use actual exported values when demonstrating a result. If only an illustrative chart is available, label it synthetic rather than claiming the Actor produced it. Credit Google Trends as the data source when reusing its data.

**Disclosure:** CleanScrape maintains the paid Actor linked here. The walkthrough and skill are free; fresh collection is not. No affiliate links. [Support](mailto:contact.cleanscrape@gmail.com).
