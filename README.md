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

MacBaram is a native macOS utility for demanding work that runs for hours. Local AI, development, video exports, backups, downloads, and automation can keep a Mac busy while temperature, fan response, charging, the display, and sleep change. MacBaram treats the supported controls around that work as one operating state instead of unrelated utilities.

This repository is MacBaram's public technical knowledge base. It contains product explanations, support guidance, compatibility boundaries, and public update notes. It does **not** contain the MacBaram source code, installer packages, licensing systems, private diagnostics, or internal operations material.

![MacBaram dashboard showing fan, battery, power, sleep, and system state together](assets/macbaram-dashboard.webp)

_The dashboard presents verified controls and state for the current Mac. Hardware-dependent controls vary by model._

## Why MacBaram exists

A long-running job does not happen in a single, fixed system state. Temperature and fan response change with load. A portable Mac may remain connected to power and fully charged for a long period. A job can also stop when macOS goes to sleep.

MacBaram gives supported Macs one place to manage these related conditions without presenting them as guaranteed performance improvements or guaranteed hardware protection. Feedback-based fan control responds to measured state, while capability, temperature, remaining-charge, license, and connection interlocks decide when an intervention is allowed and when MacBaram should return control toward macOS defaults. The app shows what it can control on the current Mac and keeps unsupported controls unavailable.

The name carries the same product idea. **Baram** means “wind” in Korean. MacBaram was developed in Korea to manage the heat and airflow around sustained Mac work with clear feedback and recoverable control. That origin is part of the product identity, not a claim of technical superiority or a guaranteed result.

## Available now

- **Fan curves and fan control** — Set a user-defined response curve and choose how supported fans react across temperature ranges.
- **Charging controls** — Set charging-related limits on supported portable Macs.
- **Heat Protection** — Use one supported battery-temperature condition to pause charging and coordinate an available fan response, then restore the active fan policy after cooling.
- **Sleep prevention for long work** — Keep supported work from being interrupted by normal system sleep when the feature is active.
- **Display and Virtual Clamshell controls** — Let the physical display turn off while supported work continues, including a virtual screen session for lid-closed work on supported Apple silicon MacBooks without a real external monitor.
- **Low-battery return to normal sleep** — At the battery level selected by the user, MacBaram can release sleep prevention so macOS can return to its normal sleep behavior.
- **Unified dashboard** — Review fan, battery, power, and sleep state together instead of checking separate utilities.

The exact controls shown depend on the hardware capabilities detected on that Mac. A desktop Mac has no portable battery controls, and a fanless Mac has no fan controls.

The current individual plan families are **Air**, **Desktop**, and **Pro**. They expose different combinations of fan, battery, and sleep/display controls according to hardware capability. Current pricing, trial terms, purchase availability, and the exact plan matrix remain on the official website. Enterprise directions and access programs that are not currently active are kept separately in [Roadmap and non-current programs](docs/roadmap.md).

## Supported Macs

MacBaram requires Apple silicon and macOS 13 or later. The current support scope covers Mac mini and Mac Studio, plus MacBook Air and MacBook Pro models whose required capabilities are verified by the app.

Intel Macs are not supported. iMac support is not currently declared; MacBaram fails closed when the required iMac capabilities have not been verified. See [Supported Macs](docs/supported-macs.md) for the complete boundary.

## Safety boundary

MacBaram changes only controls that the current Mac reports as available. If a required capability cannot be verified, the related control remains unavailable. Quitting, disabling a control, or reaching a configured safety condition is designed to return the affected behavior toward macOS defaults where applicable.

MacBaram does not promise a specific performance increase, a particular throttling outcome, longer battery lifespan, uninterrupted operation, or protection against every hardware failure. Users remain responsible for appropriate ventilation, power, backups, and monitoring of important workloads. Read [Safety and permissions](docs/safety-and-permissions.md) before relying on MacBaram for unattended work.

## Download and pricing

Use only the canonical **[MacBaram download](https://www.macbaram.com/download)**. GitHub Releases, repository attachments, comments, mirrors, and third-party hosts are not installer channels. Current plans, trial terms, and pricing remain on the [official website](https://www.macbaram.com/#pricing) so commercial information has one source.

## Documentation

- [Documentation index](docs/README.md)
- [Features and behavior](docs/features.md)
- [Battery-aware sleep](docs/battery-aware-sleep.md)
- [Heat Protection](docs/heat-protection.md)
- [Roadmap and non-current programs](docs/roadmap.md)
- [Supported Macs](docs/supported-macs.md)
- [Safety and permissions](docs/safety-and-permissions.md)
- [Known limitations](KNOWN_LIMITATIONS.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Frequently asked questions](docs/faq.md)
- [Public update notes](CHANGELOG.md)
- [How update notes are published](docs/update-policy.md)

The official [MacBaram Guides](https://www.macbaram.com/guides/) provide longer workflow-oriented articles. The website remains the product source of truth. This repository is a reviewed public projection for technical explanations and compatibility, plus the maintained home of support guidance and post-release update notes. Information flows from a verified production release into this repository, never from an unreviewed GitHub edit into the product website.

## Support and feedback

Start with [SUPPORT.md](SUPPORT.md). Public issues are for reproducible, non-sensitive problems and documentation feedback; never post account, payment, license, device, or raw diagnostic data. Report security concerns through [SECURITY.md](SECURITY.md), and submit documentation corrections through [CONTRIBUTING.md](CONTRIBUTING.md).

## Source availability

MacBaram is proprietary, closed-source software. This repository documents the product; it does not license the application source, artwork, installer, or brand assets.
