import threading

import pandas as pd

from data_migration import write_data_to_firestore

datasets = ['./data.xlsx']
dataset_iter = iter(datasets)


def process_dataset():
    try:
        dataset = next(dataset_iter)
        df = pd.read_excel(dataset, sheet_name='data_temp')
        write_data_to_firestore(df)
    except StopIteration:
        print('All datasets have been processed')


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


if __name__ == '__main__':
    set_interval(process_dataset, 5)
