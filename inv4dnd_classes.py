from inv4dnd_main_classes import *
from tkinter import messagebox
import pickle
import utilities.pop_up_desc as pop_up_desc


class CharacterImage(tk.Frame):
    def __init__(self, root, listbox, number, all_characters, custom_item_frame, search_frame,
                 select_listbox_menubutton):
        super().__init__(root, bg='#DDD')

        self.root = root
        self.listbox = listbox
        self.all_characters = all_characters
        self.custom_item_frame = custom_item_frame
        self.search_frame = search_frame
        self.select_listbox_menubutton = select_listbox_menubutton
        self.owner = None
        self.states = ['inventory', 'states']
        self.state = 0
        self.states_label = None

        self.name_label = tk.Button(self, bd=0, bg='#EEE', justify=tk.CENTER, font='Cambria 14',
                                    command=self.try_add_item, activebackground='#F7F7F7')
        self.name_label.place(x=0, y=0, relwidth=0.6, height=40)
        self.choose_character_button = tk.Button(self, text='~', bd=0, bg='#EEE', activebackground='#F7F7F7',
                                                 command=lambda: AttachCharacterWindow(self.root, self, all_characters))
        self.choose_character_button.place(relx=0.6, y=0, relwidth=0.05, width=30, height=40)

        self.total_weights = tk.Label(self, text='Вес\n', bg='#DDD')
        self.total_weights.place(relx=0.75, y=0, relwidth=0.125, height=40)
        self.total_costs = tk.Label(self, text='Цена\n', bg='#DDD')
        self.total_costs.place(relx=0.875, y=0, relwidth=0.125, height=40)
        tk.Label(self, bg='#AAA').place(x=0, y=40, relwidth=1, height=1)
        tk.Label(self, bg='#AAA').place(relx=0.6, y=0, width=1, height=40)
        tk.Label(self, bg='#AAA').place(relx=0.75, y=0, width=1, height=40)
        tk.Label(self, bg='#AAA').place(relx=0.875, y=0, width=1, height=40)

        self.items_zone = tk.Frame(self, bg='#EEE')
        tk.Label(self.items_zone, bg='#AAA').place(relx=0.75, y=0, width=1, relheight=1)
        tk.Label(self.items_zone, bg='#AAA').place(relx=0.875, y=0, width=1, relheight=1)
        self.items_zone.place(x=0, y=41, relwidth=1, relheight=1, height=-41)

        self.place(x=40 + number * 301, y=0, width=300, relheight=1)

    def attach_a_character(self, owner):
        self.owner = owner
        owner.image = self
        owner.is_displayed = True
        self.name_label['text'] = owner.name
        self.total_costs['text'] = 'Цена\n' + str(self.owner.total_cost)
        self.total_weights['text'] = 'Вес\n' + str(self.owner.total_weight)
        self.refresh()

    def try_add_item(self):
        if self.owner:
            custom_name = self.custom_item_frame.name_entry.get()
            custom_cost = self.custom_item_frame.cost_entry.get()
            custom_weight = self.custom_item_frame.weight_entry.get()
            if custom_name and custom_cost and custom_weight:
                self.owner.add_item(Item('Другое', custom_name, str_to_simpl_num(custom_cost),
                                         str_to_simpl_num(custom_weight)))
                self.custom_item_frame.name_entry.delete(0, tk.END)
                self.custom_item_frame.cost_entry.delete(0, tk.END)
                self.custom_item_frame.weight_entry.delete(0, tk.END)
            else:
                if self.listbox.items_lb.curselection():
                    name = self.listbox.items_lb.get(self.listbox.items_lb.curselection()[0])
                    category = 0
                    for source, category_name in zip(self.select_listbox_menubutton.files,
                                                     self.select_listbox_menubutton.categories):
                        file = open(source, 'r', encoding=self.listbox.encoding)
                        temp_list_of_items = []
                        for line in file:
                            data = line.strip().split('\t')[0]
                            temp_list_of_items.append(data)
                        if name in temp_list_of_items:
                            category = category_name
                            break
                    self.owner.add_item(Item(category, name, self.listbox.items_lb.master.alles[name][0],
                                             self.listbox.items_lb.master.alles[name][1]))
            self.root.focus()
            self.search_frame.entry.delete(0, tk.END)
            self.search_frame.modify_listboxes()
            self.search_frame.entry.delete(0, tk.END)

    def refresh(self):
        if self.owner:
            if self.states[self.state] == 'inventory':
                self.total_weights['text'] = 'Вес\n' + str(self.owner.total_weight)
                self.total_costs['text'] = 'Цена\n' + str(self.owner.total_cost)
                if self.items_zone:
                    self.items_zone.destroy()
                if self.owner:
                    self.items_zone = CharacterInventoryZone(self)
            elif self.states[self.state] == 'states':
                self.total_weights['text'] = 'Вес\n' + str(self.owner.total_weight)
                self.total_costs['text'] = 'Цена\n' + str(self.owner.total_cost)
                if self.items_zone:
                    self.items_zone.destroy()
                if self.owner:
                    self.items_zone = CharacterStatesZone(self)

    def refresh_total_values(self):
        self.owner.calculate_cost_weight()
        self.total_costs['text'] = 'Цена\n' + str(self.owner.total_cost)
        self.total_weights['text'] = 'Вес\n' + str(self.owner.total_weight)

    def switch(self):
        if self.state == 0:
            self.state = 1
            self.refresh()
        elif self.state == 1:
            self.state = 0
            self.refresh()


