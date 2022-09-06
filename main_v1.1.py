#!/usr/bin/env python

'''
Author: Bram Schork
Date: 05-Sep-2022
Version: v1.1

Copyright (C) 2022 Bram Schork - All Rights Reserved
 * For questions contact bram@bramschork.com
'''
 
 
# Imports
import pandas as pd
from datetime import date
import tkinter as tk
from tkinter import filedialog
import os

# Define tkinter main window
root = tk.Tk()
root.withdraw()

# Get file path of CSV input data
file_path = filedialog.askopenfilename()

# Get current working directory
cwd = os.getcwd() 

# Read data from input data

df = pd.read_csv(file_path)
# Get current month and day | MM-DD-YY
today = date.today().strftime("%m/%d")
year = int(date.today().strftime('%Y'))

class Solution(object):
   def romanToInt(self, s):
      """
      :type s: str
      :rtype: int
      """
      roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,'IV':4,'IX':9,'XL':40,'XC':90,'CD':400,'CM':900}
      i = 0
      num = 0
      while i < len(s):
         if i+1<len(s) and s[i:i+2] in roman:
            num+=roman[s[i:i+2]]
            i+=2
         else:
            num+=roman[s[i]]
            i+=1
      return num

### CONVERT THE FORM TO INTEGERS AND ADD GRADUATING YEAR###
int_list = []
grad_years = []
roman_list = list(df['form'])
repeat = []
for item in roman_list:
    ob1 = Solution()
    item = ob1.romanToInt(item)
    int_list.append(item)
    
    grad_year = year+(7-item)
    grad_years.append(grad_year)
    
    repeat.append(grad_year-year)

df['repeat'] = repeat
df['form'] = int_list
df['graduating'] = grad_years

########### EMAILS ###########
names = list(df["name"])
emails = []
subjects = []
for name in names:
    name = name.replace(' ', '')
    last_name, first_name = name.split(',')
    email = first_name[0:4] + last_name[0:4] + '@haverford.org'
    email = email.lower()
    emails.append(email)
    subjects.append("{} {}'s Birthday!".format(first_name, last_name))
df['email'] = emails

### edit the birthdays and add the number of times to put on Calendar
birthdays = list(df['birthday'])
short_bday = []
for day in birthdays:
    short_bday.append(day[0:5])
df['short_bday'] = short_bday


#### DELETING DUPLICATES ####
duplicate = df
duplicate = duplicate.drop(columns=['form', 'repeat', 'graduating', 'email','short_bday'])
duplicate = duplicate[duplicate.duplicated()]

deletes = duplicate.index.to_list()

df = df.drop(deletes)
calendarEvents = pd.DataFrame(columns=['Subject', 'All Day Event', 'Start Date', 'Description'])

currentStudents = df.loc[df['graduating'] >= year]
currentStudents = currentStudents.reset_index()  # make sure indexes pair with number of rows
for index, row in currentStudents.iterrows():
    name = row['name']
    name = name.replace(' ', '')
    last_name, first_name = name.split(',')
    repeat = row['repeat']
    short_bday = row['short_bday']
    email = row['email']
    
    description = email
    
    rows = []
    
    i = 0
    while i < repeat:
        addition = ["{} {}'s Birthday!".format(first_name, last_name), 'True', short_bday + '/' + str(year+i), description]
        rows.append(list(addition))
        i += 1
    for item in rows:
        calendarEvents.loc[len(calendarEvents.index)] = item

calendarEvents.to_csv(cwd + '/OUTPUT_CalendarEvents.csv', index=False)
