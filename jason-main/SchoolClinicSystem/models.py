from abc import ABC, abstractmethod

class Person:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    def get_full_name(self):
        return f"{self._first_name} {self._last_name}"


class Student(Person):
    def __init__(
        self,
        first_name,
        last_name,
        student_id,
        contact_number=""
    ):
        super().__init__(first_name, last_name)
        self.student_id = student_id
        self.contact_number = contact_number

    def get_person_type(self):
        return "Student"


class Faculty(Person):
    def __init__(
        self,
        first_name,
        last_name,
        employee_id,
        contact_number=""
    ):
        super().__init__(first_name, last_name)
        self.employee_id = employee_id
        self.contact_number = contact_number

    def get_person_type(self):
        return "Faculty"


class Patient:
    def __init__(
        self,
        patient_id,
        first_name,
        last_name,
        patient_type,
        contact_number=""
    ):
        self.__patient_id = patient_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__patient_type = patient_type
        self.__contact_number = contact_number

    @property
    def patient_id(self):
        return self.__patient_id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def patient_type(self):
        return self.__patient_type

    @property
    def contact_number(self):
        return self.__contact_number

    def get_full_name(self):
        return f"{self.__first_name} {self.__last_name}"



class MedicalSupply(ABC):
    def __init__(
        self,
        name,
        category,
        quantity,
        unit,
        expiration_date=""
    ):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.unit = unit
        self.expiration_date = expiration_date

    def get_status(self):
        if self.quantity <= 5:
            return "LOW STOCK"
        return "OK"

    @abstractmethod
    def get_supply_type(self):
        pass


class Medicine(MedicalSupply):
    def get_supply_type(self):
        return "Medicine"


class FirstAidItem(MedicalSupply):
    def get_supply_type(self):
        return "First Aid Item"


def display_person(person):
    return f"{person.get_full_name()} - {person.get_person_type()}"

def display_supply(supply):
    return f"{supply.name} - {supply.get_supply_type()} - {supply.get_status()}"    