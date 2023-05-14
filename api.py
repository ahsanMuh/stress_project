from fastapi import FastAPI, Request
import json

from db_helper import DBHelper

app = FastAPI()

conn_str = '' # removed it for security purposes
db_helper = DBHelper(conn_str)


@app.post("/admin/login")
async def admin_login(body : Request):
    body = await body.json()
    username = body['username']
    password = body['password']

    _id = db_helper.verify_admin_login(username, password)  # gets admin id or -1 incase of an error 

    response = {'id': _id, 'token': 'dummytoken'} 

    return json.dumps(response)

@app.post("/admin/signup")
async def admin_signup(body : Request):
    body = await body.json()
    name = body['name']
    password = body['password']
    email = body['email']
    username = body['username']
    company = body['company']
    phone = int(body['phone'])


    # creates a new user in admin table with the given data
    _id = db_helper.create_admin(name, username, password,
                       email, phone, company) 

    response = {'id': _id, 'token': 'dummytoken'} 

    return json.dumps(response)


@app.get("/admin/profile")
async def get_admin_profile(_id: int):
    # returns a json object with name, user_id, email, and phone 
    # of admin
    admin_profile = db_helper.read_admin_profile(_id)

    return json.dumps(admin_profile)


@app.get("/stress/list")
async def get_recent_stress(_id: int):
    # return list of name, stress-status(bool), id of employes
    # recent for each related to the admin_id
    stress_list = db_helper.get_stress_admin(_id)

    response = {'stress_list': stress_list}

    return response

@app.get("/stress/history")
async def get_stress_history(_id: int, start_datetime: str,
                            end_datetime: str):
    # return list of a stress for an employee in the range of
    # start and end time

    stress_list = db_helper.get_stress_employee(_id, start_time, end_datetime)

    response = {'stress_list': stress_list}

    return response