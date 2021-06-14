# Eugene Tin
# TP061195
# ASIA PACIFIC UNIVERSITY OF TECHNOLOGY AND INNOVATION
# GITHUB REPO https://github.com/EuJin03/SCRS_APU

# Chia Wen Xuen
# TP061184
# ASIA PACIFIC UNIVERSITY OF TECHNOLOGY AND INNOVATION

# Copyright (C) 2021 SCRS_APU Open Source Project 

# Licensed under the MIT License
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at 
 
#       https://choosealicense.com/licenses/mit/
 
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and 
# limitations under the License.

# convention
# 1. return multiple statements using list
# 2. double quotes for str
# 3. current_user variable holds logged in user details
# 4. snake casing variables
# 5. store values in the form of json data
# 6. convert datetime into str datatype
# 7. tabs preferred, default indentation=2  
# 8. four classes of function: util/users/vehicles/user_interface 
# 9. two data files: userlist/carlist

# admin credentials
# username: admin
# password: admin

# customer credentials
# username: wenxuen
# password: wenxuen

import os
import re
import datetime 
from datetime import timedelta
import json
import hashlib
clear = lambda: os.system("cls")

# ---------------------------------------------------------------------------------
# UTILITIES FUNCTIONS
# ---------------------------------------------------------------------------------
def read_file(filename):
  # -------------------------
  # read txt files
  # -------------------------
  try:
    with open(filename) as f:
      data = f.read()
    return json.loads(data)
  except:
    return []

def write_file(filename, content):
  # -------------------------
  # write txt files
  # -------------------------
  with open(filename, "w") as f:
    f.write(json.dumps(content, indent=2, sort_keys=True, default=str))
    f.close()
  return

def hash_password(password):
  # -------------------------
  # hash password
  # -------------------------
    return hashlib.sha256(str.encode(password)).hexdigest()

def validation(username="*****", email="*****@mail.com", password="*****", confirm_password="*****"): 
  # -------------------------
  # user info validation
  # -------------------------
  userlist = read_file("userlist.txt")

  # password
  if len(password) < 5:
    return [True, "Password length must be greater than 5"]

  # password
  if password != confirm_password:
    return [True, "Password do not match, please try again"]

  # username
  if len(username) < 5:
    return [True, "Username length must greater than 5"]

  # username
  for user in userlist:
    if user[0].lower() == username.lower():
      return [True, "Username has been taken, please try again"]

  # email
  REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')
  if not REGEX.match(email):
    return [True, "Email format is incorrect, please try again"]

  return [False]

def user_input():
  # -------------------------
  # user info
  # extend from register 
  # -------------------------
  clear()
  print("REGISTRATION")
  print("------------")

  # username
  while True: 
    username = input("Username: ")

    validated_info = validation(username=username)

    if validated_info[0]:
    
      print(validated_info[1])
      continue
    else:
      break

  # email
  while True: 
    email = input("Email: ")

    validated_info = validation(email=email)

    if validated_info[0]:
    
      print(validated_info[1])
      continue
    else:
      break

  # password
  while True: 
    password = input("Password: ")
    confirm_password = input("Confirm Password: ")

    validated_info = validation(password=password, confirm_password=confirm_password)

    if validated_info[0]:
    
      print(validated_info[1])
      continue
    else:
      break

  clear()
  print("----------------")
  print("Personal Details")
  print("----------------")

  # contact
  while True: 
    contact = input("Contact Number: +6")

    if not contact.isnumeric():
    
      print("Contact number must contain numbers only...")
      continue
    else:
      break

  while True: 
    city = input("Currently lived in [state]: ")

    if len(city) < 4:
    
      print("State not found, please try again...")
      continue
    else:
      break

  while True:
    print("\nWould you like to make an initial deposit into your wallet?")
    print("<Enter> to skip the deposit\n")

    wallet = input("Deposit amount: RM")

    if wallet == "":
      wallet = 0
      break
    elif not wallet.isnumeric():
    
      print("Invalid amount")
    else: 
      break
    
  return [username.lower(), email, hash_password(password), "0" + contact, city, int(wallet), [], ""]

def field_control(field_text, type, wildcard="404"):
  # -------------------------
  # input field check with error handling
  # extend from add_car()
  # -------------------------
  while True:
    field_input = input(f"{field_text}")

    if field_input == "":
      return wildcard

    # 0 = str
    if type == 0:
      if len(field_input) < 2:
        print("Text unknown, please try again")
        continue
      else:
        break
    
    # 1 = int
    if type == 1:
      if field_input == "" or not field_input.isnumeric():
        print("Please fill in with numbers only...")
        continue
      else:
        break

  return field_input  

