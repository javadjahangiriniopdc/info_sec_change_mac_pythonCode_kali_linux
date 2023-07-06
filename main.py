#! /usr/bin/env python3

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface for change mac")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please enter interface,use --help for more information...")
    if not options.new_mac:
        parser.error("[-] Please enter mac address,use --help for more information...")
    return options


def change_mac(interface, new_mac):
    print(f"[+] Changing Mac Address for {interface} to {new_mac}")
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])
    mac_address_ifconfig_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_address_ifconfig_result:
        return mac_address_ifconfig_result.group(0)
    else:
        return "[-] Can not read mac address"


options = get_arguments()

current_mac = get_current_mac(options.interface)
if current_mac != options.new_mac:
    change_mac(options.interface, options.new_mac)
else:
    print(f'[-] Current Mac:{current_mac} Equal New Mac:{options.new_mac} on interface:{options.interface} '
          f'No Need Action ...')
