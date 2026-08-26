# Verification strategy

Read this reference when adding a feature, fixing a defect, or judging whether FPGA work is complete.

## Build a verification ladder

Use the lowest-cost level that can expose the current risk, then move upward as evidence requires:

1. syntax/elaboration and lint;
2. focused self-checking module simulation;
3. integrated protocol or top-level simulation;
4. synthesis and resource/inference review;
5. implementation timing and DRC;
6. bitstream generation and controlled board bring-up;
7. instrumented measurement against the physical timing contract.

Passing one level does not imply the next. State skipped levels in the handoff.

## Make tests self-checking

Prefer checks that fail with a precise message and terminate with a nonzero simulator status. Include a watchdog timeout so a stalled FSM cannot hang CI.

For each interface or state machine, cover:

- reset and safe outputs;
- minimum, nominal, and maximum legal values;
- zero, one, last address, and wrap boundaries where meaningful;
- malformed, truncated, overlong, and bad-integrity frames;
- start while busy, stop in every important phase, and timeout;
- exact pulse width and cycle alignment;
- backpressure, buffer-full behavior, and recovery;
- read latency and ordered data after memory changes.

Use asymmetric data patterns to expose byte swaps and stale-word errors. Check not only the expected assertion but also that hazardous outputs are deasserted after completion, stop, error, and reset.

## Keep simulation realistic enough

Drive asynchronous inputs at non-clock-aligned times when testing CDC wrappers, while recognizing that digital simulation cannot model metastability probability. Avoid relying on simulator scheduling accidents; clock driving, stimulus, and sampling should have explicit ordering.

When a vendor primitive is not available in the lightweight simulator, isolate it behind a wrapper and test the surrounding contract. Run vendor simulation when primitive behavior is itself the risk.

The included `scripts/run_iverilog.py` compiles all RTL sources with one testbench and runs the resulting simulation. Use an explicit `--top` when the file contains more than one candidate top module.
