PROTO=proto/vds.proto

.PHONY: proto python go java csharp clean

python:
	$(MAKE) -C server/python proto

proto: python

go:
	protoc -Iproto --go_out=. --go-grpc_out=. $(PROTO)

java:
	protoc -Iproto --java_out=. --grpc-java_out=. $(PROTO)

csharp:
	protoc -Iproto --csharp_out=. --grpc_csharp_out=. $(PROTO)

clean:
	rm -f server/python/*_pb2*.py
