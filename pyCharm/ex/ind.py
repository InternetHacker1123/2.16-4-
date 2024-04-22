#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from jsonschema import validate


def add(sp):
    punkt_naznachenia = input("Пункт назначения поезда: ")
    train_number = input("Номер поезда: ")
    time_otpravlenia = input("Время отправления: ")

    dictionary = {
        'Пункт назначения ': punkt_naznachenia,
        'Номер поезда: ': train_number,
        'Время отправления:': time_otpravlenia
    }

    sp.append(dictionary)
    sp = sorted(sp, key=lambda x: x['Номер поезда: '])


def choose(sp):
    inp = input("Введите номер поезда: ")
    for d in sp:
        if inp in d.values():
            print(d)
        else:
            print('Поезда с таким номером нет')


def get_list(sp):
    line = '+-{}-+-{}-+-{}-+-{}-+'.format(
        '-' * 4,
        '-' * 30,
        '-' * 20,
        '-' * 20
    )
    print(line)
    print(
        '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
            "№",
            "Пункт назначения",
            "Номер поезда",
            "Время отправления"
        )
    )
    print(line)
    for idx, train in enumerate(sp, 1):
        print(
            '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                idx,
                train.get('Пункт назначения ', ''),
                train.get('Номер поезда: ', ''),
                train.get('Время отправления:', 0)
            )
        )
        print(line)


def help():
    print("Список команд:\n")
    print("add - добавить поезд;")
    print("list - вывести список поездов;")
    print("choose - найти поезд с заданным номером")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")
    print("save - сохранить поезда в джсон")
    print("load - загрузить поезда из джсона")


def main():
    while True:
        inp = input(">>> ").lower()
        match inp:
            case 'add':
                add(sp)
            case 'list':
                get_list(sp)
            case 'help':
                help()
            case 'choose':
                choose(sp)
            case 'save':
                save_trains(sp)
            case 'load':
                load_trains()


def save_trains(staff):
    """
   Сохранить все поезда в файл JSON.
       """
    # Открыть файл с заданным именем для записи.
    file_name = input("Введите название файла куда сохранить")

    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_trains():
    """
   Загрузить все поезда из файла JSON.
   """
    file_name = input("Введите названия файла из которого загрузить данные")
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        json_schema = {
            "type": "object",
            "properties": {
                "Пункт назначения ": {"type": "string"},
                "Номер поезда: ": {"type": "string"},
                "Время отправления:": {"type": "string"}
            },
            "required": ["Пункт назначения ", "Номер поезда: ", "Время отправления:"]
        }

        # Валидация данных
        data = json.load(fin)
        try:
            for item in range(len(data)):
                validate(instance=data[item], schema=json_schema)
                print("Данные прошли валидацию по JSON Schema.")
                return data
        except Exception as e:
            print(f"Ошибка валидации данных: {e}")


if __name__ == '__main__':
    sp = []
    main()
