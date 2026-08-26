#!/usr/bin/env python3
"""Compile an RTL tree with one testbench and run it using Icarus Verilog."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rtl", type=Path, required=True, help="RTL file or directory")
    parser.add_argument("--testbench", type=Path, required=True, help="testbench .v/.sv file")
    parser.add_argument("--top", required=True, help="testbench top module")
    parser.add_argument("--include", action="append", default=[], type=Path, help="include directory")
    parser.add_argument("--define", action="append", default=[], help="macro, optionally NAME=VALUE")
    parser.add_argument("--keep-output", type=Path, help="keep the compiled simulation here")
    return parser.parse_args()


def collect_sources(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if not path.is_dir():
        raise FileNotFoundError(f"RTL path does not exist: {path}")
    return sorted((*path.rglob("*.sv"), *path.rglob("*.v")))


def require_tool(name: str) -> str:
    executable = shutil.which(name)
    if executable is None:
        raise RuntimeError(f"{name} was not found on PATH")
    return executable


def main() -> int:
    args = parse_args()
    try:
        iverilog = require_tool("iverilog")
        vvp = require_tool("vvp")
        sources = collect_sources(args.rtl.resolve())
        testbench = args.testbench.resolve(strict=True)
        if not sources:
            raise RuntimeError(f"no .v or .sv files found under {args.rtl}")

        with tempfile.TemporaryDirectory(prefix="fpga-iverilog-") as temp_dir:
            output = args.keep_output.resolve() if args.keep_output else Path(temp_dir) / "simulation.out"
            output.parent.mkdir(parents=True, exist_ok=True)
            command = [iverilog, "-g2012", "-s", args.top, "-o", str(output)]
            command.extend(f"-I{item.resolve()}" for item in args.include)
            command.extend(f"-D{item}" for item in args.define)
            command.extend(str(item) for item in sources)
            if testbench not in sources:
                command.append(str(testbench))

            print("Compiling:", " ".join(command), flush=True)
            subprocess.run(command, check=True)
            print("Running:", vvp, output, flush=True)
            subprocess.run([vvp, str(output)], check=True)
        return 0
    except (FileNotFoundError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
