#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# import json
# import functools


# def to_json(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         return json.dumps(func(*args, **kwargs))
#     return wrapper


# @to_json
# def get_data():
#     return {
#         'data': 42
#     }


# print(type(get_data())) 


# # Неделя № 3_2

# In[1]:


# class FileReader:
#     def __init__(self, path): self.path = path
#     def read(self):
#         try:
#             f = open(self.path, 'r')
#             info = f.read()
#         except:
#             info = ''
#         return info


# In[4]:


import csv
import sys
import os.path


class CarBase:
    """Базовый класс с общими методами и атрибутами"""

    def __init__(self, brand, photo_file_name, carrying):
        # проверка что аргументы не являются пустой строкой
        if not all(i != '' for i in (brand, photo_file_name, carrying)):
            raise ValueError

        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)
        # вызов метода для проверки расширения файла изображения
        self.ext = self.get_photo_file_ext()

    def get_photo_file_ext(self):
        _, ext = os.path.splitext(self.photo_file_name)
        if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
            raise ValueError
        return ext


class Car(CarBase):
    """Класс легковой автомобиль"""

    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    """Класс грузовой автомобиль"""

    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        # обрабатываем поле body_whl
        try:
            length, width, height = (float(c) for c in body_whl.split('x', 2))
        except ValueError:
            length, width, height = .0, .0, .0

        self.body_length = length
        self.body_width = width
        self.body_height = height

    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    """Класс спецтехника"""

    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        # проверка что аргумент extra не является пустой строкой
        if extra == '':
            raise ValueError
        self.extra = extra


def get_car_list(csv_filename):
    with open(csv_filename, encoding='utf-8') as csv_fd:
        # создаем объект csv.reader для чтения csv-файла
        reader = csv.reader(csv_fd, delimiter=';')

        # пропускаем заголовок csv
        next(reader)

        # это наш список, который будем возвращать
        car_list = []

        # объявим словарь, ключи которого - тип автомобиля (car_type),
        # а значения - функция, создающая экземпляр нужного класса
        car_types = {
            'car': lambda x: Car(x[1], x[3], x[5], x[2]),
            'truck': lambda x: Truck(x[1], x[3], x[5], x[4]),
            'spec_machine': lambda x: SpecMachine(x[1], x[3], x[5], x[6])}

        # обрабатываем csv-файл построчно
        for row in reader:
            try:
                car_type = row[0]
                # если тип машины в словаре - создаем экземпляр класса
                if car_type in car_types:
                    car_list.append(car_types[car_type](row))
            # при возникновении ошибки - пропускаем строку
            except (ValueError, IndexError):
                pass

    return car_list


# # Неделя № 3

# In[5]:


# import csv
# import sys
# import os.path

# class CarBase:
#     def __init__(self, brand, photo_file_name, carrying):
#         if not all(i != '' for i in (brand, photo_file_name, carrying)):
#             raise ValueError
#     def get_photo_file_ext(self):
#         ex = os.path.splitext(self.photo_file_name)
#         return ex[-1]

# class Car(CarBase):
#     def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
#         self.car_type = 'car'
#         self.brand = brand
#         self.photo_file_name = photo_file_name
#         self.carrying = float(carrying)
#         self.passenger_seats_count = int(passenger_seats_count)


# class Truck(CarBase):
#     def __init__(self, brand, photo_file_name, carrying, body_whl):
#         self.car_type = 'truck'
#         self.brand = brand
#         self.photo_file_name = photo_file_name
#         self.carrying = float(carrying)
#         try:
#             if len(body_whl.split('x'))== 3:
#                 self.body_height = float(body_whl.split('x')[2])
#                 self.body_width = float(body_whl.split('x')[1])
#                 self.body_length = float(body_whl.split('x')[0])
#             else:
#                 self.body_height = 0.0
#                 self.body_width = 0.0
#                 self.body_length = 0.0
#         except:
#             self.body_height = 0.0
#             self.body_width = 0.0
#             self.body_length = 0.0
            
#     def get_body_volume(self):
#         return float(self.body_width)*float(self.body_height)*float(self.body_length)
        
# class SpecMachine(CarBase):
#     def __init__(self, brand, photo_file_name, carrying, extra):
#         self.car_type = 'spec_machine'
#         self.brand = brand
#         if '.' not in photo_file_name:
#             raise ValueError
        
#         self.photo_file_name = photo_file_name    
#         #if extra == '':
#         self.extra = extra
#         self.carrying = float(carrying)
        
        

# def get_car_list(csv_filename):
#     car_list = []
#     try:
#         #with open(csv_filename) as csv_fd:
#         reader = csv.reader(open(csv_filename,  encoding='utf-8'), delimiter=';')    
#         next(reader)  # пропускаем заголовок
#         for row in reader:
#             if len(row)!=0:
#                 if str(row[0])=='car': car_list.append(Car(row[1], row[3], row[5], row[2]))
#                 elif str(row[0])=='truck': car_list.append(Truck(row[1], row[3], row[5], row[4]))
#                 elif str(row[0])=='spec_machine': car_list.append(SpecMachine(row[1], row[3], row[5], row[6]))
#     except (ValueError, IndexError):
#                 pass
#     return car_list
 


