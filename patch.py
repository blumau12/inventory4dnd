from inv4dnd_classes import *

old_characters = []
new_characters = []

open_all(old_characters)


def verify_attr(old_object, attr_name, new_object):
    if hasattr(old_object, attr_name):
        setattr(new_object, attr_name, getattr(old_object, attr_name))


for old_character in old_characters:
    new_character = Character(old_character.name)
    attrs = ['name', 'container', 'total_cost', 'total_weight', 'company', 'is_displayed', 'image', 'categories_hidden',
             'dark_vision', 'concentration', 'exhausted', 'passive_perception', 'hp_total', 'hp_temp', 'states',
             'saving_throws', 'armor', 'armor_temp', 'exp', 'stabilization', 'abilities', 'conditions',
             'spell_saving_throws', 'hit_dices']
    for attr in attrs:
        verify_attr(old_character, attr, new_character)
    new_characters.append(new_character)

    for category in old_character.container:
        for item in old_character.container[category]:
            new_item = Item(item.category, item.name, item.cost, item.weight)
            attrs = ['category', 'name', 'cost', 'weight', 'description', 'amount', 'owner', 'label', 'num_entry', 'old_data']
            for attr in attrs:
                verify_attr(item, attr, new_item)
            new_character.add_item(new_item)


save_all(new_characters)
