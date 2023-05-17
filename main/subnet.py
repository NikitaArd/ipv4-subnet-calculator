"""
File contains class of subnet calculator
"""


class Subnet:
    """
    NOT NOW
    After creating an instance of class you can call instance which returns a tuple of (..., ..., ...)
    """
    def __init__(self, address, mask):
        self.address = address
        self.mask = mask
        self.net_address = []
        self.net_broadcast = []
        self.sum_hosts = 0

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


def main():
    address = input('IP Address: ')
    mask = input('Mask: ')

    subnet = Subnet(address, mask)

    print(subnet.address)
    print(subnet.mask)


if __name__ == '__main__':
    main()
