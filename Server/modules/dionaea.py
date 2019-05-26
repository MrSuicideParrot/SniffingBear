from yapsy.IPlugin import IPlugin
import socket

class FTPTest():
    """Name"""
    __name = "dionaea FTP Banner Test"

    """ Description """
    __description = "Test for service banner of dionaea"

    """ Port nedded on the test"""
    __port = [20, 21, 989, 990]

    @staticmethod
    def get_name():
        return FTPTest.__name

    @staticmethod
    def get_description():
        return FTPTest.__description

    @staticmethod
    def get_port():
        return FTPTest.__port

    @staticmethod
    def run(ip):
        banners = [
            b'220 DiskStation FTP server ready.\r\n'
        ]
        
        for j in FTPTest.__port:
            try:
                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                soc.settimeout(2)
                soc.connect((ip, j))

                max_length = len(banners[0])

                for i in banners:
                    if max_length < len(i):
                        max_length = len(i)

                r = soc.recv(max_length)
                soc.close()
                for i in banners:
                    if i in r:
                        return True  
            except socket.error: 
                pass
        return False
        


class Dionaea(IPlugin):

    """ List of tests """
    __test_list = [FTPTest]

    @staticmethod
    def get_test_list():
        return Dionaea.__test_list

    @staticmethod
    def get_port_list():
        port_list = set()

        for i in Dionaea.__test_list:
            port_list.update(i.get_port())
        return port_list

    @staticmethod
    def run(ip):
        list = []
        for i in Dionaea.__test_list:
            list.append(i.run(ip))
        return list
