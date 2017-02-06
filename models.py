class Position(object):
    def __init__(self, p_x, p_y, p_z, r_x, r_y, r_z, r_w):
        self.p_x = p_x
        self.p_y = p_y
        self.p_z = p_z
        self.r_x = r_x
        self.r_y = r_y
        self.r_z = r_z
        self.r_w = r_w


class Item(object):
    def __init__(self, name):
        self.name = name


class Try(object):
    def __init__(self, items):
        self.duration = 0
        self.items_positions = {}
        for item in items:
            self.items_positions[item.name] = []

    def add_item_position(self, item, position):
        self.items_positions[item.name].append(position)


class Task(object):
    def __init__(self, name, user, tries):
        self.name = name
        self.user = user
        self.tries = tries
