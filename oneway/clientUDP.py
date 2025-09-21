#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:51:57 2024

@author: widhi
"""

import socket

# Set up the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address (match serverUDP.py listening port 12345)
# Use docker compose service name for UDP server
server_address = ('udp-server', 12345)

# Send data to server
message = "Hello, UDP server2! nama saya Rahmat dari Brawijaya"
client_socket.sendto(message.encode('utf-8'), server_address)

# Receive response from server
data, server = client_socket.recvfrom(1024)
print(f"Received from server: {data.decode('utf-8')}")

# Close the socket
client_socket.close()
