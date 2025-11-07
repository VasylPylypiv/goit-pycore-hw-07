import datetime
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if (len(value) != 10 or not value.isdigit()):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.datetime.strptime(value, '%d.%m.%Y').date()
            super().__init__(self.value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone number {phone} not found")

    def edit_phone(self, old_phone, new_phone):
        # Перевіряємо новий телефон через клас Phone
        try:
            Phone(new_phone)  # Якщо номер невалідний, згенерується помилка
        except ValueError:
            raise ValueError(f"New phone number '{new_phone}' is invalid.")

        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone
        else:
            raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"
    

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact {name} not found")
        
    def get_upcoming_birthdays(self):
        congratulations_list = []
        today = datetime.date.today()
        current_year = today.year

        for record in self.data.values():
            if record.birthday:
                try:
                    birthday_this_year = record.birthday.value.replace(year=current_year)

                    if birthday_this_year < today:
                        birthday_this_year = birthday_this_year.replace(year=current_year + 1)

                    seven_days_later = today + datetime.timedelta(days=7)

                    if today <= birthday_this_year <= seven_days_later:
                        if birthday_this_year.weekday() == 5:
                            congratulation_date = birthday_this_year + datetime.timedelta(days=2)
                        elif birthday_this_year.weekday() == 6:
                            congratulation_date = birthday_this_year + datetime.timedelta(days=1)
                        else:
                            congratulation_date = birthday_this_year

                        congratulations_list.append({
                            'name': record.name.value,
                            'congratulation_date': congratulation_date.strftime('%d.%m.%Y')
                        })

                except ValueError:
                    continue

        return congratulations_list