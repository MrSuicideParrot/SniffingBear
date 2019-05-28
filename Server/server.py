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
        if addrs in workerList:
            workerList.pop(addrs)
            print("\n[*] Connection over: "+addrs)
        else :
            tmp={str(addrs):True}
            workerList.update(tmp)
            print("\n[*] New Connection: "+addrs)

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

        if moduleToScan == "all":
            moduleToScan=','.join(plugins.GetPluginsNames())
            

        elif plugins.checkIfPluginExists(moduleToScan)==False:
            result = {'Resposta':'ERROR'}
            return scan_pb2.ScanResponse(**result)

        sendScanToWorker(ipToScan,moduleToScan,portasToScan,False)

        resp=""
        for i in range(len(results)): #TODO Mudar resposta
            x=results.pop()
            if resp != "":
                resp=resp+";"+x
            else:
                resp=x

        result = {'Resposta':resp} #TODO Mudar resposta
        return scan_pb2.ScanResponse(**result)

    def CustomScan(self, request, context):
        ipToScan=request.IpRange
        moduleUrl=request.ModuloUrl
        
        sendScanToWorker(ipToScan,moduleUrl,[],True)
        
        resp=""
        for i in range(len(results)): #TODO Mudar resposta
            x=results.pop()
            if resp != "":
                resp=resp+";"+x
            else:
                resp=x
        
        result = {'RespostaCustomScan':resp} #TODO Mudar resposta
        return scan_pb2.CustomScanResponse(**result)


def sendScanToWorker(ipToScan,moduleToScan,portasToScan,isUrl):
    ipScanList=[]
    dividir=0
    try:
        for x in netaddr.IPNetwork(ipToScan):
            ipScanList.append(str(x))
        dividir=len(ipScanList)/len(workerList)
    except:
        if isUrl == False:
            result = {'Resposta':'ERROR'}
            return scan_pb2.ScanResponse(**result)
        result = {'RespostaCustomScan':'ERROR'}
        return scan_pb2.CustomScanResponse(**result)

    dividirInit=0
    dividirFim=dividir-1
    workersize=len(workerList)
    
    for worker,avaiable in workerList.iteritems():
        print("Dividing Range "+ipScanList[dividirInit]+" "+ipScanList[dividirFim])
        ips = netaddr.IPRange(ipScanList[dividirInit], ipScanList[dividirFim])
        for cidr in ips.cidrs():
            if avaiable == True:
                if isUrl == False:
                    sendScan(worker,str(cidr),moduleToScan,portasToScan)
                    
                else:
                    sendCustomScan(worker,str(cidr),moduleToScan)
        if len(ipScanList)==1:
            break
        dividirInit=dividirInit+dividir
        dividirFim=dividirFim+dividir
       
    while(True):
        if len(results) == workersize or len(results) > 0 and len(ipScanList)==1:
            break


def start_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    connect_pb2_grpc.add_ConnectServicer_to_server(ServerInit(),server)
    scan_pb2_grpc.add_ScanServicer_to_server(ClientCom(),server)
    server.add_insecure_port('0.0.0.0:{}'.format(portaServidor))

    server.start()
    print ('[*] Server Started')

    try:
        while True:
            time.sleep(60 * 60 * 24)

    except KeyboardInterrupt:
        server.stop(0)
        print('[*] Server Shut Down')

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

def sendCustomScan(worker,range,moduleUrl):

    def GetScanResults(done):
        results.append(done.result().RespostaCustomScan)
        replaceValueDic(workerList,worker,True)

    channel = grpc.insecure_channel(worker)
    replaceValueDic(workerList,worker,False)
    stub = scan_pb2_grpc.ScanStub(channel)
    message =scan_pb2.CustomScanRequest(IpRange=range,ModuloUrl=moduleUrl)
    call_future= stub.CustomScan.future(message)
    call_future.add_done_callback(GetScanResults)

    
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