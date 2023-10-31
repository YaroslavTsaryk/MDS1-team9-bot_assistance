import re
from datetime import datetime, date
from collections import UserDict, defaultdict


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
        self.is_valid_title(title)
        super().__init__(title)
        self.__title_min_length = 3
        self.__title_max_length = 50

    def is_valid_title(self, title: str):
        if not title:
            raise IncorrectTitleException("the required title is missing")
        if self.__title_min_length < len(title) < self.__title_max_length:
            raise IncorrectTitleException(
                f"the title must be {self.__title_min_length} to {self.__title_max_length} characters long ")


class Tag(Field):
    def __init__(self, tag: str):
        self.is_valid_tag(tag)
        super().__init__(tag)
        self.__tag_min_length = 3
        self.__tag_max_length = 20

    def update_value(self, new_value: str):
        self.is_valid_tag(new_value)
        self.value = new_value

    def is_valid_tag(self, tag: str):
        if not tag:
            raise IncorrectTagException("the required tag is missing")
        if self.__tag_min_length < len(tag) < self.__tag_max_length:
            raise IncorrectTagException(
                f"the tag must be {self.__tag_min_length} to {self.__tag_max_length} characters long ")


class Text(Field):
    def __init__(self, text: str):
        self.is_valid_text(text)
        super().__init__(text)
        self.__text_min_length = 0
        self.__text_max_length = 256

    def is_valid_text(self, text: str):
        if not text:
            raise IncorrectTextException("missing required text")
        if self.__text_min_length < len(text) < self.__text_max_length:
            raise IncorrectTagException(
                f"the text must be {self.__text_min_length} to {self.__text_max_length} characters long ")


class Record:
    record_auto_id = 0

    def __init__(self, title: Title, text: Text):
        Record.record_auto_id += 1
        self.record_auto_id = Record.record_auto_id
        self.tags: list[Tag] = []
        self.text: Text = text
        self.title: Title = title

    def __str__(self):
        return f"Id: {self.record_auto_id}, Title: {self.title.value}, Tags: {'; '.join(p.value for p in self.tags)}, Text: {self.text.value}"

    def add_tag(self, tag: Tag):
        self.tags.append(tag)

    def remove_tag(self, tag: Tag):
        found = list(filter(lambda p: str(p) == str(tag), self.tags))
        for i in found:
            self.tags.remove(i)


class NotePad(UserDict):
    def __init__(self):
        self.data = list()

    def add_record(self, record: Record):
        self.data.append(record)

    def find(self, title: Title):
        result = list(filter(lambda record: str(record.title).lower()
                             == str(title).lower(), self.data))
        return result[0] if result else None

    def delete(self, title: Title):
        result = self.find(title)
        if result:
            self.data.remove(result)
