# Fresh local install and verification

Use Python 3.12 and a browser. These commands are for macOS/Linux; only the platform named in the candidate's fresh-install evidence is verified. Windows commands and acceptance have not been tested here.

From the extracted candidate root, with provider configuration absent:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip --isolated install --no-cache-dir --disable-pip-version-check --index-url https://pypi.org/simple -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m py_compile app.py local_ml.py benchmark_local_ml.py
.venv/bin/python benchmark_local_ml.py
.venv/bin/python app.py --port 8769 --data-dir .review-runtime
```

The full discovered candidate suite includes the 60 core application/local-ML tests plus public-surface and clean-benchmark regressions. Use the included result log for the final count. All payment tests use fake providers; temporary loopback HTTP test servers are real. No original private fixtures or hash-patching review runner are needed by this public tree.

Open `http://127.0.0.1:8769` on the same computer. Exercise the synthetic example, local scope generation and explicit approval. Without Sandbox credentials, checkout must report missing configuration and delivery must remain locked. Stop the server with Ctrl-C. Remove `.review-runtime/`, `.venv/`, caches and generated evidence from any distributable artifact according to its manifest.

The benchmark command must succeed when `evidence/` is absent; it creates the directory and writes a detailed synthetic report. That report does not establish general scientific or model accuracy.

For a separately authorized Sandbox test, configure `PAYPAL_SANDBOX_CLIENT_ID` and `PAYPAL_SANDBOX_CLIENT_SECRET` only in the owner's server-process environment, without exposing values in commands, files, screenshots, logs or chat. `.env` files are not automatically loaded. The public candidate has no credential-entry page or restoration/debug interface. Use a separate Sandbox Personal buyer and no real-money account/card flow.

A genuine private transaction was accepted on an earlier exact build. Installing or passing tests for this changed candidate does not repeat that acceptance. Do not create or recapture its completed original operation. See [demo notes](DEMO_NOTES.md).
