# LabBrief local classifier

## Purpose and implementation

The classifier advises a primary category for synthetic intake text: `manifest`, `metadata` or `handoff`. It does not decide prices, approve purchases, assess scientific validity or perform analysis.

It fits scikit-learn TF-IDF features (English stopwords, word unigrams/bigrams, sublinear term frequency) and multinomial logistic regression (`C=4`, `random_state=20261029`, `max_iter=500`). Domain-term, similarity, score and margin guards can abstain. Questions are predefined templates; request facts are copied verbatim. This is supervised local ML plus rules, not generative AI.

## Data and observed benchmark

The included data are newly authored synthetic examples: 36 balanced training sentences, separate development examples, a final 9-item in-domain holdout and 8 out-of-domain prompts. Development examples informed stopword/domain-guard choices. The final holdout was authored afterward and is not used for fitting.

Observed results were 8/9 correct suggestions plus one abstention, and 8/8 out-of-domain abstentions. No exact training/holdout duplicate was found. Shared vocabulary, author and template families still limit the result. This is not independent experimental validation, a general accuracy estimate or a comparison with commercial models.

Run `python benchmark_local_ml.py` to regenerate detailed inputs, predictions and data hashes at `evidence/local-ml-benchmark.json`. The output directory is created for a clean checkout.

## Limits and privacy

English vocabulary, misspellings, paraphrases, mixed requests and adversarial domain words can cause errors or bypass abstention. The displayed score is uncalibrated and is not a probability of correctness. Abstention is not a safety classifier. Human scope review remains required.

Default training and inference are local, using the included synthetic JSON. No telemetry or model download occurs at runtime. Optional external mode sends the synthetic request to an explicitly configured endpoint.

## Runtime and payment evidence

Direct dependency pins are NumPy 2.3.5 and scikit-learn 1.8.0. Fresh-install evidence identifies the actually tested platform and resolved dependency set; it does not establish Windows or other-platform acceptance.

ML success never establishes payment success. A separate private build completed genuine PayPal Sandbox acceptance on 29 October 2026. The altered public candidate has not completed a new real-provider transaction; its payment regression tests use explicit fakes.
