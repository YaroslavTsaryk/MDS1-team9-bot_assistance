import re
from datetime import datetime
from collections import UserDict


class IncorrectTagException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Incorrect tag: {self.message}"


class IncorrectTitleException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Incorrect title: {self.message}"


class IncorrectTextException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Incorrect text: {self.message}"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Title(Field):
    def __init__(self, title: str):
        Title.is_valid_title(title)
        super().__init__(title)

    @staticmethod
    def is_valid_title(title: str):
        title_min_length = 3
        title_max_length = 50
        if not title:
            raise IncorrectTitleException("the required title is missing")
        if not title_min_length <= len(title) <= title_max_length:
            raise IncorrectTitleException(
                f"the title must be {title_min_length} to {title_max_length} characters long ")


class Tag(Field):
    def __init__(self, tag: str):
        Tag.is_valid_tag(tag)
        super().__init__(tag)

    def __eq__(self, other):
        if isinstance(other, Tag):
            return self.value == other.value
        return False

    def update_value(self, new_value: str):
        self.is_valid_tag(new_value)
        self.value = new_value

    @staticmethod
    def is_valid_tag(tag: str):
        tag_min_length = 3
        tag_max_length = 20
        pattern = r'^[a-zA-Z0-9-_]+$'
        if not tag:
            raise IncorrectTagException("the required tag is missing")
        if not re.match(pattern, tag):
            raise IncorrectTagException(
                f"the tag must contain only letters, numbers and symbols '_' and '-'")
        if not tag_min_length <= len(tag) <= tag_max_length:
            raise IncorrectTagException(
                f"the tag must be {tag_min_length} to {tag_max_length} characters long ")


class Text(Field):
    def __init__(self, text: str):
        Text.is_valid_text(text)
        super().__init__(text)

    def __eq__(self, other):
        if isinstance(other, Text):
            return self.value == other.value
        return False

    @staticmethod
    def is_valid_text(text: str):
        text_min_length = 0
        text_max_length = 256
        if not text:
            raise IncorrectTextException("the required text is missing")
        if not text_min_length <= len(text) <= text_max_length:
            raise IncorrectTextException(
                f"the text must be {text_min_length} to {text_max_length} characters long ")


class Record:
    record_auto_id = 0

    def __init__(self, title):
        Record.record_auto_id += 1
        self.record_auto_id = Record.record_auto_id
        self.title: Title = title
        self.text: Text = None
        self.tags: list[Tag] = []
        self.timestamp = datetime.now().time()
        self.datestamp = datetime.now().date()

    def __str__(self):
        return f"Id: {self.record_auto_id}, Title: '{self.title}', Tags: '{', '.join(p.value for p in self.tags)}', Text: '{self.text}', Datestamp: {self.datestamp}, Timestamp: {self.timestamp}"

    def add_tag(self, tag: Tag):
        self.tags.append(tag)

    def remove_tag(self, tag: Tag):
        found = list(filter(lambda p: str(p) == str(tag), self.tags))
        for i in found:
            self.tags.remove(i)

    def remove_all_tags(self):
        self.tags.clear()

    def add_text(self, text: Text):
        self.text = text

    def remove_text(self):
        self.text = None

    def edit_text(self, new_text: Text):
        self.text = new_text

    def rename_title(self, new_title: Title):
        self.title = new_title


class NotePad(UserDict):
    def __init__(self):
        self.data = list()

    def add_record(self, record: Record):
        self.data.append(record)

    def find_record_by_title(self, title: Title):
        result = list(filter(lambda record: title == record.title, self.data))
        return result[0] if result else None

    def find_record_by_tag(self, tag: Tag):
        result = list(filter(lambda record: tag in record.tags, self.data))
        return result[0] if result else None

    def find_record_by_id(self, record_auto_id: int):
        result = list(
            filter(
                lambda record: record.record_auto_id == record_auto_id,
                self.data))
        return result[0] if result else None

    def get_all_records(self):
        return [str(record) for record in self.data]


    def delete(self, title: Title):
        result = self.find_record_by_title(title)
        if result:
            self.data.remove(result)


# The debugging section. It will be the last to be deleted.
print("Create notepad")
notepad = NotePad()

print("Add record 1")
record1 = Record("MyTitle-1")
print("Add record 2")
record2 = Record("MyTitle-2")
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
record1.remove_text()
print(record1)
print(record2)

print("Add record 1 to notepad")
notepad.add_record(record1)
print(notepad)

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
