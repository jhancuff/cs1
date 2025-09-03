PROTO=../../proto/vds.proto

all: proto

proto:
	python -m grpc_tools.protoc -I../../proto --python_out=. --grpc_python_out=. $(PROTO)
	@echo 'Generated Python stubs in server/python/'
