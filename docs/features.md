# Features and behavior

MacBaram treats fan, charging, and sleep as related parts of a long-running Mac workload. The dashboard shows the controls that are available on the current hardware.

## Fan control

On supported Macs with controllable fans, a user can define a fan curve across temperature ranges and select the intended response. The control uses measured temperature feedback rather than assuming that one fixed fan command remains correct as conditions change. MacBaram reports the current state so the control is not separated from the workload it affects.

Fan control is not available on fanless Macs or when the required hardware capability cannot be verified. MacBaram does not claim that a selected curve will produce a specific throttling or performance result.

## Charging controls

On supported portable Macs, MacBaram provides charging-related limits intended for users who keep their Mac connected to power during long work.

Charging controls depend on the battery and power capabilities reported by the current Mac. They are not shown on desktop Macs. MacBaram does not promise a particular battery-health or battery-lifespan outcome.

### Power-Only and Safety Drain

On supported portable Macs, Power-Only can keep operation primarily on external power after the selected charging target is reached and the current hardware and power state allow it. It does not claim that the battery is physically disconnected or uninvolved in every transient condition.

Safety Drain can return a battery that is above the selected target toward that target by temporarily withholding supported charging and using the Mac's normal system load. It does not create an artificial discharge workload. After the target is reached, MacBaram resumes the selected charging policy.

## Heat Protection

On a supported fan-equipped MacBook, Heat Protection can use one high battery-temperature condition to pause charging and coordinate an available fan response. After cooling, it returns to the active user fan curve or toward macOS automatic control according to the current policy. A fanless Mac can pause supported charging but does not gain a fan.

## Sleep prevention

MacBaram can prevent normal system sleep while a long-running job is active. This helps avoid an avoidable sleep interruption, but it does not guarantee that an application, network connection, power source, or workload will remain available.

The display and system-sleep controls are separate. A user can allow the physical display to turn off while supported work continues.

## Virtual Clamshell

On supported M-series MacBooks, Virtual Clamshell can maintain a software virtual display for lid-closed work without requiring a dummy display adapter. This lets the closed built-in panel turn off while an already authorized screen session remains available. When a real external monitor is connected, MacBaram releases the virtual-display path and uses the normal external-display workflow.

Virtual Clamshell does not bypass a lock, login, application permission, or remote-tool authorization. An existing remote-control or screen-control tool must keep its own connection and permission, and the workload must still be checked independently.

## Low-battery return to normal sleep

The user can set a low-battery threshold for long-work protection. After external power disappears, a brief grace period lets a momentary adapter transition settle before MacBaram evaluates that threshold. When the level is reached, MacBaram can stop Stay Awake and Virtual Clamshell, return supported fan, charging, and sleep behavior toward macOS defaults, and allow normal sleep to occur. Saved choices can be considered again after external power returns or the battery recovers, but only when the current authorization still allows them. This does not guarantee that an application has saved or completed its work.

## Coordinated long-running work

MacBaram does not optimize or operate Ollama, LM Studio, Final Cut Pro, Blender, Xcode, Claude Code, Docker, or another workload application itself. It coordinates the supported Mac conditions around work such as local AI, builds and tests, photo processing, video and 3D rendering, backups, large downloads, automation, and already-connected remote sessions.

Current Air, Desktop, and Pro plans require the user to choose controls and presets. They do not automatically detect Ollama or switch settings by workload. Workload-aware assistance remains a future direction, not a current feature; see the [roadmap](roadmap.md).

## Unified dashboard

Fan, battery, power, display, and sleep state are shown together. The dashboard is evidence of the current Mac's detected capabilities; it is not a promise that every control exists on every model.

For longer explanations, see the official guides for [Mac fan control](https://www.macbaram.com/guides/mac-fan-control/), [battery charge limits](https://www.macbaram.com/guides/mac-battery-charge-limit/), and [keeping a Mac awake](https://www.macbaram.com/guides/keep-mac-awake/).
