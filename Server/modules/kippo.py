from yapsy.IPlugin import IPlugin
import socket


class VersionSpecificKippo():
    """Name"""
    __name = "Kippo Error Message Bug Test"

    """ Description """
    __description = "Tests presence of an obsolte version of kippo"

    """ Port nedded on the test"""
    __port = [23, 992]

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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)

        for j in VersionSpecificKippo.__port:
            response = ""
            try:
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
