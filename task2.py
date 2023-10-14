from collections import UserDict
import operator

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
    def __init__(self, Field):
        self.value = Field

class Phone(Field):
    # реалізація класу
    def __init__(self, Field):
        self.value = Field
    
    @property
    def value(self):
        return self._value
    
    @value.setter        
    def value(self, v):
        if len(v) != 10: raise Exception("value must be 10 digits")
        self._value = v
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, value):
        field=Phone(value)
        self.phones.append(field)
    def remove_phone(self, value):
        res=""
        for ph in self.phones:
            if ph.value==value:
                res=ph.value
        if res:
            self.phones.remove(res)
    def edit_phone(self, old_value, new_value):
        for ph in self.phones:
            if ph.value==old_value:
                ph.value=new_value
    def find_phone(self, value):
        for ph in self.phones:
            if ph.value==value:
                return ph
        return None

    # реалізація класу

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    # реалізація класу
    def add_record(self, record):
        self.data[record.name]=record
    def find(self, name):
        for n in self.data.keys():
            if n.value==name:
                return self.data[n]
        return None
    def delete(self, name):
        for n in self.data.keys():
            if n.value==name:
                res=n
        del self.data[res]

    
    
    
def main():    
     # Створення нової адресної книги
    book = AddressBook()
    
    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    #john_record.add_phone("55555555551")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)


    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
        
    for name, record in book.data.items():
        print(record)
        
if __name__ == "__main__":
    main()
