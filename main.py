from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime
import pickle


class Books(ABC):
    @abstractmethod
    def add_record(self, data):
        pass

    @abstractmethod
    def save_ab(self):
        pass

    @abstractmethod
    def open_ab(self):
        pass


class Field:
    def __init__(self, value) -> None:
        self.__private_value = None
        self.value = value

    @property
    def value(self):
        return self.__private_value

    @value.setter
    def value(self, value):
        self.__private_value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        right_len = len(value) == 10 or len(value) == 12
        if value.isdigit() and right_len:
            Field.value.fset(self, value)
        else:
            raise Exception("Wrong number")


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            Field.value.fset(self, value)
        except ValueError:
            print("Wrong date format. Should be dd.mm.yyyy")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = list()
        self.birthday = birthday
        if phone:
            self.phones.append(phone)

    def change_phone(self, old_phone, new_phone):
        index = self.phones.index(old_phone)
        self.phones[index] = new_phone

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def days_to_birthday(self):
        if self.birthday.value:
            birthday_date = datetime.strptime(self.birthday.value, "%d.%m.%Y")
            current_date = datetime.now()
            birthday_date = birthday_date.replace(year=current_date.year)
            delta_days = birthday_date - current_date

            if delta_days.days > 0:
                return delta_days.days
            else:
                birthday_date = birthday_date.replace(year=current_date.year + 1)
                delta_days = birthday_date - current_date
                return delta_days.days


class AddressBook(UserDict, Books):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return self.data

    def iterator(self, n):
        result = dict(list(self.data.items())[0:n])
        yield result

    def save_ab(self):
        dict_to_save = {}
        for k, v in self.data.items():
            if v.birthday == None:
                dict_to_save[k] = v.phones[0].value
            else:
                dict_to_save[k] = (v.phones[0].value, v.birthday.value)

        with open("addressbook.bin", "wb") as file:
            pickle.dump(dict_to_save, file)

    def open_ab(self):
        with open("addressbook.bin", "rb") as file:
            unpacked = pickle.load(file)
            return unpacked

    def find_user(self, search_str: str):
        result = []
        for k, v in self.data.items():
            if search_str in k or search_str in v.phones[0].value:
                result.append((k, v.phones[0].value))
        return result


if __name__ == "__main__":
    # pass
    nm = Name("Ivan")
    ph = Phone("380965050500")
    # bd = Birthday("03.07.1991")
    rec = Record(nm, ph)

    nm_2 = Name("Bill")
    ph_2 = Phone("0966050500")
    bd_2 = Birthday("03.07.1998")
    rec_2 = Record(nm_2, ph_2, bd_2)

    nm_3 = Name("Will")
    ph_3 = Phone("0986050500")
    bd_3 = Birthday("03.07.1998")
    rec_3 = Record(nm_3, ph_3, bd_3)

    ab = AddressBook()
    ab.add_record(rec)
    ab.add_record(rec_2)
    ab.add_record(rec_3)

    # print(ab[nm.value].birthday.value)
    # print(rec.days_to_birthday())
    # print(next(ab.iterator(3)))

    ab.save_ab()
    print(ab.open_ab())
    print(ab.find_user("09660"))
    print(ab.find_user("Iva"))
