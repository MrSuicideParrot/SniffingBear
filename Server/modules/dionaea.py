from yapsy.IPlugin import IPlugin
import socket

class FTPTest(IPlugin):
    """Name"""
    __name = "dionaea FTP Banner Test"

    """ Description """
    __description = "Test for service banner of dionaea"

    """ Port nedded on the test"""
    __port = 20

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
