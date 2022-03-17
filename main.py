# run scripts command details

# https://docs.google.com/document/d/16mn3OPFBTQpLuddHh0yskn2IfMMr1UlXn0MWOgFRLGM/edit


from fastapi import FastAPI
from uncleengineer import thaistock
from typing import Optional
from pydantic import BaseModel


app = FastAPI()



### get method ###
@app.get("/")
def homepage():
    return {"message": "hello world"}



@app.get("/name")
def name():
    return {"name": "kimtee"}

products = [
    {'id': 101, 'name': 'toothblush', 'price': 20},
    {'id': 102, 'name': 'toothpaste', 'price': 30},
    {'id': 103, 'name': 'shampoo', 'price': 50}
]

@app.get('/product')
def allproducts():
    return products


@app.get('/product/{index}/') ### can use as api and get date valid
def check_product(index: int):
    return products[index]

# check stock price

@app.get('/stock/{stock_name}/')
async def stock(stock_name: str):
    price = thaistock(stock_name)
    return price

@app.get('/mystock/')
async def mystock(stock_name: str = 'BBL'):
    price = thaistock(stock_name)
    return price
# can query with other parameters ( not default ) like this
# "? and kwargs"
# http://localhost:8000/mystock/?stock_name=scb

@app.get('/checkapi/{api}/')
async def check_api(api: str):
    for i in valid:
        if api == i['api']:
            return i['valid_date']
    else:
        return ('your api "{}" is incorrect please recheck your api').format(api)

valid = [
    {'api': 'testapi1', 'valid_date': 'good'},
    {'api': 'testapi2', 'valid_date': 'end'}
]


# ***** ความจริง ควรต้องมี ระบบ token เพื่อความปลอดภัย ***** #
######### post method ###############

class Fruit(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    
fruit_stock = []

### post ใช้สำหรับ post api ใหม่ของลูกค้าเข้าไป
@app.post('/addfruit/')
async def add_fruit(fruit: Fruit):
    fruit_stock.append(fruit.dict()) # append fruit to fruit_stoctk
    # to prepared for sql (achemy) db write
    print(fruit_stock)
    return fruit

@app.get('/fruit/')
def all_fruit():
    return fruit_stock


### put ใช้สำหรับ update วันหมดอายุของลูกค้า กรณีซ้ือเพิ่ม
# put() จะอ updated ทั้งก้อน ถ้าเป็นจุดๆ จะสามารถใช้ patch() แทนได้
@app.put('/update/{ID}')
async def update_fruit(ID: int, fruit: Fruit):
    fruit_stock[ID]['price'] = fruit.dict()['price']
    return {'message': 'updated', 'data': fruit.dict()}


# delete
@app.delete('/delete/{ID}')
async def delete_fruit(ID: int):
    data = fruit_stock[ID]
    del fruit_stock[ID]
    return {'message': 'updated', 'data': data}

# ** Heroku Deploy method
#https://www.youtube.com/watch?v=QdhwYWwYfc0&ab_channel=rithmic
# 1 pip freeze > requirement.txt
### ? if dont have repo
# 2 git init
# 3 touch .gitignore
# 3 -- copy .gitignore python from google
# 4 heroku login
# 5 heroku create ( and copy app name)
# touch Procfile
# * write command what to run in Procfile 
# * in this case gonna run uvicorn main:app
# heroku git:remote -a "name of heroku project"