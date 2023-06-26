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

        octet_input = event.control

        try:
            render_default_labels()
            if not event.data:
                return
            octet_value = int(event.data)
        except ValueError:

            if octet_input in ip_input:
                render_error_message_on_label(ip_label, 'Enter a digit')
            elif octet_input in mask_input:
                render_error_message_on_label(mask_label, 'Enter a digit')

            return

        if octet_value > 255:
            octet_input.value = '255'
            # ip_input[int(event.control['key']) + 1].focus()
        elif octet_value < 0:
            octet_input.value = '0'

        event.page.update()

    def render_error_message_on_label(label: ft.Text, error_message: str):
        """
        Changes text and color of label and blocks  ( usage only for errors )
        """

        label.value = error_message
        label.color = ft.colors.RED
        start_button.disabled = True

        page.update()

    def render_default_labels():
        """
        Reset form labels and enables start button
        """

        ip_label.value = default_ip_label
        ip_label.color = ft.colors.BLACK

        mask_label.value = default_mask_label
        mask_label.color = ft.colors.BLACK

        start_button.disabled = False

        page.update()

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

        try:
            result = get_calculations()
        except ValueError:
            render_error_message_on_label(mask_label, 'Invalid Mask')
            return

        net_address.value = f'Net address: {result.net_address}'
        broadcast_address.value = f'Broadcast address: {result.net_broadcast}'
        host_count.value = f'Host count : {result.sum_hosts}'

        page.update()

    # Creating IPv4 form
    default_ip_label = 'Enter IP'
    ip_label = ft.Text(default_ip_label, text_align=ft.TextAlign.CENTER, size=18, weight=ft.FontWeight.W_600)
    ip_input = create_input_list()

    # Creating Mask form
    default_mask_label = 'Enter MASK'
    mask_label = ft.Text(default_mask_label, text_align=ft.TextAlign.CENTER, size=18, weight=ft.FontWeight.W_600)
    mask_input = create_input_list()

    start_button = ft.TextButton(text='Start', width=90, height=40, on_click=render_calculations,
                                 style=ft.ButtonStyle(bgcolor={ft.MaterialState.DEFAULT: ft.colors.BLUE_50}))

    net_address = ft.Text('Net address: ')
    broadcast_address = ft.Text('Broadcast address: ')
    host_count = ft.Text('Host count: ')

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
