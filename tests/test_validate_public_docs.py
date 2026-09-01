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
            "Creator Sponsorship is currently open."
        )
        self.assertEqual(len(claims), 2)

    def test_plain_availability_claim_is_rejected(self) -> None:
        self.assertEqual(
            VALIDATOR.noncurrent_promotion_claims("Enterprise Single is available."),
            ["Enterprise Single is available."],
        )

    def test_mixed_positive_and_negative_clauses_do_not_bypass_guard(self) -> None:
        claims = VALIDATOR.noncurrent_promotion_claims(
            "Enterprise Single is currently available, not merely a roadmap.\n"
            "Creator Sponsorship is currently open, but payout is not operational.\n"
            "Supporters is live, but settlement is not operational.\n"
            "Enterprise Fleet is currently available without restrictions."
        )
        self.assertEqual(len(claims), 4)

    def test_explicit_non_current_copy_is_allowed(self) -> None:
        claims = VALIDATOR.noncurrent_promotion_claims(
            "Enterprise Single is not currently available.\n"
            "No public operating launch is declared for Creator Sponsorship."
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
        self.assertTrue(any("non-current term outside roadmap surfaces" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
