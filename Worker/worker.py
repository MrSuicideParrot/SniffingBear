# -*- coding: utf-8 -*-

from concurrent import futures
import time
import sys
import grpc
from GrpcProto import connect_pb2
from GrpcProto import connect_pb2_grpc
from GrpcProto import scan_pb2
from GrpcProto import scan_pb2_grpc
import os
import plugins
import masscan
import pprint

serverIp='localhost'
serverPort="46000"
pp = pprint.PrettyPrinter(indent=4)

def doMasscan(ip, ports):
    if not type(ports) is list:
        raise Exception("Illegal Arguments")
 
    try:
        mas = masscan.PortScanner()
        mas.scan(ip, ports=",".join(str(i) for i in ports))

        hosts_Info = mas.scan_result["scan"]
        outList = []
        for key in hosts_Info: 
            outList.append(key)

        return outList
    except masscan.masscan.NetworkConnectionError:
        return []


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

class ServerScan(scan_pb2_grpc.ScanServicer): #TODO GET MODULO

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
        ipToScan=request.IpRange
        moduleToScan=request.Modulo
        print("[*] Scanning "+ipToScan+" Modulo "+moduleToScan)
        
        if plugins.checkIfPluginExists(moduleToScan)==False: #TODO FAZER DOWNLOAD
            print("Not yet Implemented")

        IP_PORTS = [22,80,8080] #TODO Retrieve this from plugin
        availableHosts = doMasscan(ipToScan, IP_PORTS)

        result = {'Resposta': "Fostes Scanado"}
        return scan_pb2.ScanResponse(**result)


def main():
    UUID = os.geteuid()
    if UUID != 0:
        print("Please execute this script with root privileges(for masscan)")
        return


    client = ServerInit()
    WorkerPort = sys.argv[1]
    print(client.connectToServer("localhost",WorkerPort))

    print("[*] Client Server Started")
    scan = ServerScan()
    scan.start_server(WorkerPort)
    print("[*] Acabou")


if __name__== "__main__":
    main()