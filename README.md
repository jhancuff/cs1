# CS-1 Infotainment Interface (Draft v0.9)

This repo contains the working draft of **CS-1: Single-Connector Infotainment Interface**.

## Contents
- `CS-1_Infotainment_Interface_Spec_v0.9.docx` — Draft spec sheet (Word format)
- `vds.proto` — gRPC service + message definitions for Vehicle Data Service
- `vds.schema.json` — JSON Schema for pub/sub + RPC envelopes

## Build Notes
### Proto Compilation
To generate stubs:

```bash
protoc --go_out=. --go-grpc_out=. vds.proto
protoc --python_out=. --grpc_python_out=. vds.proto
protoc --java_out=. --grpc-java_out=. vds.proto
protoc --csharp_out=. --grpc_csharp_out=. vds.proto
```

### Example Usage
- **Server (HU side)** subscribes to topics and makes RPCs like `SetSetpoint`.
- **Client (VBM side)** publishes ignition, vehicle, SWC, etc.

### Sample JSON (publish event)
```json
{
  "topic": "vds.vehicle",
  "event": "Gear",
  "value": "R",
  "ts": 1693612347123
}
```

### Torque → VDS Bridge
Run Torque on the HU, subscribe to OBDII PIDs, and re-publish them into `vds.vehicle` topics so other apps can consume them consistently.

## License
GPL v3