def rental_expire():
  # -------------------------
  # reset car availability status when expired
  # -------------------------
  carlist = read_file("carlist.txt")

  for i in range(len(carlist) - 1):
    car = carlist[i]
    if car[-2]:
      if datetime.datetime.strptime(car[-1][3], "%Y-%m-%d %H:%M:%S.%f") < datetime.datetime.now():
        car[-1] = False
        car[-2] = False
        write_file("carlist.txt", carlist)       
        return

def vehicle_number():
  # -------------------------
  # read the latest car id in the file
  # -------------------------
  carlist = read_file("carlist.txt")
  latest_id = 0

  for car in carlist:
    if car[0] > latest_id:
      latest_id = car[0]
  
  return latest_id
# ---------------------------------------------------------------------------------
# USER FUNCTIONS
# ---------------------------------------------------------------------------------
def register():
  # -------------------------
  # Register
  # access: anyone
  # -------------------------
  clear()
  userlist = read_file("userlist.txt")

  user_detail = user_input()
  userlist.append(user_detail)

  write_file("userlist.txt", userlist)

  clear()
  if user_detail[-3] != 0:
    float_price = "{:.2f}".format(user_detail[-3])
    print(f"Total amount of RM{float_price} deposited into your account")
  print("You have registered successfully, please login now...")

def login(username, password):
  # -------------------------
  # Login
  # access: anyone
  # -------------------------
  userlist = read_file("userlist.txt")

  err = True
  for user in userlist:
    if user[0] == username.lower():
      if user[2] == hash_password(password):
        err = False
        clear()
        print("You have login successfully")
        return user

  if err:
    clear()
    input("Username or password is incorrect, please try again...\n\n <Enter> to return back to main menu...")
    return ""

def display_user(current_user):
  # -------------------------
  # Display user information to modify
  # access: logged in users
  # -------------------------
  clear()
  username = current_user[0][0]
  email = current_user[0][1]
  contact = "+6" + str(current_user[0][3])

  print("Update Personal Information\n")
  print(f"1. Username: [{username}]\n2. Email: [{email}]\n3. Contact Number: [{contact}]\n4. Password\n\n0. Go Back\n")
  detail = input("Which detail do you wish to update? ")
  clear()
  return detail

def update_user(action, current_user):
  # -------------------------
  # Update user information
  # access: logged in users
  # -------------------------
  if not action.isnumeric() or action > "4":
    return [False, "something went wrong", current_user[0]]

  if action == "0":
    return ""

  userlist = read_file("userlist.txt")

  # update username
  while action == "1":
    username = input("Enter new username: ")
    validated = validation(username=username)
    
    if validated[0]:
      clear()
      print(validated[1])
    
    if not validated[0]:
      for user in userlist:
        if user[0] == current_user[0][0]:
          user[0] = username
          break
      write_file("userlist.txt", userlist)
      return [False, "User info has been successfully updated!", user]

  # update email
  while action == "2":
    email = input("Enter new email: ")
    validated = validation(email=email)

    if validated[0]:
      clear()
      print(validated[1])

    if not validated[0]:
      for user in userlist:
        if user[0] == current_user[0][0]:
          user[1] = email
          break
      write_file("userlist.txt", userlist)
      return [False, "User info has been successfully updated!", user]
          

  # update contact
  while action == "3":
    contact = input("Enter new contact number: +6")

    if not contact.isnumeric():
      clear()
      print("Please insert correct information...")
      continue

    for user in userlist:
      if user[0] == current_user[0][0]:
        user[3] = contact
        break
    write_file("userlist.txt", userlist)
    return [False, "User info has been successfully updated!", user]
  
  # update password
  while action == "4":
    err = False
    clear()
    old = input("Enter old password: ")
    new_password = input("\nEnter new password: ")
    new_confirm = input("Confirm new password: ")

    validated = validation(password=new_password, confirm_password=new_confirm)

    if validated[0]:
      clear()
      print(validated[1])
      continue

    for user in userlist:
      if user[0] == current_user[0][0]:
        if user[2] != hash_password(old):
          err = True
          clear()
          print("Old password incorrect\n\n1. Retry\n0. Quit\n")
          choice = input("Choice: ")

          if choice == "0":
            clear()
            return [True, "Please try again later..."]

          if choice == "1":
            continue

        if not validated[0] and not err:
          user[2] = hash_password(new_password)
          break

    write_file("userlist.txt", userlist)
    return [True, "User info has been successfully updated, please login again..."]

