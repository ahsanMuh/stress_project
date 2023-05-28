from fastapi import FastAPI, Request, File, Form, HTTPException
import json
import config

from db_helper import DBHelper
from predictor import main_predictor


app = FastAPI()

conn_str = config.SQL_CONN_STR
db_helper = DBHelper(conn_str)

edf_file_name = config.EDF_FILE_NAME


@app.post("/admin/login")
async def admin_login(body : Request):
    body = await body.json()
    username = body['username']
    password = body['password']

    _id = db_helper.verify_admin_login(username, password)  # gets admin id or -1 incase of an error 

    if _id == -1:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    response = {'id': _id, 'token': 'dummytoken'}

    return response


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

    return response

@app.post("/employee/signup")
async def admin_signup(body : Request):
    body = await body.json()
    name = body['name']
    admin_id = int(body['admin_id'])


    # creates a new user in admin table with the given data
    _id = db_helper.create_employee(name, admin_id) 

    response = {'id': _id} 

    return response

@app.get("/admin/profile")
async def get_admin_profile(_id: int):
    # returns a json object with name, user_id, email, and phone 
    # of admin
    admin_profile = db_helper.read_admin_profile(_id)

    return admin_profile


@app.get("/stress/list")
async def get_recent_stress(_id: int):
    # return list of name, stress-status(bool), id of employes
    # recent for each related to the admin_id
    stress_list = db_helper.get_stress_admin(_id)

    response = {'stress_list': stress_list}

    return response

@app.get("/stress/history")
async def get_stress_history(_id: int):
    # return list of a stress for an employee in the range of
    # start and end time

    stress_list = db_helper.get_stress_employee(_id)

    response = {'stress_list': stress_list}

    return response

@app.post("/stress/add")
async def add_stress_entry(file: bytes = File(...),
                            employee_id: int = Form(...)):
    # Save the file locally
    with open(edf_file_name, "wb") as f:
        f.write(file)

    stress_pred = main_predictor()

    _ = db_helper.create_stress(employee_id, stress_pred)
    # Return a success message
    return {"message": "Stress entry added successfully"}