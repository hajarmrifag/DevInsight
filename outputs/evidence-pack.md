# DevInsight: Vite onboarding evidence pack

> Scope: analysis of a small purposive sample of public `vitejs/vite` GitHub reports. It is not representative of all developers or all Vite users. No interviews took place. This independent portfolio project is not associated with MLH.

## Research question

What onboarding, documentation, or setup problems do developers report about Vite?

## Methodology

Public GitHub issues/discussions were selected using documented relevance criteria, validated against a fixed schema, normalized, and URL-deduplicated. Researcher-assigned multi-label codes are preserved in the input, and the flagged records were owner-adjudicated before publication. When human codes are absent, the pipeline falls back to transparent keyword suggestions that remain review-required.

Every observation is an author-reported public experience. Source metadata, excerpts, and resolution context were checked against the linked pages; the underlying product behavior was not independently reproduced.

The 2026-11-08 search combined the public Vite issue/discussion indexes with terms including `create-vite`, `getting started`, `setup`, `install`, `Node version`, `documentation`, `docs`, `scaffold`, `error when starting dev server`, `failed to load config`, and `fresh project fails`.

Inclusion requires a public report in `vitejs/vite` that describes onboarding, documentation, initial setup, a setup-related error, or configuration friction and contains enough detail to code. Exclusions include duplicates, unrelated runtime bugs, general feature requests without onboarding evidence, and items lacking usable first-hand detail.

## Sample

- Included: 18 (issues: 15; discussions: 3)
- Excluded rows in the imported CSV: 0
- Pending eligibility rows in the imported CSV: 0
- Included source creation dates: 2021-01-16 to 2025-09-23
- Collection snapshot: 2026-11-08

This is issue analysis, not participant research. No interviews were conducted for this project.

## Evidence inventory

