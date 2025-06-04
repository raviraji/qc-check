import requests
import socket
from datetime import datetime
import psutil
import subprocess
from datetime import datetime
import time
import re
url = "http://india.remoteiot.com:30060/upload"
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
    config_path1 = "/sys/devices/soc0/soc_uid"
    try:
        vALID = iMX_Module()
        if vALID == "IMX7":
           with open(config_path, "r") as file:
             for line in file:
                 if line.startswith("Serial"):
                     return line.strip().split(":", 1)[1]
        else:
           with open(config_path1, "r") as file:
                return file.read().strip()
    except Exception as e:
        return f"Error: {e}"
iMX_SN = iMX_Serial()
#print("iMX Serial No:", iMX_SN)

def LTE_IMEI():
    try:
        output = subprocess.run(["mmcli", "-m", "0"], capture_output=True, text=True)
        RaW = re.search(r'equipment id:\s+(\w+)', output.stdout, re.IGNORECASE)
        if RaW:
           RaWout = RaW.group(1)
           return RaWout
        return "Not There"
    except Exception as e:
        return e
imei = LTE_IMEI()
#print("LTE IMEI No:",imei)

def SIM_NuM():
    try:
        output = subprocess.run(['mmcli', '-m', '0'], capture_output=True, text=True)
        RaW = re.search(r'own:\s+(\w+)', output.stdout, re.IGNORECASE)
        if RaW:
           oUT = RaW.group(1)
           return oUT
        return "NoT There"
    except Exception as e:
        return e
Sim_number = SIM_NuM()
#print("SIM Number:",Sim_number)

def SIG_Status():
    try:
        result = subprocess.run(['mmcli', '-m', '0'], capture_output=True, text=True)
        match = re.search(r'signal quality:\s+(\d+)%', result.stdout, re.IGNORECASE)
        if match:
            out = int(match.group(1))
            return out
        else:
           return "Not available"
    except Exception as e:
         return e
Sig_Status = SIG_Status()
#print("Signal strength:",Sig_Status)

def Operator_Status():
    try:
        result = subprocess.run(["mmcli", "-m", "0"], capture_output=True, text=True)
        match = re.search(r'operator name:\s+(\w+)', result.stdout, re.IGNORECASE)
        if match:
            out = match.group(1)
            return out
        return "Not There"
    except Exception as e:
        return f"NA"
opr_Status = Operator_Status()
#print("SIM Name:",opr_Status)

def Lte_module():
    try:
        output = subprocess.run(["mmcli", "-m", "0"], capture_output=True, text=True)
        RaW = re.search(r'revision:\s+(\w+)', output.stdout, re.IGNORECASE)
        if RaW:
           RaW_out = RaW.group(1)[:5]
           return RaW_out
        return "Not there"
    except Exception as e:
        return e
LTE_Module = Lte_module()
#print("LTE Type:",LTE_Module)

def SDcard():
    try:
        output = subprocess.run(["lsblk", "-o", "NAME,SIZE"], capture_output=True, text=True)    
        parts = re.search(r'mmcblk1\s+(\w+)', output.stdout, re.IGNORECASE)
        print(parts)
        RaW = parts.group(1)
        if len(RaW) >= 1:
           return parts[0][:6], parts[1]
        return "NOT THERE"
    except Exception as e:
        return ("NA", "NA")
SDname, SDsize = SDcard()
print("SD Card Name:", SDname)
print("Size:", SDsize)


Time = datetime.now().isoformat()
payload = {
    "Device_ID": device_name,
    "IMX_ID": hostname,
    "IMX_Type": iMX,
    "IMX_Serial_No": iMX_SN,
    "IMX_IMEI": imei,
    "SIM_Number": Sim_number,
    "SIM_Signal": Sig_Status,
    "SIM_Operator": opr_Status,
    "LTE_Module_Type": LTE_Module,
    "SD_Card_Type": SDname,
    "SD_Card_Size": SDsize,
    "UpdateTime":Time,
}
r = requests.post(url, json=payload)
print(r.status_code, r.text)
