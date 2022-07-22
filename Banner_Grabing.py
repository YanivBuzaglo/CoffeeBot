import socket
def banner_grabbing():
    while True:
        try:
            sock = socket.socket()
            target = input("Insert your target IP: ==> ")
            port = input("Insert port to scan in the target machine: ==> ")
            if "exit" in port or "exit" in target:
                break
            else:
                sock.connect((target, int(port)))
                sock.send("What is your banner?\r\n".encode())
                socket.setdefaulttimeout(4)
                rec = sock.recv(1024).decode()
                print(f"[+] The banner of the service --> {rec} AND THE PORT IS : ==> {port}")
                sock.close()
        except:
            continue