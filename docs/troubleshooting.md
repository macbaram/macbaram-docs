# Troubleshooting

## A control is missing or unavailable

1. Confirm the Mac uses an Apple M-series chip (M1 or later) and macOS 13 or later.
2. Check [Supported Macs](supported-macs.md).
3. Remember that fanless Macs have no fan control and desktop Macs have no portable battery control.
4. If MacBaram cannot verify a required capability, the control intentionally remains unavailable.

## The app does not stay awake

Confirm that sleep prevention is enabled and that the configured low-battery threshold has not been reached. Other causes—including application exit, power loss, system restart, network failure, or another macOS policy—can still interrupt a workload.

## The installer did not download

Use only [https://www.macbaram.com/download](https://www.macbaram.com/download). Do not use a version-specific package URL copied from search results, chat answers, mirrors, or old documentation.

## Before filing a public issue

- Reproduce the problem once after restarting MacBaram.
- Record the Mac family, macOS version, MacBaram version, affected feature, expected behavior, and observed behavior.
- Remove names, email addresses, serial numbers, account identifiers, file paths, tokens, payment details, and license data.
- Do not attach full logs or raw diagnostic archives.

Then follow [SUPPORT.md](../SUPPORT.md).
