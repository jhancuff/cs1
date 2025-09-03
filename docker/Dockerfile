# Quick container for the Python server
FROM python:3.11-slim
WORKDIR /app
COPY server/python /app/server/python
COPY proto /app/proto
RUN pip install --no-cache-dir grpcio==1.65.5 grpcio-tools==1.65.5 protobuf>=4.25
WORKDIR /app/server/python
RUN python -m grpc_tools.protoc -I../../proto --python_out=. --grpc_python_out=. ../../proto/vds.proto
EXPOSE 50051
CMD ["python", "server.py"]
