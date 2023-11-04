import re
from datetime import datetime
from collections import UserDict


class IncorrectTagException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return (
            "{:<7} {} {}".format(
                "[error]",
                "Incorrect tag:",
                self.message))


class IncorrectTitleException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return (
            "{:<7} {} {}".format(
                "[error]",
                "Incorrect title:",
                self.message))


class IncorrectTextException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return (
            "{:<7} {} {}".format(
                "[error]",
                "Incorrect text:",
                self.message))


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Title(Field):
    def __init__(self, title: str):
        Title.is_valid_title(title)
        super().__init__(title)

    def __eq__(self, other):
        if isinstance(other, Title):
            return self.value == other.value
        return False

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
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: Tag):
        found = list(filter(lambda p: p == tag, self.tags))
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

    def __eq__(self, other):
        if isinstance(other, Title):
            return self.value == other.value
        if isinstance(other, Text):
            return self.value == other.value
        if isinstance(other, Tag):
            return self.value == other.value
        return False

    def add_record(self, record: Record):
        self.data.append(record)

    def find_record_by_title(self, title: Title):
        result = list(filter(lambda record: title == record.title, self.data))
        return result[0] if result else None

    def find_record_by_tag(self, tag: Tag):
        result = list(filter(lambda record: tag in record.tags, self.data))
        return result if result else None

    def find_record_by_id(self, record_auto_id: int):
        result = list(
            filter(
                lambda record: record.record_auto_id == record_auto_id,
                self.data))
        return result[0] if result else None

    def find_record_by_text(self, text):
        result = list(filter(lambda record: str(text).lower() in str(record.text).lower(), self.data))
        return result if result else None

    def get_all_records(self):
        return [str(record) for record in self.data]

    def delete(self, title: Title):
        result = self.find_record_by_title(title)
        if result is None:
            return False
        else:
            self.data.remove(result)
            return True