class CharacterInventoryZone(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.place(x=0, y=41, relwidth=1, relheight=1, height=-41)
        self.refresh()

    def refresh(self):
        position = 0
        for category in sorted(list(self.master.owner.container), key=lambda x: self.master.select_listbox_menubutton.categories.index(x)):
            category_label = tk.Label(self, text='- '+category, anchor=tk.W, font='Arial 9 bold')
            category_label.place(x=0, y=position * 16, relwidth=0.6, height=15)

            def hide_category(event):
                text = event.widget['text'][2:]
                if text in event.widget.master.master.owner.categories_hidden:
                    # show it
                    event.widget.master.master.owner.categories_hidden.remove(text)
                    event.widget.master.master.refresh()
                else:
                    # hide it
                    event.widget.master.master.owner.categories_hidden.append(text)
                    event.widget.master.master.refresh()

            category_label.bind('<Button-1>', hide_category)

            position += 1
            if category in self.master.owner.categories_hidden:
                category_label['text'] = '+ ' + category_label['text'][2:]
                continue
            for item in sorted(self.master.owner.container[category]):
                item.label = tk.Label(self, text=item.name)
                item.label.item = item
                item.label.place(x=0, y=position * 16, relwidth=0.6, height=15)
                item.label.bind("<Button-3>", item.context_menu)
                pop_up_desc.button_description(item.label, item.description, self)
                item.num_entry = tk.Entry(self, bd=0, justify=tk.CENTER, takefocus=0,
                                          bg='SystemMenu')
                item.num_entry.insert(0, item.amount)
                item.num_entry.place(relx=0.675, x=-10, y=position * 16, width=20, height=15)
                item.num_entry.bind("<Button-1>", item.start)
                item.num_entry.bind("<Leave>", item.unfocus)
                item.num_entry.bind("<FocusOut>", item.take_entry)
                tk.Button(self, text='-', bd=0, command=item.decrease_amount).place(
                    relx=0.6, y=position * 16, width=10, height=15)
                tk.Button(self, text='+', bd=0, command=item.increase_amount).place(
                    relx=0.75, x=-10, y=position * 16, width=10, height=15)
                tk.Label(self, text=item.weight).place(
                    relx=0.75, y=position * 16, relwidth=0.125, height=15)
                tk.Label(self, text=item.cost).place(
                    relx=0.875, y=position * 16, relwidth=0.125, height=15)
                position += 1
            position += 1

        tk.Label(self, bg='#AAA').place(relx=0.6, y=0, width=1, relheight=1)
        tk.Label(self, bg='#AAA').place(relx=0.75, y=0, width=1, relheight=1)
        tk.Label(self, bg='#AAA').place(relx=0.875, y=0, width=1, relheight=1)


class CharacterStatesZone(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        # галочки ------------------------------------------------------------------------------------------------------
        self.darkvision_var = tk.IntVar()
        self.darkvision_var.set(self.master.owner.darkvision)
        self.darkvision_checkbutton = tk.Checkbutton(self, text='Темновидение', font='Cambria 11',
                                                     activeforeground='blue', var=self.darkvision_var,
                                                     command=self.darkvision_do)
        self.darkvision_var.checkbutton = self.darkvision_checkbutton
        self.darkvision_checkbutton.place(x=-21, y=0, height=15)

        self.concentration_var = tk.IntVar()
        self.concentration_var.set(self.master.owner.concentration)
        self.concentration_checkbutton = tk.Checkbutton(self, text='Концентрация', font='Cambria 11',
                                                        activeforeground='orange', var=self.concentration_var,
                                                        command=self.concentration_do)
        self.concentration_var.checkbutton = self.concentration_checkbutton
        self.concentration_checkbutton.place(x=-21, y=16, height=15)

        self.exhausted_var = tk.IntVar()
        self.exhausted_var.set(self.master.owner.exhausted)
        self.exhausted_checkbutton = tk.Checkbutton(self, text='Истощение', font='Cambria 11',
                                                    activeforeground='red', var=self.exhausted_var,
                                                    command=self.exhausted_do)
        self.exhausted_var.checkbutton = self.exhausted_checkbutton
        self.exhausted_checkbutton.place(x=-21, y=32, height=15)
        # --------------------------------------------------------------------------------------------------------------
        tk.Label(self, bg='#AAA').place(relx=0.4, width=1, height=54)
        tk.Label(self, bg='#AAA').place(y=53, relwidth=1, height=0)
        tk.Label(self, text='ХП\n~', font='Cambria 11', anchor=tk.E).place(x=180, y=5, width=40, height=40)
        tk.Label(self, text='/\n/', font='Cambria 11', anchor=tk.E).place(x=155, y=5, width=10, height=40)
        self.hp_total = tk.Entry(self, bd=0, fg='green', bg='SystemMenu', font='Cambria 12', justify=tk.CENTER)
        self.hp_total.place(x=123, y=10, relwidth=0.1, height=12)
        self.hp_total.bind('<Button-1>', self.start_hp_total)
        self.hp_total.bind('<Leave>', self.get_hp_total)
        self.hp_total_max = tk.Entry(self, bd=0, fg='green', bg='SystemMenu', font='Cambria 12', justify=tk.CENTER)
        self.hp_total_max.place(x=165, y=10, relwidth=0.1, height=12)
        self.hp_total_max.bind('<Button-1>', self.start_hp_total_max)
        self.hp_total_max.bind('<Leave>', self.get_hp_total_max)

        self.hp_temp = tk.Entry(self, bd=0, fg='green', bg='SystemMenu', font='Cambria 12', justify=tk.CENTER)
        self.hp_temp.place(x=123, y=28, relwidth=0.1, height=12)
        self.hp_temp.bind('<Button-1>', self.start_hp_temp)
        self.hp_temp.bind('<Leave>', self.get_hp_temp)
        self.hp_temp_max = tk.Entry(self, bd=0, fg='green', bg='SystemMenu', font='Cambria 12', justify=tk.CENTER)
        self.hp_temp_max.place(x=165, y=28, relwidth=0.1, height=12)
        self.hp_temp_max.bind('<Button-1>', self.start_hp_temp_max)
        self.hp_temp_max.bind('<Leave>', self.get_hp_temp_max)
        # --------------------------------------------------------------------------------------------------------------
        tk.Label(self, bg='#AAA').place(y=53, relwidth=1, height=0)
        tk.Label(self, bg='#AAA').place(relx=0.75, width=1, height=60)
        tk.Label(self, text='Пассивное\nвосприятие:', font='Cambria 9').place(relx=0.75, x=1, y=0, relwidth=0.25, width=-1, height=30)
        self.passive_perception_entry = tk.Entry(self, bd=0, bg='#EEE', font='Cambria 10')
        self.passive_perception_entry.place(relx=0.85, y=32, relwidth=0.05, height=15)
        self.passive_perception_entry.bind('<Button-1>', self.start_passive_perception)
        self.passive_perception_entry.bind('<Leave>', self.get_passive_perception)
        # --------------------------------------------------------------------------------------------------------------
        tk.Label(self, text='доспех    щит    ловк        а)          б)', font='Cambria 7').place(x=133, y=54, height=9)
        tk.Label(self, text='КД постоянный:', font='Cambria 10').place(x=0, y=63, height=15)
        self.armor_label = tk.Label(self, text='0', font='Cambria 10')
        self.armor_label.place(x=110, y=63, width=20, height=15)
        tk.Label(self, text='='+'       +'*4, font='Cambria 10').place(x=130, y=63, height=15)
        self.armor_e1 = tk.Entry(self, bd=0, bg='#FFF', font='Cambria 10', justify=tk.CENTER)
        self.armor_e1.place(x=143, y=63, width=16, height=15)
        self.armor_e2 = tk.Entry(self, bd=0, bg='#FFF', font='Cambria 10', justify=tk.CENTER)
        self.armor_e2.place(x=171, y=63, width=16, height=15)
        self.armor_e3 = tk.Entry(self, bd=0, bg='#FFF', font='Cambria 10', justify=tk.CENTER)
        self.armor_e3.place(x=199, y=63, width=16, height=15)
        self.armor_e4 = tk.Entry(self, bd=0, bg='#FFF', font='Cambria 10', justify=tk.CENTER)
        self.armor_e4.place(x=227, y=63, width=16, height=15)
        self.armor_e5 = tk.Entry(self, bd=0, bg='#FFF', font='Cambria 10', justify=tk.CENTER)
        self.armor_e5.place(x=255, y=63, width=16, height=15)

        tk.Label(self, text='КД альтер-ный:', font='Cambria 10').place(x=0, y=79, height=15)
        self.armor_temp_label = tk.Label(self, text='0', font='Cambria 10')
        self.armor_temp_label.place(x=110, y=79, width=20, height=15)
        tk.Label(self, text='='+'       +'*4, font='Cambria 10').place(x=130, y=79, height=15)
        self.armor_temp_e1 = tk.Entry(self, bd=0, bg='#FFF', font='Cambria 10', justify=tk.CENTER)
        self.armor_temp_e1.place(x=143, y=79, width=16, height=15)
        self.armor_temp_e2 = tk.Entry(self, bd=0, bg='#FFF', font='Cambria 10', justify=tk.CENTER)
        self.armor_temp_e2.place(x=171, y=79, width=16, height=15)
        self.armor_temp_e3 = tk.Entry(self, bd=0, bg='#FFF', font='Cambria 10', justify=tk.CENTER)
        self.armor_temp_e3.place(x=199, y=79, width=16, height=15)
        self.armor_temp_e4 = tk.Entry(self, bd=0, bg='#FFF', font='Cambria 10', justify=tk.CENTER)
        self.armor_temp_e4.place(x=227, y=79, width=16, height=15)
        self.armor_temp_e5 = tk.Entry(self, bd=0, bg='#FFF', font='Cambria 10', justify=tk.CENTER)
        self.armor_temp_e5.place(x=255, y=79, width=16, height=15)

        tk.Button(self, bd=0, bg='#DDD', text='OK', command=self.get_armors,
                  activebackground='#E9E9E9').place(relx=1, x=-26, y=63, width=26, height=31)

        self.place(x=0, y=41, relwidth=1, relheight=1, height=-41)
        self.refresh()

    def darkvision_do(self):
        value = int(self.darkvision_var.get())
        self.master.owner.darkvision = value
        self.darkvision_checkbutton['fg'] = ['#DDD', 'blue'][value]

    def concentration_do(self):
        value = int(self.concentration_var.get())
        self.master.owner.concentration = value
        self.concentration_checkbutton['fg'] = ['#DDD', 'orange'][value]

    def exhausted_do(self):
        value = int(self.exhausted_var.get())
        self.master.owner.exhausted = value
        self.exhausted_checkbutton['fg'] = ['#DDD', 'red'][value]

    def start_hp_total(self, event):
        self.hp_total.focus()
        self.hp_total.delete(0, tk.END)

    def get_hp_total(self, event):
        try:
            self.master.owner.hp_total[0] = int(self.hp_total.get())
        except ValueError:
            self.hp_total.delete(0, tk.END)
            self.hp_total.insert(0, self.master.owner.hp_total[0])
        self.focus()

    def start_hp_total_max(self, event):
        self.hp_total_max.focus()
        self.hp_total_max.delete(0, tk.END)

    def get_hp_total_max(self, event):
        try:
            self.master.owner.hp_total[1] = int(self.hp_total_max.get())
        except ValueError:
            self.hp_total_max.delete(0, tk.END)
            self.hp_total_max.insert(0, self.master.owner.hp_total[1])
        self.focus()

    def start_hp_temp(self, event):
        self.hp_temp.focus()
        self.hp_temp.delete(0, tk.END)

    def get_hp_temp(self, event):
        try:
            self.master.owner.hp_temp[0] = int(self.hp_temp.get())
            if not self.master.owner.hp_temp[0]:
                self.hp_temp.delete(0, tk.END)
        except ValueError:
            self.hp_temp.delete(0, tk.END)
            if self.master.owner.hp_temp[0]:
                self.hp_temp.insert(0, self.master.owner.hp_temp[0])
        self.focus()

    def start_hp_temp_max(self, event):
        self.hp_temp_max.focus()
        self.hp_temp_max.delete(0, tk.END)

    def get_hp_temp_max(self, event):
        try:
            self.master.owner.hp_temp[1] = int(self.hp_temp_max.get())
            if not self.master.owner.hp_temp[1]:
                self.hp_temp_max.delete(0, tk.END)
        except ValueError:
            self.hp_temp_max.delete(0, tk.END)
            if self.master.owner.hp_temp[1]:
                self.hp_temp_max.insert(0, self.master.owner.hp_temp[1])
        self.focus()

    def start_passive_perception(self, event):
        self.passive_perception_entry.focus()
        self.passive_perception_entry.delete(0, tk.END)

    def get_passive_perception(self, event):
        try:
            self.master.owner.passive_perception = int(self.passive_perception_entry.get())
        except ValueError:
            self.passive_perception_entry.delete(0, tk.END)
            self.passive_perception_entry.insert(0, self.master.owner.passive_perception)
        self.focus()

    def get_armors(self):
        armor = 0
        armor_temp = 0
        for en1, en2, i in zip([self.armor_e1, self.armor_e2, self.armor_e3, self.armor_e4, self.armor_e5],
                               [self.armor_temp_e1, self.armor_temp_e2, self.armor_temp_e3, self.armor_temp_e4, self.armor_temp_e5],
                               range(1, 6)):
            try:
                if en1.get():
                    self.master.owner.armor[i] = int(en1.get())
                    armor += int(en1.get())
                else:
                    self.master.owner.armor[i] = 0
            except ValueError:
                pass
            try:
                if en2.get():
                    self.master.owner.armor_temp[i] = int(en2.get())
                    armor_temp += int(en2.get())
                else:
                    self.master.owner.armor_temp[i] = 0
            except ValueError:
                pass
        self.master.owner.armor[0] = armor
        self.master.owner.armor_temp[0] = armor_temp
        self.focus()
        self.refresh()

    def refresh(self):
        self.darkvision_do()
        self.concentration_do()
        self.exhausted_do()
        self.hp_total.delete(0, tk.END)
        self.hp_total.insert(0, self.master.owner.hp_total[0])
        self.hp_total_max.delete(0, tk.END)
        self.hp_total_max.insert(0, self.master.owner.hp_total[1])
        if self.master.owner.hp_temp[0]:
            self.hp_temp.delete(0, tk.END)
            self.hp_temp.insert(0, self.master.owner.hp_temp[0])
        if self.master.owner.hp_temp[1]:
            self.hp_temp_max.delete(0, tk.END)
            self.hp_temp_max.insert(0, self.master.owner.hp_temp[1])
        self.passive_perception_entry.delete(0, tk.END)
        self.passive_perception_entry.insert(0, self.master.owner.passive_perception)
        self.armor_label['text'] = self.master.owner.armor[0]
        self.armor_temp_label['text'] = self.master.owner.armor_temp[0]
        for en1, en2, i in zip([self.armor_e1, self.armor_e2, self.armor_e3, self.armor_e4, self.armor_e5],
                               [self.armor_temp_e1, self.armor_temp_e2, self.armor_temp_e3, self.armor_temp_e4,
                                self.armor_temp_e5],
                               range(1, 6)):
            en1.delete(0, tk.END)
            if self.master.owner.armor[i]:
                en1.insert(0, self.master.owner.armor[i])
            en2.delete(0, tk.END)
            if self.master.owner.armor_temp[i]:
                en2.insert(0, self.master.owner.armor_temp[i])


class ItemsListBoxFrame(tk.Frame):
    def __init__(self, root, source, **kwargs):
        super().__init__(root)

        self.source = source
        self.select_listbox_menubutton = None
        self.search_frame = None
        self.is_shown = True

        scrollbar_src = tk.Scrollbar(self, orient=tk.VERTICAL, bd=0)
        self.items_lb = tk.Listbox(self, yscrollcommand=scrollbar_src.set, activestyle='none', bd=0, takefocus=0)
        self.items_lb.place(x=0, y=0, relwidth=1, width=-16, relheight=1)
        scrollbar_src.config(command=self.items_lb.yview)
        scrollbar_src.place(relx=1, x=-17, y=0, relheight=1)

        self.alles = {}
        self.encoding = 'cp1251'

        self.refresh()
        self.place(x=0, relwidth=1, width=-1, **kwargs)

    def refresh(self, filter_str=None, source=None):
        if not source:
            source = self.source
        temp_list_of_items = []
        temp_list_of_items_2 = []
        if filter_str:
            for one_file in self.select_listbox_menubutton.files:
                file = open(one_file, 'r', encoding=self.encoding)
                for line in file:
                    data = line.strip().split('\t')
                    if data[0].upper().startswith(filter_str.upper()):
                        temp_list_of_items.append(data)
                file.seek(0)
                for line in file:
                    data = line.strip().split('\t')
                    if (filter_str.upper() in data[0].upper()) and not (data[0].upper().startswith(filter_str.upper())):
                        temp_list_of_items_2.append(data)
        else:
            file = open(source, 'r', encoding=self.encoding)
            for line in file:
                data = line.strip().split('\t')
                temp_list_of_items.append(data)
        temp_list_of_items.sort()
        temp_list_of_items_2.sort()
        self.items_lb.delete(0, tk.END)
        for item in temp_list_of_items + temp_list_of_items_2:
            self.alles[item[0]] = [str_to_simpl_num(item[1]), str_to_simpl_num(item[2])]
            self.items_lb.insert(tk.END, item[0])


class AttachCharacterWindow(tk.Toplevel):
    def __init__(self, root, character_image, all_characters):
        super().__init__(root)
        self.title('Attach')
        self.geometry('500x300+400+350')
        self.grab_set()
        self.focus_set()

        self.character_image = character_image
        self.all_characters = all_characters
        self.not_displayed_characters = []

        scrollbar_src = tk.Scrollbar(self, orient=tk.VERTICAL, bd=0)
        self.characters_lb = tk.Listbox(self, yscrollcommand=scrollbar_src.set, activestyle='none', bd=0)
        self.characters_lb.place(x=0, y=0, width=250, relheight=1, height=-40)
        scrollbar_src.config(command=self.characters_lb.yview)
        scrollbar_src.place(x=250, y=0, relheight=1, height=-40)
        tk.Button(self, bg='#22B14C', activebackground='#00CC00', text='Ok', fg='white', activeforeground='white',
                  bd=0, command=self.apply).place(x=0, rely=1, y=-40, relwidth=1, height=40)
        tk.Label(self, text='Create new character:').place(x=268, y=0, relwidth=1, width=-268, height=30)
        self.new_char_name_entry = tk.Entry(self, bd=0, bg='#FAFAFA', font='Cambria 15 bold', justify=tk.CENTER)
        self.new_char_name_entry.bind('<Return>', self.new_character)
        self.new_char_name_entry.place(x=268, y=30, relwidth=1, width=-268, height=30)
        tk.Button(self, text='<<<', bd=0, command=self.new_character,
                  bg='#DDD').place(x=268, y=60, relwidth=1, width=-268, height=30)
        tk.Label(self, text='Remove character').place(x=268, rely=1, y=-100, relwidth=1, width=-268, height=30)
        tk.Button(self, text='>>>', bd=0, command=self.remove_character,
                  bg='#DDD').place(x=268, rely=1, y=-70, relwidth=1, width=-268, height=30)

        self.refresh_lb()

    def refresh_lb(self):
        self.characters_lb.delete(0, tk.END)
        self.not_displayed_characters.clear()
        for character in self.all_characters:
            if not character.is_displayed:
                self.not_displayed_characters.append(character)
                self.characters_lb.insert(tk.END, character)

    def new_character(self, event=None):
        data = self.new_char_name_entry.get()
        if data:
            for character in self.all_characters:
                if character.name == data:
                    return
            self.all_characters.insert(0, Character(data))
            self.new_char_name_entry.delete(0, tk.END)
            self.refresh_lb()
            save_all(self.all_characters)

    def remove_character(self):
        if self.characters_lb.curselection():
            if messagebox.askokcancel('Remove', 'Really remove "{0}"?'.format(
                    self.all_characters[self.characters_lb.curselection()[0]].name)):
                temp_characters = []
                for character in self.all_characters:
                    if not character.is_displayed:
                        temp_characters.append(character)
                self.all_characters.remove(temp_characters[self.characters_lb.curselection()[0]])
                self.refresh_lb()

    def apply(self):
        if self.characters_lb.curselection():
            new_character = self.not_displayed_characters[self.characters_lb.curselection()[0]]
            if self.character_image.owner:
                self.character_image.owner.is_displayed = False
            self.character_image.attach_a_character(new_character)
            self.destroy()


class CustomItemFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, bg='#DDD')

        tk.Label(self, text='Создание нового предмета:').place(x=0, y=0, width=186, height=20)
        tk.Label(self, text='Цена:').place(x=187, y=0, width=40, height=20)
        tk.Label(self, text='Вес:').place(x=228, y=0, width=40, height=20)
        self.name_entry = tk.Entry(self, bd=0)
        self.name_entry.place(x=0, y=20, width=186, height=20)
        self.cost_entry = tk.Entry(self, bd=0, justify=tk.CENTER)
        self.cost_entry.place(x=187, y=20, width=40, height=20)
        self.weight_entry = tk.Entry(self, bd=0, justify=tk.CENTER)
        self.weight_entry.place(x=228, y=20, width=40, height=20)

        self.place(x=0, y=0, relwidth=1, width=-1, height=40)


class SearchFrame(tk.Frame):
    def __init__(self, root, listbox, **kwargs):
        super().__init__(root, **kwargs)

        self.listbox = listbox
        self.listbox.search_frame = self
        self.entering = False

        tk.Label(self, text='Поиск:', anchor=tk.W).place(x=0, y=0, width=50, relheight=1)
        self.entry = tk.Entry(self, bd=0)
        self.entry.bind('<Button-1>', self.cursor_in)
        self.entry.bind('<Leave>', self.cursor_out)
        self.entry.bind('<Key>', self.key_pressed)
        self.entry.place(x=50, y=0, width=218, relheight=1)

        self.place(x=0, y=62, relwidth=1, width=-1, height=20)

    def cursor_in(self, event):
        self.entry.focus()
        self.after(1, lambda: self.entry.select_range(0, tk.END))
        self.entering = True

    def cursor_out(self, event):
        self.entering = False
        self.focus()

    def key_pressed(self, event):
        if self.entering:
            self.after(50, self.modify_listboxes)

    def modify_listboxes(self):
        self.listbox.refresh(self.entry.get())


class SelectListboxMenubutton(tk.Menubutton):
    def __init__(self, root, listbox, search_frame):
        super().__init__(root, text='Снаряжение - сменить тип предметов', bd=0, anchor=tk.W)

        self.root = root
        self.listbox = listbox
        self.listbox.select_listbox_menubutton = self
        self.menu = tk.Menu(self, tearoff=0)
        self.categories = ['Снаряжение', 'Другое', 'Оружие', 'Броня', 'Инструменты', 'Животные',
                           'Сёдла, упряжь и транспорт', 'Водный транспорт', 'Товары', 'Услуги']
        self.files = ['items library\\items_main.txt', 'items library\\items_other.txt',
                      'items library\\items_weapons.txt', 'items library\\items_armors.txt',
                      'items library\\items_instruments.txt', 'items library\\items_animals.txt',
                      'items library\\items_transport.txt', 'items library\\items_naval.txt',
                      'items library\\items_goods.txt', 'items library\\items_services.txt']
        self.selected_lb = self.categories[0]

        def change_type(new_type, filename):
            self.listbox.source = filename
            self.listbox.refresh(search_frame.entry.get())
            self.selected_lb = new_type
            self['text'] = self.selected_lb + ' - сменить тип предметов'
            return filename

        self.menu.add_command(label='Снаряжение', command=lambda: change_type('Снаряжение',
                                                                              'items library\\items_main.txt'))
        self.menu.add_command(label='Оружие', command=lambda: change_type('Оружие', 'items library\\items_weapons.txt'))
        self.menu.add_command(label='Броня', command=lambda: change_type('Броня', 'items library\\items_armors.txt'))
        self.menu.add_command(label='Инструменты', command=lambda: change_type('Инструменты',
                                                                               'items library\\items_instruments.txt'))
        self.menu.add_command(label='Животные', command=lambda: change_type('Животные',
                                                                            'items library\\items_animals.txt'))
        self.menu.add_command(label='Сёдла, упряжь и транспорт',
                              command=lambda: change_type('Сёдла, упряжь и транспорт',
                                                          'items library\\items_transport.txt'))
        self.menu.add_command(label='Водный транспорт',
                              command=lambda: change_type('Водный транспорт', 'items library\\items_naval.txt'))
        self.menu.add_command(label='Товары', command=lambda: change_type('Товары', 'items library\\items_goods.txt'))
        self.menu.add_command(label='Услуги', command=lambda: change_type('Услуги',
                                                                          'items library\\items_services.txt'))

        self['menu'] = self.menu

        self.place(x=0, y=41, relwidth=1, width=-1, height=20)


class MenuBar(tk.Frame):
    def __init__(self, root, all_characters, lb_frame, holder):
        super().__init__(root, bg='SystemMenu')
        self.root = root
        self.all_characters = all_characters
        self.lb_frame = lb_frame
        self.holder = holder

        tk.Button(self, text='Инв/\nстаты', bg='#c9efff', activebackground='#c9efff', bd=0,
                  command=self.switch_char_images).place(x=0, y=0, relwidth=1, height=40)
        self.hide_show_button = tk.Button(self, command=self.hide_show_itemslbframe, bd=0, fg='white',
                                          activeforeground='white', bg='#BBB', activebackground='#CCC', text='-',
                                          font='Arial 15')
        self.hide_show_button.place(x=0, rely=1, y=-39, relwidth=1, height=39)

        self.place(x=0, y=0, width=39, relheight=1)

    def switch_char_images(self):
        for image in self.root.character_images:
            image.switch()

    def hide_show_itemslbframe(self):
        if self.lb_frame.is_shown:
            self.lb_frame.master.place_forget()
            self.holder.place(x=0, y=0, relwidth=1, relheight=1)
            self.lb_frame.is_shown = False
            self.hide_show_button['text'] = '+'
        else:
            self.holder.place(x=268, y=0, relwidth=1, relheight=1)
            self.lb_frame.master.place(x=0, y=0, width=268, relheight=1)
            self.lb_frame.is_shown = True
            self.hide_show_button['text'] = '-'


def open_all(all_characters):
    try:
        file = open('inv4dnd_save.bin', 'rb')
        all_characters.clear()
        temp = pickle.load(file)
        for character in temp:
            all_characters.append(character)
    except FileNotFoundError:
        file = open('inv4dnd_save.bin', 'wb')
        file.close()


def save_all(all_characters):
    file = open('inv4dnd_save.bin', 'wb')
    images = []
    lables = []
    num_entries = []
    for character in all_characters:
        images.append(character.image)
        for category in character.container:
            for item in character.container[category]:
                lables.append(item.label)
                item.label = None
                num_entries.append(item.num_entry)
                item.num_entry = None
        character.image = None
    pickle.dump(all_characters, file)
    file.close()
    for character, image in zip(all_characters, images):
        character.image = image
        for category in character.container:
            for item in character.container[category]:
                item.label = lables.pop(0)
                item.num_entry = num_entries.pop(0)
    print('saved', all_characters)
