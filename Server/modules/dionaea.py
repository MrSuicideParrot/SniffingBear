from yapsy.IPlugin import IPlugin
import socket

class FTPTest():
    """Name"""
    __name = "dionaea FTP Banner Test"

    """ Description """
    __description = "Test for service banner of dionaea"

    """ Port nedded on the test"""
    __port = 20

    @staticmethod
    def get_name():
        return PortTest.__name

    @staticmethod
    def get_description():
        return PortTest.__description

    @staticmethod
    def get_port():
        return PortTest.__port

    @staticmethod
    def run(ip):
        banners = [
            b'220 DiskStation FTP server ready.\r\n'
        ]

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
                soc.settimeout(2)
                soc.connect((ip, FTPTest.__port))

                max_length = len(banners[0])

                for i in banners:
                    if max_length < len(i):
                        max_length = len(i)

                r = soc.recv(max_length)
                for i in banners:
                    if i in r:
                        return True

                return False
        except socket.timeout: 
            print("conexao deu timeout")


class Dionaea(IPlugin):

    """ List of tests """
    __test_list = [FTPTest]

    @staticmethod
    def get_test_list():
        return Module.__test_list

    @staticmethod
    def get_port_list():
        port_list = set()

        for i in Module.__test_list:
            port_list.add(i.get_port())

    @staticmethod
    def run(ip):
        for i in Dionaea.__test_list:
            i.run(ip)
