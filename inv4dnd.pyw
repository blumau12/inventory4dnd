from complex_widgets import *


def on_closing():
    for character in all_characters:
        character.is_displayed = False
    save_all(all_characters)
    main.destroy()


current_company = None
all_characters = []

open_all(all_characters)

# window construct: ----------------------------------------------------------------------------------------------------
main = tk.Tk()
main.title('Equipment')
main.geometry('1209x450+300+300')
root = tk.Frame(main, bg='#555')
root.place(x=0, y=0, relwidth=1, relheight=1)
main.protocol("WM_DELETE_WINDOW", on_closing)

# holders:
holder = tk.Frame(root, bg='red')
holder.place(x=268, y=0, relwidth=1, relheight=1)

# items bar:
items_bar_holder = tk.Frame(root, bg='#555')
items_bar_holder.place(x=0, y=0, width=268, relheight=1)
custom_item_frame = CustomItemFrame(items_bar_holder)
lb1 = ItemsListBoxFrame(items_bar_holder, y=83, relheight=1, height=-83)
search_frame = SearchFrame(items_bar_holder, lb1)
select_listbox_menubutton = SelectListboxMenubutton(items_bar_holder, lb1, search_frame)

# company bar:
# company_bar = CompanyBar(holder, current_company)

# menu bar:
holder = tk.Frame(root, bg='#555')
holder.place(x=268, y=0, relwidth=1, relheight=1)
menu_bar = MenuBar(holder, all_characters, lb1, holder)

# character images:
holder.character_images = []
for i in range(5):
    holder.character_images.append(CharacterImage(holder, lb1, i, all_characters, custom_item_frame, search_frame,
                                   select_listbox_menubutton))
# ----------------------------------------------------------------------------------------------------------------------

main.mainloop()
