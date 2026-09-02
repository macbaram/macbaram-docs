from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/validate_public_docs.py"
PUBLIC_ROOT = MODULE_PATH.parents[1]
SPEC = importlib.util.spec_from_file_location("validate_public_docs", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ForbiddenContentTests(unittest.TestCase):
    def labels(self, text: str) -> set[str]:
        return {
            label
            for label, pattern in VALIDATOR.FORBIDDEN_PATTERNS.items()
            if pattern.search(text)
        }

    def test_canonical_download_is_allowed(self) -> None:
        self.assertEqual(self.labels("https://www.macbaram.com/download"), set())

    def test_version_specific_package_is_rejected(self) -> None:
        labels = self.labels("https://www.macbaram.com/files/MacBaram-1.2.3.pkg")
        self.assertIn("version-specific package URL", labels)

    def test_technical_download_paths_are_rejected(self) -> None:
        self.assertIn("technical download path", self.labels("/downloads/latest.json"))

    def test_price_is_rejected(self) -> None:
        self.assertIn("duplicated dollar price", self.labels("Only $4.99"))

    def test_commercial_state_is_rejected(self) -> None:
        self.assertIn("duplicated commercial state", self.labels("A free trial is available"))

    def test_internal_path_is_rejected(self) -> None:
        self.assertIn("private local path", self.labels("/Users/example/private.log"))

    def test_secret_like_assignment_is_rejected(self) -> None:
        self.assertIn("token-like secret", self.labels("access_token = hidden"))

    def test_imac_support_claim_is_rejected(self) -> None:
        self.assertIn("iMac support claim", self.labels("iMac is fully supported"))

    def test_imac_boundary_is_allowed(self) -> None:
        self.assertEqual(self.labels("iMac support is not currently declared"), set())

    def test_marketing_cta_does_not_bypass_download_canonical(self) -> None:
        self.assertEqual(self.labels("Official Download: https://www.macbaram.com/download"), set())

    def test_negative_creator_criticism_wording_is_rejected(self) -> None:
        self.assertIn(
            "negative creator criticism wording",
            self.labels("Honest public " + "criticism is not restricted."),
        )

    def test_positive_review_editorial_independence_is_allowed(self) -> None:
        self.assertEqual(
            self.labels(
                "If a creator chooses to publish a review, MacBaram does not interfere with its content or conclusion."
            ),
            set(),
        )


class StatusBoundaryTests(unittest.TestCase):
    def valid_facts(self) -> dict[str, dict[str, object]]:
        return {
            fact_id: {"id": fact_id, "status": status}
            for fact_id, status in VALIDATOR.EXPECTED_FACT_STATUSES.items()
        }

    def test_current_and_non_current_status_contract_passes(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_fact_status_contract(errors, self.valid_facts())
        self.assertEqual(errors, [])

    def test_enterprise_cannot_be_promoted_to_available(self) -> None:
        facts = self.valid_facts()
        facts["enterprise-single"]["status"] = "available"
        errors: list[str] = []
        VALIDATOR.validate_fact_status_contract(errors, facts)
        self.assertTrue(any("enterprise-single must be roadmap" in error for error in errors))

    def test_unregistered_fact_is_rejected(self) -> None:
        facts = self.valid_facts()
        facts["fictional-auto-tuning"] = {
            "id": "fictional-auto-tuning",
            "status": "available",
        }
        errors: list[str] = []
        VALIDATOR.validate_fact_status_contract(errors, facts)
        self.assertIn("unregistered public fact: fictional-auto-tuning", errors)

    def test_all_approved_current_and_roadmap_facts_are_required(self) -> None:
        required = {
            "virtual-clamshell": "available",
            "power-only": "available",
            "safety-drain": "available",
            "heat-protection": "available",
            "individual-plan-lineup": "available",
            "creator-sponsorship-application": "available",
            "supporters-referral-operation": "concept",
            "workload-auto-detection": "roadmap",
            "enterprise-single": "roadmap",
            "enterprise-fleet": "roadmap",
        }
        for fact_id, status in required.items():
            self.assertEqual(VALIDATOR.EXPECTED_FACT_STATUSES[fact_id], status)

    def test_non_current_fact_summary_cannot_claim_current_availability(self) -> None:
        facts = self.valid_facts()
        facts["enterprise-single"]["summary"] = "Enterprise Single is currently available."
        errors: list[str] = []
        VALIDATOR.validate_fact_status_contract(errors, facts)
        self.assertTrue(any("promotes a non-current item" in error for error in errors))

    def test_non_current_fact_summary_cannot_claim_launch(self) -> None:
        facts = self.valid_facts()
        facts["enterprise-single"]["summary"] = "Enterprise Single launched today as a product plan."
        errors: list[str] = []
        VALIDATOR.validate_fact_status_contract(errors, facts)
        self.assertTrue(any("promotes a non-current item" in error for error in errors))

    def test_roadmap_terms_are_detected_case_insensitively(self) -> None:
        self.assertIn(
            "Enterprise Single",
            VALIDATOR.roadmap_only_terms("ENTERPRISE SINGLE is available now"),
        )

    def test_roadmap_copy_cannot_contradict_its_status(self) -> None:
        claims = VALIDATOR.noncurrent_promotion_claims(
            "Enterprise Single is currently available now.\n"
            "Supporters is currently operational."
        )
        self.assertEqual(len(claims), 2)

    def test_current_creator_application_is_not_a_roadmap_term(self) -> None:
        self.assertEqual(
            VALIDATOR.noncurrent_promotion_claims(
                "Creator Sponsorship applications are currently open."
            ),
            [],
        )

    def test_plain_availability_claim_is_rejected(self) -> None:
        self.assertEqual(
            VALIDATOR.noncurrent_promotion_claims("Enterprise Single is available."),
            ["Enterprise Single is available."],
        )

    def test_mixed_positive_and_negative_clauses_do_not_bypass_guard(self) -> None:
        claims = VALIDATOR.noncurrent_promotion_claims(
            "Enterprise Single is currently available, not merely a roadmap.\n"
            "Supporters is live, but settlement is not operational.\n"
            "Enterprise Fleet is currently available without restrictions."
        )
        self.assertEqual(len(claims), 3)

    def test_explicit_non_current_copy_is_allowed(self) -> None:
        claims = VALIDATOR.noncurrent_promotion_claims(
            "Enterprise Single is not currently available.\n"
            "Supporters referral tracking is not currently operational."
        )
        self.assertEqual(claims, [])

    def test_approved_reference_surfaces_must_keep_roadmap_negative(self) -> None:
        claims = VALIDATOR.noncurrent_promotion_claims(
            "Enterprise Single is not a current plan or feature."
        )
        self.assertEqual(claims, [])

    def test_full_roadmap_validation_rejects_mutated_faq(self) -> None:
        original_root = VALIDATOR.ROOT
        with tempfile.TemporaryDirectory() as directory:
            mutated_root = Path(directory) / "public-docs"
            shutil.copytree(PUBLIC_ROOT, mutated_root)
            with (mutated_root / "docs/faq.md").open("a", encoding="utf-8") as handle:
                handle.write("\nEnterprise Single is currently available.\n")
            try:
                VALIDATOR.ROOT = mutated_root
                errors: list[str] = []
                VALIDATOR.validate_roadmap_boundaries(errors)
            finally:
                VALIDATOR.ROOT = original_root
        self.assertTrue(any("non-current item promoted as current" in error for error in errors))

    def test_creator_growth_relationship_is_required(self) -> None:
        original_root = VALIDATOR.ROOT
        with tempfile.TemporaryDirectory() as directory:
            mutated_root = Path(directory) / "public-docs"
            shutil.copytree(PUBLIC_ROOT, mutated_root)
            roadmap_path = mutated_root / "docs/roadmap.md"
            roadmap = roadmap_path.read_text(encoding="utf-8")
            roadmap_path.write_text(
                roadmap.replace(
                    "MacBaram aims to listen to creators who voluntarily share product shortcomings and improvement ideas, consider that input in product development, and grow with creators. ",
                    "",
                ),
                encoding="utf-8",
            )
            try:
                VALIDATOR.ROOT = mutated_root
                errors: list[str] = []
                VALIDATOR.validate_roadmap_boundaries(errors)
            finally:
                VALIDATOR.ROOT = original_root
        self.assertIn(
            "docs/roadmap.md must preserve the voluntary Creator growth relationship",
            errors,
        )


class LiveSourceEvidenceTests(unittest.TestCase):
    def facts(self) -> dict[str, dict[str, object]]:
        return {
            "apple-silicon-requirement": {
                "id": "apple-silicon-requirement",
                "source_url": "https://www.macbaram.com/guides/macbaram-mac-control-guide/",
            }
        }

    def creator_facts(self) -> dict[str, dict[str, object]]:
        return {
            "creator-sponsorship-application": {
                "id": "creator-sponsorship-application",
                "source_url": "https://www.macbaram.com/",
            }
        }

    def test_visible_minimum_macos_copy_passes(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            self.facts(),
            fetch=lambda _url: "<main><p>Requires Apple silicon M1 or later and macOS 13 or later.</p></main>",
        )
        self.assertEqual(errors, [])

    def test_missing_visible_minimum_macos_copy_fails(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            self.facts(),
            fetch=lambda _url: "<main><p>Requires Apple silicon M1 or later.</p></main>",
        )
        self.assertTrue(any("source body must state macOS 13 or later" in error for error in errors))

    def test_structured_data_alone_does_not_satisfy_visible_copy(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            self.facts(),
            fetch=lambda _url: '<script type="application/ld+json">{"operatingSystem":"macOS 13+"}</script><main><p>Apple silicon Mac.</p></main>',
        )
        self.assertTrue(any("source body must state macOS 13 or later" in error for error in errors))

    def test_visible_creator_application_contract_passes(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            self.creator_facts(),
            fetch=lambda _url: (
                "<main><h2>Creator Sponsorship</h2>"
                "<p>Include a public channel URL and how you plan to use it.</p>"
                "<p>Approved applicants receive a 365-day access code.</p>"
                "<p>No review, positive rating, purchase, or product feedback is required.</p>"
                "</main>"
            ),
        )
        self.assertEqual(errors, [])

    def test_creator_source_missing_no_obligation_contract_fails(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            self.creator_facts(),
            fetch=lambda _url: (
                "<main><h2>Creator Sponsorship</h2>"
                "<p>Include a public creator URL and how you plan to use it.</p>"
                "<p>Approved applicants receive a 365-day access code.</p></main>"
            ),
        )
        self.assertTrue(any("current Creator application" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
