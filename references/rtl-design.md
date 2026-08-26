# RTL design decisions

Read this reference when creating or reviewing synthesizable Verilog/SystemVerilog.

## Sequential logic and arithmetic

- Use one clear owner for each register. Multiple procedural drivers are rarely portable and make reset and priority ambiguous.
- Use nonblocking assignments for clocked state. Use blocking assignments for local combinational calculations, with defaults that cover every path.
- Size constants and intermediate values deliberately. Check truncation, carry, signed comparison, negative values, and the behavior at maximum counter values.
- Define whether an interval of `N` cycles means counts `0..N-1`, and test `N=0` and `N=1`. Avoid the common `counter == N` extra-cycle error.
- Convert human time to cycles outside the tight datapath where possible. State whether conversion floors, rounds, or saturates.

## FSMs and physical outputs

Choose state encoding based on timing, observability, safety, and tool behavior; one-hot is not a universal default. Prefer registered physical controls when a decoding glitch could create a pulse on a laser, RF gate, motor, converter, write-enable, chip-select, or reset line.

For every FSM, define:

- entry and exit conditions for each state;
- exact cycle ownership of strobes and counters;
- reset, stop, timeout, and illegal-state destinations;
- whether outputs are Moore-style registered values or combinational decodes;
- behavior when a request arrives while busy.

Set safe output defaults explicitly. A stop request should normally win over progress transitions on the same edge. If an output must remain asserted across states, encode that intent directly instead of relying on an incidental decode.

## Expensive or misleading constructs

Behaviorally small expressions can produce large hardware:

- `a / b` or `a % b` with a variable divisor may infer a deep combinational divider;
- wide priority chains, nested ternaries, and large address decoders may become long mux paths;
- variable shifts may infer barrel shifters;
- array reset loops may prevent block RAM inference;
- asynchronous reads may force distributed memory rather than block RAM.

Before preserving one of these constructs, decide whether it is constant-folded, acceptably slow, pipelined, iterative, implemented by a vendor IP, or better precomputed by software. Inspect the synthesis result rather than guessing.

## Interface ownership

Use `valid/ready`, request/acknowledge, or an equally explicit contract between modules. A one-cycle pulse is only an interface if the receiver is guaranteed to observe that cycle. Keep status distinct from commands, and do not derive state from output pins when the internal state is available.
