# Documentation consistency rules

This repository is a reviewed public projection of the released MacBaram product. It does not define product availability by itself.

## Publication direction

`approved public product facts → production deployment and readback → reviewed documentation update`

An unreviewed GitHub change must never update the product website, installer manifest, pricing, or feature availability in reverse.

## Ten rules

1. Use `https://www.macbaram.com/download` as the only public installer link.
2. Keep current pricing, trial terms, purchase options, and sales availability only on the official website.
3. Publish a binary changelog entry only after the corresponding build is available through the canonical download route and its public readback succeeds. Use a dated operational note for a material user-visible server-side or compatibility-policy change that has no new binary.
4. Describe a feature as `available` only when it exists in the current public release, has been approved for public description, and has passed the required verification.
5. Keep undisclosed plans, experiments, partial work, and approval-pending work out of the public repository. A CEO-approved public direction may appear in `docs/roadmap.md` when it states that it is not currently available. Add a matching machine-readable fact only after an official `macbaram.com` page directly supports that claim.
6. Do not infer support from a similar model name or from the fact that the app launches; use the approved capability boundary.
7. Link to canonical website guides instead of copying seven localized guide bodies into GitHub.
8. Do not publish internal paths, component names, control formulas, hardware keys, raw logs, diagnostics, account data, payment or licensing details, or security reproduction details.
9. Do not silently rewrite published release history. Add a dated correction or withdrawal note when a released statement needs correction.
10. Run the public-documentation guard before every merge and reject the entire update when a required source, locale boundary, link, or status cannot be verified.

## Automated checks

The repository validator rejects version-specific package links, duplicated price values, internal paths or component names, secret-like material, unsupported guarantees, broken relative links, missing required documents, invalid public-fact status values, non-official fact sources, and an invalid README length.

The validator also requires the current individual-plan boundary and the reviewed roadmap machine statuses. It rejects future or inactive items when a reviewed machine status or the dedicated roadmap surface promotes them as current, and it rejects their detailed copy outside that roadmap surface.

The validator is a guard, not approval. Passing it does not promote a feature or authorize a release.
