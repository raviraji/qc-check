import sys
import os
import requests
import socket
from datetime import datetime
import re
import subprocess
def import_module():
    try:
        import psutil
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
        import psutil
    return psutil

psutil = import_module()


class DeviceInfo:
    def __init__(self):
        self.url = "http://india.remoteiot.com:30060/upload"

    def get_device_name(self):
        try:
            with open("/etc/remote-iot/configure", "r") as file:
                for line in file:
                    if line.startswith("name="):
                        return line.strip().split("=", 1)[1]
            return "Name not found"
        except Exception:
            return "NA"

    def ltecheck(self):
        lte_raw = psutil.net_if_stats()
        if 'wwan0' in lte_raw:
            return "LTE OK" if lte_raw['wwan0'].isup else "LTE NOT OK"
        return "NA"

    def hostname(self):
        return socket.gethostname()

    def imx_module(self):
        try:
            with open("/sys/devices/soc0/soc_id", "r") as file:
                return file.read().strip()
        except Exception:
            return "NA"

    def imx_mac(self):
        try:
            with open("/sys/class/net/wlan0/address", "r") as file:
                return file.read().strip()
        except Exception:
            return "NA"

    def get_modem_id(self):
        output = subprocess.run(["mmcli", "-L"], capture_output=True, text=True)
        match = re.search(r'/Modem/(\d+)', output.stdout)
        return match.group(1) if match else None

    def get_mmcli_output(self):
        modem = self.get_modem_id()
        if modem:
            return subprocess.run(["mmcli", "-m", modem], capture_output=True, text=True).stdout
        return ""

    def get_lte_imei(self):
        output = self.get_mmcli_output()
        match = re.search(r'equipment id:\s+(\w+)', output, re.IGNORECASE)
        return match.group(1) if match else "Not There"

    def get_sim_number(self):
        output = self.get_mmcli_output()
        match = re.search(r'own:\s+(\w+)', output, re.IGNORECASE)
        return match.group(1) if match else "Not There"

    def get_signal_quality(self):
        output = self.get_mmcli_output()
        match = re.search(r'signal quality:\s+(\d+)%', output, re.IGNORECASE)
        return int(match.group(1)) if match else "Not available"

    def get_operator_name(self):
        output = self.get_mmcli_output()
        match = re.search(r'operator name:\s+(\w+)', output, re.IGNORECASE)
        return match.group(1) if match else "Not There"

    def get_lte_module_type(self):
        output = self.get_mmcli_output()
        match = re.search(r'revision:\s+(\w+)', output, re.IGNORECASE)
        return match.group(1)[:5] if match else "Not there"

    def get_sd_info(self):
        try:
            output = subprocess.run(["lsblk", "-o", "NAME,SIZE"], capture_output=True, text=True)
            match = re.search(r'(mmcblk1|sda)\s+([^\s]+)', output.stdout)
            if match:
                if match.group(1) == "mmcblk1":
                   return "PCBA Mount", match.group(2)
                else:
                   return "SD reader Type", match.group(2)
            return ("Not Available", "Not Available")
        except Exception:
            return ("NA", "NA")

    def collect_payload(self):
        SDname, SDsize = self.get_sd_info()
        return {
            "Device_ID": self.get_device_name(),
            "IMX_ID": self.hostname(),
            "IMX_Type": self.imx_module(),
            "IMX_MAC_ID": self.imx_mac(),
            "LTE_IMEI": self.get_lte_imei(),
            "SIM_Number": self.get_sim_number(),
            "SIM_Signal": self.get_signal_quality(),
            "SIM_Operator": self.get_operator_name(),
            "LTE_Module_Type": self.get_lte_module_type(),
            "SD_Card_Type": SDname,
            "SD_Card_Size": SDsize,
            "UpdateTime": datetime.now().isoformat()
        }

    def send_payload(self):
        payload = self.collect_payload()
        response = requests.post(self.url, json=payload)
        print(response.status_code, response.text)
    def print(self):
        SDname, SDsize = self.get_sd_info()
        print("Device name:",self.get_device_name())
        print("Hostname:",self.hostname())
        print("IMX:",self.imx_module())
        print("MAC addeess:",self.imx_mac())
        print("LTE IMEI:",self.get_lte_imei())
        print("SIM Numbers:",self.get_sim_number())
        print("Signal strenth:",self.get_signal_quality())
        print("Operator name:",self.get_operator_name())
        print("LTE module:",self.get_lte_module_type())
        print("SD card mount type:",SDname)
        print("SD card Size:",SDsize)
        print("Update Time:",datetime.now().isoformat())
if __name__ == "__main__":
    info = DeviceInfo()
    #info.send_payload()
    info.print()
