# Toolchain command patterns

Read this reference only when selecting or running local FPGA checks. Prefer repository-provided commands and versions over these generic patterns.

## Icarus Verilog

Compile SystemVerilog and run a self-checking testbench:

```text
iverilog -g2012 -s tb_top -o build/tb_top.out rtl/*.sv sim/tb_top.sv
vvp build/tb_top.out
```

Or use the portable helper:

```text
python scripts/run_iverilog.py --rtl rtl --testbench sim/tb_top.sv --top tb_top
```

Icarus is useful for fast behavioral regression but does not prove vendor primitive behavior, resource inference, timing, or constraints.

## Verilator

For lint-oriented checks:

```text
verilator --lint-only --Wall --timing --top-module top rtl/*.sv
```

Tune warnings deliberately. Do not globally suppress width, latch, clock, or unused-signal findings before understanding them.

## Vivado

Prefer a checked-in Tcl flow that creates/opens the project, adds the intended RTL and XDC, sets the exact part/top, and runs synthesis and implementation reproducibly. At minimum inspect:

```text
report_utilization
report_timing_summary
report_clock_interaction
report_cdc
report_exceptions
report_drc
```

Record WNS/TNS and WHS/THS, confirm no critical unconstrained paths, and check inferred RAM/DSP/clocking primitives. A successful `write_bitstream` is additional evidence, not a substitute for reviewing the reports.

## Tool availability

Discover local executables and repository scripts before assuming a tool exists. Do not download a vendor suite, modify licenses, or replace the user's toolchain without authorization. If the required tool is unavailable, complete checks that remain meaningful and hand off the exact command and expected evidence for the missing stage.
