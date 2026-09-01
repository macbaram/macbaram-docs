# Heat Protection: coordinating charging and available fan control

Heat Protection connects a high battery-temperature condition to more than one supported control.

## Current behavior

- It observes battery temperature while the MacBook is charging.
- When the configured high-temperature condition is met, it can pause charging.
- On a supported Mac with controllable fans, it can coordinate an available fan response from the same battery-temperature condition.
- After the condition clears, fan behavior returns to the active user-selected curve or toward macOS automatic control, according to the current policy.
- Fanless Macs do not gain fan control.

## Boundaries

- Heat Protection is an operating policy, not a guarantee against battery aging, swelling, damage, throttling, or repair.
- It does not guarantee a fixed temperature, noise, performance, or battery-life improvement.
- Results depend on the supported Mac, macOS, workload, environment, and connected equipment.

## Why this belongs in one system

Charging and fan control can each work independently while still missing the same battery-temperature event. Heat Protection is MacBaram's current example of why fan, battery, and sleep controls should share operating context instead of remaining unrelated switches.
