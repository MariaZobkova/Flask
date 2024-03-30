# Необходимо создать базу данных для интернет-магазина при помощи FastAPI. База данных должна состоять из трёх таблиц:
# товары, заказы и пользователи.
# — Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
# — Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
# — Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
# • Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия,
# адрес электронной почты и пароль.
# • Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY),
# id товара (FOREIGN KEY), дата заказа и статус заказа.
# • Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.
# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц.
# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.
import datetime

import uvicorn
from typing import List
import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, ForeignKey

# Создание экземпляра FastAPI
app = FastAPI()

DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


@app.on_event("startup")
async def startup():
    await database.connect()


# Модель данных для таблицы "Пользователи"
class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    password: str


class UserIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


# Модель данных для таблицы "Заказы"
class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: int
    status: bool


# Модель данных для таблицы "Товары"
class Product(BaseModel):
    id: int
    name: str
    description: str
    price: int


# Создание таблицы "Пользователи"

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String))

# Создание таблицы "Заказы"

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.String, ForeignKey("products.id")),
    sqlalchemy.Column("order_date", sqlalchemy.Integer),
    sqlalchemy.Column("status", sqlalchemy.Boolean))

# Создание таблицы "Товары"

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer))

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


# CRUD операции для таблицы "Пользователи"


# Создание пользователя
@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(first_name=user.first_name, last_name=user.last_name, email=user.email,
                                  password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


# Чтение пользователей
@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


# Чтение одного пользователя
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


# Обновление пользователя
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


# Удаление пользователя
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


# Остановка сервера
@app.on_event("shutdown")
def shutdown_event():
    database.disconnect()


if __name__ == '__main__':
    uvicorn.run(
        'task_06:app',
        host='127.0.0.1',
        port=8000,
        reload=True
    )