def modify_wallet(current_user):
  # -------------------------
  # Deposit money into wallet
  # access: anyone
  # -------------------------
  clear()
  balance = current_user[0][-3]
  decimal_balance = "{:.2f}".format(balance)
  print(f"Your total balance remaining: RM{decimal_balance}\n")
  print("1. Add fund\n<Enter> to Quit\n")
  add_fund = input("Do you wish to add fund into your account? ")

  while True:
    if add_fund != "1":
      return 0
  
    if add_fund == "1":
      amount = input("Enter the amount you wished to deposit: RM")
      userlist = read_file("userlist.txt")

      amount = "{:.2f}".format(int(amount))

      for user in userlist:
        if user[0] == current_user[0][0]:
          user[5] = float(user[5]) + float(amount)
          updated_user = user
          break

      write_file("userlist.txt", userlist)
      current_user[0] = updated_user
      clear()
      print(f"Total fund of RM{amount} has been deposited")
      input("<Enter> to return...")
      break

def rent_car(id, current_user):
  # -------------------------
  # Book a car and payment
  # access: customer
  # -------------------------
  clear()
  carlist = read_file("carlist.txt")
  userlist = read_file("userlist.txt")

  for car in carlist:
    if car[0] == id:
      if car[-2]:
        return [True, "Car is already been taken by someone"]

      brand = car[2].capitalize()
      model = car[3].capitalize()
      year = str(car[4])
      price = "{:.2f}".format(car[8])

      print(f"You have selected {brand} {model}, {year}")
      print(f"Rental price for this product will be fixed at the rate of RM{price} per day\n")

      confirmation = input("Do you want to confirm order? [yes/No]: ")
      if confirmation.lower() == "no":
        return
      duration = input("How many days would you like to rent? ")

      while confirmation.lower() == "yes":
        total_price = float(price) * int(duration)

        for user in userlist:
          if user[0] == current_user[0][0]:
            if user[5] < total_price:
              return [True, "Insufficient balance, you are broke!"]
          
            username = current_user[0][0]

            # update car to rented
            car[-2] = True
            car[-1] = [username, duration, datetime.datetime.now(), datetime.datetime.now() + timedelta(days=int(duration))]

            # update user rental history
            user[6].append(car)
            user[5] -= total_price

            write_file("carlist.txt", carlist)
            write_file("userlist.txt", userlist)
            current_user[0] = user

            total_price = "{:.2f}".format(total_price)
            
            print(f"\nTotal payment made RM{total_price}")
            print(f"Your booking order for {brand} {model}, {year} for the duration of {duration} days has been confirmed\nEnjoy your ride!")

            end = input("Press Enter to return back to home page!")
            return end
      break

def assign_admin():
  # -------------------------
  # Assign a new user to be an administrator
  # access: admin
  # -------------------------
  userlist = read_file("userlist.txt")

  usernames = [] # list of registered usernames 

  # display usernames
  for user in userlist: 
    if user[7] != "admin":
      usernames.append(user[0])
  usernames = list(set(usernames))
  usernames.sort()

  print("ASSIGN AN ADMINISTRATOR\n")

  print(f"Search by usernames:\n")
  count = 0
  for names in usernames:
    print(f"* {names}")
    count+=1

  print("\n<Enter> to return")
  selected_username = input("\nType an username that are in the list: ")

  # return
  if selected_username == "":
    return selected_username

  # error handling
  if selected_username.isnumeric():
    print("Username does not exist...")
    end = input("<Enter> to return")
    clear()
    return end

  # error handling 2
  if not selected_username.isnumeric() and not selected_username.lower() in usernames:
      print("Username does not exist...")
      end = input("<Enter> to return")
      clear()
      return end

  for user in userlist:
    if user[0] == selected_username:
      confirmation = input(f"\nDo you wanna assign {user[0]} as an admin? [yes/No] ")

      if confirmation.lower() == "yes":
        user[7] = "admin"
        write_file("userlist.txt", userlist) 
        clear()
        print("-"*30)  
        print("SCRS MEMBER MANAGEMENT")
        print("-"*30, "\n")  
        print(f"{user[0]} has successfully promoted as an administrator for SUPER CAR RENTAL SYSTEM\n")
        return input("<Enter> to return to admin menu...")
      else:
        return ""

