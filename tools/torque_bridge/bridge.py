# Torque → VDS Bridge (skeleton)
# Reads OBD-II PIDs (via an existing library or Torque broadcast) and republishes into VDS topics.
# TODO: implement actual OBD read loop (e.g., via python-OBD or UDP broadcast from Torque).

import time, json, socket

def main():
    # Example: receive UDP from Torque Realtime Web Server plugin (configurable)
    UDP_IP = "0.0.0.0"
    UDP_PORT = 35000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Listening for Torque UDP on {UDP_IP}:{UDP_PORT} ...")

    while True:
        data, addr = sock.recvfrom(8192)
        line = data.decode(errors="ignore").strip()
        # Parse k=v pairs like "time=16936&kff1001=88.0&rpm=1800&speed=45.2"
        kv = dict(pair.split("=",1) for pair in line.split("&") if "=" in pair)
        # Map to VDS vehicle snapshot (pseudo; real code would call gRPC client)
        vds_payload = {
            "topic": "vds.vehicle",
            "event": "OBD",
            "value": {
                "rpm": float(kv.get("rpm", 0.0)),
                "speed_kph": float(kv.get("speed", 0.0)),
                "throttle": float(kv.get("throttle", 0.0)),
            },
            "ts": int(time.time()*1000)
        }
        print(json.dumps(vds_payload))

if __name__ == "__main__":
    main()
