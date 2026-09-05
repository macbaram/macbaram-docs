# Supported Macs

## Current requirements

- Apple M-series Mac (M1 or later)
- macOS 13 or later
- A hardware capability verified by MacBaram for each control the user wants to enable

## Current support scope

| Mac family | Current status | Notes |
| --- | --- | --- |
| Mac mini | Supported | Available controls depend on detected hardware. No portable battery controls. |
| Mac Studio | Supported | Available controls depend on detected hardware. No portable battery controls. |
| MacBook Air | Capability-verified support | Fan controls are absent on fanless models; battery and sleep controls depend on detected capability. |
| MacBook Pro | Capability-verified support | Available controls depend on the specific model and detected capability. |
| MacBook Neo (A18 Pro) | Unsupported | Battery control and Virtual Clamshell have not completed model-specific verification. |
| iMac | Not currently declared supported | MacBaram keeps affected controls unavailable when required capability is not verified. |
| Intel Mac | Unsupported | An Apple M-series chip is required. |

## What capability-verified means

Model-family names alone are not sufficient evidence that a hardware control is safe to expose. MacBaram checks the capabilities required by each control. If that check fails or the capability is absent, the control stays unavailable rather than guessing.

This page describes the current public support boundary. It must not be used to infer support for an unlisted model or an unreleased feature.
