import os
import datetime
import json 
from datetime import timedelta  
clear = lambda: os.system("cls")

alphabet = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
            'u', 'v', 'w', 'x', 'y', 'z', ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
            'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# with open("carlist.txt", "w") as f:
#   f.write(json.dumps(carlist))
  
# reading the data from the file
# with open('data.txt') as f:
#   data = f.read()

# js = json.loads(data)

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

# read txt files
def read_file(filename):
  with open(filename) as f:
    data = f.read()

  return json.loads(data)

# write txt files
def write_file(filename, details):
  with open(filename, "w") as f:
    f.write(json.dumps(details, indent=4, sort_keys=True, default=str))

# user info validation
def validation(username, password, confirm_password): 
  userlist = read_file("userlist.txt")

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
    if user["username"].lower() == username.lower():
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
  userlist = read_file("userlist.txt")

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

  write_file("userlist.txt", userlist)

  clear()
  print("You have registered successfully, please login now")

# login
def login(username, password):
  with open('userlist.txt') as f:
    data = f.read()

  userlist = json.loads(data)

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

# display car brand
def display_brand():
  cars = read_file("carlist.txt")
  brand = []

  # display car brand first
  for car in cars: 
    brand.append(car["brand"])
  brand = list(set(brand))

  count = 1
  for i in brand:
    print(f"{count}. {i}")
    count+=1

  print("\n0. Go back to home page")
  option = input("Select a model: ")

  return {
    "payload": option,
    "brand": brand
  }

# display car details
def car_details(payload, brand):
  clear()
  cars = read_file("carlist.txt")
  brand_selected = brand[payload]
  model = []

  for car in cars:
    if car["brand"] == brand_selected:
      model.append(car)

  # display selected brand car model
  for i in model:
    id = i["id"]
    brand = i["brand"]
    model = i["model"]
    year = i["year"]
    price = i["price"]
    availability = i["rental_status"]
    rent_by = i["rent_by"]

    print("-"*20)
    print(f"vehicle id: {id}")
    print(f"vehicle: {brand} {model}")
    print(f"year: {year}")
    print(f"pricing: RM{price}")
    if availability:
      print(f"availability: no")
    if not availability:
      print(f"availability: yes")
    if rent_by:
      if rent_by["username"]:
        username = rent_by["username"]
        start_date = rent_by["start_date"]
        duration = rent_by["duration"]
        str_date = start_date[0:11]
        print(f"currently rented by Mr/Mrs {username}\nRented since {str_date} for {duration} days")
    print("-"*20)
    print("\n")

  return model


# ADMIN INTERFACE


# CUSTOMER INTERFACE
def delete_user(): 
  userlist = read_file("userlist.txt")

  for i in range(len(userlist)):
    if userlist[i]["username"] == current_user[0]["username"]:
      del userlist[i]
      break
  
  return userlist

def delete_car(car_brand): 
  carlist = read_file("carlist.txt")

  for i in range(len(carlist)):
    if carlist[i]["brand"] == car_brand:
      del carlist[i]
      break
  
  return carlist

def display_user():
  clear()
  username = current_user[0]["username"]

  print("Update Personal Information\n")
  print(f"1. Username: {username}\n2. Password\n\n0. Go Back\n")
  return input("Which detail do you wish to update? ")

def check_user(action):
  if action == 0:
    return 

  userlist = read_file("userlist.txt")

  while action == 1:
    username = input("Enter new username: ")
    validated = validation(username, "password", "password")
    
    if validated["err"]:
      clear()
      print(validated["message"])
    
    if not validated["err"]:
      return [1, username]
  
  while action == 2:
    err = False
    clear()
    old = input("Enter old password: ")
    new_password = input("\nEnter new password: ")
    new_confirm = input("Confirm new password: ")

    validated = validation("username", new_password, new_confirm)

    if validated["err"]:
      clear()
      print(validated["message"])

    for user in userlist:
      if user["username"] == current_user[0]["username"]:
        if user["password"] != encryption(old, default_salt, 1):
          err = True
          clear()
          print("Old password incorrect\n\n1. Retry\n0. Quit\n")
          choice = input("Choice: ")

          if choice == "0":
            err = False


    if not validated["err"] and not err:
      return [2, new_password]
    
def update_user(action):
  userlist = delete_user()

  if action[0] == 1:
    updated_user = {
      "username": action[1], 
      "email": current_user[0]["email"], 
      "password": current_user[0]["password"], 
      "wallet": current_user[0]["wallet"], 
      "rental_history": current_user[0]["rental_history"],
      "isAdmin": current_user[0]["isAdmin"]
    }

    userlist.append(updated_user)
    write_file("userlist.txt", userlist)

  if action[0] == 2:
    updated_user = {
      "username": current_user[0]["username"], 
      "email": current_user[0]["email"], 
      "password": encryption(action[1], default_salt, 1), 
      "wallet": current_user[0]["wallet"], 
      "rental_history": current_user[0]["rental_history"],
      "isAdmin": current_user[0]["isAdmin"]
    }

    userlist.append(updated_user)
    write_file("userlist.txt", userlist)

  current_user.clear()
  return "User Info has successfully updated, Please login again"

