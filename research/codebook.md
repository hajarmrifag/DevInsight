# DevInsight codebook

Version: 1.0, adjudicated 2026-11-09

## Evidence unit and evidence levels

The observation unit is one original public `vitejs/vite` GitHub issue or discussion post. A record can carry more than one code.

- **Author-reported experience:** what the original author said happened. This is the primary evidence counted in the analysis.
- **Source-verified context:** metadata, exact excerpts, labels, state, and resolution context checked on the linked GitHub page.
- **Independent product observation:** a behavior reproduced by this project. There are no independently reproduced product observations in this study.
- **Researcher interpretation:** a category or cross-record synthesis. Interpretations must remain traceable to source IDs and cannot turn an author report into a confirmed root cause.

Frequencies are overlapping descriptive counts within this 18-record purposive sample. They are not confidence scores, statistical significance, evidence-quality ratings, or prevalence estimates.

## Category definitions

### Setup friction

Use when a report describes difficulty before productive use: scaffolding, installation, first dev-server start, an official starter/example, migration setup, or enabling a non-default environment.

Do not infer that Vite alone caused the difficulty when framework templates, editor tooling, TypeScript types, Node, package managers, native dependencies, or environment policy may contribute.

### Documentation clarity

Use when the source directly reports at least one of:

1. missing, confusing, ambiguous, incomplete, or hard-to-find guidance;
2. a request for task-relevant examples or troubleshooting guidance; or
3. an explicit contrast between documented expected behavior and observed behavior.

Rule 3 is a **documentation-expectation mismatch**, not a claim that the prose was unclear or missing. A later documentation update or workaround does not retroactively make an original bug report a documentation-clarity record.

### Error messages

Use when terminal or runtime diagnostic output is material to the reported setup experience.

- **Diagnostic-friction report:** the author could not map the surfaced symptom to a next action, or the initial message exposed a low-level symptom before the useful cause.
- **Counterexample:** the message gave a concrete, actionable next step or compatibility requirement. Counterexamples remain topically coded but are reported separately from diagnostic-friction counts.

A second confusing message can coexist with an actionable warning; preserve both rather than forcing the record into a uniformly positive or negative classification.

### Configuration complexity

Use when progress depends on understanding or changing interacting configuration, config loading, module formats, project-root behavior, filesystem constraints, containers, monorepos, or environment-specific settings.

This code describes the selected report. It does not establish that typical Vite configuration is complex.

## Uncertainty and context flags

- `attribution_uncertain:*`: the experience is relevant but Vite-only causation is not established.
- `counterexample:<category>`: the record provides counterevidence within that theme.
- `single_report:*`: a directly supported experience that must not be generalized beyond one author.
- `unanswered`: no accepted answer was present at collection.
- `root_cause_unconfirmed`: the source supports the experience but not a definitive mechanism.
- `historical_regression`: the report concerns a dated regression rather than a current unresolved defect.
- `documented_behavior_mismatch`: the source explicitly contrasts documentation with observed behavior.
- `historical_resolution_context`: later source context informs resolution but does not change the original evidence type.

## Claim rules

- Every finding must list its source IDs and URLs.
- Historical reports retain their original dates and version context.
- Closure does not by itself prove universal resolution.
- Suggested fixes in unanswered threads are not treated as confirmed causes.
- Public issue authors are not research participants. No interview or demographic claim may be inferred from their posts.
- Use “selected reports,” “authors reported,” or “within this sample”; do not generalize to all developers or all Vite users.
