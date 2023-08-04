import urllib.request
import os
import socks

def detect_system_proxy():
    proxy = urllib.request.getproxies().get('https')
    if proxy:
        proxy = proxy.split('://')[1]
        proxy = proxy.split(':')
        proxy = (proxy[0], int(proxy[1]))
        set_proxy(proxy)
        print('System proxy detected:', proxy)
    else:
        print('No system proxy detected')

def set_proxy(proxy):
    socks.set_default_proxy(socks.SOCKS5, proxy[0], proxy[1])
    socket.socket = socks.socksocket