# In[6]:


# #from solution import *
# car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
# print(car.car_type, car.brand, car.photo_file_name, car.carrying, car.passenger_seats_count, sep='\n')

# truck = Truck('Nissan', 't1.jpg', '2.5', '')
# print(truck.car_type, truck.brand, truck.photo_file_name, truck.body_length,truck.body_width, truck.body_height, sep='\n')

# spec_machine = SpecMachine('Komatsu-D355', 'd355.jpg', '93', 'pipelayer specs')
# print(spec_machine.car_type, spec_machine.brand, spec_machine.carrying, spec_machine.photo_file_name, spec_machine.extra, sep='\n')
# spec_machine.get_photo_file_ext()


# cars = get_car_list('cars_week3.csv')
# #cars = get_car_list('csv.csv')
# print(len(cars))
# #assert len(cars) == 5
# for car in cars:
#     print(type(car))

# # print(cars[0].passenger_seats_count)
# # cars[1].get_body_volume()


# In[7]:


# float('2.5')


# In[8]:


# truck.body_width


# # Неделя № 4

# In[209]:


# import tempfile
# import os
# import uuid
 

# class File:
#     def __init__(self, path):
#         self.path = path
#         self.curent = 0
#         if os.path.exists(path) == True:
#             with open(path, 'r') as fp:
#                 self.file = fp.read()
                
#         else: 
#             with open(path, 'w') as fp: self.file = ''
            
    
#     def read(self):
#         file = open(self.path, 'r')
#         f = file.read()
#         self.file = f
#         file.close()
#         return self.file
    
#     def write(self, new_text):
#         old = open(self.path, "w+")
#         old.write(new_text)
#         self.file = new_text
#         old.close()
        
#         return len(new_text)
    
#     def __add__(self, obj):
#         new = self.file + obj.file
#         tempor_file = tempfile.gettempdir()
#         for_hash = str(uuid.uuid4().hex)
#         new_path = os.path.join(tempor_file, for_hash)
        
#         lines = [self.file, obj.file]
#         file1 = open(new_path, 'w') 
#         file1.writelines(lines) 
#         file1.close()
#         self.curent = 0
        
#         new_file = File(new_path)
#         return new_file
    

#     def __str__(self):
#         return self.path
 
    
#     def __iter__(self):
#         return self #.file[self.curent]
#     def __next__(self):
#         result = self.curent
        
#         file1 = open(self.path, 'r') 
#         Lines = file1.readlines() 
        
#         if result > len(Lines)-1:
#             self.curent = 0
#             raise StopIteration
        
#         self.curent+=1
#         return Lines[result]
        


# In[167]:


# import os.path

# path_to_file = 'some_fildenam'
# print(os.path.exists(path_to_file))
# #False


# file_obj = File(path_to_file)
# print(os.path.exists(path_to_file))
# #True
# for line in file_obj:
#     print(line)
#     print('000000')

# print(file_obj.read())
# #''

# print(file_obj.write('some_text'))
# #9
# print('read file:')
# print(file_obj.read())
# # #'some text'

# print(file_obj.write('other text'))
# # #10


# print(file_obj.read())
# # #'other text'

# for line in file_obj:
#     print(line)
#     print('000000')

# file_obj_1 = File(path_to_file + '_1')
# file_obj_2 = File(path_to_file + '_2')
# file_obj_3 = File(path_to_file + '_3')
# print(file_obj_1.write('line 1\n'))
# #7

# print(file_obj_2.write('line 2'))
# print(file_obj_3.write('0c8422f2bdab4eb3b73783ded388ec55\ne5fc0dc6a971420589a859195949b709\n3a467f7d694c485a9ae2886794b55831\n'))
# # #7

# new_file_obj = file_obj_1 + file_obj_2 + file_obj_3
# print(new_file_obj)
# print(isinstance(new_file_obj, File))
# #True

# new_file_obj = file_obj_1 + file_obj_2
# print(new_file_obj)
# # #C:\Users\Media\AppData\Local\Temp\71b9e7b695f64d85a7488f07f2bc051c

# for line in new_file_obj:
#     #print(line)
#     print(ascii(line))  
# print('---------')
# for line in new_file_obj:
#     #print(line)
#     print(ascii(line))  
# #'line 1\n'
# #'line 2\n'

# print(file_obj_1)

# new_file_obj.read()


# Часто при зачислении каких-то средств на счет с нас берут комиссию. Давайте реализуем похожий механизм с помощью дескрипторов. Напишите дескриптор Value, который будет использоваться в нашем классе Account.

# In[213]:


# class Value:
#     @staticmethod
#     def _prepare_value(obj, value):
#         return value*(1-obj.commission)
    
#     def __set__(self, obj, value):
#         self.value = self._prepare_value(obj, value)
#         return self.value
    
#     def __get__(self, o, t):
#         return self.value

# # class Account:
# #     amount = Value()
# #     def __init__(self, commission):
# #         self.commission = commission
        
        
# # new_account = Account(0.1)
# # new_account.amount = 100

# # print(new_account.amount)


# # Неделя № 5

# # Неделя № 6

# In[ ]:




