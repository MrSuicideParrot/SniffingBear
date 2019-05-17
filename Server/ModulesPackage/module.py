from yapsy.IPlugin import IPlugin


class Module(IPlugin):
    """ List of tests """
    __test_list = []

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
        raise NotImplementedError

