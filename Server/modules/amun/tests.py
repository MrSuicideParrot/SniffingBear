from ModulesPackages import PortTest
from pwnlib.tubes import remote

class FTPTest(PortTest):
    """Name"""
    __name = "amun FTP Banner Test"

    """ Description """
    __description = "Test for service banner of amun"

    """ Port nedded on the test"""
    __port = 20

    @staticmethod
    def run(ip):
        banners = [
            '220 Welcome to my FTP Server\r\n'
        ]

        r = remote(ip, FTPTest.__port)
        r.recvline()

        for i in banners:
            if i in r:
                return True

        return False