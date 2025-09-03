# CS-1: Single-Connector Infotainment Interface

This repository contains the **Chainsaw Standard (CS-1)** specification and reference implementation scaffolding.

## Contents
- `docs/SPEC.md` — Full Markdown spec (GitHub-friendly).
- `proto/` — gRPC definitions (`vds.proto`).
- `schema/` — JSON schema for envelopes.
- `server/python/` — Example HU-side gRPC server.
- `client/python/` — Example client that subscribes to streams.
- `tools/torque_bridge/` — Skeleton that forwards OBD-II PIDs into VDS topics.
- `tools/vbm_emulator/` — Vehicle Bridge Module emulator for local testing.
- `docker/` — Container build for quick trials.

## Quick Start (Python)
```bash
# 1) Generate Python stubs
make -C server/python proto

# 2) Install deps
python -m venv .venv && source .venv/bin/activate
pip install -r server/python/requirements.txt

# 3) Run server
python server/python/server.py

# 4) Run client (separate shell)
source .venv/bin/activate
pip install -r client/python/requirements.txt
python client/python/client.py
```

## License
CC-BY 4.0
