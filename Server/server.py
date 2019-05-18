
import grpc
from concurrent import futures
import threading
import time
import connect_pb2
import connect_pb2_grpc
import scan_pb2
import scan_pb2_grpc

workerList=[]
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
                #time.sleep(60 * 60 * 24)
                if(len(workerList)>0 ):
                    EnviarScans() #TODO
        except KeyboardInterrupt:
            server.stop(0)
            print('[*] A Encerrar o Servidor')

    def ConnectServer(self, request, context):
        ipWorker = request.WorkerIp
        portWorker = request.WorkerPort
        addrs=ipWorker+":"+portWorker

        workerList.append(addrs)
        print("[*] Nova Ligacao: "+addrs)

        result = {'Confirmation': True}
        return connect_pb2.HelloWorker(**result)

def scanSingleIp(IptoScan):
    channel = grpc.insecure_channel(workerList[0]) #TODO
    print(grpc.ChannelConnectivity(channel))
    stub = scan_pb2_grpc.ScanStub(channel)
    message =scan_pb2.ScanRequest(Ip=IptoScan)
    return stub.ScanIp(message)

def EnviarScans():
    ipToScan=input("Insira um ip : ")
    scanSingleIp(str.encode(str(ipToScan)))


def main():
    curr_server = ServerInit()
    curr_server.start_server()


if __name__== "__main__":
    main()