def display_feedback(current_user=[]):
  # -------------------------
  # Display feedbacks by customers that has used our service
  # access: everyone
  # -------------------------
  userlist = read_file("userlist.txt")

  print("-"*30)
  print("SUPER CAR RENTAL SERVICE (SCRS)")
  print("-"*30, "\n")

  header = ["Username", "Rating", "Customer Feedback"]
  format_row = "|{:^25}|{:^40}|{:^80}|"

  print(format_row.format(*header))
  print("-"*150)

  for user in userlist:
    if len(user) == 9:
      username = user[0]
      rating = user[8][0]
      feedback = user[8][1][0:60] + "..."

      print(format_row.format(username, "✰ "*rating, feedback))

  if len(current_user) > 0:
    while len(current_user[6]) != 0 and len(current_user) == 8:
      choice = submit_feedback(current_user[0])

      if len(choice[1]) > 0:
        current_user = choice[1]
      if choice[0] == "":
        break
      
  end = input("\nPress <Enter> to return to main menu...")
  clear()

  return [end, current_user]

def submit_feedback(username):
  # -------------------------
  # Allow customer to submit feedback
  # access: customer that used SCRS at least once
  # -------------------------
  userlist = read_file("userlist.txt")
  submission = input("\nDo you want to submit your own feedback or provide any suggestions? [yes/No] ")

  if submission.lower() == "yes":
    clear()

    print("-"*30)
    print("SUPER CAR RENTAL SERVICE (SCRS)")
    print("-"*30, "\n")

    print("Customer Feedback Form\n")

    while True:
      rating = input("On a scale of 1-5, how would you rate Super Car Rental Service? ")

      if rating.isnumeric() and rating > "0" and rating < "6":
        break        
    
    while True:
      feedback = input("Feel free to give short opinion on our service: ")

      if len(feedback) < 10:
        print("Message length should be greater than 10 characters")
      else:
        break

    print("-"*30)

    for user in userlist:
      if user[0] == username:
        review = [int(rating), feedback]
        user.append(review)
        write_file("userlist.txt", userlist)
        end = input("Your feedback has been submitted successfully! Press <Enter> key to return...")
        return [end, user]
  else:
    return ["", []]
   
# ---------------------------------------------------------------------------------
# CAR FUNCTIONS
# ---------------------------------------------------------------------------------
def display_brand():
  # -------------------------
  # Display car brand
  # access: anyone
  # -------------------------
  cars = read_file("carlist.txt")
  brand = [] # list of registered car brand

  # display car brand first
  for car in cars: 
    brand.append(car[2])
  brand = list(set(brand))
  brand.sort()

  print("-"*30)
  print("Select Vehicle Brand")
  print("-"*30, "\n")
  
  while True:
    count = 1
    for i in brand:
      print(f"{count}. {i}")
      count+=1

    print("\n0. Go back to home page")
    
    while True:
      num = input("Select a model: ")

      if int(num) <= count:
        break

      print("Model does not exist, please try again")


    if num.isnumeric() and num < str(count):
      break

  return [num, brand]

def car_details(brand, default=True):
  # -------------------------
  # Display car details from car brand selected
  # access: anyone
  # -------------------------
  cars = read_file("carlist.txt")
  car_model = [] # display models from car brand

  if default:
    for car in cars:
      if car[2] == brand:
        car_model.append(car)

  if not default:
    for car in cars:
      if car[2] == brand:
        if car[-2] == False:
          car_model.append(car)
  
  header = ["ID", "Number Plate",  "Vehicle", "Seats", "Short Description", "Condition", "Owner", "Price Rate", "Rental Status"]
  format_row = "{:^6}|{:^15}|{:^30}|{:^8}|{:^35}|{:^13}|{:^10}|{:^10}|{:^16}|"

  print(format_row.format(*header))
  print("-"*155)

  # display selected brand car model
  for i in car_model:
    id = i[0]
    num_plate = i[1]
    brand = i[2].capitalize()
    model = i[3].capitalize()
    year = i[4]
    vehicle = brand + " " + model + ", " + str(year)
    owner = i[5]
    condition = i[6]
    desc = i[7][0:30] + "..."
    price_rate = i[8]
    seats = i[9]
    availability = i[10]
    if availability:      
      rent_by = i[11]
      status = "Rented by " + str(rent_by[0])
    if not availability:
      status = "Not rented"

    float_price_rate = "{:.2f}".format(price_rate)
      

    print(format_row.format(id, num_plate, vehicle, seats, desc, condition, owner, float_price_rate, status))

  if len(car_model) == 0:
    print("Oops, nothing is here yet")

  car_model.clear()

