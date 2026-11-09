# Completed pre-publication review worksheet

Reviewed: 2026-11-09
Status: **approved and applied**

This worksheet preserves the source-by-source review behind the final [adjudication log](adjudication-log.md). Final codes are defined in the [codebook](../research/codebook.md).

| Record and source | Relevant evidence | Previous classification | Contradicting or limiting evidence | Approved decision |
|---|---|---|---|---|
| [GH-I-13129](https://github.com/vitejs/vite/issues/13129) | A new Vite/React author followed the official guide and saw editor errors in the linked React/TypeScript example. | `setup friction`; `documentation clarity`; attribution uncertain | The application built and ran. Editor/TypeScript compatibility and changing online dependencies limit Vite-only attribution. | Retain `setup friction`; remove `documentation clarity`; preserve explicit attribution uncertainty. |
| [GH-I-15690](https://github.com/vitejs/vite/issues/15690) | The author requested JavaScript-friendly HMR/API material and a simple watcher example. | `documentation clarity`; weak-support flag | Broad statements about TypeScript preferences are not supported by one post. Closure as not planned does not negate the reported experience. | Retain `documentation clarity`; qualify as one author's JavaScript-friendly documentation request. |
| [GH-I-20822](https://github.com/vitejs/vite/issues/20822) | A fresh project failed; output named the installed Node version, required versions, and upgrade action, then showed a separate native-binding error. | `setup friction`; `error messages`; contradictory flag | The compatibility warning was actionable, so the record cannot support uniformly unhelpful error messaging. | Retain `setup friction`; keep topical `error messages`; treat as counterevidence and preserve the separate native-binding error. |
| [GH-D-17324](https://github.com/vitejs/vite/discussions/17324) | The author showed a missing timestamped config-file error and several unsuccessful troubleshooting attempts. | `error messages`; `configuration complexity`; uncertain | The discussion is unanswered, proposed fixes conflict, and no accepted resolution confirms a root cause. | Retain both codes; mark unanswered and root cause unconfirmed; do not treat suggested fixes as proof. |
| [GH-I-5370](https://github.com/vitejs/vite/issues/5370) | The original post documents config-loading failure through a symlinked monorepo package and lists workarounds. | `documentation clarity`; `configuration complexity`; borderline documentation flag | The original post does not criticize or cite documentation. Later docs are resolution context only. | Retain `configuration complexity`; remove `documentation clarity`. |
| [GH-I-12923](https://github.com/vitejs/vite/issues/12923) | The author explicitly contrasted documented config preprocessing with a Vite 4.3 Windows regression. | `documentation clarity`; `configuration complexity`; borderline documentation flag | The prose was not necessarily unclear, and the regression was fixed in Vite 4.3.3. | Retain both codes under the explicit documentation-expectation-mismatch rule; mark as a historical fixed regression. |
| [GH-I-7007](https://github.com/vitejs/vite/issues/7007) | The author directly requested container configuration and troubleshooting guidance after spending time on interacting settings. | `setup friction`; `configuration complexity` | Non-default remote-container context limits generalization. | Add `documentation clarity`; retain `setup friction` and `configuration complexity`. |

## Final theme decisions

- Setup friction: 8 coded records.
- Documentation clarity: 6 coded records after removing GH-I-13129 and GH-I-5370 and adding GH-I-7007.
- Error messages: 7 topically relevant records, separated into 6 diagnostic-friction reports and 1 counterexample.
- Configuration complexity: 9 coded records.
- Frequency labels are descriptive sample counts only; `moderate_sample_support` was removed.

No record was excluded during adjudication.
