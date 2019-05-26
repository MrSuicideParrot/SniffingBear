from yapsy.IPlugin import IPlugin

import requests
import string
import random
import socket
import threading

"""
INDEX = re.compile(r'(/index.html|/)')
RFI_ATTACK = re.compile(r'.*((http(s){0,1}|ftp(s){0,1}):).*', re.IGNORECASE)
LFI_ATTACK = re.compile(r'.*(/\.\.)*(home|proc|usr|etc)/.*')
LFI_FILEPATH = re.compile(r'((\.\.|/).*)')
XSS_ATTACK = re.compile(r'.*<(.|\n)*?>')
CMD_ATTACK = re.compile(
    r'.*[^A-z:./]'
    r'(alias|cat|cd|cp|echo|exec|find|for|grep|ifconfig|ls|man|mkdir|netstat|ping|ps|pwd|uname|wget|touch|while)'
    r'([^A-z:./]|\b)')
PHP_CODE_INJECTION = re.compile(r'.*(;)*(echo|system|print|phpinfo)(\(.*\)).*')
CRLF_ATTACK = re.compile(r'.*(\r\n).*')
REMOTE_FILE_URL = re.compile(r'(.*(http(s){0,1}|ftp(s){0,1}):.*)')
WORD_PRESS_CONTENT = re.compile(r'/wp-content/.*')
HTML_TAGS = re.compile(r'.*<(.*)>.*')
QUERY = re.compile(r'.*\?.*=')

"""


def randomString(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits)
                   for _ in range(n))


class Ret:
    def __init__(self):
        self.result = False

    def get_result(self):
        return self.result

    def set_result(self):
        self.result = True


def simpleServerHttp(target, ret):
    port = random.randint(1025, 7777)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(("0.0.0.0", port))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

    s.settimeout(3)
    try:
        s.listen(2)
        con, = s.accept()
        data = con.recv(4096)

        if target in data and "aiohttp" in data:
            ret.set_result()

        con.close()

    except socket.timeout:
        pass

    finally:
        s.close()


class DefaultNginxVersion():
    """Name"""
    __name = "Snare Nginx Version"

    """ Description """
    __description = "Test for default nginx version"

    """ Port nedded on the test"""
    __port = [80]

    @staticmethod
    def get_name():
        return DefaultNginxVersion.__name

    @staticmethod
    def get_description():
        return DefaultNginxVersion.__description

    @staticmethod
    def get_port():
        return DefaultNginxVersion.__port

    @staticmethod
    def run(ip):
        r = requests.get("http://%s/" % (ip))

        if r.headers['Server'] == 'nginx/1.3.8':
            return True

        return False


class RFIteste():
    """Name"""
    __name = "RFI detect from Tanner"

    """ Description """
    __description = "Tanner identifies"

    """ Port nedded on the test"""
    __port = [80]

    @staticmethod
    def get_name():
        return RFIteste.__name

    @staticmethod
    def get_description():
        return RFIteste.__description

    @staticmethod
    def get_port():
        return RFIteste.__port

    @staticmethod
    def get_ip():
        return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                              if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
                                                                    s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET,
                                                                                                                           socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

    @staticmethod
    def run(ip):
        path = randomString(random.randrange(10))
        args = randomString(random.randrange(5))
        ident = randomString(random.randrange(10))
        myIp = RFIteste.get_ip()

        resp = Ret()

        t = threading.Thread(
            name="Sever", target=simpleServerHttp, args=(ident, resp))
        t.start()

        requests.get("http://%s/%s?%s=http://%s/%s" %
                     (ip, path, args, myIp, ident))

        t.join()

        return resp.get_result()


class PHPteste():
    """Name"""
    __name = "PHP injection from Tanner"

    """ Description """
    __description = "Tanner PHP injection test"

    """ Port nedded on the test"""
    __port = [80]

    @staticmethod
    def get_name():
        return PHPteste.__name

    @staticmethod
    def get_description():
        return PHPteste.__description

    @staticmethod
    def get_port():
        return PHPteste.__port

    @staticmethod
    def run(ip):
        path = randomString(random.randrange(10))
        args = randomString(random.randrange(5))
        r = requests.get("http://%s/%s" % (ip, path),
                         params={args: 'echo(system("uptime"))'})

        if r.status_code == 200 and len(r.text) == 0:
            return True
        else:
            return False


class SQLiteste():
    """Name"""
    __name = "SQLi detect from Tanner"

    """ Description """
    __description = "Tanner identifies"

    """ Port nedded on the test"""
    __port = [80]

    @staticmethod
    def get_name():
        return SQLiteste.__name

    @staticmethod
    def get_description():
        return SQLiteste.__description

    @staticmethod
    def get_port():
        return SQLiteste.__port

    @staticmethod
    def run(ip):
        path = randomString(random.randrange(10))
        args = randomString(random.randrange(5))
        r = requests.get("http://%s/%s" % (ip, path),
                         params={args: '1 UNION SELECT 1,2,3,4'})

        response = ['You have an error in your SQL syntax; check the manual',
                    'that corresponds to your MySQL server version for the',
                    'right syntax to use near  at line 1']

        resp = True

        for i in response:
            resp = resp and (i in response)
            print resp

        return resp


class Tanner(IPlugin):
    """ List of tests """
    __test_list = [DefaultNginxVersion, PHPteste, SQLiteste, RFIteste, ]

    @staticmethod
    def get_test_list():
        return Tanner.__test_list

    @staticmethod
    def get_port_list():
        port_list = set()

        for i in Tanner.__test_list:
            port_list.update(i.get_port())
        return port_list

    @staticmethod
    def run(ip):
        result = []
        for i in Tanner.__test_list:
            result.append(i.run(ip))
        return result
