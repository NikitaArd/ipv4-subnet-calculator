import flet as ft
from subnet import Subnet


def main(page: ft.Page):
    page.title = 'Addresses'
    page.window_width = 600
    page.window_height = 510
    page.window_resizable = False

    def validate_octet(event):
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

    def render_calcs(event):
        user_address = ''.join([octet.value if octet.value else '0' for octet in ip_input])
        user_mask = ''.join([octet.value if octet.value else '0' for octet in mask_input])

        subnet = Subnet(user_address, user_mask)

    ip_label = ft.Text('Enter IP', text_align=ft.TextAlign.CENTER, size=18, weight=ft.FontWeight.W_600)
    ip_input = create_input_list()
    mask_label = ft.Text('Enter MASK', text_align=ft.TextAlign.CENTER, size=18, weight=ft.FontWeight.W_600)
    mask_input = create_input_list()
    start_button = ft.TextButton(text='Start', width=80, height=30, on_click=render_calcs)

    net_address = ft.Text('Net address: ')
    broadcast_address = ft.Text('Broadcast address: ')
    host_count = ft.Text('Host count')

    outputs = (net_address, broadcast_address, host_count)

    page.add(
        # ft.Column([
        #     ip_label,
        #     ft.Row([*ip_input], alignment=ft.MainAxisAlignment.CENTER),
        #     mask_label,
        #     ft.Row([*mask_input], alignment=ft.MainAxisAlignment.CENTER),
        # ])
        ft.Row([ip_label], alignment=ft.MainAxisAlignment.CENTER, ),
        ft.Row([*ip_input], alignment=ft.MainAxisAlignment.CENTER, spacing=6, height=70),
        ft.Row([mask_label], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([*mask_input], alignment=ft.MainAxisAlignment.CENTER, spacing=6, height=70),
        ft.Row([start_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Column([net_address, broadcast_address, host_count], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
    )

    page.update()


ft.app(target=main, view=ft.FLET_APP)