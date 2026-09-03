# A Mac Control Session Needs an Ending

A long render, build, backup, download, or local AI job may justify keeping a Mac awake for a while. Starting that temporary intervention is only half of the design. The session also needs a clear ending that releases control when the user is finished or when a supported safety boundary becomes more important than continued work.

## Apple treats temporary activity as a lifecycle

Apple's [`beginActivity(options:reason:)`](https://developer.apple.com/documentation/foundation/processinfo/beginactivity(options:reason:)) API returns a token that represents an activity. Apple's documentation tells developers to pass that token to [`endActivity(_:)`](https://developer.apple.com/documentation/foundation/processinfo/endactivity(_:)) when the activity is complete.

Apple also separates two power decisions. [`idleSystemSleepDisabled`](https://developer.apple.com/documentation/foundation/processinfo/activityoptions/idlesystemsleepdisabled) prevents idle system sleep, while [`idleDisplaySleepDisabled`](https://developer.apple.com/documentation/foundation/processinfo/activityoptions/idledisplaysleepdisabled) requires the screen to remain powered on. A long task may need the Mac to stay awake without needing the display to stay lit.

These Foundation APIs are a public example of the lifecycle principle. MacBaram's current sleep controls use supported macOS power-management paths; this article does not claim that every MacBaram sleep control is implemented through `ProcessInfo`.

Apple's Mac User Guide also notes that delaying or preventing sleep may increase power consumption. An indefinite keep-awake state is therefore not a neutral default.

## Entry, active state, and exit

A complete control session has three parts:

1. **Entry:** the user starts a temporary operating state for known work.
2. **Active state:** system sleep, display sleep, fan, and charging controls remain separate and are applied only where the current Mac supports them.
3. **Exit:** temporary control is released when the user stops the session or a supported safety or authority condition requires a return.

The exit matters because a valid instruction can become wrong after the surrounding conditions change. A MacBook that was connected to power can be unplugged. A control session can lose its trusted owner. A license can stop authorizing a control domain. A manual stop can mean that the user wants macOS to resume normal power management immediately.

## Current MacBaram exit boundaries

MacBaram currently keeps system sleep and display sleep as separate user choices. The display can be allowed to sleep while supported work continues, and a request to keep the display on uses a separate temporary control.

Supported return paths include:

- **User stop or disable:** MacBaram releases its temporary sleep and display controls and ends the related virtual-display session where applicable.
- **Low battery after external power is unavailable:** at the battery cutoff selected by the user, MacBaram can stop Stay Awake and Virtual Clamshell, return supported fan, charging, and sleep behavior toward macOS defaults, and allow normal sleep.
- **Lost trusted control or invalid authorization:** MacBaram returns the affected supported controls toward macOS defaults. It does not present an authorization-related return as complete until the supported state is verified. Affected optional controls remain unavailable while that return is incomplete, and a pending entitlement-restriction return can make another supported attempt.

These paths do not erase every saved preference, and they do not mean that every control exists on every Mac. Hardware capability, current power state, and authorization still decide what can be applied.

Repository tests and documentation review do not establish the installed release's final state on a physical Mac. A physical release outcome requires separate installation and device-state readback evidence for the release being claimed.

## What the session does not know

MacBaram does not detect when every render, build, download, or local AI workload has finished. It does not promise that an application saves its work, that a network stays connected, or that a power source remains available. A user should end the session when the work is complete and verify the resulting Mac state before leaving important work unattended.

The narrow design rule is more useful than a completion guarantee: temporary control should have a visible entry, a supported exit, and a verifiable return path.

## Sources and related documentation

- [Apple Developer: ProcessInfo activities](https://developer.apple.com/documentation/foundation/processinfo)
- [Apple Developer: beginActivity(options:reason:)](https://developer.apple.com/documentation/foundation/processinfo/beginactivity(options:reason:))
- [Apple Developer: endActivity(_:)](https://developer.apple.com/documentation/foundation/processinfo/endactivity(_:))
- [Apple Developer: idleSystemSleepDisabled](https://developer.apple.com/documentation/foundation/processinfo/activityoptions/idlesystemsleepdisabled)
- [Apple Support: Set sleep and wake settings for your Mac](https://support.apple.com/en-gb/guide/mac-help/mchle41a6ccd/mac)
- [Battery-aware sleep](battery-aware-sleep.md)
- [Features and behavior](features.md)
- [Safety and permissions](safety-and-permissions.md)

_Primary Apple sources checked on 2026-09-02._
