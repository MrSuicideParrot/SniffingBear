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
import socket
import json

pp = pprint.PrettyPrinter(indent=4)
serverIp='localhost'
serverPort="46000"
defaultURL="https://raw.githubusercontent.com/0xSmiley/ModulosTMP/master/modules/" #TODO ALTERAR


def doMasscan(ip, ports):
    if not type(ports) is list:
        raise Exception("Illegal Arguments")
 
    try:
        mas = masscan.PortScanner()
        mas.scan(ip, ports=",".join(str(i) for i in ports), arguments='--wait 0')

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
        server.add_insecure_port('0.0.0.0:{}'.format(WorkerPort))

        server.start()
        print ('[*] Esperando comandos')

        try:
            while True:
                time.sleep(60*60*60)
        except KeyboardInterrupt:
            server.stop(0)
            print('[*] A Encerrar o Client')

    def ScanIp(self, request, context):
        ipToScan=request.IpRange
        moduleToScan=request.Modulo
        portasToScan=request.Ports
        portList=[]
        moduleList=[]
        
        if ',' in moduleToScan:
            moduleList=moduleToScan.split(',')
        else:
            moduleList.append(moduleToScan)
        
        if  portasToScan == "all":
            pass
        elif ',' in portasToScan:
            portasToScan=portasToScan.split(',')
            portList=list(map(int,portasToScan))
        else:
            portList.append(portasToScan)
            portList=list(map(int,portList))
        
        for module in moduleList:    
            if plugins.checkIfPluginExists(module)==False:
                downloadModule(module,False)
            
        plugins.reloadPlugins()
        
        IP_PORTS=[]
        pluginsList=[]
        
        for module in moduleList:
            print("[*] Scanning "+ipToScan+" Modulo "+module)
            if module == "telnetlogger": #TODO RESOLVER
                continue
            plugin = plugins.getPluginIfExists(module) 
            plugin = plugin.plugin_object
            pluginsList.append(plugin)
            
            if portasToScan != "all":
                portTMP=[]
                portTMP.extend(plugin.get_port_list())
                IP_PORTS.extend(list(set(portTMP).intersection(portList)))
            else:
                IP_PORTS.extend(plugin.get_port_list())
        
        if len(IP_PORTS) == 0:
            print("No matching ports")
            result = {'Resposta': "No matching ports"}
            return scan_pb2.ScanResponse(**result)
        
        IP_PORTS = list(dict.fromkeys(IP_PORTS))
        availableHosts = doMasscan(ipToScan, IP_PORTS)
        resposta = {}
        for i in availableHosts:
            for plugin in pluginsList:
                resposta[i] = plugin.run(i)
        print("Done")
        result = {'Resposta': json.dumps(resposta)}
        return scan_pb2.ScanResponse(**result)
    
    def CustomScan(self, request, context):
        ipToScan=request.IpRange
        moduleUrl=request.ModuloUrl
        
        modulo = downloadModule(moduleUrl,True)
        plugins.reloadPlugins()
        
        plugin = plugins.getPluginIfExists(modulo) 
        plugin = plugin.plugin_object
        
        IP_PORTS=[]
        IP_PORTS.extend(plugin.get_port_list())
        
        if len(IP_PORTS) == 0:
            print("No matching ports")
            result = {'RespostaCustomScan': "No matching ports"}
            return scan_pb2.CustomScanResponse(**result)
        
        IP_PORTS = list(dict.fromkeys(IP_PORTS))
        
        availableHosts = doMasscan(ipToScan, IP_PORTS)
        resposta = {}
        for i in availableHosts:
            resposta[i] = plugin.run(i)
            
        print("Done")
        result = {'RespostaCustomScan': json.dumps(resposta)}
        return scan_pb2.CustomScanResponse(**result)
        
def downloadModule(module,isUrl):
    
    customUrl=""
    if isUrl == True:
        tmp=module.split('/')
        mod=tmp[len(tmp)-1]
        customUrl =module.replace(mod, '')
        module = mod 
    print('Downloading module '+module)
    files=[]
    files.append(module + ".py")
    files.append(module + ".yapsy-plugin")
    
    for filetmp in files:
        if isUrl == False:
            filedata = urllib2.urlopen(defaultURL+filetmp)  
        else:
            filedata = urllib2.urlopen(customUrl+filetmp)  
        datatowrite = filedata.read()

        with open('./modules/'+filetmp, 'wb') as f:  
            f.write(datatowrite)
    
        st = os.stat('./modules/'+filetmp)
        os.chmod('./modules/'+filetmp, st.st_mode | stat.S_IEXEC)
    if isUrl == True:
        return module

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("WorkerPort", nargs='?', default="2000")
    parser.add_argument("ServerIp", nargs='?', default="localhost")
    parser.add_argument("ServerPort", nargs='?', default="46000")
    args = parser.parse_args()
    
    global serverIp
    global serverPort

    WorkerPort = args.WorkerPort
    serverIp=args.ServerIp
    serverPort=args.ServerPort
    
    UUID = os.geteuid()
    if UUID != 0:
        print("Please execute this script with root privileges(for masscan)")
        return
    
    client = ServerInit()
    myip=getIP()
    print(myip)
    client.connectToServer(myip,WorkerPort)

    print("[*] Client Server Started")
    scan = ServerScan()
    scan.start_server(WorkerPort)
    print("[*] Acabou")
    client.connectToServer(myip,WorkerPort)

def getIP():
    return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
    s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET,
    socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

if __name__== "__main__":
    main()
