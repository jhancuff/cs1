import grpc
import vds_pb2 as pb
import vds_pb2_grpc as rpc

def main():
    channel = grpc.insecure_channel("localhost:50051")
    power = rpc.PowerServiceStub(channel)
    vehicle = rpc.VehicleServiceStub(channel)

    print("Subscribing to ignition...")
    for i_event in power.SubscribeIgnition(pb.SubscribeRequest()):
        print("Ignition:", i_event)
        break

    print("Subscribing to vehicle snapshots...")
    for v in vehicle.SubscribeVehicle(pb.SubscribeRequest()):
        print("Vehicle:", v)
        break

if __name__ == "__main__":
    main()
