# Final publication-readiness audit

Audit date: 2026-11-09
Status: **ready for owner-controlled public release**

## Research verification

- The dataset contains 18 unique public `vitejs/vite` records: 15 issues and 3 discussions.
- Final overlapping category totals are configuration complexity 9, setup friction 8, documentation clarity 6, and error-message relevance 7.
- Error-message evidence is separated into 6 diagnostic-friction reports and 1 counterexample rather than presented as 7 uniformly negative reports.
- The seven owner-approved adjudications are applied consistently in the raw CSV, generated evidence, codebook, README, and narrative report.
- All 18 source URLs were accessible during final verification on 2026-11-09.
- Every source appears in both the generated evidence pack and the narrative report. Finding counts match their source-ID lists.
- Excerpts are 25 words or fewer; the maximum is 23 words.
- Frequencies are explicitly described as purposive-sample counts, not confidence scores, evidence-quality ratings, statistical significance, or prevalence estimates.
- Historical version and resolution context is preserved. Older reports are not presented as current unresolved defects.
- Author-reported experience, source-verified context, researcher interpretation, and independent reproduction are distinguished in the codebook. No product behavior was independently reproduced.

## Ethics, privacy, and attribution

- Public issue authors are not described as research participants, and no interviews or usability sessions are claimed.
- The dataset excludes usernames, contact details, inferred demographics, credentials, and private information.
- The research-operations kit is future-facing, requires consent and approved data handling, and contains a blank tracker with no personal data.
- Brief excerpts retain exact source links. `ATTRIBUTION.md` explains that source posts remain attributable to their original authors and are not relicensed.
- Original project code and documentation carry an MIT License. The project states that it is not associated with Vite or MLH.

## Engineering verification

- Python 3.11.17: 11/11 unit tests passed.
- Python 3.14.7: 11/11 unit tests passed.
- CLI validation: 18 valid rows, 18 unique rows, 0 duplicates.
- CLI build: 18 input rows, 4 findings, 0 LLM suggestions.
- A clean rebuild matched all five checked-in generated artifacts byte-for-byte.
- A fresh Python 3.14 virtual environment installed the package in editable mode, and the installed `devinsight` command validated the dataset.
- No broken local Markdown links were found.
- All 18 GitHub source links resolved during the final link check.
- URL/identifier agreement and unique source IDs are now enforced by validation and covered by tests.
- No remote was created, and no push or publication operation was performed.

## Residual limitations

- Small purposive, English-language, public GitHub sample with no population denominator.
- Selection and public-reporting bias toward visible, well-described problems.
- No current-version reproduction, representative sampling, severity estimate, or time-to-resolution analysis.
- Root cause remains unconfirmed for GH-D-17324; Vite-only attribution remains uncertain for GH-I-13129.
- Comments and accepted answers provide selective resolution context but were not systematically coded.
- No second researcher independently recoded the full 18-record sample.
- Exact search terms are recorded, but the project does not preserve a complete result-by-result screening log.

These limitations are disclosed in the README and research report and do not prevent publication as an exploratory portfolio sample.
