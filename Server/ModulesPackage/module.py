from yapsy.IPlugin import IPlugin


class Module(IPlugin):
    """ List of tests """
    __test_list = []

    @staticmethod
    def get_test_list():
        return Module.__test_list

    @staticmethod
    def run():
        raise NotImplementedError