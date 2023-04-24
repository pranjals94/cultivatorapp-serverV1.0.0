import datetime
from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime, Date, Time, Integer, Integer
from sqlalchemy.orm import relationship, backref
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(240), nullable=False)
    email = Column(String(50), unique=True, default=None)
    last_log_in = Column(DateTime, default=None)

    date_created = Column(DateTime, default=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)  # create trigger on sql to prevent update
    deleted_by_id = Column(Integer, ForeignKey("user.id"),
                           default=None)  # self Foreign Key , create trigger on sql to prevent updae

    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("user_role.id"), default=None, nullable=False)
    userRole = relationship("UserRole", backref="user")

    person_id = Column(Integer, ForeignKey("person.id"), unique=True,
                       default=None)  # create event in sql to make this unchangeable
    person = relationship("Person", backref="person", foreign_keys=[person_id])

    created_by_id = Column(Integer, ForeignKey("user.id"),
                           default=None)  # self Foreign Key , create trigger on sql to prevent update


class UserRole(Base):
    __tablename__ = "user_role"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, nullable=False)
    __mapper_args__ = {"version_id_col": version}

    country_code = Column(String(5), nullable=False)
    primary_mobile_no = Column(String(20), nullable=False)
    first_name = Column(String(20), nullable=False)
    middle_name = Column(String(20), default=None)
    last_name = Column(String(20), default=None)
    dob = Column(Date, default=None)

    address = relationship("PersonAddress", cascade="all, delete",
                         passive_deletes=True)  # should be list-like , 1 to many
    phone_no = relationship("PersonPhoneNo", cascade="all, delete",
                         passive_deletes=True)  # should be list-like, 1 to many
    email = relationship("PersonEmail", cascade="all, delete",
                         passive_deletes=True)


    gender = Column(String(5), default=None)
    is_deceased = Column(Boolean, default=False)
    deceased_date = Column(Date, default=None)

    date_created = Column(DateTime, default=datetime.datetime.now)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_by = relationship("User", backref="createdBy",
                              foreign_keys=[created_by_id])

    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    last_updated_by_id = Column(Integer, ForeignKey("user.id"), default=None)
    updated_by = relationship("User", backref="updatedBy",
                              foreign_keys=[last_updated_by_id])

    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(Integer, ForeignKey("user.id"), default=None)
    deleted_by = relationship("User", backref="DeletedBy",
                              foreign_keys=[deleted_by_id])

    cultivator_id = Column(Integer, ForeignKey("user.id"), default=None)  # Foreign key constraint
    cultivator = relationship("User", backref="personCultivator", foreign_keys=[cultivator_id])

    is_active = Column(Boolean, default=True)

    def full_name(self):
        fullName = self.first_name + ((" " + self.middle_name) if self.middle_name != None else '') + (
            (" " + self.last_name) if self.last_name != None else '')
        return fullName


class CountryCode(Base):
    __tablename__ = "country_code"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(5), unique=True)
    country_name = Column(String(50))
    Country_short_name = Column(String(10))


class PersonPhoneNo(Base):
    __tablename__ = "person_phone_no"
    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, nullable=False)

    person_id = Column(Integer, ForeignKey("person.id", ondelete="CASCADE"),
                       nullable=False)  # applying cascade delete to foreign key

    mobile_no = Column(String(15), nullable=False)
    country_code = Column(String(5), nullable=False)
    is_primary_no = Column(Boolean, default=False)
    is_whatsapp_no = Column(Boolean, default=False)
    dont_sms = Column(Boolean, default=False)
    dont_whatsapp = Column(Boolean, default=False)
    dont_call = Column(Boolean, default=False)

    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_by = relationship("User", backref="phoneCreatedBy",
                              foreign_keys=[created_by_id])

    date_created = Column(DateTime, default=datetime.datetime.now)

    last_updated_by_id = Column(Integer, ForeignKey("user.id"), default=None)
    updated_by = relationship("User", backref="phoneUpdatedBy",
                              foreign_keys=[last_updated_by_id])

    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    is_deleted = Column(Boolean, default=False)

    deleted_by_id = Column(Integer, ForeignKey("user.id"), default=None)
    deleted_by = relationship("User", backref="phoneDeletedBy",
                              foreign_keys=[deleted_by_id])

    __mapper_args__ = {"version_id_col": version}


