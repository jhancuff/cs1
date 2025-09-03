# CS-1: Single-Connector Infotainment Interface (Draft v0.9)

**Date:** September 03, 2025  
**License:** GPL v3  
**Authors:** Joe Hancuff (working draft)  

---

## 0. Introduction

The CS-1 specification defines a **universal single-connector standard** for vehicle infotainment head units (HUs).  
It eliminates the chaos of bespoke harnesses, CAN decoder boxes, VIN cables, and proprietary USB adapters.  
By converging **power, data, audio, video, and vehicle controls** onto one ruggedized connector, aftermarket and OEM systems become swappable and interoperable.  

---

## 1. Goals

- **Single physical connector (Automotive-C)** between vehicle and HU.  
- **No decoder boxes**: all functions are native (cameras, SWC, chimes, CAN data, amps).  
- **Plug-and-swap** aftermarket reliability at OEM quality.  
- **Secure by design**: HU never directly touches the vehicle CAN bus.  
- **Extensible**: designed for EV, ADAS, and future sensor stacks.  

---

## 2. Physical & Electrical

### 2.1 Connector
- Form factor: **USB-C Automotive-C** (locking, keyed, IP5X+, -40 °C to +85 °C).  
- ≥10,000 mating cycles, vibration-rated, EMI shielded.  

### 2.2 Power
- Transport: **USB Power Delivery 3.1 (EPR)**.  
- Profiles: 5V@3A, 12V@5A, 20V@5A, 48V@5A (up to 240W).  
- Classes:  
  - A: ≤60W — small displays.  
  - B: ≤100W — typical HU + DSP.  
  - C: ≤240W — HU + internal amps/AI.  
- Ignition sense: logical event (`vds.power`) instead of discrete ACC pin.  

---

## 3. Data Transport

### 3.1 Link
- Minimum: USB 3.2 Gen 2×1 (10 Gb/s).  
- Recommended: USB4 (20–40 Gb/s).  
- HU is **USB host**; vehicle side = **Vehicle Bridge Module (VBM)**.

### 3.2 Composite Interfaces (from VBM)
- **CDC-ECM/RNDIS:** Ethernet-over-USB (IP stack).  
- **USB-CAN-FD:** up to 5 logical buses.  
- **UAC2:** Audio playback/capture (multi-channel).  
- **UVC:** Cameras (reverse, 360, ADAS).  
- **HID:** Steering wheel controls and buttons.  
- **MSC (opt):** RO storage for manuals/logos.  
- **Vendor DFU:** Signed firmware update interface.  

---

## 4. Vehicle Data Service (VDS)

### 4.1 Transport
- gRPC over HTTP/2 over USB-Ethernet.  
- Namespace: `vds.*`.  
- Mandatory mutual TLS (mTLS).  

### 4.2 Core Topics
- **vds.power**: ignition state, Sleep/Wake RPC.  
- **vds.vehicle**: VIN, odometer, speed, fuel, TPMS, doors.  
- **vds.swc**: steering wheel button events.  
- **vds.chime**: chime requests.  
- **vds.camera**: enumerate/list cameras.  
- **vds.climate**: read/write setpoints.  
- **vds.lighting**: headlights/dimming state.  

### 4.3 Example Message
```json
// Reverse trigger
{"topic":"vds.vehicle","event":"Gear","value":"R","ts":1693612347123}
```

---

## 5. Audio / Video

### 5.1 Audio
- Playback: UAC2 PCM → vehicle amps.  
- Capture: OEM mic array → HU.  
- DSP metadata over `vds.audio`.  

### 5.2 Video
- UVC cameras (1080p30).  
- Legacy analog cameras digitized in VBM.  
- Reverse camera latency ≤300ms.  

---

## 6. Security & Safety

- **Mutual TLS** with factory-burned certs.  
- HU never touches vehicle CAN directly; VBM mediates.  
- Writable endpoints whitelisted + rate-limited.  
- Fail-safe: VBM maintains cameras/chimes if HU dies.  
- Signed audit logs in VBM NVRAM.  

---

## 7. Compliance Levels

- **Bronze:** USB 3.2 10 Gb/s, PD ≤100 W, 2 cams, 4ch audio.  
- **Silver:** USB4 20 Gb/s, PD ≤140 W, 3 cams, 6ch audio.  
- **Gold:** USB4 40 Gb/s, PD ≤240 W, 4 cams, 8ch audio, ADAS latency.  

---

## 8. Migration Example (2015 Ford Focus)

- Install VBM-Legacy-Ford-C1 behind dash.  
- 12V battery → PD3.1 → HU.  
- Ford CAN ↔ USB-CAN.  
- Factory reverse cam ↔ UVC.  
- Steering buttons ↔ HID.  
- One Automotive-C cable, no Maestro/Metra/PAC boxes.  

---

## 9. Developer Notes

### 9.1 Proto Compilation
```bash
protoc --go_out=. --go-grpc_out=. vds.proto
protoc --python_out=. --grpc_python_out=. vds.proto
protoc --java_out=. --grpc-java_out=. vds.proto
protoc --csharp_out=. --grpc_csharp_out=. vds.proto
```

### 9.2 Torque → VDS Bridge
- HU runs Torque app.  
- BT OBDII dongle feeds PID data.  
- Publish into `vds.vehicle` topics.  

### 9.3 Sample JSON RPC
```json
{"service":"vds.climate","method":"SetSetpoint","args":{"zone":"driver","c":20.0}}
```

---

## 10. Appendices

### 10.1 vds.proto
See [`vds.proto`](./vds.proto).

### 10.2 JSON Schema
See [`vds.schema.json`](./vds.schema.json).

---

**Contact:** Hancuff Automation CS-1 Working Group.  
**Status:** Draft v0.9 (open for contributions).  
