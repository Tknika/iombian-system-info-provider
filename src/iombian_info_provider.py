#!/usr/bin/env python3

import logging
import platform
import psutil
import socket
import time

from generic_info_provider import GenericInfoProvider

logger = logging.getLogger(__name__)


class IoMBianInfoProvider(GenericInfoProvider):

    def __init__(self):
        self.hostname = None
        self.system_time = None
        self.uptime = None
        self.total_disk = None
        self.used_disk = None
        self.percent_disk = None
        self.local_network = None
        self.internet_status = None

    def update(self):
        self.has_changed = False
        self.hostname = platform.node()
        self.system_time = time.strftime('%H:%M')
        self.uptime = self.__process_uptime(psutil.boot_time())
        disk_usage = psutil.disk_usage("/")
        self.total_disk = float("{:.1f}".format(disk_usage.total / (10**9)))
        self.used_disk = float("{:.1f}".format(disk_usage.used / (10**9)))
        self.percent_disk = float("{:.0f}".format(disk_usage.percent))
        self.local_network = self.__process_local_network(psutil.net_if_addrs())
        self.internet_status = self.__check_internet_connection()

        return super().update()

    def to_json(self):
        info = {    
                    "hostname": self.hostname,
                    "system_time": self.system_time,
                    "uptime": self.uptime,
                    "total_disk": self.total_disk,
                    "used_disk": self.used_disk,
                    "percent_disk": self.percent_disk,
                    "local_network": self.local_network,
                    "internet_status": self.internet_status
                }
        return info

    def __process_local_network(self, networks):
        network_info = { "status": False, "interfaces": {}}
        for iface, addrs in networks.items():
            if iface == "lo":
                continue
            inet_addr = [addr for addr in addrs if addr.family == socket.AF_INET]
            if inet_addr:
                network_info["status"] = True
                network_info["interfaces"].update({iface: inet_addr[0].address})
            else:
                network_info["interfaces"].update({iface: "-"})
        return network_info

    def __check_internet_connection(self, host="8.8.8.8", port=53, timeout=2):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False

    def __process_uptime(self, boot_time):
        uptime_sec = time.time() - boot_time
        uptime = "now"
        if uptime_sec > 86400: # Day
            uptime = "{:.1f}d".format(uptime_sec/86400)
        elif uptime_sec > 3600: # Hours
            uptime = "{:.1f}h".format(uptime_sec/3600)
        return uptime