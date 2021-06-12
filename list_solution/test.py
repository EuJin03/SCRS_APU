dota_teams = ["Liquid", "Virtus.pro", "PSG.LGD", "Team Secret"] 

data = [[1, 2, 1, 'x'],
['x', 1, 1, 'x'],
[1, 'x', 0, 1],
[2, 0, 2, 1]] 

format_row = "{:>12}" * (len(dota_teams) + 1)

print(format_row.format("", *dota_teams))


for team, row in zip(dota_teams, data):
  print(format_row.format("", *row))


# print(f"Number plate: {num_plate}")
#           print(f"{vehicle}")
#           print(f"Order booked on {start_date}for {duration} days")
#           print(f"Total spent: RM{price_per_order}")
#           print(f"Expire on {end_date}\n")


format_row = "{:^20}|" * len(header)
header = ["Number Plate",  "Vehicle", "Booked on",  "Expire on", "duration", "Total Amount"]

format_row = "{:^20}|" * len(header)
print(format_row.format(*header))
print("-"*125)
if len(user[-2]) > 0:
  for record in user[-2]:
    
    start_date = record[-1][2][0:11]
    end_date = record[-1][3][0:11]
    duration = record[-1][1]
    vehicle = f"{record[2]} {record[3]}, {record[4]}"
    num_plate = record[1].upper()
    price_per_order = "RM " + "{:.2f}".format(record[8] * int(duration))

    print(format_row.format(num_plate, vehicle, start_date,end_date,str(duration) + " days", price_per_order))

header = ["Number Plate",  "Vehicle", "Booked on",  "Expire on", "Owner", "Total Amount", "Rented By"]

format_row = "{:^20}|" * len(header)

booking_details = car[-1]
num_plate = car[1].upper()
vehicle = car[2].capitalize() + car[3].capitalize() + ", " + str(car[4])
owner = car[5]
price_rate = car[8]
start_date = booking_details[2][0:11]
end_date = booking_details[3][0:11]
username = booking_details[0]
duration = booking_details[1]

total_price = "{:.2f}".format(int(duration) * float(price_rate))

print(format_row.format(num_plate, vehicle, start_date,end_date, owner, total_price, username))