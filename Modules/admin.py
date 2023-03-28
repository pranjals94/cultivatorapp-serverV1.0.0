import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, Request, Response, HTTPException
from Modules import auth
from sqlalchemy.orm import Session
from models import model
from schemas import schema

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={401: {"user": "Not Authorised"}},
)


@router.post("/createuser")
async def user(user: schema.user, db: Session = Depends(auth.get_db), User: None = Depends(auth.get_current_user)):
    User = {"id": 1}
    if User is None:
        raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")

    person = db.get(model.Person, user.person_id)  # search in person if exist
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with id {user.person_id} not found")
    db_user = db.query(model.User).filter(model.User.person_id == user.person_id).first()
    if db_user:
        raise HTTPException(status_code=404, detail=f"Person id {user.person_id} Already Registered")
    db_user = db.query(model.User).filter(model.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=404, detail=f"Username already taken")

    create_person_model = db.get(model.Person, user.person_id)
    create_person_model.cultivator_id = 0 if user.role_id == '2' else None  # set role as self cultivator

    person_role = db.get(model.Role, user.role_id)
    if person_role:
        raise HTTPException(status_code=404, detail=f"Assigned Role id {user.role_id} does not exist.")

    create_user_model = model.User(
        username=user.username,
        hashed_password=auth.get_password_hash(user.password),
        role_id=user.role_id,
        person=create_person_model,
        personRole=person_role
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"msg": "User created"}


@router.get("/listpersons")
async def list_persons(offset: int | None = 0, limit: int | None = 15, db: Session = Depends(auth.get_db)):
    tempPersons = db.query(model.Person).order_by(
        model.Person.id.desc()).offset(offset).limit(limit).all()
    persons: list = []
    for person in tempPersons:
        user = db.query(model.User).filter(model.User.person_id == person.id).first()
        if user:
            role = user.personRole.name
        else:
            role = None
        results = {"id": person.id, "name": person.name, "phone_no": person.phone_no, "gender": person.gender,
                   "role": role}
        persons.append(results)
    return {"persons": persons}
