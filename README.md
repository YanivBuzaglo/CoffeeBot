# Coffee Bot Network_mapper&Brute Forcing Banner Grabbing able tool.
Coffee bot combined with Cyber Security tools written in python.
1. This repo contains all python projects I've Wroten so far.

2. First, In order to run this script in your environment, you need to install all libraries imported.

3. Second, you'll need to create account in MongoDB Atlas(database in the cloud, super friendly interface), and connect the database to python application.

4. Once you successfully done section 2 and 3, you are good to go(make sure you got the main script CoffeeBot.py + PasswordList.txt + Order.jpg).

5. Once you run the main script, the main menu of this app will be displayed, the first three options a+b+c+d are represents the coffee bot.

# Sign up, Sign in, Forgot Password and Orders History functions(a+b+c+d in the main menu) ==>
# CoffeeBot
1. The a options is the sign up function, once you choose it, It will ask you to your name, username, email and password.

2. If your password is over 8 characters contains at least one uppercase letter and at least one digit and your email address is not registered before you will be able to continue using this bot.

3. Once you successfully done section 2, you'll get email to the mail address you registered with, a mail containing six digits code for two step authentication.

4. Once you inserted the code and the sign up process is complete you will be register in a document in the database you created inside a collection named 'userDB' inside 'CoffeeBotDB' after this you'll be transferred to the sign in function which is the b option.

5. You'll need to sign in with your email and password from the previous step, this function preforms two step authentication, insert the six digits code.

6. Once the sign in process is done, you will be transferred to the menu of the coffee bot, from that menu you will order and receive the item you ordered, after your order sent it will be registered in collection in the database named 'Orders History' with the values of the date of the order, the item ordered and the account the order was made from.

7. Once you choose the c option, you'll be need to preform sign in and two step authentication, than the script will create a file in the working directory of the script named 'Orders_History.txt', a for loop will read from the mongoDB and write all your orders history to this file, the file will be available for 60 second and then will be erased.

8. Once you choose the d option, you'll be activating the Forgot Password function, provide the email that you registered, provide your new password, and the six digits code that sent to you, if the code is correct your password will update and you will be transformed to the main menu.

9. === THAT'S IT FOR THE COFFEE BOT EXPLENATION ===

# Network Mapper function(e in the main menu)
# Network Mapper&Brute Force tool
1.  


