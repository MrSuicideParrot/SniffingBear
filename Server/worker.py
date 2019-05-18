# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from concurrent import futures
import time
import sys
import grpc
from GrpcServerWorker import connect_pb2
from GrpcServerWorker import connect_pb2_grpc
from GrpcServerWorker import scan_pb2
from GrpcServerWorker import scan_pb2_grpc


serverIp='localhost'
serverPort="46000"
#WorkerPort="46001"

class ServerInit():
    def __init__(self):
        self.host = serverIp
        self.server_port = serverPort

        #self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))
        self.channel = grpc.insecure_channel(serverIp+":"+serverPort)
        self.stub = connect_pb2_grpc.ConnectStub(self.channel)

    def connectToServer(self, messageIp,messagePort):
        message =connect_pb2.HelloServer(WorkerIp=messageIp,WorkerPort=messagePort)
        return self.stub.ConnectServer(message)

class ServerScan(scan_pb2_grpc.ScanServicer):

    def start_server(self,WorkerPort):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        scan_pb2_grpc.add_ScanServicer_to_server(ServerScan(),server)
        server.add_insecure_port('[::]:{}'.format(WorkerPort))

        server.start()
        print ('[*] Esperando comandos')

        try:
            while True:
                time.sleep(60*60*60)
        except KeyboardInterrupt:
            server.stop(0)
            print('[*] A Encerrar o Client')

    def ScanIp(self, request, context): #TODO


        print("[*] Scanning "+request.IpRange+" Modulo "+request.Modulo)

        result = {'Resposta': "Fostes Scanado"}
        return scan_pb2.ScanResponse(**result)


def main():

    client = ServerInit()
    WorkerPort = sys.argv[1]
    print(client.connectToServer("localhost",WorkerPort))

    print("[*] Client Server Started")
    scan = ServerScan()
    scan.start_server(WorkerPort)
    print("[*] Acabou")


if __name__== "__main__":
    main()