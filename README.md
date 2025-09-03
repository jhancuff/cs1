# CS-1: Single-Connector Infotainment Interface (Chainsaw Standard)

Welcome to the **CS-1 Reference Implementation Repo** — also known as the *Chainsaw Standard*.  
This project defines and demonstrates a **single, universal connector** for vehicle infotainment head units (HUs), eliminating the cluster of bespoke harnesses, CAN decoder boxes, VIN cables, and proprietary USB adapters.  

CS-1 unifies **power, data, audio, video, and vehicle controls** over one ruggedized cable: **Automotive-C**.  

---

## 🌟 Vision

- **One connector.** Every OEM and aftermarket HU uses the same port.  
- **No decoder boxes.** All integration (cameras, SWC, chimes, CAN data, amps) is native.  
- **Drop-in aftermarket.** Replace or upgrade without reverse-engineering.  
- **Future-ready.** EV telemetry, ADAS sensors, rear-seat displays, all supported.  
- **Secure by design.** HU never touches raw CAN — the Vehicle Bridge Module (VBM) mediates.  

---

## 📂 Repo Structure

```
cs1-repo/
├─ README.md                # This file
├─ LICENSE                  # GPL v3
├─ COPYING                  # Full GPLv3 license text
├─ CODE_OF_CONDUCT.md
├─ CONTRIBUTING.md
├─ SECURITY.md
├─ .gitignore
├─ Makefile                 # Proto build shortcuts
├─ docs/
│  └─ SPEC.md               # Full Markdown spec (GitHub-friendly)
├─ proto/
│  └─ vds.proto             # Full gRPC API (Power, Vehicle, SWC, Climate, etc.)
├─ schema/
│  └─ vds.schema.json       # Pub/Sub + RPC envelope schema
├─ server/
│  └─ python/
│     ├─ Makefile           # protoc rules
│     ├─ requirements.txt
│     └─ server.py          # Example HU-side gRPC server
├─ client/
│  └─ python/
│     ├─ requirements.txt
│     └─ client.py          # Example gRPC client
├─ tools/
│  ├─ torque_bridge/
│  │  └─ bridge.py          # OBD-II → VDS bridge skeleton
│  └─ vbm_emulator/
│     └─ README.md          # Notes for a VBM simulator
└─ docker/
   └─ Dockerfile            # Containerized server
```

---

## 📜 Specification

The detailed technical specification is in [`docs/SPEC.md`](docs/SPEC.md). Highlights:

- **Connector:** Ruggedized USB-C Automotive-C, PD 3.1 (up to 240 W).  
- **Data transport:** USB 3.2 / USB4 carrying composite interfaces (Ethernet, CAN-FD, Audio, Video, HID).  
- **APIs:** gRPC services defined in [`proto/vds.proto`](proto/vds.proto).  
- **Security:** Mutual TLS, policy-gated writes, fail-safe VBM isolation.  
- **Compliance levels:** Bronze, Silver, Gold (scaling bandwidth/power).  
- **Migration example:** Retrofit a 2015 Ford Focus with a single CS-1 port, no Maestro/Metra boxes.  

---

## 🚀 Quick Start

### Python server + client

```bash
# Generate stubs
make -C server/python proto

# Install deps
python -m venv .venv && source .venv/bin/activate
pip install -r server/python/requirements.txt

# Run server
python server/python/server.py
```

In another shell:

```bash
source .venv/bin/activate
pip install -r client/python/requirements.txt
python client/python/client.py
```

You should see ignition and vehicle snapshot events streaming.

---

### Docker

```bash
cd docker
docker build -t cs1-vds .
docker run --rm -p 50051:50051 cs1-vds
```

---

## 🔧 Tools

- **Torque Bridge:** Listens for Torque Realtime Web Server UDP broadcasts, repackages OBD-II PIDs into `vds.vehicle` events. Extendable to any OBD-II source.  
- **VBM Emulator:** Placeholder for a real Vehicle Bridge Module; currently use `server/python/server.py` as your simulator.  

---

## 📡 Protocols

- **gRPC services:** Power, Vehicle, SWC, Chime, Camera, Climate, Lighting.  
- **Messages:** JSON envelopes validated by [`schema/vds.schema.json`](schema/vds.schema.json).  
- **Sample event:**
```json
{
  "topic": "vds.vehicle",
  "event": "Gear",
  "value": "R",
  "ts": 1693612347123
}
```

---

## 🤝 Contributing

1. Fork and branch off `main`.  
2. Update the spec in [`docs/SPEC.md`](docs/SPEC.md).  
3. Update `proto/` and `schema/` if adding/changing fields.  
4. Add tests/examples for new methods.  
5. Open a PR.  

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.  

---

## 🛡️ Security

Found a vulnerability? Please follow [SECURITY.md](SECURITY.md) — do **not** file public issues for exploits.  

---

## 📜 License

- Code and documentation are licensed under the **GNU General Public License v3 (GPL v3)**.  
- See [LICENSE](LICENSE) and [COPYING](COPYING).  

---

## 🧭 Roadmap

- [ ] Expand VBM emulator to handle mock CAN, UVC, and UAC devices.  
- [ ] Implement Torque Bridge → gRPC publisher.  
- [ ] Add Go and Node.js clients.  
- [ ] GitHub Actions CI (lint + proto build + server smoke test).  
- [ ] Demo dashboard (React) for live VDS events.  

---

**CS-1: One connector. No excuses. Chainsaw the bullshit.**
