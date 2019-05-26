from yapsy.IPlugin import IPlugin
import socket

def connectToSSH(host, port):
    socket.setdefaulttimeout(5)
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.connect((host, port))
    sockfd.recv(1024)        

    return sockfd

class DefaultSSHVersion:
    """Name"""
    __name = "DefaultSSHVersion  cowrie"

    """ Description """
    __description = "Test for default ssh version"

    """ Port nedded on the test"""
    __port = [2222]

    @staticmethod
    def get_name():
        return DefaultSSHVersion.__name

    @staticmethod
    def get_description():
        return DefaultSSHVersion.__description

    @staticmethod
    def get_port():
        return DefaultSSHVersion.__port

    @staticmethod
    def run(ip):
        DEFAULT_KIPPOCOWRIE_BANNERS = ["SSH-2.0-OpenSSH_5.1p1 Debian-5", "SSH-1.99-OpenSSH_4.3", "SSH-1.99-OpenSSH_4.7",
                                       "SSH-1.99-Sun_SSH_1.1", "SSH-2.0-OpenSSH_4.2p1 Debian-7ubuntu3.1",
                                       "SSH-2.0-OpenSSH_4.3", "SSH-2.0-OpenSSH_4.6", "SSH-2.0-OpenSSH_5.1p1 Debian-5",
                                       "SSH-2.0-OpenSSH_5.1p1 FreeBSD-20080901", "SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu5",
                                       "SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu6", "SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu7",
                                       "SSH-2.0-OpenSSH_5.5p1 Debian-6", "SSH-2.0-OpenSSH_5.5p1 Debian-6+squeeze1",
                                       "SSH-2.0-OpenSSH_5.5p1 Debian-6+squeeze2", "SSH-2.0-OpenSSH_5.8p2_hpn13v11 FreeBSD-20110503",
                                       "SSH-2.0-OpenSSH_5.9p1 Debian-5ubuntu1", "SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2",
                                       "SSH-2.0-OpenSSH_5.9", "SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2"]

        for p in DefaultSSHVersion.__port:
            try:
                socket.setdefaulttimeout(5)
                sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sockfd.connect((ip, p))
                banner = sockfd.recv(1024)[:-2]

                if banner in DEFAULT_KIPPOCOWRIE_BANNERS:
                    return True

            except Exception:
                pass
        
        return False
    

class ProbeSpacerPacketCorrupt:
    """Name"""
    __name = "Test packet handling Cowrie"

    """ Description """
    __description = "Cowrie"

    """ Port nedded on the test"""
    __port = [2222]

    @staticmethod
    def get_name():
        return ProbeSpacerPacketCorrupt.__name

    @staticmethod
    def get_description():
        return ProbeSpacerPacketCorrupt.__description

    @staticmethod
    def get_port():
        return ProbeSpacerPacketCorrupt.__port

    @staticmethod
    def run(ip):
        for p in ProbeSpacerPacketCorrupt.__port:
            try:
                s = connectToSSH(ip, p)
                s.sendall("SSH-2.0-OpenSSH\n\n\n\n\n\n\n\n\n\n")
                
                response = s.recv(1024)
                s.close()

                if 'corrupt' in response or 'mismatch' in response:
                    return True

            except Exception:
                pass

        return False


class DoubleBanner:
    """Name"""
    __name = "Double banner Cowrie"

    """ Description """
    __description = "Cowrie Double banner test"

    """ Port nedded on the test"""
    __port = [2222]

    @staticmethod
    def get_name():
        return DoubleBanner.__name

    @staticmethod
    def get_description():
        return DoubleBanner.__description

    @staticmethod
    def get_port():
        return DoubleBanner.__port

    @staticmethod
    def run(ip):
        for p in DoubleBanner.__port:
            try:
                s = connectToSSH(ip, p)
                s.sendall("SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2\nSSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2\n")
                response = s.recv(1024)
                s.close()

                if "corrupt" in response or "mismatch" in response:
                    return True
            except Exception:
                pass
        
        return False


class Cowrie(IPlugin):
    """ List of tests """
    __test_list = [DefaultSSHVersion, DoubleBanner, ProbeSpacerPacketCorrupt]

    @staticmethod
    def get_test_list():
        return Cowrie.__test_list

    @staticmethod
    def get_port_list():
        port_list = set()

        for i in Cowrie.__test_list:
            port_list.update(i.get_port())
        return port_list

    @staticmethod
    def run(ip):
        result = []
        for i in Cowrie.__test_list:
            result.append(i.run(ip))
        return result

if __name__ == "__main__":
    ip = "172.17.0.2"
    print(Cowrie.run(ip))