class PersonEmail(Base):
    __tablename__ = "person_email"
    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, nullable=False)
    person_id = Column(Integer, ForeignKey("person.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(30), nullable=False)
    is_primary_email = Column(Boolean, default=False)
    dont_email = Column(Boolean, default=False)

    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_by = relationship("User", backref="emailCreatedBy",
                              foreign_keys=[created_by_id])

    date_created = Column(DateTime, default=datetime.datetime.now)

    last_updated_by_id = Column(Integer, ForeignKey("user.id"), default=None)
    updated_by = relationship("User", backref="emailUpdatedBy",
                              foreign_keys=[last_updated_by_id])

    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    is_deleted = Column(Boolean, default=False)

    deleted_by_id = Column(Integer, ForeignKey("user.id"), default=None)
    deleted_by = relationship("User", backref="emailDeletedBy",
                              foreign_keys=[deleted_by_id])

    __mapper_args__ = {"version_id_col": version}


class PersonAddress(Base):
    __tablename__ = "person_address"
    id = Column(Integer, primary_key=True, index=True)
    version = Column(Integer, nullable=False)

    person_id = Column(Integer, ForeignKey("person.id", ondelete="CASCADE"), nullable=False)

    address_line1 = Column(String(30), nullable=False)
    address_line2 = Column(String(30))
    city = Column(String(20))
    district = Column(String(20), nullable=False)
    state = Column(String(20), nullable=False)
    country = Column(String(20), nullable=False)
    postal_code = Column(String(10))

    is_primary_address = Column(Boolean, default=False)

    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_by = relationship("User", backref="addressCreatedBy",
                              foreign_keys=[created_by_id])

    date_created = Column(DateTime, default=datetime.datetime.now)

    last_updated_by_id = Column(Integer, ForeignKey("user.id"), default=None)
    updated_by = relationship("User", backref="addressUpdatedBy",
                              foreign_keys=[last_updated_by_id])
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    is_deleted = Column(Boolean, default=False)

    deleted_by_id = Column(Integer, ForeignKey("user.id"), default=None)
    deleted_by = relationship("User", backref="addressDeletedBy",
                              foreign_keys=[deleted_by_id])

    __mapper_args__ = {"version_id_col": version}
#
#
# class Visit(Base):
#     __tablename__ = "visit"
#     id = Column(Integer, primary_key=True, index=True)
#     version = Column(Integer, nullable=False)
#     person_id = Column(Integer, ForeignKey("person.id"), nullable=False)
#     location = Column(String(50))
#     remarks = Column(String(100))
#     tentative_check_in_date_time = Column(DateTime)
#     tentative_check_out_date_time = Column(DateTime)
#     actual_check_in_date_time = Column(DateTime)
#     actual_check_out_date_time = Column(DateTime)
#     pax = Column(Integer)  # no of persons in group
#     accommodation = Column(String(100))
#
#     created_by_id = Column(Integer, default=None)
#     date_created = Column(DateTime, default=datetime.datetime.now)
#     last_updated_by_id = Column(Integer, default=None)
#     last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
#     is_deleted = Column(Boolean, default=False)
#     deleted_by_id = Column(Integer, default=None)
#
#     is_active = Column(Boolean, default=True)
#
#     __mapper_args__ = {"version_id_col": version}
#
#
# class Orientation(Base):
#     __tablename__ = "orientation"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50))
#     cultivator_id = Column(Integer)  # will be tour guide for persons whom cultivator is already assigned
#     cultivator_assistant_id = Column(Integer)
#     orienter_id = Column(Integer)
#     orientation_date = Column(DateTime)
#     venue = Column(String(30))
#
#     created_by_id = Column(Integer, default=None)
#     date_created = Column(DateTime, default=datetime.datetime.now)
#     last_updated_by_id = Column(Integer, default=None)
#     last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
#     is_deleted = Column(Boolean, default=False)
#     deleted_by_id = Column(Integer, default=None)
#
#
# class OrientationParticipants(Base):
#     __tablename__ = "orientation_participants"
#
#     id = Column(Integer, primary_key=True, index=True)
#     orientation_id = Column(Integer, default=None)
#     visit_id = Column(Integer, default=None)
#     check_in_time = Column(Time)
#     attended = Column(Boolean, default=False)
#
#
# class PersonRelationships(Base):
#     __tablename__ = "person_relationships"
#
#     id = Column(Integer, primary_key=True, index=True)
#
#     relationship_name = Column(String(50))
#     person_primary_id = Column(Integer, ForeignKey("person.id"), default=None)
#     person_secondary_id = Column(Integer, ForeignKey("person.id"), default=None)
#     reverse_relationship_name = Column(String(50))
#
#     created_by_id = Column(Integer, default=None)
#     date_created = Column(DateTime, default=datetime.datetime.now)
#     last_updated_by_id = Column(Integer, default=None)
#     last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
#     is_deleted = Column(Boolean, default=False)
#     deleted_by_id = Column(Integer, default=None)
#
#
# class RelationshipNames(Base):
#     __tablename__ = "relationship_names"
#
#     id = Column(Integer, primary_key=True, index=True)
#     relationship_name_wrt_primary_id = Column(String(50))
#     relationship_name_wrt_secondary_id = Column(String(50))
#
#     created_by_id = Column(Integer, default=None)
#     date_created = Column(DateTime, default=datetime.datetime.now)
#     last_updated_by_id = Column(Integer, default=None)
#     last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
#     is_deleted = Column(Boolean, default=False)
#     deleted_by_id = Column(Integer, default=None)
