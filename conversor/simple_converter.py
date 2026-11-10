# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 18:20:56 2020

@author: alvar
"""

# de centímetros a pulgadas
# de pulgadas a centímetros
# de segundos a horas, minutos y segundos
# de horas, minutos y segundos a segundos

menu = """    This is a converter. Select your option:
    1. From inches to centimeters
    2. From centimeters to inches
    3. From seconds to hours, minutes & seconds
    4. From hours, minutes & seconds to hours
    """

def inches_cm(num):
    answer = input("Do you want to convert inches to cm? (y/n) ".lower())
    if answer == "y":
        cm = num * 2.54
        print(num, "inches are", cm, "cm.")
       
def cm_inches(num):
    answer = input("Do you want to convert cm to inches? (y/n) ".lower())
    if answer == "y":
        inches = num / 2.54
        print(num, "cm are", inches, "inches.")

def to_hours(seconds):
    print("\n", seconds, "seconds...")
    s = seconds % 60
    m = (seconds // 60) % 60
    h = (seconds // 60) // 60
    print("...", int(h), "hours", int(m), "minutes", int(s), "seconds")
    
def to_seconds(hours, minutes, seconds):
    print("\n",hours, "hours", minutes, "minutes", seconds, "seconds are...")
    time = int(hours * 60 * 60 + minutes * 60 + seconds)
    print("...",time, "seconds")



print(menu)
opt = int(input("Option: "))


if opt == 1:
    num = float(input("What number do you want to convert?: "))
    inches_cm(num)
if opt == 2:
    num = float(input("What number do you want to convert?: "))
    cm_inches(num)
if opt == 3:
    s = float(input("Introduce number of seconds: "))
    to_hours(s)
if opt == 4:
    h = float(input("Introduce number of hours: "))
    m = float(input("Introduce number of minutes: "))
    s = float(input("Introduce number of seconds: "))
    to_seconds(h,m,s)





