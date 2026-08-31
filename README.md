<p align="center">
  <img src="assets/macbaram-icon.png" width="96" height="93" alt="MacBaram app icon">
</p>

<h1 align="center">MacBaram</h1>

<p align="center"><strong>Fan, battery, and sleep. One app for your Mac.</strong></p>

<p align="center">
  <a href="https://www.macbaram.com/">Official Website</a> ·
  <a href="https://www.macbaram.com/download">Official Download</a> ·
  <a href="https://www.macbaram.com/guides/">Mac Guides</a> ·
  <a href="CHANGELOG.md">Update Notes</a>
</p>

MacBaram is a native macOS utility for people who leave demanding work running on their Mac. Local AI, development, video exports, and other long jobs can keep a Mac busy for hours. During that time, fan behavior, charging, and sleep are usually managed in separate places. MacBaram brings those controls and their current state into one app.

This repository is MacBaram's public technical knowledge base. It contains product explanations, support guidance, compatibility boundaries, and public update notes. It does **not** contain the MacBaram source code, installer packages, licensing systems, private diagnostics, or internal operations material.

![MacBaram dashboard showing fan, battery, power, sleep, and system state together](assets/macbaram-dashboard.webp)

_The dashboard presents verified controls and state for the current Mac. Hardware-dependent controls vary by model._

## Why MacBaram exists

A long-running job does not happen in a single, fixed system state. Temperature and fan response change with load. A portable Mac may remain connected to power and fully charged for a long period. A job can also stop when macOS goes to sleep.

MacBaram gives supported Macs one place to manage these related conditions without presenting them as guaranteed performance improvements or guaranteed hardware protection. The app shows what it can control on the current Mac and keeps unsupported controls unavailable.

A local AI job is a practical example: it may run for hours while fan response, charging state, and sleep conditions change. MacBaram keeps those controls visible together; the longer workflow explanation remains in the official [Local AI guide](https://www.macbaram.com/guides/local-ai-mac-workloads/).

## Available now

- **Fan curves and fan control** — Set a user-defined response curve and choose how supported fans react across temperature ranges.
- **Charging controls** — Set charging-related limits on supported portable Macs.
- **Sleep prevention for long work** — Keep supported work from being interrupted by normal system sleep when the feature is active.
- **Low-battery return to normal sleep** — At the battery level selected by the user, MacBaram can release sleep prevention so macOS can return to its normal sleep behavior.
- **Unified dashboard** — Review fan, battery, power, and sleep state together instead of checking separate utilities.

The exact controls shown depend on the hardware capabilities detected on that Mac. A desktop Mac has no portable battery controls, and a fanless Mac has no fan controls.

## Supported Macs

MacBaram requires Apple silicon and macOS 13 or later. The current support scope covers Mac mini and Mac Studio, plus MacBook Air and MacBook Pro models whose required capabilities are verified by the app.

Intel Macs are not supported. iMac support is not currently declared; MacBaram fails closed when the required iMac capabilities have not been verified. See [Supported Macs](docs/supported-macs.md) for the complete boundary.

## Safety boundary

MacBaram changes only controls that the current Mac reports as available. If a required capability cannot be verified, the related control remains unavailable. Quitting, disabling a control, or reaching a configured safety condition is designed to return the affected behavior toward macOS defaults where applicable.

MacBaram does not promise a specific performance increase, a particular throttling outcome, longer battery lifespan, uninterrupted operation, or protection against every hardware failure. Users remain responsible for appropriate ventilation, power, backups, and monitoring of important workloads. Read [Safety and permissions](docs/safety-and-permissions.md) before relying on MacBaram for unattended work.

## Download and pricing

The only canonical public download address is:

**[Download MacBaram from the official website](https://www.macbaram.com/download)**

Installer packages are not published through GitHub Releases. Do not download a MacBaram installer from a repository attachment, issue, comment, mirror, or third-party file host.

Current plans, trial terms, and pricing are maintained only on the [official MacBaram website](https://www.macbaram.com/#pricing). They are intentionally not duplicated here because commercial terms can change independently of the technical documentation.

## Documentation

- [Documentation index](docs/README.md)
- [Features and behavior](docs/features.md)
- [Battery-aware sleep](docs/battery-aware-sleep.md)
- [Supported Macs](docs/supported-macs.md)
- [Safety and permissions](docs/safety-and-permissions.md)
- [Known limitations](KNOWN_LIMITATIONS.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Frequently asked questions](docs/faq.md)
- [Public update notes](CHANGELOG.md)
- [How update notes are published](docs/update-policy.md)

The official [MacBaram Guides](https://www.macbaram.com/guides/) provide longer workflow-oriented articles. The website remains the product source of truth. This repository is a reviewed public projection for technical explanations and compatibility, plus the maintained home of support guidance and post-release update notes. Information flows from a verified production release into this repository, never from an unreviewed GitHub edit into the product website.

## Support and feedback

Start with [SUPPORT.md](SUPPORT.md). Public issues are suitable for reproducible, non-sensitive problems and documentation feedback. Never post email addresses, account identifiers, serial numbers, payment details, license data, full logs, or raw diagnostic archives in a public issue.

Security concerns should follow [SECURITY.md](SECURITY.md) and must not be disclosed in a public issue.

Documentation corrections are welcome through the process in [CONTRIBUTING.md](CONTRIBUTING.md). This does not open the private application source for code contributions.

## Source availability

MacBaram is proprietary, closed-source software. This public repository documents the product; it does not grant a license to the application source code, artwork, installer, or brand assets. Contributions to public documentation may be accepted separately from the application itself.
