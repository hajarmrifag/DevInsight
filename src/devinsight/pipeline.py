from __future__ import annotations

import csv
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, Sequence
from urllib.parse import urlsplit, urlunsplit


RAW_FIELDS = (
    "source_id",
    "source_type",
    "repository",
    "identifier",
    "url",
    "title",
    "created_at",
    "excerpt",
    "selection_rationale",
    "retrieved_at",
    "state_observed",
    "inclusion_status",
    "evidence_direction",
    "human_codes",
    "review_flags",
    "researcher_notes",
)

CATEGORIES = {
    "setup friction": (
        "install", "setup", "getting started", "scaffold", "create-vite",
        "npm create", "node version", "prerequisite", "onboarding", "new project",
    ),
    "documentation clarity": (
        "documentation", "docs", "guide", "unclear", "missing documentation",
        "example", "explain", "readme", "instruction",
    ),
    "error messages": (
        "error", "failed", "failure", "stack trace", "warning", "unexpected",
        "cannot", "could not", "message", "traceback",
    ),
    "configuration complexity": (
        "config", "configuration", "vite.config", "proxy", "alias", "plugin",
        "environment variable", ".env", "typescript", "migration", "build option",
    ),
}

ALLOWED_SOURCE_TYPES = {"issue", "discussion"}
ALLOWED_INCLUSION = {"included", "excluded", "pending"}
ALLOWED_DIRECTION = {"problem_report", "contradicts_problem", "unclear"}
SPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class ValidationIssue:
    row: int
    field: str
    message: str

    def format(self) -> str:
        return f"row {self.row}, {self.field}: {self.message}"


def normalize_text(value: str) -> str:
    return SPACE_RE.sub(" ", (value or "").strip())