def add_car():
  # -------------------------
  # Add car into file
  # access: admin
  # -------------------------
  clear()
  print("-"*20)
  print("SCRS Vehicle Management")
  print("-"*20, "\n")

  num_plate = field_control("Number Plate: ", 0)
  brand = field_control("Vehicle Brand: ", 0)
  model = field_control("Vehicle Model: ", 0)
  year = field_control("Manufactured Year: ", 1)
  owner = field_control("Owner of the vehicle: ", 0)
  condition = field_control("Condition of the car [?]/10: ", 1)
  desc = field_control("Short description: ", 0)
  price_rate = field_control("Price rate per day: RM", 1)
  seats = field_control("Number of seats: ", 1)

  carlist = read_file("carlist.txt")

  if str(num_plate) == "404":
    return ""

  latest_id = vehicle_number()

  new_car = [int(latest_id) + 1, num_plate.upper(), brand.capitalize().rstrip(), model.capitalize().rstrip(), int(year), owner.capitalize().rstrip(), float(condition), desc, float(price_rate), int(seats), False, False]

  carlist.append(new_car)

  write_file("carlist.txt", carlist)
  detail = input("Car has been successfully added to the system... <Enter> to return:")
  clear()
  return detail

def modify_car(id):
  # -------------------------
  # Update car details 
  # extended from select car
  # access: admin
  # -------------------------
  clear()
  print('Car model: ')
  carlist = read_file("carlist.txt")

  for car in carlist:
    if car[0] == id:
      print("Modify details of", car[2], car[3], ",", car[4])
      print("Current number plate: ", car[1])
      print("\n<Enter> to keep previous data...\n")

      num_plate = field_control("Number Plate [" + car[1] + "]: ", 0, car[1])
      brand = field_control("Vehicle Brand [" + car[2] + "]: ", 0, car[2])
      model = field_control("Vehicle Model [" + car[3] + "]: ", 0, car[3])
      year = field_control("Manufactured Year [" + str(car[4]) + "]: ", 1, car[4])
      owner = field_control("Owner of the vehicle [" + car[5] + "]: ", 0, car[5])
      condition = field_control("Condition of the car [" + str(car[6]) + "/10)" + ": ", 1, car[6])
      desc = field_control("Short description: [" + car[7] + "]\n: ", 0, car[7])
      price_rate = field_control("Price rate per day: [RM" + "{:.2f}".format(car[8]) + "]: ", 1, car[8])
      seats = field_control("Number of seats [" + str(car[9]) + "]: ", 1, car[9])

      new_car = [car[0], num_plate, brand, model, int(year), owner, float(condition), desc, float(price_rate), int(seats), car[10], car[11]]
      break

  for i in range(len(carlist)):
    if carlist[i][0] == id:
      del carlist[i]
      break

  carlist.append(new_car)
  write_file("carlist.txt", carlist)

  return [True, "Car's details has been modified successfully"]

def select_car(callback):
  # -------------------------
  # Select a car to modify
  # access: admin
  # -------------------------
  clear()
  print("-"*20)
  print("SCRS Vehicle Management")
  print("-"*20, "\n")

  carlist = read_file("carlist.txt")

  action = display_brand()

  if action[0] == "0":
    clear()
    return ""

  while action[0] != "0":
    clear()
    payload = int(action[0]) - 1
    car_details(brand=action[1][payload])
    latest_id = vehicle_number()

    while True:
      vehicle_id = input("\nSelect vehicle ID to modify or <Enter> to go back: ")

      if int(vehicle_id) <= latest_id:
        break

      print("Id does not exist, please try again\n")

    while len(vehicle_id) > 0:
      clear()
      status = callback(int(vehicle_id))

      if status[0]:
        print(status[1])
        input("<Enter> to return back to main menu...")
        break

    if vehicle_id == "":
      clear()
      break   

