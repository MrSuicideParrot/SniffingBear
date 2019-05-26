# -*- coding: utf-8 -*-

from concurrent import futures
import grpc
from cmd import Cmd
from GrpcProto import scan_pb2
from GrpcProto import scan_pb2_grpc
import argparse

serverIp='localhost'
serverPort="46000"

class MyPrompt(Cmd):
    prompt = 'sb > '
    intro = "Welcome to Sniffing Bear! The place to find honey\nType ? to list commands"
    def do_exit(self, inp):
        print("Bye :)")
        return True

    def help_exit(self):
        print("DESCRIPTION\n\tExits the current shell")

    def do_list(self, inp):
        channel = grpc.insecure_channel(serverIp+":"+serverPort)
        stub = scan_pb2_grpc.ScanStub(channel)
        message =scan_pb2.ModulesRequest(RequestModulesName="GetAllModules")
        resp=stub.ListModules(message)
        channel.close()
        print("Listing current modules:")
        for module in resp.ModulesNames:
            print("\t"+module)



    def help_list(self):
        print("DESCRIPTION\n\tWill list all of the current honeypot modules\nUsage: list")

    def help_description(self):
        print("DESCRIPTION\n\tBrief explanation about the module in question\nUsage: description <moduleName>")

    def do_description(self,module):
        channel = grpc.insecure_channel(serverIp+":"+serverPort)
        stub = scan_pb2_grpc.ScanStub(channel)
        message =scan_pb2.DescriptionRequest(Modulo=module)
        resp=stub.ScanDescription(message)
        channel.close()
        if resp.Description == "ERROR":
            print("Module not found\nType 'help description' to see documentation")
        else:
            print("Description: "+resp.Description)

    def do_scan(self,args):
        arg = args.split()
        if len(arg) > 3:
            print("*** Invalid number of arguments\nType 'help scan' to see documentation")
            return

        ipRange=arg[0]
        module=arg[1]
        ports="all"
        if len(arg)==3:
            ports=arg[2]
        print(ports)
        channel = grpc.insecure_channel(serverIp+":"+serverPort)
        stub = scan_pb2_grpc.ScanStub(channel)
        message =scan_pb2.ScanRequest(IpRange=ipRange,Modulo=module)
        resp=stub.ScanIp(message)
        channel.close()
        if resp.Resposta == "ERROR":
            print("Invalid arguments\nType 'help scan' to see documentation")
            return
        print(resp.Resposta)


    def help_scan(self):
        print("DESCRIPTION\n\tScan either a range of ip addresses or just one specific ip with a module.\n\tYou can run all the modules by specifying 'all' in the <moduleName> argument.\nUsage: scan <IP> <moduleName>")

    do_EOF = do_exit

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ServerIp", nargs='?', default="localhost")
    parser.add_argument("ServerPort", nargs='?', default="46000")
    args = parser.parse_args()
    
    serverIp=args.ServerIp
    serverPort=args.ServerPort
    
    MyPrompt().cmdloop()
    
    

if __name__== "__main__":
    main()