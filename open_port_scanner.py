#!/usr/bin/env python3
"""Simple TCP open-port scanner.

Examples:
  python open_port_scanner.py --host 127.0.0.1 --start 1 --end 1024
  python open_port_scanner.py --host scanme.nmap.org --ports 22,80,443
"""

from __future__ import annotations

import argparse
import concurrent.futures
import socket
from typing import Iterable


def parse_ports(ports_arg: str | None, start: int, end: int) -> list[int]:
    """Return a validated list of ports from either --ports or a range."""
    if ports_arg:
        ports = sorted(
            {
                int(p.strip())
                for p in ports_arg.split(",")
                if p.strip()
            }
        )
    else:
        ports = list(range(start, end + 1))

    for port in ports:
        if not 1 <= port <= 65535:
            raise ValueError(f"Invalid port: {port}. Must be in [1, 65535].")

    return ports


def is_port_open(host: str, port: int, timeout: float) -> bool:
    """Check whether a TCP port is open on a host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex((host, port)) == 0


def scan_ports(host: str, ports: Iterable[int], timeout: float, workers: int) -> list[int]:
    """Scan ports concurrently and return open ones."""
    open_ports: list[int] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_port = {
            executor.submit(is_port_open, host, port, timeout): port for port in ports
        }
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                if future.result():
                    open_ports.append(port)
            except OSError:
                # Ignore transient socket errors for individual ports.
                pass

    return sorted(open_ports)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan a host for open TCP ports.")
    parser.add_argument("--host", default="127.0.0.1", help="Target host/IP (default: 127.0.0.1)")
    parser.add_argument("--ports", help="Comma-separated ports, e.g. 22,80,443")
    parser.add_argument("--start", type=int, default=1, help="Start of range when --ports not set")
    parser.add_argument("--end", type=int, default=1024, help="End of range when --ports not set")
    parser.add_argument("--timeout", type=float, default=0.4, help="Per-port timeout in seconds")
    parser.add_argument("--workers", type=int, default=200, help="Concurrent worker threads")
    args = parser.parse_args()

    try:
        ports = parse_ports(args.ports, args.start, args.end)
    except ValueError as err:
        parser.error(str(err))

    print(f"Scanning {args.host} ({len(ports)} ports)...")
    open_ports = scan_ports(args.host, ports, timeout=args.timeout, workers=args.workers)

    if open_ports:
        print("Open TCP ports:", ", ".join(map(str, open_ports)))
    else:
        print("No open TCP ports found in the selected range.")


if __name__ == "__main__":
    main()
