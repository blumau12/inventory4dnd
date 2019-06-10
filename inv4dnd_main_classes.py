import tkinter as tk


class Character:
    def __init__(self, name='Character Name'):
        super().__init__()
        self.name = name
        self.container = {}
        self.total_cost = 0
        self.total_weight = 0
        self.company = None

        self.is_displayed = False
        self.image = None
        self.categories_hidden = []

        self.dark_vision = False
        self.concentration = False
        self.exhausted = False
        self.passive_perception = 0
        self.hp_total = [0, 0]
        self.hp_temp = [0, 0]
        self.states = {'Strength': 0, 'Dexterity': 0, 'Constitution': 0, 'Intelligence': 0, 'Wisdom': 0, 'Charisma': 0}
        self.saving_throws = 0
        self.armor = [0, 0, 0, 0, 0, 0]
        self.armor_temp = [0, 0, 0, 0, 0, 0]
        self.exp = [0, 0]
        self.stabilization = [0, 0]
        self.abilities = {'class': {'active': [], 'passive': []}, 'race': {'active': [], 'passive': []},
                          'spellcells': {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}}
        self.conditions = []
        self.spell_saving_throws = []
        self.hit_dices = [0, 0]

    def change_name(self, new_name):
        self.name = new_name

    def add_item(self, item):
        if item.category in self.container:
            for existing_item in self.container[item.category]:
                if item.name == existing_item.name:
                    item.name += ' +'
            self.container[item.category].append(item)
        else:
            self.container[item.category] = [item]
        item.owner = self
        self.calculate_cost_weight()
        if self.image:
            self.image.refresh()
        if item.label:
            item.label['fg'] = '#ff7200'

    def remove_item(self, item):
        self.container[item.category].remove(item)
        if not self.container[item.category]:
            del self.container[item.category]
        self.calculate_cost_weight()
        self.image.refresh()

    def calculate_cost_weight(self):
        self.total_cost = 0
        self.total_weight = 0
        for category in self.container:
            for item in self.container[category]:
                self.total_cost += item.cost * item.amount
                self.total_weight += item.weight * item.amount
        if not self.total_cost % 1:
            self.total_cost = int(self.total_cost)
        if not self.total_weight % 1:
            self.total_weight = int(self.total_weight)
        self.total_cost = round(self.total_cost, 2)
        self.total_weight = round(self.total_weight, 2)

    def __repr__(self):
        return self.name


class Item:
    def __init__(self, category, name, cost, weight):
        self.category = category
        self.name = name
        self.cost = cost
        self.weight = weight

        self.description = ''

        self.amount = 1
        self.owner = None
        self.label = None
        self.num_entry = None
        self.old_data = str(self.amount)

    def start(self, event):
        self.old_data = event.widget.get()
        event.widget.focus()
        event.widget.delete(0, tk.END)
        event.widget.icursor(0)

    def take_entry(self, event):
        data = event.widget.get()
        if not data:
            event.widget.insert(0, self.old_data)
        else:
            if can_be_num(data):
                event.widget['bg'] = 'SystemMenu'
                self.label['fg'] = 'black'
                self.amount = str_to_simpl_num(data)
                self.owner.image.refresh_total_values()
            else:
                event.widget['bg'] = 'red'
                event.widget.delete(0, tk.END)
                event.widget.insert(0, self.old_data)

    def increase_amount(self):
        self.amount = round(self.amount + 1, 2)
        self.num_entry['bg'] = 'SystemMenu'
        self.label['fg'] = 'black'
        self.owner.image.refresh_total_values()
        self.num_entry.delete(0, tk.END)
        self.num_entry.insert(0, self.amount)

    def decrease_amount(self):
        self.amount = round(self.amount - 1, 2)
        self.num_entry['bg'] = 'SystemMenu'
        self.label['fg'] = 'black'
        self.owner.image.refresh_total_values()
        self.num_entry.delete(0, tk.END)
        self.num_entry.insert(0, self.amount)

    def unfocus(self, event):
        event.widget.master.focus()

    def context_menu(self, event):
        menu = tk.Menu(self.label.master, tearoff=0)
        menu.add_command(label='Изменить описание', command=lambda: EditItemDescriptionWindow(self.label.master, self))
        menu.add_command(label='Отдать', command=lambda: MoveItemWindow(self.label.master, self))
        menu.add_command(label='Удалить "{0}"'.format(self.name), command=lambda: self.owner.remove_item(self))
        menu.post(event.x_root, event.y_root)

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return other.name < self.name


class EditItemDescriptionWindow(tk.Toplevel):
    def __init__(self, root, item):
        super().__init__(root)
        self.title('Edit '+item.name+' description')
        self.geometry('400x200+400+400')
        self.grab_set()
        self.focus_set()
        self.item = item

        self.text = tk.Text(self)
        self.text.insert(1.0, self.item.description)
        self.text.place(relwidth=1, width=-40, relheight=1)

        tk.Button(self, bg='#22B14C', activebackground='#00CC00', text='Ok', fg='white', activeforeground='white',
                  bd=0, command=self.apply).place(relx=1, x=-40, width=40, relheight=1)

    def apply(self):
        self.item.description = self.text.get(1.0, tk.END).strip()
        if self.item.description:
            if not (self.item.name[::-1].startswith('...')):
                self.item.name += '...'
        else:
            self.item.name = self.item.name[::-1].replace('...', '', 1)[::-1]
        self.item.label.master.master.refresh()
        self.destroy()


class MoveItemWindow(tk.Toplevel):
    def __init__(self, root, item):
        super().__init__(root)
        self.title('Move '+item.name)
        self.geometry('400x200+400+400')
        self.grab_set()
        self.focus_set()
        self.item = item

        scrollbar_src = tk.Scrollbar(self, orient=tk.VERTICAL, bd=0)
        self.characters_lb = tk.Listbox(self, yscrollcommand=scrollbar_src.set, activestyle='none', bd=0)
        self.characters_lb.place(relwidth=1, width=-40, relheight=1)
        scrollbar_src.config(command=self.characters_lb.yview)
        scrollbar_src.place(x=250, y=0, relheight=1, height=-40)

        for character in self.master.master.all_characters:
            if character is not self.master.master.owner:
                self.characters_lb.insert(tk.END, character)

        tk.Button(self, bg='#22B14C', activebackground='#00CC00', text='Ok', fg='white', activeforeground='white',
                  bd=0, command=self.apply).place(relx=1, x=-40, width=40, relheight=1)

    def apply(self):
        if not self.characters_lb.curselection():
            return
        old_owner = self.item.owner
        self.item.owner.container[self.item.category].remove(self.item)
        if not self.item.owner.container[self.item.category]:
            self.item.owner.container.pop(self.item.category)

        new_char_name = self.characters_lb.get(self.characters_lb.curselection())
        new_char = [char for char in self.master.master.all_characters if char.name == new_char_name]
        if new_char:
            new_char = new_char[0]
            new_char.add_item(self.item)

        old_owner.image.refresh()
        self.destroy()


def str_to_simpl_num(data):
    data = data.replace(',', '.')
    try:
        data = float(data)
        if data.is_integer():
            data = int(data)
        return data
    except ValueError:
        return 0


def can_be_num(data):
    data = data.replace(',', '.')
    try:
        float(data)
        return True
    except ValueError:
        return False
