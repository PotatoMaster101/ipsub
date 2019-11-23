#!/usr/bin/env python3
###############################################################################
# Put IP and port into strings based on network interfaces.
#
# Author: PotatoMaster101
# Date:   23/11/2019
###############################################################################

import argparse
import netifaces

def get_args():
    """Returns the user arguments.

    Returns:
        The user arguments.
    """
    ret = argparse.ArgumentParser(description="IP and port substitution.")
    ret.add_argument("input", nargs="+", help="string to substitute")
    ret.add_argument("-i", "--interface", type=str, default="", dest="iface",
            help="network interface to use")
    ret.add_argument("-p", "--port", type=int, default=9999, dest="port",
            help="port number to substitute, default to 9999")
    ret.add_argument("-ips", "--ip-sub", type=str, default="IP", dest="ipsub",
            help="string to substitute with IP address, default to IP")
    ret.add_argument("-ps", "--port-sub", type=str, default="PT", dest="ptsub",
            help="string to substitute with port, default to PT")
    ret.add_argument("-subs", "--sub-space", action="store_true", dest="subsp",
            help="output will have space replaced with ${IFS}")
    ret.add_argument("-ns", "--no-space", action="store_true", dest="nosp",
            help="output will have space removed")
    ret.add_argument("-v", "--verbose", action="store_true", dest="verb",
            help="more verbose output")
    return ret

def get_good_iface():
    """Returns the first good non-loopback interface.

    Returns:
        The first non-loopback interface. None if not found.
    """
    ifaces = netifaces.interfaces()
    for i in ifaces:
        addr = netifaces.ifaddresses(i)
        if (i == "lo") or (netifaces.AF_INET not in addr):
            continue        # make sure interface is up, skip if not
        return i
    return None

def get_iface(prefer=None):
    """Checks and returns the prefered interface.

    Args:
        prefer: The preferred network interface to use.

    Returns:
        The preferred network interface, or a non-loopback network interface
        if the preferred interface is invalid.
    """
    ifaces = netifaces.interfaces()
    if prefer not in ifaces:
        if prefer is not None:
            print("[-] Interface is invalid, getting a valid interface.")
        return get_good_iface()

    addr = netifaces.ifaddresses(prefer)
    if netifaces.AF_INET not in addr:
        print("[-] Interface is invalid, getting a valid interface.")
        return get_good_iface()
    return prefer

def get_iface_ip(iface):
    """Returns the IP of the specified interface.

    Args:
        iface: The interface to retrieve the IP.

    Returns:
        The IP address of the specified interface.
    """
    return netifaces.ifaddresses(iface)[netifaces.AF_INET][0]["addr"]

if __name__ == "__main__":
    args = get_args().parse_args()
    iface = get_good_iface() if not args.iface else get_iface(args.iface)
    if iface == None:
        print("[-] Can not find a good interface, aborting...")
        exit(1)

    ip = get_iface_ip(iface)
    if args.verb:
        print("Interface: %s" %iface)
        print("IP:        %s" %ip)
        print("Port:      %s" %args.port)
        print()

    instr = "".join(args.input) if args.nosp else " ".join(args.input)
    output = instr.replace(args.ipsub, ip)
    output = output.replace(args.ptsub, str(args.port))
    if args.subsp:
        output = output.replace(" ", "${IFS}")
    print(output)

