# python core Final project 

# Functional
This bot stores contacts and notes and allows adding, modifying, deleting, and searching. All information may be saved to o loaded from a JSON file. Intelligent suggestions are given for partly correct commands. Input erros are seamlessly processed.

## Contacts
Stored contacts have the following fields:
1. ID (automatically generated)
2. Name
3. Phones (10 digits)
4. Birthday (DD.MM.YYYY)
5. Address
6. e-mail

### The following commands are supported:
`hello` - Get a greeting    
`close` - Exit the program    
`exit` - Exit the program   
`help` - Show help    
`contact-add <contact_name> <phone_number>` - Adds contact with a phone number. Phone number must be 10 digits    
`contact-delete <id>` - Deletes contact data from book    
`contact-add-name <firstname> ... <lastname>` - Adds name to existing contact    
`contact-add-email <id> <email>` - Adds contact email    
`contact-add-address <id> <address_parapm_1> ...<address_param_8>` - Add address with up to 8 parts    
`contact-change-name <id> <firstname> ... <lastanme>` - Changes name of existing contact by ID    
`contact-change <contact_name> <old_phone_number> <new_phone_number>` - Change existing phone number for existing contact    
`contact-add-birthday <contact_name> <date>` - Add birthday data for existing contact or new contact with birthday only. Date format DD.MM.YYYY    
`contact-phone <contact_name>` - Displays phones for contact    
`contact-remove-phone <contact_name> <phone_number>` - Removes the phone number    
`contact-show-birthday <contact_name>` - Display birthday data for contact    
`birthdays <days>` - Shows contacts with birtdays within the specified number of days from now, 7 days if no value given    
`all` - Shows all available contacts    
`book-load <filename>` - loads data from json file. Default filename - data.bin    
`book-write <filename>` - writes book data into file. Default filename - data.bin    

## Notes
Notes are independent from contacts and have the following structure:
1. ID (automatically generated)
2. Title
3. Tags (multiple tags per note are allowed, tag length 3-20 characters)
4. Text (up to 256 characters)
5. Datestamp (date of note creation, automatically generated)
6. Timestamp (time of note creation, automatically generated)

### The following commands are supported
`note-add <note title> <note text>` - Add a note with the name    
`note-delete <note title>` - Delete the note with the title    
`note-add-tag <note title> <tag>` - Add a tag to a note    
`note-get-all` - Get a list of all notes    
`note-change-title <old title> <new title>` - change the note title    
`note-change-text <note title> <new text>` - Changes text in the specified note    
`note-delete-tag <note title> <tag>` - delete specified tag from the specified note    
`note-delete-all-tags <note title>` - remove all tags from the note     
`note-find-title <note title>` - Find note with the given title    
`note-find-tag <tag>` - Returns all notes with the given tag    
`note-find-id <id>` - Find note by id    
`note-sort` - Sort notes by number of tags in descending orde, then alphabetically by title    
`note-load` - Loads notes from a json file
`note-write` - Writes the notes to a json file
`note-get` - Get a note entry by its unique integer identifier or by its title
`note-edit` - Edit a note entry by its name
`note-get-tag` - Get a note entry (entries) by its tag
`note-rename` - Rename a note entry by its original title



Developed by T9:
- Yaroslav Tsarik
- Oleg Tkachuk
- Vasyl Pryimak
- Atem Rudyi
