# A Mac That Stays Awake Should Still Know When to Stop

You start a local LLM job, a render, or a long build before going to bed. The job may need several hours, so the first requirement sounds simple: do not let the Mac sleep.

A basic keep-awake switch solves that immediate problem. The display can turn off while the work continues. But it creates a second question that is easier to miss: what should happen if a cable is removed, a dock stops supplying power, or the MacBook is left running on battery?

For us, that question stopped being theoretical during testing. A keep-awake state continued doing exactly what it had been told to do after external power disappeared. Because it did not watch the remaining battery, the MacBook kept running until it reached complete discharge.

Apple notes that delaying or preventing sleep may increase power consumption. Apple's power-management assertions are also not absolute commands; low-power or thermal conditions can still cause macOS to sleep. This points to an important distinction. “The user wants this job to continue” and “the machine should remain awake right now” are not always the same decision.

That distinction became the starting point for MacBaram's sleep-and-battery design.

If sleep prevention and battery management are separate switches, each feature can behave correctly on its own while the overall result is wrong. Sleep prevention keeps the job alive. Battery protection watches the remaining charge. But without a shared rule, the Mac can continue obeying the first switch after the condition for the second has become more important.

MacBaram's conclusion was that sleep prevention needs both a battery boundary and a clean way to step out of the system's way.

The user chooses a battery cutoff for long-running work. While the battery remains above that boundary—or external power is available—the Mac can continue honoring the user's request to stay awake. If the battery falls below the safety band, MacBaram releases its runtime sleep-prevention intervention and returns the machine to vanilla macOS power behavior. From that point, MacBaram is no longer the reason the Mac stays awake; macOS can make its normal sleep decision again.

The important detail is that MacBaram does not erase the user's intention. It keeps “I want this job to stay awake” separate from “it is safe to enforce that request right now.” When power conditions recover, the runtime can restore the original intention instead of forcing the user to configure everything again.

MacBaram also uses a small gap around the cutoff rather than switching at one exact percentage. Without that gap, a battery hovering around the boundary could repeatedly turn sleep prevention off and on. The lower boundary is used to step back; the upper boundary is used to restore. This is a simple control principle, but it turns two unrelated toggles into one operating policy.

This design does not promise that every overnight job will finish. It does not promise longer battery life. It makes a narrower and more honest promise: MacBaram will not treat “stay awake” as permission to ignore the battery.

That is what we mean when we say, “Sleep should understand battery.”

The story did not begin with a new sleep button. It began with a conflict between two valid goals: protect the user's long-running work and avoid keeping a portable Mac awake without regard for its remaining power. MacBaram's answer was not to choose one goal forever. It was to make the decision change with the condition of the machine.

## Related documentation

- [A Mac Control Session Needs an Ending](control-session-lifecycle.md)
- [MacBaram Guide: Battery-aware sleep prevention](https://www.macbaram.com/guides/battery-aware-sleep-prevention/)
- [Features and behavior](features.md)
- [Safety and permissions](safety-and-permissions.md)
- [Apple: Set sleep and wake settings for your Mac](https://support.apple.com/en-gb/guide/mac-help/mchle41a6ccd/mac)
- [Apple Developer: IOPMAssertionTypes](https://developer.apple.com/documentation/iokit/iopmlib_h/iopmassertiontypes)
- [Apple: View energy consumption in Activity Monitor](https://support.apple.com/en-gb/guide/activity-monitor/actmntr43697/mac)
