from __future__ import annotations

import importlib.util
import json
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

    def test_reusable_complimentary_code_claim_is_rejected(self) -> None:
        self.assertIn(
            "reusable complimentary code claim",
            self.labels("The same code can be used for multiple accounts."),
        )

    def test_unauthorized_reapplication_claim_is_rejected(self) -> None:
        self.assertIn(
            "unauthorized reapplication claim",
            self.labels("Saved controls can be reapplied without current authorization."),
        )

    def test_unverified_restore_success_claim_is_rejected(self) -> None:
        self.assertIn(
            "unverified restore success claim",
            self.labels("A return is considered complete without state verification."),
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
            "korean-name-origin": "available",
            "five-day-evaluation-start": "available",
            "license-access-source-boundary": "available",
            "creator-sponsorship-application": "available",
            "supporters-referral-operation": "concept",
            "workload-auto-detection": "roadmap",
            "enterprise-single": "roadmap",
            "enterprise-fleet": "roadmap",
        }
        for fact_id, status in required.items():
            self.assertEqual(VALIDATOR.EXPECTED_FACT_STATUSES[fact_id], status)

    def test_canonical_baseline_meanings_are_required(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_canonical_baseline(errors)
        self.assertEqual(errors, [])

    def test_missing_evaluation_start_boundary_fails(self) -> None:
        original_root = VALIDATOR.ROOT
        with tempfile.TemporaryDirectory() as directory:
            mutated_root = Path(directory) / "public-docs"
            shutil.copytree(PUBLIC_ROOT, mutated_root)
            faq_path = mutated_root / "docs/faq.md"
            faq_path.write_text(
                faq_path.read_text(encoding="utf-8").replace(
                    "first successful license check after Google sign-in",
                    "starts after installation",
                ),
                encoding="utf-8",
            )
            try:
                VALIDATOR.ROOT = mutated_root
                errors = []
                VALIDATOR.validate_canonical_baseline(errors)
            finally:
                VALIDATOR.ROOT = original_root
        self.assertTrue(any("missing canonical baseline meaning" in error for error in errors))

    def assert_missing_baseline_phrase(self, relative: str, phrase: str) -> None:
        original_root = VALIDATOR.ROOT
        with tempfile.TemporaryDirectory() as directory:
            mutated_root = Path(directory) / "public-docs"
            shutil.copytree(PUBLIC_ROOT, mutated_root)
            path = mutated_root / relative
            path.write_text(path.read_text(encoding="utf-8").replace(phrase, "removed contract"), encoding="utf-8")
            try:
                VALIDATOR.ROOT = mutated_root
                errors: list[str] = []
                VALIDATOR.validate_canonical_baseline(errors)
            finally:
                VALIDATOR.ROOT = original_root
        self.assertTrue(any(f"{relative}: missing canonical baseline meaning" in error for error in errors))

    def test_missing_safe_return_retry_boundary_fails(self) -> None:
        self.assert_missing_baseline_phrase(
            "docs/control-session-lifecycle.md",
            "a pending entitlement-restriction return can make another supported attempt",
        )

    def test_missing_paid_and_complimentary_access_contract_fails(self) -> None:
        self.assert_missing_baseline_phrase("docs/faq.md", "Creem-confirmed paid access")

    def test_missing_adapter_grace_and_reapply_authority_fails(self) -> None:
        self.assert_missing_baseline_phrase(
            "docs/battery-aware-sleep.md",
            "When external power returns or the battery recovers above the separate recovery boundary",
        )

    def assert_missing_public_fact_summary_phrase(self, fact_id: str, phrase: str) -> None:
        original_root = VALIDATOR.ROOT
        with tempfile.TemporaryDirectory() as directory:
            mutated_root = Path(directory) / "public-docs"
            shutil.copytree(PUBLIC_ROOT, mutated_root)
            facts_path = mutated_root / "data/public-facts.json"
            facts_path.write_text(
                facts_path.read_text(encoding="utf-8").replace(phrase, "removed contract"),
                encoding="utf-8",
            )
            try:
                VALIDATOR.ROOT = mutated_root
                errors: list[str] = []
                VALIDATOR.validate_public_facts(errors)
            finally:
                VALIDATOR.ROOT = original_root
        self.assertIn(f"public fact {fact_id} summary must state: {phrase}", errors)

    def test_public_facts_preserve_safe_return_summary(self) -> None:
        self.assert_missing_public_fact_summary_phrase(
            "control-interlocks",
            "pending entitlement-restriction return can make another supported attempt",
        )

    def test_public_facts_preserve_access_source_summary(self) -> None:
        self.assert_missing_public_fact_summary_phrase(
            "license-access-source-boundary",
            "Creem-confirmed paid access without a complimentary code",
        )

    def test_public_facts_preserve_low_battery_reapply_summary(self) -> None:
        self.assert_missing_public_fact_summary_phrase(
            "low-battery-sleep-return",
            "after external power returns or the battery recovers",
        )

    def assert_public_fact_contradiction_fails(self, fact_id: str, contradiction: str) -> None:
        original_root = VALIDATOR.ROOT
        with tempfile.TemporaryDirectory() as directory:
            mutated_root = Path(directory) / "public-docs"
            shutil.copytree(PUBLIC_ROOT, mutated_root)
            facts_path = mutated_root / "data/public-facts.json"
            payload = json.loads(facts_path.read_text(encoding="utf-8"))
            fact = next(item for item in payload["facts"] if item["id"] == fact_id)
            fact["summary"] += f" {contradiction}"
            facts_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            try:
                VALIDATOR.ROOT = mutated_root
                errors: list[str] = []
                VALIDATOR.validate_content(errors)
            finally:
                VALIDATOR.ROOT = original_root
        self.assertTrue(any("claim" in error for error in errors))

    def test_reusable_code_contradiction_fails(self) -> None:
        self.assert_public_fact_contradiction_fails(
            "license-access-source-boundary",
            "The same code can be used for multiple accounts.",
        )

    def test_unauthorized_reapplication_contradiction_fails(self) -> None:
        self.assert_public_fact_contradiction_fails(
            "low-battery-sleep-return",
            "Saved controls can be reapplied without current authorization.",
        )

    def test_unverified_restore_success_contradiction_fails(self) -> None:
        self.assert_public_fact_contradiction_fails(
            "control-interlocks",
            "A return is considered complete without state verification.",
        )

    def test_structured_access_boundary_is_required(self) -> None:
        original_root = VALIDATOR.ROOT
        with tempfile.TemporaryDirectory() as directory:
            mutated_root = Path(directory) / "public-docs"
            shutil.copytree(PUBLIC_ROOT, mutated_root)
            facts_path = mutated_root / "data/public-facts.json"
            payload = json.loads(facts_path.read_text(encoding="utf-8"))
            fact = next(item for item in payload["facts"] if item["id"] == "license-access-source-boundary")
            fact["complimentary_account_bound"] = False
            facts_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            try:
                VALIDATOR.ROOT = mutated_root
                errors: list[str] = []
                VALIDATOR.validate_public_facts(errors)
            finally:
                VALIDATOR.ROOT = original_root
        self.assertIn(
            "public fact license-access-source-boundary complimentary_account_bound must be True",
            errors,
        )

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

    def test_every_summary_contract_has_a_live_source_guard(self) -> None:
        self.assertEqual(
            set(VALIDATOR.PUBLIC_FACT_SUMMARY_REQUIREMENTS) - set(VALIDATOR.LIVE_SOURCE_REQUIREMENTS),
            set(),
        )

    def test_visible_compatibility_boundary_passes(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            self.facts(),
            fetch=lambda _url: (
                "<main><p>Requires Apple M-series M1 or later and macOS 13 or later.</p>"
                "<p>MacBook Neo is not currently supported.</p></main>"
            ),
        )
        self.assertEqual(errors, [])

    def test_missing_visible_minimum_macos_copy_fails(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            self.facts(),
            fetch=lambda _url: (
                "<main><p>Requires Apple M-series M1 or later.</p>"
                "<p>MacBook Neo is not currently supported.</p></main>"
            ),
        )
        self.assertTrue(any("source body must state Apple M-series" in error for error in errors))

    def test_apple_silicon_wording_without_neo_boundary_fails(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            self.facts(),
            fetch=lambda _url: (
                "<main><p>Requires Apple silicon M1 or later and macOS 13 or later.</p></main>"
            ),
        )
        self.assertTrue(any("source body must state Apple M-series" in error for error in errors))

    def test_structured_data_alone_does_not_satisfy_visible_copy(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            self.facts(),
            fetch=lambda _url: '<script type="application/ld+json">{"operatingSystem":"macOS 13+"}</script><main><p>Apple silicon Mac.</p></main>',
        )
        self.assertTrue(any("source body must state Apple M-series" in error for error in errors))

    def test_visible_creator_application_contract_passes(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            self.creator_facts(),
            fetch=lambda _url: (
                "<main><h2>Creator Sponsorship</h2>"
                "<p>Include a public channel URL and how you plan to use it.</p>"
                "<p>Approved applicants receive a 365-day access code.</p>"
                "<p>Feedback is not a condition of sponsorship.</p>"
                "<p>We do not require a review, positive rating, or purchase.</p>"
                "<p>We do not influence its content or conclusions.</p>"
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
                "<p>Approved applicants receive a 365-day access code.</p>"
                "<p>We do not require a review, positive rating, or purchase.</p>"
                "<p>We do not influence its content or conclusions.</p></main>"
            ),
        )
        self.assertTrue(any("current Creator application" in error for error in errors))

    def test_new_canonical_facts_require_their_complete_public_meaning(self) -> None:
        facts = {
            fact_id: {"id": fact_id, "source_url": "https://www.macbaram.com/"}
            for fact_id in (
                "korean-name-origin",
                "five-day-evaluation-start",
                "license-access-source-boundary",
            )
        }
        source = (
            "Baram means wind in Korean. MacBaram is made in Korea. This origin is not a claim of "
            "technical superiority, is not a safety claim, and is not a promise of guaranteed results. "
            "For an eligible first-time user, the 5-day period begins at the first successful license check "
            "after Google sign-in. Opening sign-in or clicking a button does not start it. The effective plan "
            "comes from a validated signed license, and the app does not widen access without a valid plan. "
            "A normal purchase is processed by Creem and grants access without a complimentary access code. "
            "Supporter complimentary access uses a one-time code bound to the approved Supporter's own account and "
            "states the approved plan and duration. Creator Access uses a one-time, account-bound 365-day code for "
            "the selected plan. "
            "A Supporter recommendation connection is not product access, a discount, or code redemption."
        )
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(errors, facts, fetch=lambda _url: source)
        self.assertEqual(errors, [])

    def test_partial_public_copy_does_not_false_pass_new_facts(self) -> None:
        facts = {
            fact_id: {"id": fact_id, "source_url": "https://www.macbaram.com/"}
            for fact_id in (
                "korean-name-origin",
                "five-day-evaluation-start",
                "license-access-source-boundary",
            )
        }
        partial_source = (
            "Baram means wind in Korean. The 5-day period begins at the first license check after Google sign-in. "
            "Creator Sponsorship and Supporters are separate."
        )
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(errors, facts, fetch=lambda _url: partial_source)
        for fact_id in facts:
            self.assertTrue(any(fact_id in error for error in errors))

    def test_new_public_fact_cannot_use_its_own_summary_as_live_proof(self) -> None:
        fact = {
            "license-access-source-boundary": {
                "id": "license-access-source-boundary",
                "source_url": "https://www.macbaram.com/",
                "source_evidence": "verified",
                "summary": (
                    "Normal purchase uses Creem-confirmed paid access without a complimentary access code. "
                    "A complimentary code creates one account-bound access grant for its selected plan and period."
                ),
            }
        }
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(
            errors,
            fact,
            fetch=lambda _url: "<main>Normal purchase grants access without a complimentary access code.</main>",
        )
        self.assertTrue(any("license-access-source-boundary source body must state" in error for error in errors))

    def test_new_public_safe_source_contracts_can_pass(self) -> None:
        facts = {
            "license-access-source-boundary": {
                "id": "license-access-source-boundary",
                "source_url": "https://www.macbaram.com/",
            },
            "low-battery-sleep-return": {
                "id": "low-battery-sleep-return",
                "source_url": "https://www.macbaram.com/guides/battery-aware-sleep-prevention/",
            },
            "control-interlocks": {
                "id": "control-interlocks",
                "source_url": "https://www.macbaram.com/guides/a-mac-control-session-needs-an-ending/",
                "supporting_source_urls": ["https://www.macbaram.com/"],
            },
        }
        license_source = (
            "A normal purchase is processed by Creem and grants access without a complimentary access code. "
            "Supporter complimentary access uses a one-time code bound to the approved Supporter's own account and states the approved plan and duration. "
            "Creator Access uses a one-time, account-bound 365-day code for the selected plan. "
            "A Supporter recommendation connection is not product access, a discount, or code redemption."
        )
        low_battery_source = (
            "After a brief adapter-disconnect grace period, saved choices may return when external power returns or the "
            "battery recovers, but only when the current product access still permits that control."
        )
        control_source = (
            "Sending a restore command "
            "is not enough to call the return complete. When product access becomes restricted, MacBaram keeps the affected "
            "selected control unavailable until state readback and may retry a supported return. This does not mean that "
            "every manual or automatic ending path retries until it is verified."
        )
        errors: list[str] = []
        supporting_source = (
            "A successful restore command alone does not verify that the physical state was restored. "
            "MacBaram checks available state readback, and physical-release evidence remains separate from source or build checks."
        )
        VALIDATOR.validate_live_source_evidence(
            errors,
            facts,
            fetch=lambda url: {
                "https://www.macbaram.com/": f"{license_source} {supporting_source}",
                "https://www.macbaram.com/guides/battery-aware-sleep-prevention/": low_battery_source,
                "https://www.macbaram.com/guides/a-mac-control-session-needs-an-ending/": control_source,
            }[url],
        )
        self.assertEqual(errors, [])

    def test_control_interlock_missing_supporting_source_fails(self) -> None:
        facts = {
            "control-interlocks": {
                "id": "control-interlocks",
                "source_url": "https://www.macbaram.com/guides/a-mac-control-session-needs-an-ending/",
                "supporting_source_urls": ["https://www.macbaram.com/"],
            }
        }
        primary = (
            "Sending a restore command is not enough to call the return complete. When product access becomes restricted, "
            "MacBaram keeps the affected selected control unavailable until state readback and may retry a supported return. "
            "This does not mean that every manual or automatic ending path retries until it is verified."
        )
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(errors, facts, fetch=lambda _url: primary)
        self.assertTrue(any("supporting source body must state" in error for error in errors))

    def test_control_interlock_missing_primary_source_fails(self) -> None:
        facts = {
            "control-interlocks": {
                "id": "control-interlocks",
                "source_url": "https://www.macbaram.com/guides/a-mac-control-session-needs-an-ending/",
                "supporting_source_urls": ["https://www.macbaram.com/"],
            }
        }
        supporting = (
            "A successful restore command alone does not verify that the physical state was restored. "
            "MacBaram checks available state readback, and physical-release evidence remains separate from source or build checks."
        )
        errors: list[str] = []
        VALIDATOR.validate_live_source_evidence(errors, facts, fetch=lambda _url: supporting)
        self.assertTrue(any("source body must state the public-safe authorization return" in error for error in errors))


class ControlSessionLifecycleTests(unittest.TestCase):
    def test_current_control_session_contract_passes(self) -> None:
        errors: list[str] = []
        VALIDATOR.validate_control_session_lifecycle(errors)
        self.assertEqual(errors, [])

    def test_missing_workload_completion_boundary_fails(self) -> None:
        original_root = VALIDATOR.ROOT
        with tempfile.TemporaryDirectory() as directory:
            mutated_root = Path(directory) / "public-docs"
            shutil.copytree(PUBLIC_ROOT, mutated_root)
            lifecycle_path = mutated_root / "docs/control-session-lifecycle.md"
            lifecycle = lifecycle_path.read_text(encoding="utf-8")
            lifecycle_path.write_text(
                lifecycle.replace(
                    "MacBaram does not detect when every render, build, download, or local AI workload has finished.",
                    "MacBaram detects when every workload has finished.",
                ),
                encoding="utf-8",
            )
            try:
                VALIDATOR.ROOT = mutated_root
                errors: list[str] = []
                VALIDATOR.validate_control_session_lifecycle(errors)
            finally:
                VALIDATOR.ROOT = original_root
        self.assertIn(
            "docs/control-session-lifecycle.md must preserve workload completion boundary",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
