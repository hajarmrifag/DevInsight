# DevInsight

DevInsight is a small, evidence-first portfolio project demonstrating a Developer Research Coordinator workflow. It asks:

> **What onboarding, documentation, or setup problems do developers report about Vite?**

The project analyzes 18 public `vitejs/vite` GitHub issues and discussions collected through purposive search on 2026-11-08. It preserves source links, separates author reports from researcher interpretation, records counterevidence, and keeps every substantive finding reviewable.

This is exploratory public-issue analysis—not participant research, a prevalence study, or a product-quality score. No interviews took place, and the project is not associated with Vite or MLH.

## Key findings

Codes overlap because one report can describe more than one kind of friction.

| Theme | Frequency in this sample | Evidence-bounded interpretation |
|---|---:|---|
| Configuration complexity | 9/18 | Selected reports cluster around config loading and environment boundaries such as module formats, containers, monorepos, filesystem constraints, and unsupported Node versions. |
| Setup friction | 8/18 | Eight authors reported friction during scaffolding, an official starter/example, first server start, or non-default environment setup. |
| Documentation clarity | 6/18 | Reports requested clearer prerequisites, task-linked guidance, JavaScript-friendly examples, container troubleshooting, or described an explicit documentation/behavior mismatch. |
| Error messages | 7/18 relevant records | Six reports described diagnostic friction; one record provided counterevidence through an actionable Node.js version warning while also containing a separate native-binding error. |

These frequencies describe the selected records only. They are not confidence scores, evidence-quality ratings, statistical significance, or estimates for all developers.

## Start here

- [Research report](reports/vite-onboarding-friction.md) — concise methodology, evidence register, findings, counterevidence, uncertainty, and limitations.
- [Codebook](research/codebook.md) — category definitions and the boundary between author reports, verified source context, and interpretation.
- [Final adjudication log](review/adjudication-log.md) — approved decisions for the seven reviewed records.
- [Publication-readiness audit](review/pre-publication-audit-report.md) — final research, privacy, attribution, link, packaging, and test checks.
- [Generated evidence pack](outputs/evidence-pack.md) — deterministic inventory and finding tables produced by the CLI.
- [Research-operations kit](research_ops/participant-screener.md) — future-only screener, communications templates, blank tracker, and fieldwork checklist. It does not imply completed fieldwork.

## Method

The sample contains 15 issues and 3 discussions created from 2021 through 2025. Records were included when an original post described a concrete onboarding, documentation, setup-error, migration, or configuration task and supplied enough detail for source-linked coding. Duplicates, unrelated runtime bugs, vague complaints, and feature requests without relevant task evidence were excluded.

The observation unit is one original public post—not one developer, confirmed defect, or verified root cause. Comments and accepted answers provide resolution context but are not independently counted. Product behavior was not reproduced by this project.

## Reproduce the analysis

Python 3.10+ is required. Runtime dependencies: none.

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m devinsight validate data/raw/evidence.csv
python -m devinsight build data/raw/evidence.csv --output-dir outputs
python -m unittest discover -s tests -v
```

Generated artifacts:

- `outputs/coded-evidence.csv` — normalized final codes and adjudication notes.
- `outputs/duplicates.csv` — duplicate audit.
- `outputs/findings-review.csv` — source IDs, frequency-only counts, experience reports, and counterexamples.
- `outputs/llm-suggestion-review.csv` — optional offline suggestion audit; no suggestions were used for the published sample.
- `outputs/evidence-pack.md` — generated evidence inventory and sample-bounded findings.

Optional theme suggestions can be supplied as offline JSON matching `data/llm-suggestions.example.json`. Suggestions are never accepted automatically and must cite valid source IDs.

## Repository map

```text
data/raw/evidence.csv                Source-preserving 18-record sample
reports/vite-onboarding-friction.md Human-synthesized research report
research/codebook.md                Final category and claim rules
review/adjudication-log.md           Approved pre-publication decisions
review/pre-publication-audit-report.md Final release audit
research_ops/                       Future interview operations templates
src/devinsight/                     Standard-library pipeline and CLI
tests/                              Automated validation and report tests
outputs/                            Reproducible evidence pack and audit CSVs
```

## Limitations

- Small, purposive, English-language public GitHub sample with no denominator.
- Search and issue-reporting behavior favor visible, well-described failures.
- Records span historical Vite versions, beta releases, unsupported environments, and closed issues; they are not all current unresolved defects.
- Root-cause attribution remains uncertain for some records, and no current-version reproduction was performed.
- No interviews, usability tests, demographic analysis, or representative prevalence estimates were conducted.
- Frequencies are overlapping sample descriptions, not measures of confidence or severity.

## Public-data handling and license

The dataset retains URLs, identifiers, dates, brief excerpts, and research notes while excluding usernames, contact details, and inferred demographics. See [ATTRIBUTION.md](ATTRIBUTION.md) for public-data handling and source attribution.

Original project code and documentation are available under the [MIT License](LICENSE). Linked GitHub content remains attributable to its original authors and is not relicensed here.