def modify_wallet():
  clear()
  balance = current_user[0]["wallet"]
  decimal_balance = "{:.2f}".format(balance)
  print(f"Your total balance remaining: RM{decimal_balance}\n")
  print("1. Add fund\n<Enter> to Quit\n")
  add_fund = input("Do you wish to add fund into your account? ")

  if add_fund != "1":
    return 0
  
  if add_fund == "1":
    amount = input("Enter the amount you wished to deposit: RM")
    userlist = delete_user()

    updated_user = {
      "username": current_user[0]["username"], 
      "email": current_user[0]["email"], 
      "password": current_user[0]["password"], 
      "wallet": int(current_user[0]["wallet"]) + float(amount), 
      "rental_history": current_user[0]["rental_history"],
      "isAdmin": current_user[0]["isAdmin"]
    }

    userlist.append(updated_user)
    write_file("userlist.txt", userlist)
    current_user[0] = updated_user
    modify_wallet()

def rent_car(id):
  carlist = read_file("carlist.txt")
  userlist = read_file("userlist.txt")
  chosen_car = []

  for car in carlist:
    if car["id"] == id:
      if car["rental_status"]:
        return {
          "err": True,
          "message": "Car is already been taken by someone"
        }

      chosen_car.append(car)
      brand = car['brand'].capitalize()
      model = car['model'].capitalize()
      year = car['year']
      price = "{:.2f}".format(car['price'])

      print(f"You have selected {brand} {model}, {year}")
      print(f"Rental price for this product will be fixed at the rate of RM{price} per day\n")

      confirmation = input("Do you want to confirm order? (yes/No): ")
      if confirmation.lower() == "no":
        return
      duration = input("How many days would you like to rent? ")

      while confirmation.lower() == "yes":
        total_price = float(price) * int(duration)

        for user in userlist:
          if user["username"] == current_user[0]["username"]:
            if user["wallet"] < total_price:
              return {
                "err": True,
                "message": "Insufficient balance, you are broke!"
              } 

            reset_user = delete_user()
            reset_car = delete_car(brand)

            rental_history = current_user[0]["rental_history"]

            updated_car = {
              "id": id, 
              "brand": brand, 
              "model": model, 
              "year": year, 
              "price": price, 
              "rental_status": True, 
              "rent_by": {
                "username": "eugene", 
                "duration": duration, 
                "start_date": datetime.datetime.now(), 
                "end_date": datetime.datetime.now() + timedelta(days=int(duration)),
              }
            }

            rental_history.append(updated_car)

            updated_user = {
              "username": current_user[0]["username"], 
              "email": current_user[0]["email"], 
              "password": current_user[0]["password"], 
              "wallet": int(current_user[0]["wallet"]) - int(total_price), 
              "rental_history": rental_history,
              "isAdmin": current_user[0]["isAdmin"]
            }

            reset_user.append(updated_user)
            reset_car.append(updated_car)
            write_file("carlist.txt", reset_car)
            write_file("userlist.txt", reset_user )
            current_user[0] = updated_user
            
            print(f"\nYour booking order for {brand} {model}, {year} for the duration of {duration} days has been confirmed\nEnjoy your ride!")

            end = input("Press Enter to return back to home page!")
            return end
        break

# def rental_expire():


# USER INTERFACE
def main():
  clear()
  print('-'*20)
  print('Super Car Rental Service (SCRS)')
  print('-'*20)

  # main page
  while len(current_user) == 0:
    print('\n1. Login\n2. Register\n3. View Cars\n0. Quit')

    option = input('Please select a choice: ')
    if option == "2":
      register()

    if option == "1":
      username = input("Username: ")
      password = input("Password: ")

      login(username, password)

    while option == "3":
      clear()
      action = display_brand()

      if action["payload"] == "0":
        clear()
        break

      while action["payload"] != "0":
        payload = int(action["payload"]) - 1
        brand = action["brand"]
        car_details(payload, brand)
        input("Press Enter to quit: ")
        clear()
        break       
      
    if option == "0":
      break

  # admin
  while len(current_user) > 0 and current_user[0]["isAdmin"]:
    clear()
    print("Welcome Mr/Mrs", current_user[0]["username"].capitalize(), "\n")
    num = input("enter a number: ")

    if num == "1":
      break

  # customer
  while len(current_user) > 0 and not current_user[0]["isAdmin"]:
    clear()
    print("Welcome Mr/Mrs", current_user[0]["username"].capitalize(), "\n")
    print('1. Rent a Car\n2. Update Personal Information\n3. Rental History\n4. Check Wallet\n\n0. Logout\n')
    user_option = input("Please enter your choice: ")

    while user_option == "4":
      clear()
      instruction = modify_wallet()

      if instruction == 0:
        break      

    while user_option == "2":
      personal_action = display_user()
      if personal_action == "0":
        break
      user_data = check_user(int(personal_action))
      msg = update_user(user_data)
      clear()
      print(msg, "\n")
      main()
    
    while user_option == "1":
      clear()
      action = display_brand()

      if action["payload"] == "0":
        clear()
        break

      while action["payload"] != "0":
        payload = int(action["payload"]) - 1
        brand = action["brand"]
        car_details(payload, brand)
        vehicle_id = input("Select vehicle ID to rent or <Enter> to go back: ")

        while len(vehicle_id) > 0:
          clear()
          status = rent_car(int(vehicle_id))

          if status == "":
            break

          try:
            if status["err"]:
              print(status["message"])   
              retry = input("Please select other car available for rent. <Enter> to continue")
              if retry == "":
                clear()
                break
          except:
            return 

        if vehicle_id == "":
          clear()
          break   


    if user_option == "0":
      main() 
      break       

main()
print(current_user)