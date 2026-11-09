# Final adjudication log

Approved: 2026-11-09

This log records the owner-approved decisions applied to `data/raw/evidence.csv`, the pipeline outputs, and the narrative report.

| Record | Final decision | Applied coding and interpretation |
|---|---|---|
| [GH-I-5370](https://github.com/vitejs/vite/issues/5370) | Recode | Retained `configuration complexity`; removed `documentation clarity`. Later config-loader documentation is resolution context, not evidence that the original post reported a documentation problem. |
| [GH-I-20822](https://github.com/vitejs/vite/issues/20822) | Retain with counterevidence | Retained `setup friction` and topical `error messages`. The explicit Node.js version warning is actionable counterevidence; the separate native-binding error is also preserved. This record is not counted among diagnostic-friction reports. |
| [GH-I-13129](https://github.com/vitejs/vite/issues/13129) | Recode and qualify | Retained `setup friction`; removed `documentation clarity`. The author reported editor/TypeScript compatibility errors in an official example, while the app built and ran. Vite-only causation is not established. |
| [GH-I-15690](https://github.com/vitejs/vite/issues/15690) | Retain and qualify | Retained `documentation clarity` for a JavaScript-friendly examples request. The report represents one author's experience, not all users. |
| [GH-D-17324](https://github.com/vitejs/vite/discussions/17324) | Retain and qualify | Retained `error messages` and `configuration complexity`. Marked unanswered with no confirmed root cause; suggested fixes are not treated as proof. |
| [GH-I-12923](https://github.com/vitejs/vite/issues/12923) | Retain under explicit rule | Retained `configuration complexity` and `documentation clarity` only as a documented-expectation mismatch. It is a historical Vite 4.3 regression fixed in 4.3.3, not evidence of unclear prose or a current unresolved defect. |
| [GH-I-7007](https://github.com/vitejs/vite/issues/7007) | Add code | Added `documentation clarity` because the author directly requested container configuration and troubleshooting guidance. Retained `setup friction` and `configuration complexity`. |

## Resulting theme frequencies

- Configuration complexity: 9 of 18 coded records.
- Setup friction: 8 of 18 coded records.
- Documentation clarity: 6 of 18 coded records.
- Error messages: 7 of 18 topically relevant records, comprising 6 diagnostic-friction reports and 1 counterexample.

These are overlapping frequencies in a purposive sample, not prevalence or quality estimates.
