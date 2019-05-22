# -*- coding: utf-8 -*-

import grpc
from concurrent import futures
import threading
import time
from GrpcProto import connect_pb2
from GrpcProto import connect_pb2_grpc
from GrpcProto import scan_pb2
from GrpcProto import scan_pb2_grpc
import plugins
import ipcalc
import socket

workerList={}
scanQueue={}
portaServidor="46000"

class ServerInit(connect_pb2_grpc.ConnectServicer):

    def ConnectServer(self, request, context):
        ipWorker = request.WorkerIp
        portWorker = request.WorkerPort
        addrs=ipWorker+":"+portWorker
        tmp={str(addrs):True}
        workerList.update(tmp)
        print("\n[*] Nova Ligacao: "+addrs)

        result = {'Confirmation': True}
        return connect_pb2.HelloWorker(**result)

class ClientCom(scan_pb2_grpc.ScanServicer):

    def ListModules(self, request, context):
        PluginList=plugins.GetPluginsNames()
        result = {'ModulesNames': PluginList}
        return scan_pb2.ModuleList(**result)

    def ScanDescription(self, request, context):
        description=plugins.GetPluginDescription(request.Modulo)
        result = {'Description':description}
        return scan_pb2.DescriptionResponse(**result)

    def ScanIp(self, request, context):
        ipToScan=request.IpRange
        moduleToScan=request.Modulo

        if plugins.checkIfPluginExists(moduleToScan)==False:
            result = {'Resposta':'ERROR'}
            return scan_pb2.ScanResponse(**result)
        
        try:
            for x in ipcalc.Network(ipToScan):
                tmp={str(x):moduleToScan}
                scanQueue.update(tmp)
        except:
            result = {'Resposta':'ERROR'}
            return scan_pb2.ScanResponse(**result)

        for worker,avaiable in workerList.iteritems(): #TODO Pedidos assincronos?
                if avaiable == True:
                    if len(scanQueue) >0:
                        ip,module=scanQueue.popitem()
                        avaiable=False
                        sendScan(worker,ip,module)
                        avaiable=True

        result = {'Resposta':'TEMPORARIO'} #TODO Mudar resposta
        return scan_pb2.ScanResponse(**result)

def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    connect_pb2_grpc.add_ConnectServicer_to_server(ServerInit(),server)
    scan_pb2_grpc.add_ScanServicer_to_server(ClientCom(),server)
    server.add_insecure_port('[::]:{}'.format(portaServidor))

    server.start()
    print ('[*] Servidor Iniciado')

    try:
        while True:
            time.sleep(60 * 60 * 24)

    except KeyboardInterrupt:
        server.stop(0)
        print('[*] A Encerrar o Servidor')

def sendScan(worker,range,module):
    channel = grpc.insecure_channel(worker)
    stub = scan_pb2_grpc.ScanStub(channel)
    message =scan_pb2.ScanRequest(IpRange=range,Modulo=module)
    return stub.ScanIp(message)


def main():
    start_server()

if __name__== "__main__":
    main()