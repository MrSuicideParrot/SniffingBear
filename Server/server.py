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
import socket
import argparse
import netaddr

workerList={}
scanQueue={}
portaServidor="46000"
results=[]

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
        portasToScan=request.Ports
        
        if moduleToScan == "all":#TODO
            moduleToScan=','.join(plugins.GetPluginsNames())
            print("aqui"+moduleToScan)
            
        elif plugins.checkIfPluginExists(moduleToScan)==False:
            result = {'Resposta':'ERROR'}
            return scan_pb2.ScanResponse(**result)
        ipScanList=[]
        dividir=0
        
        if portasToScan == "all": #TODO get portas do plugin
            print(portasToScan)
        
        
        try:
            for x in netaddr.IPNetwork(ipToScan):
                ipScanList.append(str(x))
                
            dividir=len(ipScanList)/len(workerList)
            
        except:
            result = {'Resposta':'ERROR'}
            return scan_pb2.ScanResponse(**result)
      
        dividirInit=0
        dividirFim=dividir-1
        workersize=len(workerList)
        for worker,avaiable in workerList.iteritems():
            print("Dividir Range "+ipScanList[dividirInit]+" "+ipScanList[dividirFim])
            ips = netaddr.IPRange(ipScanList[dividirInit], ipScanList[dividirFim])
           
            for cidr in ips.cidrs():
                if avaiable == True:
                    
                    sendScan(worker,str(cidr),moduleToScan,portasToScan)
                    break
            dividirInit=dividirInit+dividir
            dividirFim=dividirFim+dividir 
        
        
        while(True):
            if len(results) == workersize:
                break
            
        for i in range(len(results)): #TODO Mudar resposta
            x=results.pop()
            print(x)
    
        result = {'Resposta':'TEMPORARIO'} #TODO Mudar resposta
        return scan_pb2.ScanResponse(**result)

    def CustomScan(self, request, context):
        ipToScan=request.IpRange
        moduleUrl=request.ModuloUrl

        print(moduleUrl)


def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    connect_pb2_grpc.add_ConnectServicer_to_server(ServerInit(),server)
    scan_pb2_grpc.add_ScanServicer_to_server(ClientCom(),server)
    server.add_insecure_port('0.0.0.0:{}'.format(portaServidor))

    server.start()
    print ('[*] Servidor Iniciado')

    try:
        while True:
            time.sleep(60 * 60 * 24)

    except KeyboardInterrupt:
        server.stop(0)
        print('[*] A Encerrar o Servidor')

def sendScan(worker,range,module,portas):
    
    def GetScanResult(done):
        results.append(done.result().Resposta)
        replaceValueDic(workerList,worker,True)

    
    channel = grpc.insecure_channel(worker)
    replaceValueDic(workerList,worker,False)
    stub = scan_pb2_grpc.ScanStub(channel)
    message =scan_pb2.ScanRequest(IpRange=range,Modulo=module,Ports=portas)
    call_future= stub.ScanIp.future(message)
    call_future.add_done_callback(GetScanResult)



    
def replaceValueDic(dicionario, key_to_find, replace):
    for key in dicionario.keys():
        if key == key_to_find:
            dicionario[key] = replace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ServerPort", nargs='?', default="46000")
    args = parser.parse_args()
    portaServidor=args.ServerPort

    start_server()

if __name__== "__main__":
    main()