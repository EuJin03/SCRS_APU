import os
import datetime
from datetime import timedelta  
clear = lambda: os.system("cls")

alphabet = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

carlist = [
  {
    "brand": "Honda",
    "model": "Civic",
    "year": "2018",
    "price": 100,
    "rental_status": False,
    "rent_by": "",
  },
  {
    "brand": "Toyota",
    "model": "Vios",
    "year": "2020",
    "price": 100,
    "rental_status": False,
    "rent_by": "",
  },
  {
    "brand": "Mercedes",
    "model": "Benz",
    "year": "2018",
    "price": 100,
    "rental_status": True,
    "rent_by": {
      "username": "eugene",
      "duration": "2d",
      "start_date": datetime.datetime(2020, 5, 17),
      "end_date": datetime.datetime(2020, 5, 17) + timedelta(days=2)  
    },
  },
]

userlist = [
  {
    "username": "admin",
    "email": "admin@mail.com",
    "password": " foach123",
    "wallet": 100,
    "rental_history": [],
    "isAdmin": True,
  },
  {
    "username": "eugene",
    "email": "eugene@mail.com",
    "password": " foach123",
    "wallet": 100000,
    "rental_history": [],
    "isAdmin": True,
  },
  {
    "username": "wenxuen",
    "email": "wenxuen@mail.com",
    "password": " foach123",
    "wallet": 0,
    "rental_history": [],
    "isAdmin": False,
  }
]

current_user = []
default_salt = 10 % 26

def encryption(text, salt, direction):
  crypted_text = ""
  if direction == 0:
    salt = (-1 * salt) + 27
  for letter in text:
    if letter in alphabet:
      position = alphabet.index(letter)
      new_position = position + salt
      crypted_text += alphabet[new_position]
    else:
      crypted_text += letter
  return crypted_text

def validation(username, password, confirm_password): 
  if len(password) < 5:
    return {
      "err": True,
      "message": "Password must be greater than 5"
    }

  if password != confirm_password:
    return {
      "err": True,
      "message": "Password do not match, please try again"
    }

  if len(username) < 5:
    return {
      "err": True,
      "message": "username length must greater than 5"
    }
  
  for user in userlist:
    if user["username"] == username:
      return {
        "err": True,
        "message": "Username has been taken, please try again"
      }

  return {
    "err": False
  }

# user info
def user_input():
  username = input("Username: ")
  email = input("Email: ")
  password = input("Password: ")
  confirm_password = input("Confirm Password: ")

  err = True

  while err:
    validated = validation(username, password, confirm_password)

    if not validated["err"]:
      err = False
    
    if validated["err"]:
      print(validated["message"])
      print("-"*20)
      username = input("Username: ")
      email = input("Email: ")
      password = input("Password: ")
      confirm_password = input("Confirm Password: ")
      print("-"*20)
    
  return {
    "username": username,
    "email": email,
    "password": encryption(password, default_salt, 1),
  }

# register
def register():
  user_detail = user_input()

  user = {
    "username": user_detail["username"],
    "email": user_detail["email"],
    "password": user_detail["password"],
    "wallet": 0,
    "rental_history": [],
    "isAdmin": False,
  }

  userlist.append(user)

  clear()
  print("You have registered successfully, please login now")
  

# login
def login(username, password):
  err = True
  for user in userlist:
    if user["username"] == username:
      decrypted_password = encryption(user["password"], default_salt, 0)
      if decrypted_password  == password:
        err = False
        clear()
        current_user.append(user)
        print("You have login successfully")

  if err:
    clear()
    print("Username or password is incorrect, please try again")


# USER INTERFACE
def main():
  print('-'*20)
  print('Super Car Rental Service (SCRS)')
  print('-'*20)

  # main page
  while len(current_user) == 0:
    print('\n1. Login\n2. Register\n3. View Cars\n0. Quit')

    option = input('Please enter your choice: ')
    if option == "2":
      register()

    if option == "1":
      username = input("Username: ")
      password = input("Password: ")

      login(username, password)

    if option == "0":
      break

  # admin
  while len(current_user) > 0 and current_user[0]["isAdmin"]:
    print("Welcome Mr/Mrs", current_user[0]["username"])
    num = input("enter a number: ")

    if num == "1":
      break

  # customer
  while len(current_user) > 0 and not current_user[0]["isAdmin"]:
    print("hello")
    break

main()
print(current_user)
print(userlist)