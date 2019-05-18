# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import grpc
from concurrent import futures
import threading
import time
import connect_pb2
import connect_pb2_grpc
import scan_pb2
import scan_pb2_grpc


workerList={}
scanQueue={}
portaServidor="46000"

class ServerInit(connect_pb2_grpc.ConnectServicer):

    def start_server(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        connect_pb2_grpc.add_ConnectServicer_to_server(ServerInit(),server)
        server.add_insecure_port('[::]:{}'.format(portaServidor))

        server.start()
        print ('[*] Servidor Iniciado')

        try:
            while True:
                ipToScan=raw_input("Insira um ip : ")
                moduleToScan=raw_input("Insira o url de um modulo : ")
                tmp={ipToScan:moduleToScan}
                scanQueue.update(tmp) #TODO redistribuir o iprange
                for worker,avaiable in workerList.iteritems():
                    if avaiable == True:
                        ip,module=scanQueue.popitem()
                        sendScan(worker,ip,module)
                #time.sleep(60 * 60 * 24)

        except KeyboardInterrupt:
            server.stop(0)
            print('[*] A Encerrar o Servidor')

    def ConnectServer(self, request, context):
        ipWorker = request.WorkerIp
        portWorker = request.WorkerPort
        addrs=ipWorker+":"+portWorker
        tmp={str(addrs):True}
        workerList.update(tmp)
        print("\n[*] Nova Ligacao: "+addrs)

        result = {'Confirmation': True}
        return connect_pb2.HelloWorker(**result)

def sendScan(worker,range,module):
    channel = grpc.insecure_channel(worker) #TODO
    stub = scan_pb2_grpc.ScanStub(channel)
    message =scan_pb2.ScanRequest(IpRange=range,Modulo=module)
    return stub.ScanIp(message)


def main():
    curr_server = ServerInit()
    curr_server.start_server()
    print("[*] Acabou")

if __name__== "__main__":
    main()