| Source | Created | State observed | Brief excerpt | Final codes | Adjudication notes |
|---|---:|---|---|---|---|
| [Issue #18812](https://github.com/vitejs/vite/issues/18812) — Vite project not created in Node version | 2024-11-28 | Closed as not planned | “running the command npm create vite@latest to initialize a new Vite project results in an error.” | setup friction | None |
| [Issue #19539](https://github.com/vitejs/vite/issues/19539) — New `create-vite` command wont work with `--template` flag | 2025-02-28 | Closed | “it is asking me to choose a framework” | setup friction | None |
| [Issue #13129](https://github.com/vitejs/vite/issues/13129) — New TypeScript React app using Vite - JSX.IntrinsicElements errors | 2023-05-09 | Closed | “I'm trying out Vite with React TS and using their official documentation.” | setup friction | attribution_uncertain:editor_types_compatibility |
| [Issue #7007](https://github.com/vitejs/vite/issues/7007) — Add troubleshooting and container sections to documentation for faster start | 2022-02-20 | Closed | “I spent many hours trying to figure out what need to git this going.” | setup friction; documentation clarity; configuration complexity | non_default_container_context |
| [Issue #16734](https://github.com/vitejs/vite/issues/16734) — Incomprehensible Node.js version requirement in documentation | 2024-05-21 | Closed | “What is the actual requirement? Version 18+? Version 20+? Either? Anything in between?” | documentation clarity | None |
| [Issue #13253](https://github.com/vitejs/vite/issues/13253) — Update root documentation to include vite config file location | 2023-05-18 | Closed | “it does not mention that we ALSO have to move the Vite config file” | documentation clarity; configuration complexity | None |
| [Issue #12891](https://github.com/vitejs/vite/issues/12891) — Documentation for disabling CORS is confusing | 2023-04-18 | Closed as not planned | “Just clarify what the correct way is to disable CORS?” | documentation clarity; configuration complexity | None |
| [Issue #15690](https://github.com/vitejs/vite/issues/15690) — Provide documentation in TypeScript and JavaScript flavours | 2024-01-22 | Closed as not planned | “Also examples, examples, examples.” | documentation clarity | single_report:javascript_friendly_documentation |
| [Discussion #19031](https://github.com/vitejs/vite/discussions/19031) — Having trouble starting dev server for my Vite project | 2024-12-20 | Answered | “ReferenceError: structuredClone is not defined.” | setup friction; error messages | None |
| [Issue #20822](https://github.com/vitejs/vite/issues/20822) — pnpm create vite - fresh project fails to start | 2025-09-23 | Closed as completed | “When initializing a new project with pnpm create vite, the project fails to start after installation.” | setup friction; error messages | counterexample:error messages; separate_native_binding_error |
| [Discussion #15108](https://github.com/vitejs/vite/discussions/15108) — Urgent Help - Unable to view my React Project when I perform npm run dev | 2023-11-22 | Answered | “Error: The specified module could not be found.” | error messages | None |
| [Issue #5801](https://github.com/vitejs/vite/issues/5801) — Error when starting dev server permission denied 127.0.0.1:3000 | 2021-11-22 | Closed as environment-specific | “If need to flip a permission, I just need to know which one.” | setup friction; error messages | None |
| [Discussion #17324](https://github.com/vitejs/vite/discussions/17324) — How to solve: Error: ENOENT: no such file or directory , open vite.config.js | 2024-05-27 | Unanswered | “I don't know what else to do.” | error messages; configuration complexity | unanswered; root_cause_unconfirmed |
| [Issue #18839](https://github.com/vitejs/vite/issues/18839) — Cannot start Vite 6 due to .vite-temp directory creation in node_modules | 2024-11-29 | Closed by linked fix | “There is a new `.vite-temp` directory that is trying to be created in the `node_modules` directory, which fails.” | setup friction; configuration complexity | None |
| [Issue #1560](https://github.com/vitejs/vite/issues/1560) — Fail to import packages in vite.config.ts when "type": "module" is set | 2021-01-16 | Closed | “TypeError [ERR_INVALID_URL]: Invalid URL: vite.” | error messages; configuration complexity | None |
| [Issue #5370](https://github.com/vitejs/vite/issues/5370) — vite.config.ts can't import untranspiled ts files from other packages in the same monorepo | 2021-10-21 | Open | “There are two workarounds: compile the ts file to the common js file, or specify the importee path to its real file path.” | configuration complexity | historical_resolution_context |
| [Issue #12923](https://github.com/vitejs/vite/issues/12923) — Failed to load vite.config.js during build - Cannot use import statement outside a module | 2023-04-20 | Closed | “the import/export statements in it should be pre-processed according to the documentation.” | documentation clarity; configuration complexity | historical_regression; documented_behavior_mismatch |
| [Issue #13631](https://github.com/vitejs/vite/issues/13631) — Vite cannot load vite.config.ts with Node 17 and vite@4.4.0-beta.3 | 2023-06-25 | Closed | “Error: The URL must be of scheme file.” | error messages; configuration complexity | None |

## Theme and evidence table

| Theme | Frequency in sample | Sample-bounded finding | Experience reports | Counterevidence | Status |
|---|---:|---|---|---|---|
| setup friction | 8/18 coded records | Within this purposive sample, 8 public report(s) were coded as setup friction. | [GH-I-18812](https://github.com/vitejs/vite/issues/18812), [GH-I-19539](https://github.com/vitejs/vite/issues/19539), [GH-I-13129](https://github.com/vitejs/vite/issues/13129), [GH-I-7007](https://github.com/vitejs/vite/issues/7007), [GH-D-19031](https://github.com/vitejs/vite/discussions/19031), [GH-I-20822](https://github.com/vitejs/vite/issues/20822), [GH-I-5801](https://github.com/vitejs/vite/issues/5801), [GH-I-18839](https://github.com/vitejs/vite/issues/18839) | None | owner_approved |
| documentation clarity | 6/18 coded records | Within this purposive sample, 6 public report(s) were coded as documentation clarity. | [GH-I-7007](https://github.com/vitejs/vite/issues/7007), [GH-I-16734](https://github.com/vitejs/vite/issues/16734), [GH-I-13253](https://github.com/vitejs/vite/issues/13253), [GH-I-12891](https://github.com/vitejs/vite/issues/12891), [GH-I-15690](https://github.com/vitejs/vite/issues/15690), [GH-I-12923](https://github.com/vitejs/vite/issues/12923) | None | owner_approved |
| error messages | 7/18 coded records | Within this purposive sample, 6 public reports described diagnostic friction related to error messages, while 1 record provided counterevidence. | [GH-D-19031](https://github.com/vitejs/vite/discussions/19031), [GH-D-15108](https://github.com/vitejs/vite/discussions/15108), [GH-I-5801](https://github.com/vitejs/vite/issues/5801), [GH-D-17324](https://github.com/vitejs/vite/discussions/17324), [GH-I-1560](https://github.com/vitejs/vite/issues/1560), [GH-I-13631](https://github.com/vitejs/vite/issues/13631) | [GH-I-20822](https://github.com/vitejs/vite/issues/20822) | owner_approved |
| configuration complexity | 9/18 coded records | Within this purposive sample, 9 public report(s) were coded as configuration complexity. | [GH-I-7007](https://github.com/vitejs/vite/issues/7007), [GH-I-13253](https://github.com/vitejs/vite/issues/13253), [GH-I-12891](https://github.com/vitejs/vite/issues/12891), [GH-D-17324](https://github.com/vitejs/vite/discussions/17324), [GH-I-18839](https://github.com/vitejs/vite/issues/18839), [GH-I-1560](https://github.com/vitejs/vite/issues/1560), [GH-I-5370](https://github.com/vitejs/vite/issues/5370), [GH-I-12923](https://github.com/vitejs/vite/issues/12923), [GH-I-13631](https://github.com/vitejs/vite/issues/13631) | None | owner_approved |

## Counterevidence and uncertainty

- **F03:** Within this purposive sample, 6 public reports described diagnostic friction related to error messages, while 1 record provided counterevidence. Counterevidence: [GH-I-20822](https://github.com/vitejs/vite/issues/20822).

### Record-level adjudication notes

- [GH-I-13129](https://github.com/vitejs/vite/issues/13129): attribution_uncertain:editor_types_compatibility.
- [GH-I-7007](https://github.com/vitejs/vite/issues/7007): non_default_container_context.
- [GH-I-15690](https://github.com/vitejs/vite/issues/15690): single_report:javascript_friendly_documentation.
- [GH-I-20822](https://github.com/vitejs/vite/issues/20822): counterexample:error messages | separate_native_binding_error.
- [GH-D-17324](https://github.com/vitejs/vite/discussions/17324): unanswered | root_cause_unconfirmed.
- [GH-I-5370](https://github.com/vitejs/vite/issues/5370): historical_resolution_context.
- [GH-I-12923](https://github.com/vitejs/vite/issues/12923): historical_regression | documented_behavior_mismatch.

## Optional LLM suggestions

0 suggestion(s) were imported. Suggestions are never accepted automatically; see `llm-suggestion-review.csv` for references, missing sources, flags, and review status.

## Limitations

- The purposive sample is small and shaped by repository search terms, issue-reporting behavior, and public visibility.
- A GitHub post is an authored report, not a direct observation of task performance.
- Final researcher codes reflect the approved adjudication log; keyword fallback codes, if used on future imports, can miss context, sarcasm, workarounds, or multi-theme evidence.
- Frequencies are descriptive counts within this sample, not confidence scores or evidence-quality ratings.
- Counts describe this sample only and must not be generalized to all developers or Vite users.
- Closed, resolved, or older reports may not reflect the current Vite experience.
- English-language search terms and public issue-reporting behavior favor visible, well-described failures.
- Present-day reproducibility, task completion, severity, time-to-resolution, and incidence were not tested.

## Potential follow-up interview questions

1. Tell me about the last time you created or migrated a Vite project. Where did you pause or seek help?
2. Which setup instructions did you expect to find, and what was missing or ambiguous?
3. What did the first error or warning lead you to try, and why?
4. Which configuration decision required the most prior knowledge?
5. What would have made the setup feel complete and trustworthy?

These are proposed questions only. The separate research-operations kit supports future fieldwork; it does not imply interviews occurred.

## Publication verification checklist

- Open every linked source and confirm identifier, date, excerpt, and relevance.
- Confirm that final researcher codes match the approved adjudication log.
- Review every counterexample, unsupported suggestion, or overgeneralized claim.
- Re-run the pipeline after edits and retain the generated audit files.
