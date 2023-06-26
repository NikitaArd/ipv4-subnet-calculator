"""
File contains class of subnet calculator
"""

from collections import namedtuple


class Subnet:
    """
    After creating an instance of class you can call instance which returns a tuple of
    (subnet address, broadcast address, max host count)
    """

    def __init__(self, address, mask):
        self.address = address
        self.mask = mask
        self.net_address = []
        self.net_broadcast = []
        self.sum_hosts = 0

        self.result = namedtuple('result', ['net_address', 'net_broadcast', 'sum_hosts'])

        self.__calculate()

    def __call__(self):
        return self.result('.'.join(self.net_address), '.'.join(self.net_broadcast), self.sum_hosts)

    @property
    def address(self):
        """
        IP address Getter
        """
        return self._address

    @address.setter
    def address(self, address):
        """
        IP address Setter
        """
        fted_address = address.split('.')

        if len(fted_address) != 4:
            raise ValueError('Enter IPv4 address')

        for octet in fted_address:
            if 255 < int(octet) < 0:
                raise ValueError('Octet of IPv4 address must be in [0,255]')

        self._address = fted_address

    @property
    def mask(self):
        """
        Mask Getter
        """
        return self._mask

    @mask.setter
    def mask(self, mask):
        """
        Mask Setter
        """

        # TODO: Add mask validator of preventing entering an octet which is less then the previous octet
        #  (ex. 255.255.128.192 , 255.255.0.192, 255.0.128.0 )

        fted_mask = mask.split('.')

        if len(fted_mask) != 4:
            raise ValueError('Enter IPv4 address')

        for octet in fted_mask:
            if int(octet) not in [0, 128, 192, 224, 240, 248, 252, 254, 255]:
                raise ValueError('Entered invalid octet of mask')

        self._mask = fted_mask

    @staticmethod
    def __dec2bin(address_list: list, *, rev: bool = False) -> list:
        """
        Converting DEC IP address ( list ) to BIN IP address ( list )

        rev = False -> DEV to BIN
        rev = True -> BIN to DEC
        """

        # TODO: Simplify and improve readability of this method

        if rev:
            return [str(int(x, base=2)) for x in address_list]
        bin_address = list()
        for x in address_list:
            x = bin(int(x))[2:]
            if len(x) < 8:
                # ex 101 -> 00000101
                x = '0' * (8 - len(x)) + x
            bin_address.append(x)

        return bin_address

    @staticmethod
    def __get_sum_octets(address1: list, address2: list) -> list:
        """
        Returns sum of every octet of address1 and address2
        """

        octet = 0
        octet_sum = list()
        while octet < 4:
            octet_sum.append(str(int(address1[octet]) + int(address2[octet])))
            octet += 1

        return octet_sum

    def __get_invert_mask(self) -> list:
        """
        Method returns invert BIN representation of mask

        ex.
        -> 11111111.11111111.00000000.000000000
        <- 00000000.00000000.11111111.111111111

        """

        invert = {'0': '1', '1': '0'}
        invert_mask = []
        for octet in self.__dec2bin(self.mask):
            invert_mask.append(''.join([invert[char] for char in octet]))

        return self.__dec2bin(invert_mask, rev=True)

    def __get_short_mask(self) -> int:
        """
        Returns short representation of mask

        ex.
        255.255.255.0 -> 24
        """

        bin_mask = self.__dec2bin(self.mask)
        return sum([int(x) for x in ''.join(bin_mask)])

    def __set_subnet_address(self):
        """
        Sets subnet address to class variable
        """

        bin_address_list = self.__dec2bin(self.address)
        bin_mask = self.__dec2bin(self.mask)

        octet = 0
        net_address = []
        while octet < 4:
            new_octet = str()
            for key, char in enumerate(bin_address_list[octet]):
                new_octet += str(int(bin_mask[octet][key]) * int(char))
            net_address.append(new_octet)

            octet += 1

        self.net_address = self.__dec2bin(net_address, rev=True)

    def __set_subnet_broadcast(self):
        """
        Sets subnet broadcast address to class variable
        """

        self.__set_subnet_address()
        invert_mask = self.__get_invert_mask()

        self.net_broadcast = self.__get_sum_octets(self.net_address, invert_mask)

    def __set_hosts_count(self):
        """
        Sets subnet host count to class variable
        """

        short_mask = self.__get_short_mask()

        self.sum_hosts = 2**(32-short_mask) - 2

    def __calculate(self):
        """
        Dispatch method of __set_subnet_address, __set_subnet_broadcast, __set_hosts_count
        """

        self.__set_subnet_address()
        self.__set_subnet_broadcast()
        self.__set_hosts_count()


def main():
    address = input('IP Address: ')
    mask = input('Mask: ')

    subnet = Subnet(address, mask)

    print(subnet())


if __name__ == '__main__':
    main()
