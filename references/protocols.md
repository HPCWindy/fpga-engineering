# Framed protocols and control planes

Read this reference when RTL parses or emits UART, SPI, byte-stream, packet, command, or configuration data.

## Specify the wire contract first

Write down the sync bytes, version, command/type, length, payload layout, endianness, integrity field, timeout, maximum frame size, and response/error behavior. State whether the checksum covers its own field and whether a zero-length payload is valid.

The parser should recover from noise without requiring reset. Bound every advertised length before using it as a counter or memory address. On a malformed length or checksum failure, discard the staged frame and return to a documented resynchronization state.

## Stage then commit

Receive configuration into shadow storage. Validate command, length, field ranges, cross-field relationships, and checksum before producing a one-cycle commit or swapping the shadow and active banks. Active experiment parameters should normally be frozen for the duration of a run.

This prevents a truncated or corrupt frame from changing only the early fields. Test that invalid frames leave the previous complete configuration intact.

## Separate transport from behavior

Keep byte collection and serialization separate from command execution and long-running datapaths. Define what happens when:

- a command arrives while busy;
- stop and completion occur on the same edge;
- transmit backpressure lasts indefinitely;
- a response cannot keep up with acquisition;
- an acknowledgement is duplicated, stale, or missing;
- a sequence number or buffer index wraps.

Acquisition should not silently lose data because a slow UART is busy. Use buffering, backpressure at a safe boundary, a bounded timeout, or an explicit overflow error. If work pauses, leave physical controls in safe levels during the pause.

## Endianness and integrity

Use explicit byte assembly rather than relying on packed-struct layout across tools. Verify multi-byte fields with asymmetric values such as `32'h1234_abcd`; all-zero or small values can hide endianness bugs.

For CRCs, record polynomial, reflected/non-reflected processing, initial value, final XOR, byte order, and the exact covered bytes. Validate RTL against a known software implementation and at least one published or independently generated test vector.