def rental_history(current_user):
  # -------------------------
  # View rental history
  # access: customer
  # -------------------------
  clear()
  userlist = read_file("userlist.txt")
  print("-"*25)
  print(f"{current_user[0][0]}'s Rental History")
  print("-"*25, "\n")
  for user in userlist:
    if user[0] == current_user[0][0]:
      if len(user[6]) == 0:
        print("Start placing order today for exclusive discounts!\n")
        return input("<Enter> to return back to home page...")

      header = ["Number Plate",  "Vehicle", "Booked on",  "Expire on", "Duration", "Total Amount"]
      format_row = "{:^20}|" * len(header)

      print(format_row.format(*header))
      print("-"*125)
      for rent in user[6]:
        num_plate = rent[1].upper()
        brand = rent[2].capitalize()
        model = rent[3].capitalize()
        year = rent[4]
        vehicle = brand + " " + model + ", " + str(year)
        price_rate = rent[8]
        start_date = rent[-1][2][0:11]
        end_date = rent[-1][3][0:11]
        duration = rent[-1][1]

        price_per_order = "{:.2f}".format(float(price_rate) * int(duration))

        print(format_row.format(num_plate, vehicle, start_date,end_date,str(duration) + " days", "RM " + price_per_order))
      break


  end = input("\n<Enter> to return back to home page...")
  clear()
  return end

def rented_out():
  # -------------------------
  # View vehicles that are currently rented out
  # access: admin
  # -------------------------
  clear()

  print("-"*25)
  print("CARS ON TRANSIT RECORDS")
  print("-"*25, "\n")

  carlist = read_file("carlist.txt")

  header = ["Number Plate",  "Vehicle", "Booked on",  "Expire on", "Owner", "Total Amount", "Rented By"]
  format_row = "{:^20}|" * len(header)
  print(format_row.format(*header))
  print("-"*145)
  for car in carlist:
    if car[-2]:
      if len(car[-1]) > 0:
        
        booking_details = car[-1]
        num_plate = car[1].upper()
        vehicle = car[2].capitalize() + " " + car[3].capitalize() + ", " + str(car[4])
        owner = car[5]
        price_rate = car[8]
        start_date = booking_details[2][0:11]
        end_date = booking_details[3][0:11]
        username = booking_details[0]
        duration = booking_details[1]

        total_price = "{:.2f}".format(int(duration) * float(price_rate))

        print(format_row.format(num_plate, vehicle, start_date,end_date, owner, total_price, username))

  end = input("\n<Enter> to go back...")
  clear()
  return end

def rent_available():
  # -------------------------
  # View vehicles that are available for rent
  # access: admin
  # -------------------------  
  clear()
  print("-"*20)
  print("SCRS Vehicle Management")
  print("-"*20, "\n")

  action = display_brand()

  if action[0] == "0":
    clear()
    return ""
    
  while action[0] != "0":
    clear()
    print("-"*20)
    print("Available vehicle")
    print("-"*20, "\n")
    payload = int(action[0]) - 1
    car_details(action[1][payload], False)
    input("\nPress Enter to quit: ")
    clear()
    break   

def customer_payment():
  # -------------------------
  # View customer bookings and payments
  # access: admin
  # -------------------------
  clear()
  print("-"*20)
  print("SCRS Customer Order Record")
  print("-"*20, "\n")

  userlist = read_file("userlist.txt")

  for user in userlist:
    if len(user[6]) > 0:
      username = user[0]
      email = user[1]
      total_spent = 0

      print("-"*15)
      print(f"Username: {username}")
      print(f"Email: {email}")
      print("-"*15, "\n")

      header = ["Number Plate",  "Vehicle", "Booked on",  "Expire on", "Duration", "Total Amount", "Rented By"]
      format_row = "{:^20}|" * len(header)

      print(format_row.format(*header))
      print("-"*150)

      for data in user[6]:
        num_plate = data[1]
        start_date = data[-1][2][0:11]
        end_date = data[-1][3][0:11]
        duration = data[-1][1]
        vehicle = f"{data[2]} {data[3]}, {data[4]}"
        price_per_order = "{:.2f}".format(data[8] * int(duration))
        
        print(format_row.format(num_plate, vehicle, start_date,end_date, duration + " days", "RM " + price_per_order, username))

        total_spent += float(price_per_order)
        
      str_spent = "{:.2f}".format(total_spent)
      print("-"*5)
      print(f"Total amount earned: RM {str_spent}\n")

  end = input("<Enter> to go back...")
  clear()
  return end

