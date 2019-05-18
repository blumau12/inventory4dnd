from classes import *

old_characters = []
new_characters = []

open_all(old_characters)


for old_character in old_characters:  # в чарах
    new_character = Character(old_character.name)
    new_characters.append(new_character)

    for category in old_character.container:  # в категориях
        for item in old_character.container[category]:  # в предметах
            new_character.add_item(Item(item.category, item.name, item.cost, item.weight))


save_all(new_characters)
