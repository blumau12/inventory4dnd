from os.path import join as join_path, isfile

categories_ordered = ['main', 'weapons', 'armors', 'instruments', 'services', 'transport', 'animals', 'goods', 'naval']


class Category:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.items = {}  # {name: [weight, cost]}

    def fill_category(self, file):
        for line in open(file, 'r', encoding='utf-8'):
            item = line.strip().split(',')
            self.items[item[0]] = [item[1], item[2]]

    def __repr__(self):
        return str({self.name: self.items})


categories = []

for category in categories_ordered:
    file = join_path('items_library', 'items_{0}.csv'.format(category))
    if not isfile(file):
        print('file {0} not found'.format(file))
        continue
    category = Category(category, 0)
    categories.append(category)
    category.fill_category(file)