def customer_query():
  userlist = read_file("userlist.txt")

  usernames = [] # list of registered usernames 

  # display usernames
  for user in userlist: 
    usernames.append(user[0])
  usernames = list(set(usernames))
  usernames.sort()

  print(f"Search by usernames:\n")
  count = 0
  for names in usernames:
    print(f"{count}. {names}")
    count+=1

  print("\n<Enter> to return")
  selected_username = input("\nSelect an user by listed numbers or type the username: ")

  # return
  if selected_username == "":
    return selected_username

  # error handling
  if selected_username.isnumeric():
    if float(selected_username) >= len(usernames) or int(selected_username) < 0:
      print("Username does not exist...")
      end = input("<Enter> to return")
      clear()
      return end

  # error handling 2
  if not selected_username.isnumeric() and not selected_username.lower() in usernames:
      print("Username does not exist...")
      end = input("<Enter> to return")
      clear()
      return end

  while True:
    clear()
    if selected_username.isnumeric():
      for user in userlist:
        if user[0] == usernames[int(selected_username)]:
          username = user[0]
          email = user[1]
          print("-"*15)
          print(f"Username: {username}")
          print(f"Email: {email}")
          print("-"*15, "\n")
          
          header = ["Number Plate",  "Vehicle", "Booked on",  "Expire on", "duration", "Total Amount"]

          format_row = "{:^20}|" * len(header)
          print(format_row.format(*header))
          print("-"*125)
          if len(user[6]) > 0:
            for record in user[6]:
              
              start_date = record[-1][2][0:11]
              end_date = record[-1][3][0:11]
              duration = record[-1][1]
              vehicle = f"{record[2]} {record[3]}, {record[4]}"
              num_plate = record[1].upper()
              price_per_order = "RM " + "{:.2f}".format(record[8] * int(duration))

              print(format_row.format(num_plate, vehicle, start_date,end_date,str(duration) + " days", price_per_order))
          
    # query by username
    if len(selected_username) > 1:
        for user in userlist:
          if user[0].lower() == selected_username.lower():
            username = user[0]
            email = user[1]
            print("-"*15)
            print(f"Username: {username}")
            print(f"Email: {email}")
            print("-"*15, "\n")
            header = ["Number Plate",  "Vehicle", "Booked on",  "Expire on", "duration", "Total Amount"]

            format_row = "{:^20}|" * len(header)
            print(format_row.format(*header))
            print("-"*125)
            if len(user[6]) > 0:
              for record in user[6]:
                
                start_date = record[-1][2][0:11]
                end_date = record[-1][3][0:11]
                duration = record[-1][1]
                vehicle = f"{record[2]} {record[3]}, {record[4]}"
                num_plate = record[1].upper()
                price_per_order = "RM " + "{:.2f}".format(record[8] * int(duration))

                print(format_row.format(num_plate, vehicle, start_date,end_date,str(duration) + " days", price_per_order))

    end = input("\n<Enter> to return...")
    clear()
    return end
