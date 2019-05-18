from classes import *


def on_closing():
    for character in all_characters:
        character.is_displayed = False
    # save_all(all_characters)
    main.destroy()


current_company = None
all_characters = []

# open_all(all_characters)

# window construct: ----------------------------------------------------------------------------------------------------
main = tk.Tk()
main.title('Equipment')
main.geometry('1210x450+300+300')
root = tk.Frame(main, bg='#555')
root.place(x=0, y=0, relwidth=1, relheight=1)
main.protocol("WM_DELETE_WINDOW", on_closing)

# holders:
items_bar_holder = tk.Frame(root, bg='#555')
items_bar_holder.place(x=0, y=0, width=268, relheight=1)
holder = tk.Frame(root, bg='#555')
holder.place(x=268, y=0, relwidth=1, relheight=1)

# items bar:
custom_item_frame = CustomItemFrame(items_bar_holder)
lb1 = ItemsListBoxFrame(items_bar_holder, 'items library\\items_main.txt', y=83, relheight=1, height=-83)
search_frame = SearchFrame(items_bar_holder, lb1)
select_listbox_menubutton = SelectListboxMenubutton(items_bar_holder, lb1, search_frame)

# menu bar:
menu_bar = Menubar(holder, all_characters, lb1, holder)

# company bar:
company_bar = CompanyBar(holder, current_company)

# character images:
holder.character_images = []
for i in range(5):
    holder.character_images.append(CharacterImage(holder, lb1, i, all_characters, custom_item_frame, search_frame,
                                   select_listbox_menubutton))
# ----------------------------------------------------------------------------------------------------------------------

main.mainloop()
