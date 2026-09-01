# MacBaram documentation

This directory explains the public, currently verified behavior of MacBaram.

## Start here

- [Features and behavior](features.md) — what MacBaram currently does and how the controls relate.
- [Battery-aware sleep](battery-aware-sleep.md) — why a keep-awake request should step back when remaining power becomes more important.
- [Heat Protection](heat-protection.md) — how a high battery-temperature condition can coordinate charging and available fan control.
- [Supported Macs](supported-macs.md) — hardware and operating-system boundaries.
- [Safety and permissions](safety-and-permissions.md) — fail-closed behavior, system access, and user responsibilities.
- [Known limitations](../KNOWN_LIMITATIONS.md) — current public boundaries that should not be inferred away.
- [Troubleshooting](troubleshooting.md) — safe first checks for common problems.
- [Frequently asked questions](faq.md) — short answers about downloads, compatibility, pricing, and updates.
- [Public update notes](../CHANGELOG.md) — user-visible changes after a release is promoted to the official download channel.
- [Update publication policy](update-policy.md) — when release and operational notes become public.

## Sources of truth

| Subject | Canonical source |
| --- | --- |
| Download, availability, trial, and pricing | [Official website](https://www.macbaram.com/) |
| Released product behavior and compatibility | Official website, reviewed and projected into this repository |
| Workflow guides | [MacBaram Guides](https://www.macbaram.com/guides/) |
| Public support process and post-release update notes | This repository |
| Machine-readable reviewed public facts | [`data/public-facts.json`](../data/public-facts.json) |

Only verified, public behavior belongs here. A planned feature must not be described as available. Internal implementation notes, unreleased builds, account data, licensing internals, and raw diagnostics must remain outside this repository. See [Consistency rules](consistency-rules.md) for the one-way publication contract.