# ---------------------------------------------------------------------------------
# USER INTERFACE
# ---------------------------------------------------------------------------------
def main():
  current_user = []
  clear()
  print('-'*30)
  print('Super Car Rental Service (SCRS)')
  print('-'*30)

  # main page without login
  while len(current_user) == 0:
    print('\n1. Login\n2. Register\n3. View Cars\n4. Feedback/Suggestion\n\n0. Quit\n')
    option = input('Please select a choice: ')

    while option == "4":
      clear()
      end = display_feedback()
      if end[0] == "":
        break

    while option == "3":
      clear()
      action = display_brand()

      if action[0] == "0":
        clear()
        break

      while action[0] != "0":
        clear()
        payload = int(action[0]) - 1
        brand = action[1][payload]
        print("-"*20)
        print(brand)
        print("-"*20, "\n")
        car_details(brand=brand)
        input("\nPress Enter to quit: ")
        clear()
        break       

    if option == "2":
      register()

    if option == "1":
      clear()
      print("LOGIN\n")
      username = input("Username: ")
      password = input("Password: ")

      login_user = login(username, password)

      if login_user == "":
        main()

      current_user.append(login_user)
      
    if option == "0":
      break

  # admin interface
  while len(current_user) > 0 and current_user[0][7].lower() == "admin":
    clear()
    print('-'*20)
    print('Super Car Rental Service (SCRS)')
    print('-'*20, "\n")
    print("Welcome, " + current_user[0][0].capitalize(), "\n")
    print("1. Add a Vehicle\n2. Modify a Vehicle\'s Details\n3. Update Personal Information\n4. Vehicle Rental Records\n5. Query Customer Record\n\n6. Assign a new administrator\n7. Customer Feedback\n\n0. Logout\n")
    admin_option = input("Please enter your choice: ")

    # Customer feedback
    while admin_option == "7":
      clear()
      end = display_feedback()

      if end[0] == "":
        break

    # Assign admin
    while admin_option == "6":
      clear()
      end = assign_admin()

      if end == "":
        break

    # customer record query 
    while admin_option == "5":
      clear()
      print("-"*20)
      print("SCRS Customer Records Management")
      print("-"*20, "\n")

      end = customer_query()

      if end == "":
        break

    # rental records
    while admin_option == "4":
      clear()
      print("-"*20)
      print("SCRS Vehicle Management")
      print("-"*20, "\n")

      print("1. Vehicles in transit\n2. Vehicles available for Rent\n3. Customer Payments for a specific time duration\n\n0.Back\n")
      record_option = input("Please enter your choice: ")      

      # return
      if record_option == "0":
        break

      # cars booked
      while record_option == "1":
        clear()
        end = rented_out()

        if end == "":
          clear()
          break     

      # cars available
      while record_option == "2":
        clear()
        end = rent_available()
        
        if end == "":
          break 

      # customer payments
      while record_option == "3":
        clear()
        end = customer_payment()

        if end == "":
          break

    # update personal info
    while admin_option == "3":
      action = display_user(current_user)
      payload = update_user(action, current_user)

      if payload == "":
        break

      if payload[0]:
        print(payload[1])
        input("<Enter> to continue")
        current_user[0] = []
        main()
      
      if not payload[0]:
        print(payload[1])
        current_user[0] = payload[2]
        choice = input("<Enter> to continue...")
        break

    # modify vehicle
    while admin_option == "2":
      data = select_car(modify_car)

      if data == "":
        break

    # add vehicle
    while admin_option == "1":
      data = add_car()

      if data == "":
        break

    # quit
    if admin_option == "0":
      current_user.clear()
      main() 
      break  

  # customer interface
  while len(current_user) > 0 and current_user[0][7].lower() != "admin":
    clear()
    print("-"*30)
    print("SUPER CAR RENTAL SERVICE")
    print("-"*30, "\n")
    print("Welcome, " + current_user[0][0].capitalize() + "\n")
    print('1. Rent a Car\n2. Update Personal Information\n3. Rental History\n4. Check Wallet\n5. Customer Feedback\n\n0. Logout\n')
    user_option = input("Please enter your choice: ")

    # feedback / suggestion
    while user_option == "5":
      clear()
      choice = display_feedback(current_user[0])
      if len(choice[1]) > 0:
        current_user[0] = choice[1]

      if choice[0] == "":
        break

    # check wallet
    while user_option == "4":
      end = modify_wallet(current_user)

      if end == 0:
        break 

    # rental history
    while user_option == "3":
      end = rental_history(current_user)

      if end == "":
        break

    # update personal info
    while user_option == "2":
      action = display_user(current_user)
      payload = update_user(action, current_user)

      if payload == "":
        break   

      if payload[0]:
        print(payload[1])
        input("<Enter> to continue")
        current_user[0] = []
        main()
      
      if not payload[0]:
        print(payload[1])
        current_user[0] = payload[2]
        choice = input("<Enter> to continue...")
        break
     
      if choice:
        break 

    # rent car
    while user_option == "1":
      clear()
      action = display_brand()

      if action[0] == "0":
        clear()
        break

      while action[0] != "0":
        clear()
        payload = int(action[0]) - 1
        car_details(brand=action[1][payload])
      
        while True:
          latest_id = vehicle_number()
          vehicle_id = input("\nSelect vehicle ID to modify or <Enter> to go back: ")

          if int(vehicle_id) <= latest_id:
            break

          print("Id does not exist, please try again\n")

        while len(vehicle_id) > 0:
          clear()
          status = rent_car(int(vehicle_id), current_user)

          if status == "":
            break

          try:
            if status[0]:
              print("\n", "-"*30)
              print(status[1])  
              print("-"*30, "\n") 
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
      current_user.clear()
      main() 
      break         

# ---------------------------------------------------------------------------------
rental_expire() # return car
main()