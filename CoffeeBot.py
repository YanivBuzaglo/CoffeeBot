#My coffee bot Yaniv Bouzaglo version 1.3
import Finale
import pymongo
import time
import ssl
from email.message import EmailMessage
import smtplib
import random
import os
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
welcome_options = ["[a] Sign up","[b] Sign in","[c] Forgot Password"]
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
                Verfication_Mail(email,body)
                status = Verfication_Mail(email,body)
                if status == False:
                    print("Sign up proccess failed please try again.")
                    sign_up()
                else:
                    print(f"Two step verification!{code}")
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
                return fin
            else:
                fin = False
    return fin 
def main():
    welcome_options_input = input("Choose from the list ahead :\n"
    f"{welcome_options[0]}\n\n"
    f"{welcome_options[1]}\n\n"
    f"{welcome_options[2]}\n\n"
    "----- INSERT YOUR PICK HERE ----- > ")
    if welcome_options_input == 'a' or welcome_options_input == 'A':
        sign_up()
        print("Sign in to the bot.")
        auth = sign_in()
        if auth == True:
            print("Signed in successfully!")
        else:
            print("Authentication failed!")
    elif welcome_options_input == 'b' or welcome_options_input == 'B':
        auth = sign_in()
        if auth == True:
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
            else:
                print("Authentication failed!")
                sign_in()
        else:
            print("Wrong mail address or password.")
            main()
    elif  welcome_options_input == 'c' or welcome_options_input == 'C':
        pass
    else:
        pass
main()
