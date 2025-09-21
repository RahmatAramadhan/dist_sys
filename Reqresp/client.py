#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 14:09:52 2024

@author: widhi
"""

import socket

def client_program():
    client_socket = socket.socket()  
    # Use docker compose service DNS name
    client_socket.connect(('reqresp-server', 2222))  

    
    while True: 
        message = input("Enter message(type 'exit to exit command'): ")
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024).decode()
        print("Received from server:", data)

        if message.lower().strip() == "exit":
            print("Connection closed.")
            break
    
    client_socket.close()

if __name__ == '__main__':
    client_program()
