import os
import sys

from sqlalchemy import or_, and_

sys.path.append("..")

from fastapi import Depends, APIRouter, Request, Response, HTTPException, UploadFile, File
from Modules import auth
from sqlalchemy.orm import Session
from models import model
from schemas import schema

router = APIRouter(
    prefix="/common",
    tags=["common"],
    responses={401: {"user": "Not Authorised"}},
)


@router.get("/getuser")  # function
async def get_user(db: Session = Depends(auth.get_db),
                   user: None = Depends(auth.get_current_user)):  # Depends() is local dependency
    if user is None:
        # return {"reactNavigateTo": "/localhost:8000", "msg": "could not varify token/cookie"}
        raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")
    userDetails = db.get(model.User, user.get("id"))
    return {"nameOfUser": userDetails.person.first_name, "role": userDetails.personRole.name, "user_id": userDetails.id,
            "person_id": userDetails.person.id}


@router.post("/createperson")
async def create_person(person: schema.create_person, db: Session = Depends(auth.get_db),
                        user: None = Depends(auth.get_current_user)):
    user = {"id": 1}
    if user is None:
        raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")

    if person.country_code == '+91' and len(person.mobile_no) != 10:
        raise HTTPException(status_code=403, detail="Indian phone numbers should be 10 digits only.")

    db_person = db.query(model.Person.id, model.PersonPhoneNo.mobile_no) \
        .filter(
        (and_(model.Person.country_code + model.Person.primary_mobile_no == person.country_code + person.mobile_no,
              model.Person.first_name == person.first_name,
              model.Person.middle_name == person.middle_name,
              model.Person.last_name == person.last_name,
              model.Person.is_deleted == False, model.Person.is_active == True))).first()  # set all() to get all the child as array

    # db_person = db.query(model.Person).filter(model.Person.primary_mobile_no == 9127024200).first()
    # print(db_person.person_phone_no[0].mobile_no)
    # print(bool(~db_person.is_deleted)) # Negation of a bool value not operator

    if db_person:
        raise HTTPException(status_code=400,
                            detail=f"Person with same name and phone no. Already Exist. {db_person}")

    db_user = db.get(model.User, user.get("id"))

    create_person_PhoneNo_model = model.PersonPhoneNo(
        mobile_no=person.mobile_no,
        country_code=person.country_code,
        is_primary_no=True,
        created_by=db_user
    )
    create_person_Address_model = model.PersonAddress(


    )

    create_person_Email_model = model.PersonEmail(


    )

    create_person_model = model.Person(
        country_code=person.country_code,
        primary_mobile_no=person.mobile_no,
        first_name=person.first_name,
        middle_name=person.middle_name,
        last_name=person.last_name,
        gender=person.gender,
        dob=person.dob,
        created_by=db_user,
        phone_no=[create_person_PhoneNo_model],
        address=[create_person_Address_model],
        email=[create_person_Email_model]
    )

    db.add(create_person_model)
    db.commit()
    db.refresh(create_person_model)

    return {"msg": "Person Created", "person":"create_person_model"}


@router.post("/updateperson")
async def update_person(person: schema.update_person,
                        db: Session = Depends(auth.get_db)):  # , user: None = Depends(auth.get_current_user)
    # if user is None:
    #     raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")

    user = {"id": 1}

    create_person_model = db.get(model.Person, person.id)  # search in person if exist
    if not create_person_model:
        raise HTTPException(status_code=404, detail=f"Person with id {person.id} not "
                                                    f"found")
    # full_name = person.first_name + (  # turnery operator
    #     "" if person.middle_name is None else " " + person.middle_name) + (
    #                 "" if person.last_name is None else " " + person.last_name)
    # create_person_model.full_name = full_name
    create_person_model.first_name = person.first_name
    create_person_model.middle_name = person.middle_name
    create_person_model.last_name = person.last_name
    create_person_model.gender = person.gender
    create_person_model.dob = person.dob
    create_person_model.last_updated_by_id = user.get("id")
    db.add(create_person_model)
    db.commit()
    return {"msg": f"person Updated {person.id}"}


@router.get("/getroles")
async def get_roles(db: Session = Depends(auth.get_db)):
    roles = db.query(model.UserRole).all()
    return {"roles": roles}

@router.get("/getcountrycodes")
async def get_roles(db: Session = Depends(auth.get_db)):
    countryCodes = db.query(model.CountryCode).order_by(
        model.CountryCode.country_name.asc()).all()
    return {"countryCodes": countryCodes}
