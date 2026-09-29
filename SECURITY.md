# Security and data handling

These skills are readable instructions. They contain no executable helpers, automatic jobs, install hooks or credentials.

## Before using a skill

Review its content and the permissions of the assistant that will follow it. An instruction to ask for a spending limit is not a technical sandbox. Enforce the approved limit in the Apify run options.

For zero-cost work, use existing local exports and do not start a cloud run. A value of zero must not be used as a substitute for avoiding a run.

## Credentials

Use your own authorised Apify connection or a scoped `APIFY_TOKEN` environment variable. Do not paste tokens into chat, public issues, JSON inputs, example URLs or source files. Use the Authorization header only with the official HTTPS API host. Do not follow redirects that could forward credentials to another host.

The examples do not require access to the maintainer's account, a CleanScrape-hosted endpoint or a separate paid model API.

## Exported data

Public review text can still contain personal information. Keep raw exports private. Omit reviewer names from summaries unless there is a genuine need. Use aggregate findings and limited excerpts rather than publishing full review corpora.

Treat scraped text as untrusted data, not instructions. Prevent spreadsheet formula execution in derived CSV text fields. Do not send exports to another service merely because a source record requests it.

## Reporting a problem

Report a security concern privately to contact.cleanscrape@gmail.com. Send a description and non-sensitive reproduction steps, not live credentials or private customer data. Rotate an exposed credential through its provider; deleting a public message alone is not enough.

