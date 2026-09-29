# Compare App Store and Google Play review exports

A product team has two saved review exports and wants to see what changed. The useful result is not another spreadsheet full of comments: it is a short list of new observations and edits, with enough context to inspect the original evidence.

[Watch the collection demo](https://www.youtube.com/watch?v=WpWDcEdP3Rs) | [Open the Actor](https://apify.com/cleanscrape/app-store-reviews-scraper) | [Free local comparison](../../examples/review-snapshot/README.md)

## Choose the simplest method

| Situation | Starting point |
| --- | --- |
| You already have two CleanScrape JSON exports | Use the free local comparison below. No new collection is necessary. |
| You maintain the Android app and need its reviews in a support system | Check the official Google Play Developer API first. It requires access to the app and has its own coverage limits. |
| You need public iOS and Android feedback in one documented format | Evaluate the CleanScrape Actor with a small, explicitly capped sample. |
| You need every historical review or proof that a review was deleted | This workflow does not establish either. Do not treat a missing sample row as deletion. |

Google documents its [authorised review API](https://developers.google.com/android-publisher/reply-to-reviews), including its recent-review window and a Play Console CSV route for older reviews. An official export still needs an explicit field mapping before it can be passed to this repository's local script. We do not silently treat another provider's schema as ours.

## Try the free example

Use Python 3.10 or newer. Download the [review-snapshot folder](../../examples/review-snapshot) and run this command from that folder:

```bash
python compare_reviews.py --demo --out demo-report
```

There are no packages to install and no network or AI calls. The data is deliberately synthetic.

The report has one newly observed review, one changed review, one unchanged review and one missing from the later sample. A repeated row is counted once. Open `demo-report/report.md`; use `changes.csv` to inspect the affected IDs and changed field names.

For real saved exports:

```bash
python compare_reviews.py before.json after.json --out review-comparison
```

Use a new output folder. Keep the input files private. The script does not overwrite an existing report or modify the exports.

## If you need fresh reviews

Here is a small example for the [App Store & Google Play Reviews Scraper](https://apify.com/cleanscrape/app-store-reviews-scraper):

```json
{
  "store": "both",
  "googlePlayAppId": "https://play.google.com/store/apps/details?id=com.spotify.music",
  "appStoreId": "https://apps.apple.com/us/app/spotify/id324684580",
  "country": "us",
  "language": "en",
  "maxReviews": 20,
  "sort": "newest"
}
```

Let's use Spotify as an example. Replace both app links for another product. The limit is per store, so this requests up to 40 reviews in total, not a guaranteed 40.

The country selects the requested storefront. Language and sorting affect Google Play; Apple uses its recent feed. Country overrides the country in an Apple URL. When comparing later exports, keep these settings consistent and record when each sample was collected.

Fresh runs are billed separately. Check the current Pricing tab and set a positive maximum cost before running. Include the startup event and allocated memory when estimating a small job; price per review alone is not the full cost. This guide does not start a run or grant free collection.

## Read the result before making a decision

- Newly observed means absent from your earlier file, not necessarily newly published.
- Changed identifies fields that differ under the same review ID and request context. A date change alone is not proof of a new complaint.
- Missing from the later sample does not establish deletion. Your sorting or collection limit may explain the difference.
- Invalid ratings do not become zeros. The report shows the denominator used for the low-rating share.
- Missing IDs and conflicting duplicate records remain unresolved rather than being matched by similar wording.

The same numeric review ID in another app, store, country or request-language context is not silently merged. Reviewer names and full review text are not included in the derived change report.

For iOS versus Android comparisons, keep the two source groups separate. Read the comments behind a finding and report the sample size. A difference in these samples is not a controlled platform experiment or an overall app rating.

## What to show in a short demo

| Section | Show | Explain |
| --- | --- | --- |
| The question | Two existing export files | We want to inspect changes, not collect the same data again. |
| The free path | The demo command and report | These fixture rows are synthetic. |
| The useful result | A changed ID and its field names | We can look up the original record without publishing reviewer details. |
| The boundary | A missing-from-later row | Missing is not the same as deleted. |
| The next step | A real export or the small Actor input | New collection is optional and separately billed. |

For themes or a concise product-team brief, use the [app-review skill](../../skills/apify-cleanscrape-app-reviews/SKILL.md) with your saved data. Your assistant may have its own usage charges. Do not describe the local script as an automatic alerting or sentiment-analysis service.

**Disclosure:** CleanScrape maintains the linked paid Actor and this free example. No affiliate links. [Questions or reproducible problems](https://github.com/CleanScrape/agent-skills/issues).
