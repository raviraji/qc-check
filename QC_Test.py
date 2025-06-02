import requests
import socket
from datetime import datetime
import psutil
import subprocess
from datetime import datetime

url = "http://india.remoteiot.com:30136/upload"
def get_device_name():
    config_path = "/etc/remote-iot/configure"
    try:
        with open(config_path, "r") as file:
            for line in file:
                if line.startswith("name="):
                    return line.strip().split("=", 1)[1]
        return "Name not found"
    except Exception as e:
        return f"Error: {e}"
device_name = get_device_name()
#print("Device Name:", device_name)

def ltecheck():
    lte = psutil.net_if_stats()
    if 'wwan0' in lte:
        is_up = lte['wwan0'].isup
        lout = f"LTE {'OK' if is_up else 'NOT OK'}"

    else:
        lout = "NA"
    return lout

lte = ltecheck()
#print("LTE Status:", lte)

def Host_name():
    Hostname = socket.gethostname()
    return Hostname
hostname = Host_name()
#print ("Hostname:",hostname)


def iMX_Module():
    try:
        output = subprocess.check_output(["lscpu"], text=True)
        for line in output.splitlines():
            if line.startswith("Model name:"):
                model = line.split(":", 1)[1].strip()
                if "Cortex-A7" in model:
                    return "IMX7"
                else:
                    return "IMX8"
        return "Unknown"
    except Exception as e:
        return f"Error: {e}"
iMX = iMX_Module()
#print("iMX Status:",iMX)

def iMX_Serial():
    config_path = "/proc/cpuinfo"
    try:
        with open(config_path, "r") as file:
            for line in file:
                if line.startswith("Serial"):
                    return line.strip().split(":", 1)[1]
        return "Serial Number not found"
    except Exception as e:
        return f"Error: {e}"
iMX_SN = iMX_Serial()
#print("iMX Serial No:", iMX_SN)

def LTE_IMEI():
    try:
        output = subprocess.check_output(["mmcli -m 0"], text=True)
        for line in output.splitlines():
            if line.startswith("equipment id"):
                return line.split(":", 1)[1].strip()
        return "Unknown"
    except Exception as e:
        return f"NA"
imei = LTE_IMEI()
#print("LTE IMEI No:",imei)

def SIM_Status():
    try:
        output = subprocess.check_output(["mmcli -m 0"], text=True)
        for line in output.splitlines():
            if line.startswith("state"):
                return line.split(":", 1)[1].strip()
        return "Unknown"
    except Exception as e:
        return f"NA"
Sim_Status = SIM_Status()
#print("SIM Status:",Sim_Status)


def SIG_Status():
    try:
        output = subprocess.check_output(["mmcli -m 0"], text=True)
        for line in output.splitlines():
            if line.startswith("signal quality"):
                return line.split(":", 1)[1].strip()
        return "Unknown"
    except Exception as e:
        return f"NA"
Sig_Status = SIG_Status()
#print("Signal Strength:",Sig_Status)

def Operator_Status():
    try:
        output = subprocess.check_output(["mmcli -m 0"], text=True)
        for line in output.splitlines():
            if line.startswith("operator name"):
                return line.split(":", 1)[1].strip()
        return "Not Available"
    except Exception as e:
        return f"NA"
opr_Status = Operator_Status()
#print("SIM Name:",opr_Status)

def Lte_module():
    try:
        output = subprocess.check_output(["mmcli -m 0"], text=True)
        for line in output.splitlines():
            if line.startswith("firmware revision"):
                return line.split(":", 1)[1].strip()[:5]
        return "Not Available"
    except Exception as e:
        return f"NA"
LTE_Module = Lte_module()
#print("LTE Series:",LTE_Module)

def SDcard():
    try:
        output = subprocess.check_output(["lsblk -o NAME,VENDOR,SIZE"], text=True)
        for line in output.splitlines():
            if line.startswith("sda","sdb","mmcblk1"):
                parts = line.split()
                if len(parts) >= 3:
                    name, vendor, size = parts[0], parts[1], parts[2]
                    return name, vendor, size
        return ("Not Available", "Not Available", "Not Available")
    except Exception as e:
        return ("NA", "NA", "NA")
SDname, SDvendor, SDsize = SDcard()
#print("SD type:", SDvendor)
#print("SD Card Size:", SDsize)


Time = datetime.now().isoformat()
payload = {
    "Device_ID": device_name,
    "IMX_ID": hostname,
    "IMX_Type": iMX,
    "IMX_Serial_No": iMX_SN,
    "IMX_IMEI": imei,
    "SIM_Status": Sim_Status,
    "SIM_Signal": Sig_Status,
    "SIM_Operator": opr_Status,
    "LTE_Module_Type": LTE_Module,
    "SD_Card_Type": SDvendor,
    "SD_Card_Size": SDsize,
    "UpdateTime":Time,
}
r = requests.post(url, json=payload)
print(r.status_code, r.text)
