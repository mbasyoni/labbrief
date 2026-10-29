# LabBrief Checkout — public candidate

LabBrief turns a synthetic data-preparation request into a traceable intake brief: review exact request quotations, choose catalog deliverables, approve a fixed quote, and optionally test a PayPal Sandbox checkout before downloading the approved intake bundle.

This is independent utility code for a bounded demonstration. It does not perform laboratory work, produce scientific findings, or support real-money payments. At the candidate audit, this source had not yet been published. On 29 October 2026, this repository published the audited source, with a protective .gitignore and this publication-status update. Public application deployment is separate and has not been performed.

## Run locally

Use Python 3.12 and a modern browser. From this directory:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip --isolated install --no-cache-dir --disable-pip-version-check --index-url https://pypi.org/simple -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python app.py --port 8769 --data-dir .review-runtime
```

Open **http://127.0.0.1:8769** on the same computer. Use the exact loopback address. Stop the server with Ctrl-C. See [fresh-install instructions](review/FRESH_INSTALL.md) for checks and platform limits.

Default classification fits a local TF-IDF/logistic model from the included synthetic training examples. It needs no AI API or network after dependencies are installed. Without Sandbox configuration, checkout fails closed and the bundle remains locked.

## Optional Sandbox configuration

The server reads `PAYPAL_SANDBOX_CLIENT_ID` and `PAYPAL_SANDBOX_CLIENT_SECRET` from its process environment. The app does **not** automatically load `.env` files. Configure only through an owner-controlled secure process environment; do not place values in source, commands, screenshots, logs or chat. No credential-entry page or private recovery interface is included in this candidate.

Use the approved Sandbox application and a separate Sandbox Personal buyer. Do not use a real card or a live-money flow. The adapter is fixed to PayPal Sandbox. A “configured” message detects configuration; it does not establish authentication or payment success.

`LABBRIEF_AI_MODE=local` is the default. Optional `external` mode uses an explicitly configured compatible endpoint (`LABBRIEF_AI_URL`, `LABBRIEF_AI_MODEL`, optional `LABBRIEF_AI_KEY`) and sends the synthetic request there. Keep confidential data out of this prototype.

## Judge setup: use your own free PayPal Sandbox

The local classifier and scope-review UI run without payment credentials. To evaluate checkout and delivery, use your own PayPal Developer Sandbox; this repository does not distribute the author's account credentials.

1. Sign in to the [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/) with your own developer account. Select **Sandbox**, then **Apps & Credentials**. Select an existing Sandbox REST app, or create a **Merchant** app associated with your Sandbox Business account. Obtain that app's Sandbox Client ID and Client Secret. Do not select Live credentials. Follow PayPal's [REST getting-started guide](https://developer.paypal.com/api/get-started/).
2. Under **Testing Tools → Sandbox Accounts**, locate a separate **Personal** buyer account. Use **View/Edit Account** to obtain its generated test login. If needed, create a Personal test account; keep the app's Business merchant and Personal buyer separate. PayPal documents this in [Sandbox accounts](https://developer.paypal.com/sandbox-testing/accounts).
3. Configure the local server process with `PAYPAL_SANDBOX_CLIENT_ID` and `PAYPAL_SANDBOX_CLIENT_SECRET` through your secure environment-variable manager or IDE secret configuration. Never commit credentials, paste them into command history, or include them in screenshots/logs. The app does not load `.env` automatically. Restart the server after configuration. Keep the default `LABBRIEF_AI_MODE=local`.
4. Follow **Run locally** above and open `http://127.0.0.1:8769`. Enter only a synthetic request, select a catalog deliverable, generate/review the scope and approve the displayed quote. A manifest brief uses USD 5.00 in **test funds**, not real money.
5. Create a Sandbox checkout. In the PayPal approval flow, sign in as your separate **Sandbox Personal buyer**, not the merchant and not a real-money buyer. Confirm that the provider page is on `sandbox.paypal.com`. Do not enter a real card. Return to the original LabBrief tab after approval.
6. Use **Capture and verify**. The server independently checks provider status, reference and exact amount before enabling the intake ZIP. Download and inspect the bundle; an unapproved, mismatched or incomplete payment must not unlock delivery. Missing Sandbox configuration intentionally fails closed.
7. Stop the local server when finished and remove its temporary credential configuration. Keep Sandbox and local operation records private. Do not reuse the author's historical operation or attempt to recapture it.

PayPal account availability can depend on location. If obtaining your own Sandbox access is blocked, use the official developer support path; do not substitute live credentials. The included automated payment tests use explicit fake providers and are not an alternative claim of real-provider acceptance.

## Workflow and delivery

1. Enter a synthetic request and select catalog services.
2. Review the exact quotations, advisory category/checklist questions and server price; explicitly approve the scope.
3. If configured and separately authorized, create one Sandbox checkout and approve it with the test buyer. Return to the original LabBrief tab.
4. Capture and verify. The server retrieves provider state first, reuses its capture request key, and independently verifies the completed order, reference and exact amount before delivery.
5. Download the ZIP containing `approved-intake.json`, `sandbox-receipt.json`, `README.txt` and `manifest.json` with content hashes.

Test prices are USD 5 for a manifest brief, USD 3 for a metadata checklist and USD 2 for a handoff plan. These are synthetic demonstration amounts. The deliverable is an approved intake, not performed laboratory work.

## Validation scope

The accepted **private** build completed a genuine USD 5.00 Sandbox capture and authenticated download on macOS on 29 October 2026. Its original receipts and identifiers remain private. This public candidate removes private interfaces and changes code; that historical result is **not** a real-provider acceptance result for this changed build.

Candidate tests use explicit fake providers and temporary loopback HTTP servers. Current test, fresh-install and source-comparison evidence accompanies the candidate. No fresh payment is authorized or claimed here. [Demo notes](review/DEMO_NOTES.md) distinguish actual candidate screens from the separately recorded private acceptance summary.

The local model's tiny same-author benchmark observed 8/9 correct in-domain suggestions with one abstention and 8/8 out-of-domain abstentions. It is not independent scientific validation or a general accuracy guarantee. See [MODEL_CARD.md](MODEL_CARD.md). Regenerate the report with `python benchmark_local_ml.py`; it creates its `evidence/` output directory when needed.

## Boundaries

Prices and payment state are server-controlled. A client assertion, return URL or click cannot unlock delivery. Order access requires session ownership; mutations require matching Host/Origin and CSRF checks. Provider redirects are refused. User/model text is rendered as text rather than HTML.

This remains a loopback development prototype. In-memory sessions expire after eight hours; restarting loses browser access to persisted orders. There is no account recovery, webhook processor, refund/tax system, multi-process lock or production hosting. Private setup/recovery endpoints, flags and operation fixtures are excluded. Source release and public deployment remain separate review decisions.

## References and license

- [PayPal Orders v2](https://developer.paypal.com/api/orders/v2)
- [PayPal REST authentication](https://developer.paypal.com/api/rest/authentication/)

The independent source is supplied under the MIT license in [LICENSE](LICENSE). See [PROVENANCE.md](PROVENANCE.md). No publication is performed by this package.
