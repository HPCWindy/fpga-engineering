# Timing, arithmetic, and memory inference

Read this reference before optimizing for frequency or changing storage implementation.

## Diagnose timing from reports

Start from the worst path's source, destination, logic levels, cell types, route delay, and clock relationship. Map that path back to an RTL operation. A negative slack is a symptom; synthesis cells often reveal the cause.

Typical remedies include pipelining, reducing fanout, registering decodes, retiming an interface, using an iterative operator, selecting a device primitive, or moving a precomputable value to software. Avoid relaxing the clock or adding an exception unless the external requirement and path semantics justify it.

A representative failure pattern is a variable 32-bit division used to compute a scan length in one cycle. It can synthesize into hundreds of carry elements and miss a fast clock by tens of nanoseconds. Prefer one of:

- a constant or power-of-two transformation;
- precomputation by the control software;
- a multi-cycle iterative divider with explicit busy/done behavior;
- a pipelined vendor divider when throughput requires it.

Test divide-by-zero, quotient rounding, overflow, start-while-busy, and latency.

## Infer memory deliberately

Follow the selected vendor's inference template. Large memories generally need clocked writes and synchronous reads; asynchronous read logic or broad reset loops can force LUT storage.

When changing a memory from combinational read to synchronous read:

1. add an explicit request/address cycle;
2. wait the documented read latency;
3. consume data only when valid;
4. update every automatic and debug read path;
5. test first, last, consecutive, and backpressured reads.

Do not consider the change complete merely because synthesis now reports BRAM. Confirm functional alignment after the added latency and check the actual RAMB/M20K resource report.

## Closure evidence

Behavioral simulation proves neither resource inference nor timing. Synthesis can expose inferred primitives and gross path problems, but final setup/hold closure requires implementation. Record target part, tool version, clocks, WNS/TNS, WHS/THS, unconstrained paths, DRC status, and whether bitstream generation completed.
