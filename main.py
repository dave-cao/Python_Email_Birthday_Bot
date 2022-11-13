import datetime as dt
import random
import smtplib

import pandas

with open("./.credentials.txt") as file:
    my_email = file.readline()
    password = file.readline()

# Current dates
now = dt.datetime.now()
current_month = now.month
current_day = now.day
data = pandas.read_csv("./birthdays.csv")


# Grab birthdays from dictionary (account for same birthdays)
birthday_months = data[data["month"] == current_month].iterrows()
birthday_list = [
    {"name": key["name"], "email": key["email"]}
    for (_, key) in birthday_months
    if key.day == current_day
]


# Load letters into list
letters = []
if birthday_list:
    for i in range(1, 4):
        with open(f"./letter_templates/letter_{i}.txt") as file:
            letters.append(file.read())

    # Pick a random letter
    for birthday in birthday_list:
        letter = random.choice(letters)
        letter = letter.replace("[NAME]", birthday["name"])

        # email the letter to person
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=birthday["email"],
                msg=f"Subject:Happy Birthday!\n\n{letter}",
            )
