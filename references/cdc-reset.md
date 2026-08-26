# CDC and reset

Read this reference whenever data, pulses, resets, or external pins cross into a clock domain.

## Classify every crossing

| Crossing | Suitable pattern |
|---|---|
| Slow or static single-bit level | Two or more destination-domain synchronizer stages |
| Single-bit event that may be shorter than a destination cycle | Pulse stretcher, toggle synchronizer, or request/acknowledge handshake |
| Related multi-bit value held stable | Handshake the validity; capture the bus only under the proven stability contract |
| Continuous multi-bit stream | Asynchronous FIFO with Gray-coded pointers |
| Counter observed across domains | Gray code, snapshot handshake, or domain-local accumulation |

Do not synchronize each bit of a changing bus independently: different bits can settle on different destination cycles. Do not edge-detect the raw asynchronous input; edge-detect the synchronized level.

For mechanical or detector inputs, synchronization does not replace debouncing, dead-time enforcement, or event-rate analysis. Decide whether repeated transitions inside the suppression window are ignored, merged, or reported.

## Synchronizer implementation

- Put the stages in the destination clock domain and keep ordinary logic out of the chain.
- Apply the vendor's synchronizer attribute, such as `ASYNC_REG`, when supported by the selected tool.
- Constrain and review the crossing using the actual tool flow. Do not blanket-false-path the entire destination logic cone.
- Compute whether the event rate, destination clock, and chosen pattern can lose events. A two-flop level synchronizer alone does not guarantee narrow pulse capture.

## Reset strategy

Asynchronous assertion can be appropriate for immediate safety, but deassertion should normally be synchronized separately in each clock domain. Avoid using a reset release as an undocumented CDC event.

Define reset values from required hardware behavior, not aesthetic uniformity. Active-low gates, output enables, transceiver resets, and chip selects may need different safe levels. Verify reset during idle, during a transaction, and near a clock-domain interaction.

Treat reset constraints carefully: a false path to asynchronous reset pins may be valid for assertion, while recovery/removal and synchronized release still require a sound structure. Follow the device and tool documentation for the exact pattern.
