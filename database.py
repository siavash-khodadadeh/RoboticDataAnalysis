import os
from os import listdir
from os.path import join

from models import Task, Item, Position, Try


class Database(object):
    trajectories_directory = 'trajectories/'
    tasks = []

    @staticmethod
    def load_data():
        trajectory_files = [
            trajectory_file for trajectory_file in
            listdir(Database.trajectories_directory) if trajectory_file.endswith('.txt')
        ]

        for trajectory_file in trajectory_files:
            trajectory_file_absolute_path = join(os.getcwd(), Database.trajectories_directory, trajectory_file)
            if Database.check_if_trajectory_file_is_valid(trajectory_file_absolute_path):
                with open(trajectory_file_absolute_path) as f:
                    print(trajectory_file_absolute_path)
                    Database.create_task_from_file(f)

    @staticmethod
    def check_if_trajectory_file_is_valid(trajectory_file):
        with open(trajectory_file) as trajectory:
            trajectory.readline()
            line = trajectory.readline()
            return not line[0].isdigit()

    @staticmethod
    def create_task_from_file(trajectory_file):
        trajectory_file.readline()

        items_string = trajectory_file.readline()
        items = Database.extract_items(items_string)

        labels_string = trajectory_file.readline()
        labels = Database.extract_labels(labels_string)

        try_in_task = Try(items)

        try_number = 0
        tries = []
        for line in trajectory_file:
            data_row = line.split(',')[:-1]
            data_row_dict = {}
            for i in range(len(data_row)):
                data_row_dict[labels[i]] = data_row[i]

            for item in items:
                position = Database.extract_position_of_item(item, data_row_dict)
                try_in_task.add_item_position(item, position)

            if data_row_dict['try_in_task'] != try_number:
                try_number += 1
                tries.append(try_in_task)

        tries.append(try_in_task)
        task = Task(data_row_dict['task'], data_row_dict['username'], tries)
        Database.tasks.append(task)

    @staticmethod
    def extract_items(items_string):
        items = []
        for item_string in items_string.split(',')[:-1]:
            item = Item(name=item_string)
            items.append(item)
        return items

    @staticmethod
    def extract_labels(labels_string):
        return labels_string.split(',')

    @staticmethod
    def extract_position_of_item(item, data_row_dict):
        p_x = data_row_dict[item.name + '_p_x']
        p_y = data_row_dict[item.name + '_p_y']
        p_z = data_row_dict[item.name + '_p_z']
        r_x = data_row_dict[item.name + '_r_x']
        r_y = data_row_dict[item.name + '_r_y']
        r_z = data_row_dict[item.name + '_r_z']
        r_w = data_row_dict[item.name + '_r_w']
        return Position(p_x, p_y, p_z, r_x, r_y, r_z, r_w)


if __name__ == '__main__':
    Database.load_data()
