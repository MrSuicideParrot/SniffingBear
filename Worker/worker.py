# -*- coding: utf-8 -*-

from concurrent import futures
import time
import sys
import grpc
from GrpcProto import connect_pb2
from GrpcProto import connect_pb2_grpc
from GrpcProto import scan_pb2
from GrpcProto import scan_pb2_grpc
import plugins
import argparse
import urllib2
import os
import stat
import masscan
import pprint

pp = pprint.PrettyPrinter(indent=4)
serverIp='localhost'
serverPort="46000"
defaultURL="https://raw.githubusercontent.com/0xSmiley/ModulosTMP/master/modules/" #TODO ALTERAR


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
        print("[*] Scanning "+ipToScan+" Modulo "+moduleToScan) #TODO Check if all plugins
            
        if plugins.checkIfPluginExists(moduleToScan)==False:
            print('Downloading module '+moduleToScan)
            files=[]
            files.append(moduleToScan + ".py")
            files.append(moduleToScan + ".pyc")
            files.append(moduleToScan + ".yapsy-plugin")
            
            for filetmp in files:
                filedata = urllib2.urlopen(defaultURL+filetmp)  
                datatowrite = filedata.read()

                with open('./modules/'+filetmp, 'wb') as f:  
                    f.write(datatowrite)
            
                if ".pyc" not in filetmp:
                    st = os.stat('./modules/'+filetmp)
                    os.chmod('./modules/'+filetmp, st.st_mode | stat.S_IEXEC)
            
            plugins.reloadPlugins()
            
        IP_PORTS = [22,80,8080] #TODO Retrieve this from plugin
        #availableHosts = doMasscan(ipToScan, IP_PORTS)
            
        result = {'Resposta': "Fostes Scanado"}
        return scan_pb2.ScanResponse(**result)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("WorkerPort", nargs='?', default="2000")
    parser.add_argument("ServerIp", nargs='?', default="localhost")
    parser.add_argument("ServerPort", nargs='?', default="46000")
    args = parser.parse_args()
    
    WorkerPort = args.WorkerPort
    serverIp=args.ServerIp
    serverPort=args.ServerPort
    
    UUID = os.geteuid()
    if UUID != 0:
        print("Please execute this script with root privileges(for masscan)")
        return
    
    client = ServerInit()
    
    print(client.connectToServer("localhost",WorkerPort))

    print("[*] Client Server Started")
    scan = ServerScan()
    scan.start_server(WorkerPort)
    print("[*] Acabou")


if __name__== "__main__":
    main()