from app.notepad import NotePad, Record, Title, Text, Tag

# The debugging section. It will be the last to be deleted.
print("Create notepad")
notepad = NotePad()

print("Add record 1")
record1 = Record("MyTitle-1")
print("Add record 2")
record2 = Record("MyTitle-2")

print("--------------------------")
tag4 = Tag('tag-4')
record3 = Record("MyTitle-2")
record3.add_tag(tag4)
notepad.add_record(record3)
print(record3)
print(notepad)
print("--------------------------")
print(record1)
print(record2)

print("Add tag 1")
tag1 = Tag('tag-1')
print("Add tag 2")
tag2 = Tag('tag-2')
print("Add tag 3")
tag3 = Tag('tag-3')

print("Add tag 1 to record 1")
record1.add_tag(tag1)
print("Add tag 2 to record 1")
record1.add_tag(tag2)
print("Add tag 3 to record 1")
record1.add_tag(tag3)

print("Add text 1")
text1 = Text('This text just for the debug')
print("Add text 1 to record 1")
record1.add_text(text1)
print(record1)
print(record2)

print("Editing text in record 1")
record1.edit_text("New text for the debug!!!")
print(record1)
print(record2)

print("Remove text from the record 1")
# record1.remove_text()
print(record1)
print(record2)

print("Add record 1 to notepad")
notepad.add_record(record1)
print(notepad)

print(f"DEBUG: find_record_by_title")
print(notepad.find_record_by_title('MyTitle-1'))

print("Add record 2 to notepad")
notepad.add_record(record2)
print(notepad)

print("Find a record by title")
title1 = notepad.find_record_by_title('MyTitle-1')
print(title1)
print(type(title1))

print("Find a record by unique id")
title2 = notepad.find_record_by_id(2)
print(title2)

print("Find a record by tag")
title3 = notepad.find_record_by_tag(Tag('tag-1'))
print(title3)

print("Remove all tags from the record 1")
record1.remove_all_tags()
print(record1)
print(record2)

print(type(Tag('tag1')))

print(Tag('tag-1') in [Tag('tag-1'), Tag('tag-2'), Tag('tag-3')])

print("Get all notes")
all_notes = notepad.get_all_records()
print(all_notes)

print("Rename title")
print(record2)
record2.rename_title('My renamed title')
print(record2)
all_notes = notepad.get_all_records()
print(all_notes)

for i in all_notes:
    print(i)
