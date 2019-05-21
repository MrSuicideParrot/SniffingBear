# -*- coding: utf-8 -*-

from concurrent import futures
import grpc
from cmd import Cmd
from GrpcProto import scan_pb2
from GrpcProto import scan_pb2_grpc

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
            print("Module not found\nTry using description <moduleName>")
        else:
            print("Description: "+resp.Description)

    do_EOF = do_exit

def main():
    MyPrompt().cmdloop()

if __name__== "__main__":
    main()