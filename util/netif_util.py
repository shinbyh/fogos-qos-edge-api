# -*- coding: utf-8 -*-
import netifaces

def get_unique_codes():
    ifaces = netifaces.interfaces()
    uniqueCodes = []

    for iface in ifaces:
        if(iface == 'lo'):
            continue
        else:
            addrs = netifaces.ifaddresses(iface)

            ifaceType = 'undefined'
            if('eth' in iface or 'br' in iface or iface.startswith('en')):
                ifaceType = 'wired'
            elif('wlan' in iface):
                ifaceType = 'wifi'
            else:
                ifaceType = 'undefined'

            hwAddress = addrs[netifaces.AF_LINK][0]['addr']
            if('addr' in addrs[netifaces.AF_INET][0]):
                ipv4 = addrs[netifaces.AF_INET][0]['addr']
            else:
                ipv4 = 'null'

            uniqueCode = {
                'ifaceType': ifaceType,
                'hwAddress': hwAddress,
                'ipv4': ipv4
            }
            uniqueCodes.append(uniqueCode)
            return uniqueCodes

    return uniqueCodes


#
# Debug: test code
#
if __name__ == '__main__':
    res = get_unique_codes()
    print(res)