def canonical_url(value: str) -> str:
    value = normalize_text(value)
    parts = urlsplit(value)
    path = parts.path.rstrip("/")
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, "", ""))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CSV has no header")
        missing = [field for field in RAW_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV header is missing: {', '.join(missing)}")
        return [dict(row) for row in reader]


def validate_rows(rows: Sequence[dict[str, str]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    seen_source_ids: dict[str, int] = {}
    required = (
        "source_id", "source_type", "repository", "identifier", "url", "title",
        "created_at", "excerpt", "selection_rationale", "retrieved_at",
        "inclusion_status", "evidence_direction",
    )
    for number, row in enumerate(rows, start=2):
        for field in required:
            if not normalize_text(row.get(field, "")):
                issues.append(ValidationIssue(number, field, "required value is blank"))
        source_type = normalize_text(row.get("source_type", "")).lower()
        if source_type and source_type not in ALLOWED_SOURCE_TYPES:
            issues.append(ValidationIssue(number, "source_type", "must be issue or discussion"))
        inclusion = normalize_text(row.get("inclusion_status", "")).lower()
        if inclusion and inclusion not in ALLOWED_INCLUSION:
            issues.append(ValidationIssue(number, "inclusion_status", "must be included, excluded, or pending"))
        direction = normalize_text(row.get("evidence_direction", "")).lower()
        if direction and direction not in ALLOWED_DIRECTION:
            issues.append(ValidationIssue(number, "evidence_direction", "invalid evidence direction"))
        human_codes = [code.strip() for code in row.get("human_codes", "").split("|") if code.strip()]
        invalid_codes = [code for code in human_codes if code not in CATEGORIES]
        if invalid_codes:
            issues.append(ValidationIssue(number, "human_codes", f"unknown code(s): {', '.join(invalid_codes)}"))
        url = canonical_url(row.get("url", ""))
        parts = urlsplit(url)
        if url and (parts.scheme != "https" or parts.netloc != "github.com"):
            issues.append(ValidationIssue(number, "url", "must be an https://github.com source URL"))
        repo = normalize_text(row.get("repository", ""))
        if repo and repo != "vitejs/vite":
            issues.append(ValidationIssue(number, "repository", "this study is scoped to vitejs/vite"))
        source_id = normalize_text(row.get("source_id", ""))
        if source_id:
            if source_id in seen_source_ids:
                issues.append(ValidationIssue(number, "source_id", f"duplicates row {seen_source_ids[source_id]}"))
            else:
                seen_source_ids[source_id] = number
        identifier = normalize_text(row.get("identifier", ""))
        if url and repo == "vitejs/vite" and source_type in ALLOWED_SOURCE_TYPES and identifier:
            source_path = "issues" if source_type == "issue" else "discussions"
            expected_path = f"/vitejs/vite/{source_path}/{identifier}"
            if parts.path != expected_path:
                issues.append(ValidationIssue(number, "url", f"must match {source_type} identifier {identifier}"))
        for field in ("created_at", "retrieved_at"):
            value = normalize_text(row.get(field, ""))
            if value:
                try:
                    date.fromisoformat(value)
                except ValueError:
                    issues.append(ValidationIssue(number, field, "must use YYYY-MM-DD"))
        excerpt_words = normalize_text(row.get("excerpt", "")).split()
        if len(excerpt_words) > 25:
            issues.append(ValidationIssue(number, "excerpt", "must be 25 words or fewer"))
    return issues


def clean_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    cleaned: list[dict[str, str]] = []
    for row in rows:
        item = {field: normalize_text(row.get(field, "")) for field in RAW_FIELDS}
        item["source_type"] = item["source_type"].lower()
        item["inclusion_status"] = item["inclusion_status"].lower()
        item["evidence_direction"] = item["evidence_direction"].lower()
        item["url"] = canonical_url(item["url"])
        cleaned.append(item)
    return cleaned


def deduplicate(rows: Iterable[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    kept: list[dict[str, str]] = []
    duplicates: list[dict[str, str]] = []
    seen: dict[str, str] = {}
    for row in rows:
        key = canonical_url(row["url"]) or f'{row["repository"].lower()}#{row["identifier"].lower()}'
        if key in seen:
            duplicate = dict(row)
            duplicate["duplicate_of"] = seen[key]
            duplicates.append(duplicate)
            continue
        seen[key] = row["source_id"]
        kept.append(row)
    return kept, duplicates


def code_row(row: dict[str, str]) -> dict[str, str]:
    haystack = " ".join((row["title"], row["excerpt"], row["selection_rationale"], row["researcher_notes"])).lower()
    human_codes = [code.strip() for code in row.get("human_codes", "").split("|") if code.strip()]
    matches = human_codes or [
        category
        for category, terms in CATEGORIES.items()
        if any(term in haystack for term in terms)
    ]
    coded = dict(row)
    coded["categories"] = " | ".join(matches) if matches else "uncoded / human review"
    coded["coding_status"] = "researcher_coded_adjudicated" if human_codes else "rule_suggested_review_required"
    return coded


def code_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    return [code_row(row) for row in rows]


def build_findings(coded_rows: Sequence[dict[str, str]]) -> list[dict[str, str]]:
    included = [row for row in coded_rows if row["inclusion_status"] == "included"]
    findings: list[dict[str, str]] = []
    for category in CATEGORIES:
        carrying_code = [row for row in included if category in row["categories"].split(" | ")]
        counterexamples = [
            row for row in carrying_code
            if row["evidence_direction"] == "contradicts_problem"
            or f"counterexample:{category}" in row.get("review_flags", "").split(" | ")
        ]
        if not carrying_code:
            continue
        experience_reports = [row for row in carrying_code if row not in counterexamples]
        count = len(carrying_code)
        experience_count = len(experience_reports)
        counterexample_count = len(counterexamples)
        flags: list[str] = []
        if counterexamples:
            flags.append("counterexample_present")
        if category == "error messages" and counterexample_count:
            report_word = "report" if experience_count == 1 else "reports"
            record_word = "record" if counterexample_count == 1 else "records"
            claim = (
                f"Within this purposive sample, {experience_count} public {report_word} described diagnostic friction "
                f"related to error messages, while {counterexample_count} {record_word} provided counterevidence."
            )
        else:
            claim = f"Within this purposive sample, {count} public report(s) were coded as {category}."
        findings.append({
            "finding_id": f"F{len(findings) + 1:02d}",
            "theme": category,
            "claim": claim,
            "source_ids": " | ".join(row["source_id"] for row in carrying_code),
            "experience_source_ids": " | ".join(row["source_id"] for row in experience_reports),
            "counterexample_source_ids": " | ".join(row["source_id"] for row in counterexamples),
            "coded_record_count": str(count),
            "experience_report_count": str(experience_count),
            "counterexample_count": str(counterexample_count),
            "sample_size": str(len(included)),
            "frequency_in_sample": f"{count}/{len(included)} coded records",
            "adjudication_status": "owner_approved",
            "flags": " | ".join(flags),
        })
    return findings


def load_llm_suggestions(path: Path | None) -> list[dict[str, object]]:
    if path is None:
        return []
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError("LLM suggestions JSON must be a list")
    return payload


def review_suggestions(
    suggestions: Sequence[dict[str, object]], coded_rows: Sequence[dict[str, str]]
) -> list[dict[str, str]]:
    by_id = {row["source_id"]: row for row in coded_rows}
    reviewed: list[dict[str, str]] = []
    broad_terms = ("all developers", "developers generally", "proves that", "always", "never")
    for index, suggestion in enumerate(suggestions, start=1):
        claim = normalize_text(str(suggestion.get("claim", "")))
        theme = normalize_text(str(suggestion.get("theme", "")))
        raw_ids = suggestion.get("source_ids", [])
        source_ids = [normalize_text(str(value)) for value in raw_ids] if isinstance(raw_ids, list) else []
        raw_contradictions = suggestion.get("contradictory_source_ids", [])
        contradiction_ids = (
            [normalize_text(str(value)) for value in raw_contradictions]
            if isinstance(raw_contradictions, list) else []
        )
        valid = [source_id for source_id in source_ids if source_id in by_id]
        missing = [source_id for source_id in source_ids if source_id not in by_id]
        flags: list[str] = []
        if not claim:
            flags.append("blank_claim")
        if not source_ids or not valid:
            support = "unsupported"
            flags.append("no_valid_source_references")
            if missing:
                flags.append("missing_source_references")
        elif missing:
            support = "unsupported"
            flags.append("missing_source_references")
        elif len(valid) < 2:
            support = "weak_sample_support"
            flags.append("single_source")
        else:
            support = "candidate_sample_support"
        if any(term in claim.lower() for term in broad_terms):
            flags.append("overgeneralized_language")
        direction_conflict = [sid for sid in valid if by_id[sid]["evidence_direction"] == "contradicts_problem"]
        declared_conflict = [sid for sid in contradiction_ids if sid in by_id]
        if direction_conflict or declared_conflict:
            flags.append("contradictory_evidence_present")
        reviewed.append({
            "suggestion_id": normalize_text(str(suggestion.get("suggestion_id", ""))) or f"S{index:02d}",
            "theme": theme,
            "claim": claim,
            "source_ids": " | ".join(source_ids),
            "valid_source_ids": " | ".join(valid),
            "missing_source_ids": " | ".join(missing),
            "contradictory_source_ids": " | ".join(declared_conflict + direction_conflict),
            "support_status": support,
            "review_status": "pending_human_review",
            "flags": " | ".join(dict.fromkeys(flags)),
            "rationale": normalize_text(str(suggestion.get("rationale", ""))),
        })
    return reviewed


def write_csv(path: Path, rows: Sequence[dict[str, str]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _source_links(source_ids: str, by_id: dict[str, dict[str, str]]) -> str:
    links = []
    for source_id in source_ids.split(" | ") if source_ids else []:
        row = by_id.get(source_id)
        if row:
            links.append(f'[{source_id}]({row["url"]})')
    return ", ".join(links) or "None"


def render_report(coded_rows: Sequence[dict[str, str]], findings: Sequence[dict[str, str]], suggestion_reviews: Sequence[dict[str, str]]) -> str:
    included = [row for row in coded_rows if row["inclusion_status"] == "included"]
    excluded = [row for row in coded_rows if row["inclusion_status"] == "excluded"]
    pending = [row for row in coded_rows if row["inclusion_status"] == "pending"]
    by_id = {row["source_id"]: row for row in coded_rows}
    types = Counter(row["source_type"] for row in included)
    dates = sorted(row["created_at"] for row in included if row["created_at"])
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "not available"
    retrieved_dates = sorted({row["retrieved_at"] for row in included if row["retrieved_at"]})
    collected = ", ".join(retrieved_dates) if retrieved_dates else "not available"

    lines = [
        "# DevInsight: Vite onboarding evidence pack",
        "",
        "> Scope: analysis of a small purposive sample of public `vitejs/vite` GitHub reports. It is not representative of all developers or all Vite users. No interviews took place. This independent portfolio project is not associated with MLH.",
        "",
        "## Research question",
        "",
        "What onboarding, documentation, or setup problems do developers report about Vite?",
        "",
        "## Methodology",
        "",
        "Public GitHub issues/discussions were selected using documented relevance criteria, validated against a fixed schema, normalized, and URL-deduplicated. Researcher-assigned multi-label codes are preserved in the input, and the flagged records were owner-adjudicated before publication. When human codes are absent, the pipeline falls back to transparent keyword suggestions that remain review-required.",
        "",
        "Every observation is an author-reported public experience. Source metadata, excerpts, and resolution context were checked against the linked pages; the underlying product behavior was not independently reproduced.",
        "",
        "The 2026-11-08 search combined the public Vite issue/discussion indexes with terms including `create-vite`, `getting started`, `setup`, `install`, `Node version`, `documentation`, `docs`, `scaffold`, `error when starting dev server`, `failed to load config`, and `fresh project fails`.",
        "",
        "Inclusion requires a public report in `vitejs/vite` that describes onboarding, documentation, initial setup, a setup-related error, or configuration friction and contains enough detail to code. Exclusions include duplicates, unrelated runtime bugs, general feature requests without onboarding evidence, and items lacking usable first-hand detail.",
        "",
        "## Sample",
        "",
        f"- Included: {len(included)} (issues: {types.get('issue', 0)}; discussions: {types.get('discussion', 0)})",
        f"- Excluded rows in the imported CSV: {len(excluded)}",
        f"- Pending eligibility rows in the imported CSV: {len(pending)}",
        f"- Included source creation dates: {date_range}",
        f"- Collection snapshot: {collected}",
        "",
        "This is issue analysis, not participant research. No interviews were conducted for this project.",
        "",
        "## Evidence inventory",
        "",
        "| Source | Created | State observed | Brief excerpt | Final codes | Adjudication notes |",
        "|---|---:|---|---|---|---|",
    ]
    for row in included:
        excerpt = row["excerpt"].replace("|", "\\|")
        title = row["title"].replace("|", "\\|")
        categories = row["categories"].replace(" | ", "; ")
        review_flags = row["review_flags"].replace(" | ", "; ") or "None"
        lines.append(
            f'| [{row["source_type"].title()} #{row["identifier"]}]({row["url"]}) — {title} | '
            f'{row["created_at"]} | {row["state_observed"] or "Not recorded"} | “{excerpt}” | '
            f'{categories} | {review_flags} |'
        )
    if not included:
        lines.append("| — | — | — | No included evidence was available. | — | Evidence import required |")
    lines.extend([
        "",
        "## Theme and evidence table",
        "",
        "| Theme | Frequency in sample | Sample-bounded finding | Experience reports | Counterevidence | Status |",
        "|---|---:|---|---|---|---|",
    ])
    if findings:
        for finding in findings:
            lines.append(
                f'| {finding["theme"]} | {finding["frequency_in_sample"]} | {finding["claim"]} | '
                f'{_source_links(finding["experience_source_ids"], by_id)} | '
                f'{_source_links(finding["counterexample_source_ids"], by_id)} | '
                f'{finding["adjudication_status"]} |'
            )
    else:
        lines.append("| — | 0/0 | No included evidence was available. | None | None | Evidence import required |")

    qualified_findings = [finding for finding in findings if finding["flags"]]
    qualified_suggestions = [
        review for review in suggestion_reviews
        if review["support_status"] != "candidate_sample_support" or review["flags"]
    ]
    lines.extend(["", "## Counterevidence and uncertainty", ""])
    if qualified_findings or qualified_suggestions:
        for finding in qualified_findings:
            lines.append(
                f'- **{finding["finding_id"]}:** {finding["claim"]} '
                f'Counterevidence: {_source_links(finding["counterexample_source_ids"], by_id)}.'
            )
        for review in qualified_suggestions:
            lines.append(
                f'- **{review["suggestion_id"]}:** {review["claim"]} — '
                f'{review["support_status"]}; flags: {review["flags"] or "none"}.'
            )
    else:
        lines.append("No counterevidence or unresolved suggestion flags were generated.")
    flagged_records = [row for row in included if row.get("review_flags")]
    if flagged_records:
        lines.extend(["", "### Record-level adjudication notes", ""])
        for row in flagged_records:
            lines.append(f'- [{row["source_id"]}]({row["url"]}): {row["review_flags"]}.')

    lines.extend([
        "",
        "## Optional LLM suggestions",
        "",
        f"{len(suggestion_reviews)} suggestion(s) were imported. Suggestions are never accepted automatically; see `llm-suggestion-review.csv` for references, missing sources, flags, and review status.",
        "",
        "## Limitations",
        "",
        "- The purposive sample is small and shaped by repository search terms, issue-reporting behavior, and public visibility.",
        "- A GitHub post is an authored report, not a direct observation of task performance.",
        "- Final researcher codes reflect the approved adjudication log; keyword fallback codes, if used on future imports, can miss context, sarcasm, workarounds, or multi-theme evidence.",
        "- Frequencies are descriptive counts within this sample, not confidence scores or evidence-quality ratings.",
        "- Counts describe this sample only and must not be generalized to all developers or Vite users.",
        "- Closed, resolved, or older reports may not reflect the current Vite experience.",
        "- English-language search terms and public issue-reporting behavior favor visible, well-described failures.",
        "- Present-day reproducibility, task completion, severity, time-to-resolution, and incidence were not tested.",
        "",
        "## Potential follow-up interview questions",
        "",
        "1. Tell me about the last time you created or migrated a Vite project. Where did you pause or seek help?",
        "2. Which setup instructions did you expect to find, and what was missing or ambiguous?",
        "3. What did the first error or warning lead you to try, and why?",
        "4. Which configuration decision required the most prior knowledge?",
        "5. What would have made the setup feel complete and trustworthy?",
        "",
        "These are proposed questions only. The separate research-operations kit supports future fieldwork; it does not imply interviews occurred.",
        "",
        "## Publication verification checklist",
        "",
        "- Open every linked source and confirm identifier, date, excerpt, and relevance.",
        "- Confirm that final researcher codes match the approved adjudication log.",
        "- Review every counterexample, unsupported suggestion, or overgeneralized claim.",
        "- Re-run the pipeline after edits and retain the generated audit files.",
    ])
    return "\n".join(lines) + "\n"


def run_pipeline(input_path: Path, output_dir: Path, suggestions_path: Path | None = None) -> dict[str, int]:
    raw = read_csv(input_path)
    issues = validate_rows(raw)
    if issues:
        detail = "\n".join(issue.format() for issue in issues)
        raise ValueError(f"Evidence validation failed:\n{detail}")
    cleaned = clean_rows(raw)
    unique, duplicates = deduplicate(cleaned)
    coded = code_rows(unique)
    findings = build_findings(coded)
    suggestions = load_llm_suggestions(suggestions_path)
    suggestion_reviews = review_suggestions(suggestions, coded)

    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "coded-evidence.csv", coded, (*RAW_FIELDS, "categories", "coding_status"))
    write_csv(output_dir / "duplicates.csv", duplicates, (*RAW_FIELDS, "duplicate_of"))
    finding_fields = (
        "finding_id", "theme", "claim", "source_ids", "experience_source_ids",
        "counterexample_source_ids", "coded_record_count", "experience_report_count",
        "counterexample_count", "sample_size", "frequency_in_sample",
        "adjudication_status", "flags",
    )
    write_csv(output_dir / "findings-review.csv", findings, finding_fields)
    suggestion_fields = ("suggestion_id", "theme", "claim", "source_ids", "valid_source_ids", "missing_source_ids", "contradictory_source_ids", "support_status", "review_status", "flags", "rationale")
    write_csv(output_dir / "llm-suggestion-review.csv", suggestion_reviews, suggestion_fields)
    (output_dir / "evidence-pack.md").write_text(render_report(coded, findings, suggestion_reviews), encoding="utf-8")
    return {
        "input_rows": len(raw),
        "unique_rows": len(unique),
        "duplicates": len(duplicates),
        "findings": len(findings),
        "llm_suggestions": len(suggestion_reviews),
    }
