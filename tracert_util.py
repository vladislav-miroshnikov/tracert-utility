import socket

__all__ = ["init_udp_socket", "init_icmp_socket", "receive_packages"]

import struct
import sys


def init_udp_socket(ttl: int) -> socket.socket:
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    return udp_socket


def init_icmp_socket(port: int) -> socket.socket:
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    timeout = struct.pack("ll", 5, 0)
    icmp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
    icmp_socket.bind(("", port))
    return icmp_socket


def receive_packages(icmp_socket: socket.socket, curr_address, curr_name, finished):
    tries = 3
    while not finished and tries > 0:
        try:
            _, curr_address = icmp_socket.recvfrom(512)
            finished = True
            curr_address = curr_address[0]
            try:
                curr_name = socket.gethostbyaddr(curr_address)[0]
            except socket.error:
                curr_name = curr_address
        except socket.error:
            tries -= 1
            sys.stdout.write("* ")
    return curr_name, curr_address, finished
