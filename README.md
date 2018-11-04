# Teratyping

Generate [trafaret](https://github.com/Deepwalker/trafaret) from `__init__` class & add method `init_from_dict` 

# Example

~~~
import typing

from traftyping.base_traftyping import BaseTraftyping


class Pet:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class Apartment(BaseTraftyping):
    def __init__(self, street: str, number_room: int, pets: typing.List[Pet]):
        self.street = street
        self.number_room = number_room
        self.pets = pets


my_appartament = Apartment.init_from_dict({
    "street": "Pushkino",
    "number_room": "228",
    "pets": [
        {
            "name": "Pushok",
            "age": "6"
        },
        {
            "name": "Mr.Pickles",
            "age": "2"
        }
    ]
})

print(f"Steet {my_appartament.street}")
print(f"number room {my_appartament.number_room}")
print("List pets:")
for pet in my_appartament.pets:
    print(f"Age {pet.age}; Name {pet.name}")

>> Steet Pushkino
>> number room 228
>> List pets:
>> Age 6; Name Pushok
>> Age 2; Name Mr.Pickles
~~~
