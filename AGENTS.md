# MacBaram public documentation rules

This repository is a public projection, not an independent product authority.

1. Before projecting a product or business decision, confirm the current `decision@revision` in the parent `macbaram/MacBaram` repository's `docs/current/DECISION_LEDGER.json` and read its human context in `docs/current/DECISIONS.md`.
2. Use the assigned gate and decision fingerprints. Project only the target's listed `required_facts`, translated into public-safe wording without internal protocols, secrets, personal data, or unsupported guarantees.
3. Do not create, approve, broaden, or reinterpret a product decision in this repository. If the parent sources or assigned receipt are unavailable or disagree, stop and report the mismatch.
4. Never use an old personal repository, historical branch, cached search result, third-party listing, or search snapshot as the current source of truth.
5. Before reporting completion, run `python3 -m unittest discover -s tests` and `python3 scripts/validate_public_docs.py`. A passing check does not authorize merging or publication.
