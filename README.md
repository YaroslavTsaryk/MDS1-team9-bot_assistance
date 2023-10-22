"# goitneo-python-hw-3-group-5" 

Commands:

load - load data from json file. Default filename - data.bin
load <filename> - load data from specified json file
write - write book data into file. Default filename - data.bin
write <filename> - write data to cpecified json file
add <contact_name> <phone_number> - Add contact with a phone number. Phone number must be 10 digits
change <contact_name> <old_phone_number> <new_phone_number> - Change existing phone number for existing contact
add-birthday <contact_name> <date> - Add birthday data for existing contact or new contact with birthday only. Date format DD.MM.YYYY
phone <contact_name> - Display phones for contact
show-birthday <contact_name> - Display birthday data for contact
birthdays - Show birtdays for next 7 days
birthdays <date> - Show birtdays for next 7 days from selected date. Date format DD.MM.YYYY
delete <contact_name> - Delete contact data from book


Example:
load
add John 1234567891
add John 1122334451
add Jane 1112223331
change Jane 1112223334 2233442233
add-birthday John 22.10.1990
phone John
add-birthday Diana 15.10.1995
show-birthday Diana
show-birthday Jane
all
birthdays
birthdays 14.10.2023
remove-phone John 1234567890
all
delete John
all
write