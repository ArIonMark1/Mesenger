from sqlalchemy import *
import sqlite3

# 1 - подключение
CONNECT = create_engine('sqlite:///server.db3', echo=False)
# 2 - создание таблиц бд
METADATA = MetaData() # спец. класс конструктор

client = Table('client', METADATA,
               Column('id', Integer, primary_key=True),
               Column('name', String, unique=True),
               Column('last_login', DateTime)
               )
client_history = Table()
# список_контактов (составляется на основании выборки всех записей с id_владельца):
contact_list = Table()

# 3 - подтверждение создания таблиц в бд
# 4 - создание класса-посредника для добавления обьектов в таблицу бд
# 5 - связывание класса-посредника с соотв. таблицей бд
# 6 - создаем обьекты-записи в таблице
# 7 - создаем сессию для управления сохранением обьектов в таблице
# 8 - в обьект сессии добавляем обьект для сохранения в таблице и делаем комит, подтверждаем сохранение
