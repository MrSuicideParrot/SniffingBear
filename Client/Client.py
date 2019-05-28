# -*- coding: utf-8 -*-

from concurrent import futures
import grpc
from cmd import Cmd
from GrpcProto import scan_pb2
from GrpcProto import scan_pb2_grpc
import argparse
import code
import json
from termcolor import colored

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
        if len(arg) > 3 or len(arg)<2:
            print("*** Invalid number of arguments\nType 'help scan' to see documentation")
            return

        ipRange=arg[0]
        module=arg[1]
        ports="all"
        if len(arg)==3:
            ports=arg[2]
            if "-p" not in ports:
                print("*** Invalid arguments\nType 'help scan' to see documentation")
                return
            ports=ports.replace("-p", "")
                
        
        channel = grpc.insecure_channel(serverIp+":"+serverPort)
        stub = scan_pb2_grpc.ScanStub(channel)
        message =scan_pb2.ScanRequest(IpRange=ipRange,Modulo=module,Ports=ports)
        resp = stub.ScanIp(message)
        channel.close()
        if resp.Resposta == "ERROR":
            print("Invalid arguments\nType 'help scan' to see documentation")
            return
        if "No matching ports" in resp.Resposta:
            print("There is no port: "+ports+ " in module "+module)
            return
        
        printOutput(resp.Resposta)
        #code.interact(local=locals())


    def help_scan(self):
        print("DESCRIPTION\n\tScan either a range of ip addresses or just one specific ip with a module.\n\tYou can run all the modules by specifying 'all' in the <moduleName> argument.\nTo run the scan on custom ports, specify the ports after '-p' and separate them with a comma\nUsage: scan <IP> <moduleName> -p<ports>")


    def do_customScan(self,args):
        arg = args.split()
        
        if len(arg) > 2:
            print("*** Invalid number of arguments\nType 'help scan' to see documentation")
            return
        
        ipRange=arg[0]
        moduleUrl=arg[1]
        channel = grpc.insecure_channel(serverIp+":"+serverPort)
        stub = scan_pb2_grpc.ScanStub(channel)
        message =scan_pb2.CustomScanRequest(IpRange=ipRange,ModuloUrl=moduleUrl)
        resp = stub.CustomScan(message)
        channel.close()
        #if resp.Resposta == "ERROR":
        #    print("Invalid arguments\nType 'help scan' to see documentation")
        #    return
        printOutput(resp.RespostaCustomScan)
        
        
    def help_customScan(self):
        print("DESCRIPTION\n\tScan either a range of ip addresses or just one specific ip with a custom module.\n\tPlease provide a module url in the <moduleUrl> argument.\nUsage: customScan <IP> <moduleUrl>")

    
    do_EOF = do_exit

def printOutput(resp):
    printList=[]
    if ";" in resp:
        resp=resp.split(';')
        for x in resp:
            x=json.loads(x)
            printList.append(x)
    else:
        resp=json.loads(resp)
        if resp=={}:
            print("No honeypot found")
            return
        printList.append(resp)
        
    for respPrint in printList:
        if respPrint=={}:
            #print("No honeypot "+module)
            continue 
        for key,value in respPrint.iteritems():
            print(str(key))
            falsos=0
            verdades=0
            for lista in value:
                for subkey,subvalue in lista.iteritems():
                    if subvalue == False:
                        print("\t"+str(subkey)+" "+colored(str(subvalue),'red'))
                        falsos=falsos+1
                    else:
                        print("\t"+str(subkey)+" "+colored(str(subvalue),'green'))
                        verdades=verdades+1
                prob=verdades/verdades+falsos
                if prob > 0.7:
                    #prob=prob*100
                    print("\t"+colored("Honeypot Probability ","yellow")+" "+ colored(prob*100,'green') +colored('%','green'))
                elif prob > 0.4:
                    prob=prob*100
                    print("\t"+colored("Honeypot Probability ","yellow")+" "+ colored(prob,'yellow') +colored('%','yellow'))
                else:
                    prob=prob*100
                    print("\t"+colored("Honeypot Probability ","yellow")+" "+ colored(prob,'red') +colored('%','red'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ServerIp", nargs='?', default="localhost")
    parser.add_argument("ServerPort", nargs='?', default="46000")
    args = parser.parse_args()
    
    global serverIp
    global serverPort

    serverIp=args.ServerIp
    serverPort=args.ServerPort
    
    MyPrompt().cmdloop()
    
    

if __name__== "__main__":
    main()