# Constraints and board bring-up

Read this reference when editing XDC/SDC, assigning pins, connecting instruments, or debugging hardware.

## Constraints are part of the design

- Create every primary clock with the correct period and waveform.
- Define generated clocks at the real clocking primitive output when the tool cannot infer them.
- Constrain asynchronous interfaces with the selected CDC structure; audit unconstrained paths.
- Set package pin, I/O standard, bank voltage compatibility, slew, drive, pulls, and differential/single-ended usage from the board schematic and master constraint file.
- Treat active-low names and board-direction labels from the FPGA's perspective; USB-UART TX/RX labels are a frequent source of reversal.

Do not copy pin constraints across boards merely because connector names match. Verify FPGA part, package, bank voltage, connector pin, and external electrical standard.

Timing exceptions require an explanation tied to structure. A false path should identify a genuinely asynchronous or functionally irrelevant path, not conceal a synchronous violation. Re-run `report_exceptions`, unconstrained-path checks, timing summary, and DRC after changing constraints.

## Bring up safely

Start with reset, clock presence, configuration, and static-safe outputs. Then test one physical interface at a time with conservative levels and explicit ownership. Use a minimal hardware diagnostic mode when it reduces uncertainty, but enforce these properties:

- available only in a documented idle/debug state;
- rejects unsafe widths or configurations;
- cannot fight the normal datapath for a pin;
- stop and reset revoke debug ownership;
- outputs return automatically to safe levels after bounded pulses.

For cycle-accurate external timing, expose a reference trigger generated on the same registered edge as the event under measurement. Measure cable, level shifter, RF source, detector, and instrument delays relative to that trigger rather than assuming FPGA pin timing equals physical-system timing.

Before programming hardware, confirm bitstream provenance, target part, constraint set, tool version, and build result. Never infer that a behavioral test means the pinout or voltage is safe.
