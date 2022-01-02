import socket
import sys

from flush_file import flush_file
from tracert_util import init_udp_socket, init_icmp_socket, receive_packages


def tracert(destination_name):
    sys.stdout = flush_file(sys.stdout)
    address = ""

    try:
        address = socket.gethostbyname(destination_name)
    except socket.gaierror:
        print(f"Name or service {destination_name} not known, try again")
        exit(1)

    print(f"traceroute to {destination_name} ({address}), 30 hops max")
    port = 54377
    max_hops = 30
    ttl = 1

    while True:
        # udp socket is a sender socket
        udp_socket = init_udp_socket(ttl)
        # icmp socket is a receiver socket
        icmp_socket = init_icmp_socket(port)

        sys.stdout.write(" %d   " % ttl)
        udp_socket.sendto(bytes("", "utf-8"), (destination_name, port))

        curr_address = None
        curr_name = None
        finished = False

        curr_name, curr_address, finished = receive_packages(icmp_socket, curr_name, curr_address, finished)

        udp_socket.close()
        icmp_socket.close()

        if not finished:
            pass

        if curr_address is not None:
            curr_host = "%s (%s)" % (curr_name, curr_address)
        else:
            curr_host = ""
        sys.stdout.write("%s\n" % curr_host)

        ttl += 1
        if curr_address == address or ttl > max_hops:
            break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect number of input arguments, you should pass only one parameter\n")
        print(len(sys.argv))
        exit(1)
    tracert(sys.argv[1])
