import flet as ft
from subnet import Subnet

from collections import namedtuple


def main(page: ft.Page):
    """
    Main function of GUI interface
    """

    page.title = 'Addresses'
    page.window_width = 600
    page.window_height = 510
    page.window_resizable = False

    def validate_octet(event):
        """
        Calls whenever user presses any key entering the octet of IPv4 or Mask form
        """

        try:
            octet_value = int(event.data)
        except ValueError:
            # TODO: Add alert
            return
        octet_input = event.control

        if octet_value > 255:
            octet_input.value = '255'
            # ip_input[int(event.control['key']) + 1].focus()
        elif octet_value < 0:
            octet_input.value = '0'

        event.page.update()

    def create_input_list() -> list:
        """
        Creates a list of octets and dots between octets

        Output:
            [octet1, dot, octet2, dot, octet3, dot, octet4]
        """

        input_list = list()

        for i in range(4):
            octet = ft.TextField(value='',
                                 text_align=ft.TextAlign.CENTER,
                                 width=50,
                                 height=30,
                                 text_size=14,
                                 content_padding=0,
                                 on_change=validate_octet,
                                 )

            input_list.append(octet)

            if i != 3:
                dot = ft.Text('.', size=20)
                input_list.append(dot)

        return input_list

    def empty_to_zero():
        """
        Put 0 to empty octet in IPv4 and Mask forms
        """

        for octet in ip_input:
            if not octet.value:
                octet.value = '0'

        for octet in mask_input:
            if not octet.value:
                octet.value = '0'

    def get_calculations() -> namedtuple:
        """
        Returns a namedtuple which contains:
            `net_address`
            `net_broadcast`
            `sum_hosts`
        """

        user_address = ''.join([octet.value for octet in ip_input])
        user_mask = ''.join([octet.value for octet in mask_input])

        subnet = Subnet(user_address, user_mask)
        return subnet()

    def render_calculations(event):
        """
        Renders calculation from get_calculation on page
        """

        empty_to_zero()

        result = get_calculations()

        net_address.value = f'Net address: {result.net_address}'
        broadcast_address.value = f'Broadcast address: {result.net_broadcast}'
        host_count.value = f'Host count : {result.sum_hosts}'

        page.update()

    ip_label = ft.Text('Enter IP', text_align=ft.TextAlign.CENTER, size=18, weight=ft.FontWeight.W_600)
    ip_input = create_input_list()
    mask_label = ft.Text('Enter MASK', text_align=ft.TextAlign.CENTER, size=18, weight=ft.FontWeight.W_600)
    mask_input = create_input_list()
    start_button = ft.TextButton(text='Start', width=80, height=30, on_click=render_calculations)

    net_address = ft.Text('Net address: ')
    broadcast_address = ft.Text('Broadcast address: ')
    host_count = ft.Text('Host count :')

    outputs = (net_address, broadcast_address, host_count)

    page.add(
        ft.Column([
            ft.Container(content=ip_label, alignment=ft.alignment.center, margin=ft.margin.only(0, 35, 0, 0)),
            ft.Row([*ip_input], alignment=ft.MainAxisAlignment.CENTER, spacing=6, height=70),
            ft.Container(content=mask_label, alignment=ft.alignment.center),
            ft.Row([*mask_input], alignment=ft.MainAxisAlignment.CENTER, spacing=6, height=70),
            ft.Container(content=start_button, alignment=ft.alignment.center),
            ft.Container(
                content=ft.Column([net_address, broadcast_address, host_count],
                                  alignment=ft.MainAxisAlignment.CENTER,
                                  spacing=8),
                alignment=ft.alignment.center,
                margin=20,
            )
        ], alignment=ft.MainAxisAlignment.CENTER),
    )

    page.update()


ft.app(target=main, view=ft.FLET_APP)