from yapsy.IPlugin import IPlugin
import socket
#from pwnlib.tubes.ssh import ssh
#from hashlib import sha256


class VersionSpecificKippo:
    """Name"""
    __name = "Kippo Error Message Bug Test"

    """ Description """
    __description = "Tests presence of an obsolte version of kippo"

    """ Port nedded on the test"""
    __port = [22, 2222]

    @staticmethod
    def get_name():
        return VersionSpecificKippo.__name

    @staticmethod
    def get_description():
        return VersionSpecificKippo.__description

    @staticmethod
    def get_port():
        return VersionSpecificKippo.__port

    @staticmethod
    def run(ip):
        for j in VersionSpecificKippo.__port:
            response = ""
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((ip, j))
                banner = s.recv(1024)
                s.send(b'\n\n\n\n\n\n\n\n')
                response = s.recv(1024)
                s.close()
            except socket.error:
                continue

            if '168430090' in response or 'bad packet length' in response:
                return True

        return False
"""
class KippoShadow:
    
    __name = "Kippo shadow verifie"

    
    __description = "Tests presence of kippo"


    __port = [22, 2222]

    @staticmethod
    def get_name():
        return KippoShadow.__name

    @staticmethod
    def get_description():
        return KippoShadow.__description

    @staticmethod
    def get_port():
        return KippoShadow.__port

    @staticmethod
    def run(ip):
        for j in KippoShadow.__port:
            try:
                s = ssh('root', ip, j, '123456')

                data = s.download_data('/etc/shadow')
                s.close()

                print(sha256(data).hexdigest())

                return True
                
            except Exception as e:
                print(e)
                continue

        return False
"""
class Kippo(IPlugin):

    """ List of tests """
    __test_list = [VersionSpecificKippo]

    @staticmethod
    def get_test_list():
        return Kippo.__test_list

    @staticmethod
    def get_port_list():
        port_list = set()

        for i in Kippo.__test_list:
            port_list.update(i.get_port())
        return port_list

    @staticmethod
    def run(ip):
        result = []
        for i in Kippo.__test_list:
            result.append(i.run(ip))
        return result

if __name__ == "__main__":
    ip = "172.17.0.3"
    print(Kippo.run(ip))