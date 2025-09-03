import time
import grpc
from concurrent import futures

import vds_pb2 as pb
import vds_pb2_grpc as rpc

class PowerService(rpc.PowerServiceServicer):
    def SubscribeIgnition(self, request, context):
        # Stream IG_RUN every 2s
        while True:
            yield pb.IgnitionEvent(state=pb.IG_RUN, ts_ms=int(time.time()*1000))
            time.sleep(2)

    def Sleep(self, request, context):
        return pb.Ack(ok=True, msg=f"sleep in {request.timeout_s}s")

    def Wake(self, request, context):
        return pb.Ack(ok=True, msg="wake requested")

class VehicleService(rpc.VehicleServiceServicer):
    def SubscribeVehicle(self, request, context):
        while True:
            snap = pb.VehicleSnapshot(
                vin="TESTVIN1234567890",
                odometer_km=12345.6,
                speed_kph=0.0,
                gear="P",
                fuel_percent=72.5,
                soc_percent=0.0,
                ambient_c=22.0,
                ts_ms=int(time.time()*1000),
            )
            yield snap
            time.sleep(1)

class SWCService(rpc.SWCServiceServicer):
    def SubscribeButtons(self, request, context):
        while True:
            yield pb.ButtonEvent(code=pb.BTN_VOL_UP, long_press=False, repeat=0, ts_ms=int(time.time()*1000))
            time.sleep(5)

class ChimeService(rpc.ChimeServiceServicer):
    def PlayChime(self, request, context):
        print(f"Chime id={request.id} priority={request.priority} vol={request.volume}")
        return pb.Ack(ok=True, msg="chime played")

class CameraService(rpc.CameraServiceServicer):
    def ListCameras(self, request, context):
        return pb.CameraList(cameras=[pb.CameraInfo(id="rev", name="Reverse", width=1280, height=720, fps=30, encoding="h264", is_reverse=True)])

class ClimateService(rpc.ClimateServiceServicer):
    def GetSnapshot(self, request, context):
        return pb.ClimateSnapshot(driver_setpoint_c=21.5, pass_setpoint_c=22.0, fan=3, mode="AUTO", ts_ms=int(time.time()*1000))

    def SetSetpoint(self, request, context):
        print(f"Set {request.zone} setpoint to {request.c}C")
        return pb.Ack(ok=True, msg="ok")

class LightingService(rpc.LightingServiceServicer):
    def SubscribeLighting(self, request, context):
        while True:
            yield pb.LightingSnapshot(headlights_on=False, auto_mode=True, dim_level=50, ts_ms=int(time.time()*1000))
            time.sleep(3)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.PowerServiceServicer_to_server(PowerService(), server)
    rpc.VehicleServiceServicer_to_server(VehicleService(), server)
    rpc.SWCServiceServicer_to_server(SWCService(), server)
    rpc.ChimeServiceServicer_to_server(ChimeService(), server)
    rpc.CameraServiceServicer_to_server(CameraService(), server)
    rpc.ClimateServiceServicer_to_server(ClimateService(), server)
    rpc.LightingServiceServicer_to_server(LightingService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("CS-1 VDS server listening on :50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
