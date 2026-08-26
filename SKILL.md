---
name: fpga-engineering
description: Design, review, simulate, constrain, and debug FPGA RTL in Verilog or SystemVerilog. Use for FPGA modules, state machines, clock-domain crossings, reset design, serial protocols, timing closure, memory inference, testbenches, pin constraints, or board bring-up. Do not use for software-only work or ASIC sign-off flows.
---

# FPGA Engineering

Produce FPGA work that is explicit about clocks, cycles, interfaces, safety, and verification evidence. Preserve the user's device, board, toolchain, language, naming, and existing architecture unless changing one is necessary and explained.

## Start from the hardware contract

Before editing RTL, establish from the request and repository:

- target device or family, board, toolchain, HDL dialect, and clock frequencies;
- reset polarity, synchronous/asynchronous behavior, and required safe output levels;
- interface timing, byte order, units, valid ranges, latency, throughput, and backpressure;
- clock domains and which inputs originate outside the receiving domain;
- what evidence is required: lint, behavioral simulation, synthesis, implementation timing, or hardware measurement.

If a missing fact changes electrical safety, CDC correctness, pin assignment, or the external protocol, do not invent it. Ask or leave the item explicitly unresolved. For ordinary implementation details, infer from nearby code and state the assumption.

## Work in evidence-producing increments

1. Inspect the top level, clocks/resets, constraints, interfaces, existing testbenches, and build commands before changing code.
2. Translate prose into cycle-level invariants and define failure behavior before choosing the microarchitecture.
3. Partition protocol parsing, control, datapath, storage, CDC, and physical I/O when they have different timing or verification concerns.
4. Implement the smallest coherent change. Keep clocked state updates nonblocking and make widths and signedness explicit at arithmetic and protocol boundaries.
5. Extend self-checking tests for normal operation, boundaries, malformed input, interruption, timeout, reset, and safe return-to-idle behavior.
6. Run the cheapest relevant checks first, then synthesis/implementation when available. Report exactly what ran and distinguish simulation success from timing or hardware proof.

## Preserve these invariants

- Synchronize asynchronous single-bit levels before consuming them. Detect edges only after synchronization. Treat multi-bit CDC as a protocol problem, not as several independent synchronizers.
- Do not create fabric clocks from ordinary logic. Prefer a clock enable unless a device clocking primitive and generated-clock constraint are deliberately used.
- Reset, stop, timeout, invalid configuration, and error paths must leave externally hazardous controls in documented safe states.
- Validate a complete configuration or frame before atomically committing it. A partial or corrupt frame must not partially update live control registers.
- Model synchronous memory latency explicitly. A design change that improves BRAM inference may add read cycles; update every consumer and test those addresses and cycles.
- Treat variable division, modulo, wide comparisons, large muxes, and long combinational state transitions as timing risks. Do not assume behavioral brevity implies cheap hardware.
- Keep units in names or interface documentation, such as `_cycles`, `_ticks`, `_bytes`, or `_hz`. Convert once at a clear boundary and define rounding and overflow behavior.
- Do not add false paths or multicycle paths merely to make timing green. Each exception needs a structural reason and must match the actual synchronizer or protocol.
- Never claim timing closure from RTL simulation. Timing closure requires a completed implementation report for the requested clock constraints.

## Load only the relevant guidance

- For RTL structure, counters, arithmetic, FSM encoding, and glitch-free control outputs, read [references/rtl-design.md](references/rtl-design.md).
- For asynchronous inputs, CDC, pulses, multi-bit transfers, and reset release, read [references/cdc-reset.md](references/cdc-reset.md).
- For framed UART/SPI-style protocols, configuration commits, checksums, timeouts, and backpressure, read [references/protocols.md](references/protocols.md).
- For inferred RAM, pipeline decisions, expensive operators, and timing closure, read [references/timing-memory.md](references/timing-memory.md).
- For testbench strategy and proof levels, read [references/verification.md](references/verification.md).
- For XDC/SDC constraints, I/O safety, and board bring-up, read [references/constraints-debug.md](references/constraints-debug.md).
- For common Icarus, Verilator, and Vivado command flows, read [references/toolchains.md](references/toolchains.md).

Use `scripts/run_iverilog.py` when an Icarus-compatible SystemVerilog project needs a repeatable compile-and-run check. Do not install tools or change a project toolchain without the user's authorization.

## Review and handoff

In review mode, prioritize functional or safety defects, CDC errors, cycle/latency mismatches, simulation-synthesis divergence, incomplete constraints, and missing tests. Cite exact files and lines; separate confirmed defects from risks that require synthesis or hardware evidence.

When handing off implementation, summarize the hardware-visible behavior, assumptions, files changed, checks run, and remaining evidence. If vendor tools or hardware are unavailable, say so directly and provide the exact next check rather than presenting the work as fully verified.
