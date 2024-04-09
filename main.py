from fastapi import FastAPI, Query, HTTPException, Path, Body
from pymongo import MongoClient
from db import MONGO_URI, get_database
from models import Student
from models import Address
from typing import List
from bson import ObjectId

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System!"}

# Function to connect to MongoDB Atlas and return the database instance
def get_database():
    client = MongoClient(MONGO_URI)
    return client["library_db"]


# Endpoint to create a new student
@app.post("/students", status_code=201)
def create_student(student: Student):
    db = get_database()
    inserted_student = db.students.insert_one(student.dict())
    return {"id": str(inserted_student.inserted_id)}

# Endpoint to list students
@app.get("/students")
def list_students(country: str = Query(None, description="Filter by country"),
                   min_age: int = Query(None, description="Minimum age")):
    db = get_database()
    query = {}
    if country:
        query["address.country"] = country
    if min_age:
        query["age"] = {"$gte": min_age}
    students = list(db.students.find(query, {"_id": 0}))
    return {"data": students}

# Endpoint to fetch a student by ID
@app.get("/students/{id}", response_model=Student, summary="Fetch student")
def get_student_by_id(id: str = Path(..., description="The ID of the student previously created")):
    db = get_database()
    student_data = db.students.find_one({"_id": id}, {"_id": 0})
    if student_data:
        return student_data
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    
# Endpoint to update a student
@app.patch("/students/{id}", status_code=204, summary="Update student")
def update_student(id: str = Path(..., description="The ID of the student to update"),
                   student_data: Student = Body(...)):
    db = get_database()
    updated_student = db.students.update_one({"_id": id}, {"$set": student_data.dict()})
    if updated_student.modified_count == 1:
        return
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    
# @app.delete("/students/{id}", summary="Delete student")
# def delete_student(id: str = Path(..., description="The ID of the student to delete")):
#     db = get_database()
#     deleted_student = db.students.delete_one({"_id": id})
#     if deleted_student.deleted_count == 1:
#         return
#     else:
#         raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{id}", summary="Delete student")
def delete_student(id: str = Path(..., description="The ID of the student to delete")):
    try:
        # Convert string ID to ObjectId
        student_id = ObjectId(id)

        # Connect to MongoDB
        db = get_database()

        # Delete student by ObjectId
        deleted_student = db.students.delete_one({"_id": student_id})

        # Check if a document was deleted
        if deleted_student.deleted_count == 1:
            return {"message": "Student deleted successfully"}
        else:
            # Return 404 if no document was deleted
            raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        # Return 500 if any error occurs
        raise HTTPException(status_code=500, detail="Internal server error")