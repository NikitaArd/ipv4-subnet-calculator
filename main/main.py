import tkinter as tk
import customtkinter as ctk

from subnet import Subnet

# TODO: Add button to switch dark/light theme
ctk.set_appearance_mode("system")


class App(ctk.CTk):

    def __init__(self):
        """
        Creating interface
        """

        # Main settings
        super().__init__()
        self.geometry("400x400")
        self.title("Addresses")
        self.resizable(False, False)

        # IPv4 input Label
        self.ip_label = ctk.CTkLabel(self, text='Enter IP')
        self.ip_label.pack(padx=5, pady=5)

        # IPv4 input
        self.ip_address_frame = ctk.CTkFrame(self)
        self.ip_address_frame.pack(after=self.ip_label)
        self.ip_address = self.__create_ip_input(frame=self.ip_address_frame)

        # Mask input Label
        self.mask_label = ctk.CTkLabel(self, text='Enter Mask')
        self.mask_label.pack(padx=5, pady=5)

        # Mask input
        self.mask_address_frame = ctk.CTkFrame(self)
        self.mask_address_frame.pack(after=self.mask_label)
        self.mask_address = self.__create_ip_input(frame=self.mask_address_frame)

        # Blank space just to separate IPv4 and MASK input
        ctk.CTkLabel(self, text='').pack(before=self.mask_label)

        # Start button
        self.start_button = ctk.CTkButton(self, text='Start')
        self.start_button.pack(padx=30, pady=30)

        # Output labels (net address, broadcast address, host count)
        self.net_address = ctk.CTkLabel(self, text='Net address: ')
        self.net_address.pack(after=self.start_button, pady=5)

        self.bd_address = ctk.CTkLabel(self, text='Broadcast address: ')
        self.bd_address.pack(after=self.net_address, pady=5)

        self.host_count = ctk.CTkLabel(self, text='Host count: ')
        self.host_count.pack(after=self.bd_address, pady=5)

    def __create_ip_input(self, frame):
        """
        Returns list of inputs (IPv4 or Mask depends on frame)
        """

        ip_input = list()
        for i in range(4):
            octet = ctk.CTkEntry(frame, width=40)
            octet.pack(side=tk.LEFT, padx=5, pady=5)

            if i != 3:
                dot = ctk.CTkLabel(frame, text='.')
                dot.pack(side=tk.LEFT)

            ip_input.append(octet)

        return ip_input


app = App()
app.mainloop()
