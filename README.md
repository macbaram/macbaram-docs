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

MacBaram is a native macOS utility for demanding work that runs for hours. Local AI, development, build and test jobs, photo processing, video and 3D rendering, backups, large downloads, automation, and already-connected remote work can keep a Mac busy while temperature, fan response, charging, the display, and sleep change. MacBaram is not merely a collection of separate utilities: it treats the supported controls around that work as one coordinated operating state.

This repository is MacBaram's public technical knowledge base, not its source code or installer channel. It contains reviewed product explanations, compatibility boundaries, support guidance, and public update notes.

![MacBaram dashboard showing fan, battery, power, sleep, and system state together](assets/macbaram-dashboard.webp)

_The dashboard presents verified controls and state for the current Mac. Hardware-dependent controls vary by model._

## Why MacBaram exists

A long-running job does not happen in a single, fixed system state. Temperature and fan response change with load. A portable Mac may remain connected to power and fully charged for a long period. A job can also stop when macOS goes to sleep.

MacBaram gives supported Macs one place to manage these related conditions without presenting them as guaranteed performance improvements or guaranteed hardware protection. Feedback-based fan control responds to measured state, while public-safe capability, temperature, power, and session checks decide when an intervention is allowed and when MacBaram should return control toward macOS defaults. The app shows what it can control on the current Mac and keeps unsupported controls unavailable.

## Available now

- **Fan curves and fan control** — Set a user-defined response curve and choose how supported fans react across temperature ranges.
- **Charging controls** — Set charging-related limits on supported portable Macs.
- **Power-Only** — After a supported portable Mac reaches its selected charging target, keep it primarily on external power when the current hardware and power state allow it.
- **Safety Drain** — If the battery is above its selected target, use the Mac's normal system load to return toward that target before resuming the selected charging policy; MacBaram does not create an artificial discharge workload.
- **Heat Protection** — Use one supported battery-temperature condition to pause charging and coordinate an available fan response, then restore the active fan policy after cooling.
- **Sleep prevention for long work** — Keep supported work from being interrupted by normal system sleep when the feature is active.
- **Display and Virtual Clamshell controls** — Let the physical display turn off while supported work continues, including a virtual screen session for lid-closed work on supported Apple silicon MacBooks without a real external monitor.
- **Low-battery return to normal sleep** — At the battery level selected by the user, MacBaram can stop Stay Awake and Virtual Clamshell, return supported fan, charging, and sleep behavior toward macOS defaults, and allow normal sleep to occur.
- **Unified dashboard** — Review fan, battery, power, and sleep state together instead of checking separate utilities.
- **Creator Sponsorship applications** — Apply with public activity, Mac and chip, selected plan, and intended use. Approved creators receive 365 days; no review, rating, purchase, or feedback is required.

Controls depend on detected hardware capabilities. Desktop Macs have no portable-battery controls, and fanless Macs have no fan controls.

**Air**, **Desktop**, and **Pro** are current individual plan families; hardware controls vary. Commercial terms stay on the official website. Creator Sponsorship is separate from Supporters. See [Roadmap and collaboration programs](docs/roadmap.md) for Enterprise and collaboration boundaries.

Current Air, Desktop, and Pro plans do not automatically detect Ollama or switch settings by workload. Users choose the appropriate controls and presets themselves. Workload-aware assistance belongs to the **Enterprise Single roadmap**; it is not a current plan or feature.

## Supported Macs

MacBaram requires Apple silicon and macOS 13 or later. The current support scope covers Mac mini and Mac Studio, plus MacBook Air and MacBook Pro models whose required capabilities are verified by the app.

Intel Macs are not supported. iMac support is not currently declared; MacBaram fails closed when the required iMac capabilities have not been verified. See [Supported Macs](docs/supported-macs.md) for the complete boundary.

## Safety boundary

MacBaram changes only controls that the current Mac reports as available. If a required capability cannot be verified, the related control remains unavailable. Quitting, disabling a control, or reaching a configured safety condition is designed to return the affected behavior toward macOS defaults where applicable.

MacBaram does not promise a specific performance increase, throttling outcome, battery-lifespan result, uninterrupted operation, or protection against every hardware failure. Read [Safety and permissions](docs/safety-and-permissions.md) before unattended work.

## Download and pricing

Use only the canonical **[MacBaram download](https://www.macbaram.com/download)**. GitHub Releases, repository attachments, comments, mirrors, and third-party hosts are not installer channels. Current plans, trial terms, and pricing remain on the [official website](https://www.macbaram.com/#pricing) so commercial information has one source.

## Documentation

- [Documentation index](docs/README.md)
- [Features and behavior](docs/features.md)
- [Control session lifecycle](docs/control-session-lifecycle.md)
- [Battery-aware sleep](docs/battery-aware-sleep.md)
- [Heat Protection](docs/heat-protection.md)
- [Roadmap and collaboration programs](docs/roadmap.md)
- [Supported Macs](docs/supported-macs.md)
- [Safety and permissions](docs/safety-and-permissions.md)
- [Known limitations](KNOWN_LIMITATIONS.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Frequently asked questions](docs/faq.md)
- [Public update notes](CHANGELOG.md)
- [How update notes are published](docs/update-policy.md)

The official [MacBaram Guides](https://www.macbaram.com/guides/) provide longer workflow articles. The website remains the product source of truth; this repository is its reviewed public projection. Information flows from verified production into these documents, never from an unreviewed GitHub edit into the product.

## Support and feedback

Start with [SUPPORT.md](SUPPORT.md). Never post account, payment, license, device, or raw diagnostic data. Report security concerns through [SECURITY.md](SECURITY.md) and documentation corrections through [CONTRIBUTING.md](CONTRIBUTING.md).

## Source availability

MacBaram is proprietary, closed-source software. This repository documents the product; it does not license the application source, artwork, installer, or brand assets.
