class PortTest:
    """Name"""
    __name = ""

    """ Description """
    __description = ""

    """ Port nedded on the test"""
    __port = 42

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
        raise NotImplementedError