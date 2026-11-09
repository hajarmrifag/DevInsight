import csv
import tempfile
import unittest
from pathlib import Path

from devinsight.pipeline import (
    RAW_FIELDS,
    build_findings,
    clean_rows,
    code_rows,
    deduplicate,
    render_report,
    review_suggestions,
    run_pipeline,
    validate_rows,
)


def row(**updates):
    value = {
        "source_id": "GH-1",
        "source_type": "issue",
        "repository": "vitejs/vite",
        "identifier": "1",
        "url": "https://github.com/vitejs/vite/issues/1",
        "title": "Setup error lacks documentation",
        "created_at": "2024-01-02",
        "excerpt": "The setup failed and the guide did not explain the error.",
        "selection_rationale": "First-hand setup report with reproducible detail.",
        "retrieved_at": "2026-11-08",
        "state_observed": "Open",
        "inclusion_status": "included",
        "evidence_direction": "problem_report",
        "human_codes": "",
        "review_flags": "",
        "researcher_notes": "",
    }
    value.update(updates)
    return value


class PipelineTests(unittest.TestCase):
    def test_validation_flags_bad_scope_date_and_long_excerpt(self):
        bad = row(repository="other/repo", created_at="01-02-2024", excerpt=" ".join(["word"] * 26))
        issues = validate_rows([bad])
        self.assertEqual({issue.field for issue in issues}, {"repository", "created_at", "excerpt"})

    def test_validation_flags_duplicate_source_id_and_url_identifier_mismatch(self):
        rows = [
            row(),
            row(source_id="GH-1", identifier="2", url="https://github.com/vitejs/vite/issues/3"),
        ]
        issues = validate_rows(rows)
        self.assertIn("source_id", {issue.field for issue in issues})
        self.assertTrue(any("must match issue identifier 2" in issue.message for issue in issues))

    def test_clean_and_deduplicate_uses_canonical_url(self):
        rows = clean_rows([row(), row(source_id="GH-2", url="https://github.com/vitejs/vite/issues/1/?x=tracking")])
        kept, duplicates = deduplicate(rows)
        self.assertEqual(len(kept), 1)
        self.assertEqual(duplicates[0]["duplicate_of"], "GH-1")

    def test_rule_coding_is_reviewable_and_multilabel(self):
        coded = code_rows(clean_rows([row()]))[0]
        self.assertIn("setup friction", coded["categories"])
        self.assertIn("documentation clarity", coded["categories"])
        self.assertIn("error messages", coded["categories"])
        self.assertEqual(coded["coding_status"], "rule_suggested_review_required")

    def test_researcher_codes_are_preserved_over_keyword_fallback(self):
        coded = code_rows(clean_rows([row(human_codes="documentation clarity")]))[0]
        self.assertEqual(coded["categories"], "documentation clarity")
        self.assertEqual(coded["coding_status"], "researcher_coded_adjudicated")

    def test_theme_specific_counterexample_is_separated(self):
        coded = code_rows(clean_rows([row(
            human_codes="error messages",
            review_flags="counterexample:error messages",
        )]))
        finding = build_findings(coded)[0]
        self.assertEqual(finding["counterexample_source_ids"], "GH-1")
        self.assertEqual(finding["experience_report_count"], "0")
        self.assertEqual(finding["counterexample_count"], "1")
        self.assertIn("counterexample_present", finding["flags"])

    def test_findings_report_frequency_without_quality_label(self):
        coded = code_rows(clean_rows([row()]))
        findings = build_findings(coded)
        self.assertTrue(findings)
        self.assertTrue(all(finding["source_ids"] == "GH-1" for finding in findings))
        self.assertTrue(all(finding["frequency_in_sample"] == "1/1 coded records" for finding in findings))
        self.assertTrue(all(finding["adjudication_status"] == "owner_approved" for finding in findings))
        self.assertTrue(all("support_status" not in finding for finding in findings))

    def test_llm_suggestion_missing_reference_is_unsupported(self):
        coded = code_rows(clean_rows([row()]))
        reviewed = review_suggestions([{
            "claim": "All developers always struggle.",
            "theme": "setup",
            "source_ids": ["UNKNOWN"],
        }], coded)[0]
        self.assertEqual(reviewed["support_status"], "unsupported")
        self.assertIn("missing_source_references", reviewed["flags"])
        self.assertIn("overgeneralized_language", reviewed["flags"])
        self.assertEqual(reviewed["review_status"], "pending_human_review")

    def test_declared_contradiction_is_flagged_for_review(self):
        coded = code_rows(clean_rows([row(), row(
            source_id="GH-2",
            identifier="2",
            url="https://github.com/vitejs/vite/issues/2",
            evidence_direction="contradicts_problem",
        )]))
        reviewed = review_suggestions([{
            "claim": "Two sample reports relate to setup.",
            "theme": "setup friction",
            "source_ids": ["GH-1"],
            "contradictory_source_ids": ["GH-2"],
        }], coded)[0]
        self.assertIn("contradictory_evidence_present", reviewed["flags"])
        self.assertIn("GH-2", reviewed["contradictory_source_ids"])

    def test_report_separates_public_analysis_from_interviews(self):
        coded = code_rows(clean_rows([row()]))
        report = render_report(coded, build_findings(coded), [])
        self.assertIn("No interviews were conducted", report)
        self.assertIn("not representative of all developers", report)
        self.assertIn("https://github.com/vitejs/vite/issues/1", report)

    def test_end_to_end_writes_auditable_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "evidence.csv"
            with source.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=RAW_FIELDS)
                writer.writeheader()
                writer.writerow(row())
            result = run_pipeline(source, root / "out")
            self.assertEqual(result["unique_rows"], 1)
            self.assertTrue((root / "out" / "coded-evidence.csv").exists())
            self.assertTrue((root / "out" / "findings-review.csv").exists())
            self.assertTrue((root / "out" / "evidence-pack.md").exists())


if __name__ == "__main__":
    unittest.main()
