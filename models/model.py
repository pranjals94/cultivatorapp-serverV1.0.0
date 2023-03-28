import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, Time, BIGINT
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    hashed_password = Column(String(240))
    email = Column(String(50), unique=True)
    last_log_in = Column(DateTime, default=None)

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)

    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("role.id"), default=None)
    personRole = relationship("Role")  # user will also contain the personRole.(eg:
    # user.personRole.name)

    person_id = Column(BIGINT, ForeignKey("person.id"), nullable=False)  # Foreign key constraint
    person = relationship("Person")  # user will also contain the person.(eg: user.person.id)


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)


class Person(Base):
    __tablename__ = "person"
    id = Column(BIGINT, primary_key=True, index=True)
    version = Column(Integer, nullable=False)
    country_code = Column(String(5), nullable=False)
    primary_mobile_no = Column(String(20), nullable=False)
    first_name = Column(String(20))
    middle_name = Column(String(20))
    last_name = Column(String(20))
    dob = Column(Date, default=None)

    gender = Column(String(5), default=None)
    cultivator_id = Column(BIGINT, default=None)
    is_deceased = Column(Boolean, default=False)
    deceased_date = Column(Date, default=None)

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)

    is_active = Column(Boolean, default=True)

    __mapper_args__ = {"version_id_col": version}
    person_phone_no = relationship("PersonPhoneNo", back_populates="person", cascade="all, delete",
                                   passive_deletes=True)

    def print_full_name(self):
        return f"Full name is {self.full_name}"


class CountryCode(Base):
    __tablename__ = "country_code"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(5), unique=True)
    country_name = Column(String(50))
    Country_short_name = Column(String(10))


class PersonPhoneNo(Base):
    __tablename__ = "person_phone_no"
    id = Column(BIGINT, primary_key=True, index=True)
    version = Column(Integer, nullable=False)

    person_id = Column(BIGINT, ForeignKey("person.id", ondelete="CASCADE"),
                       nullable=False)  # applying cascade delete to foreign key
    person = relationship("Person", back_populates="person_phone_no")

    mobile_no = Column(String(15), nullable=False)
    country_code = Column(String(5), nullable=False)
    is_primary_no = Column(Boolean, default=False)
    is_whatsapp_no = Column(Boolean, default=False)
    dont_sms = Column(Boolean, default=False)
    dont_whatsapp = Column(Boolean, default=False)
    dont_call = Column(Boolean, default=False)

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)

    __mapper_args__ = {"version_id_col": version}


class PersonEmail(Base):
    __tablename__ = "person_email"
    id = Column(BIGINT, primary_key=True, index=True)
    version = Column(Integer, nullable=False)
    person_id = Column(BIGINT, ForeignKey("person.id"), nullable=False)
    email = Column(String(30))
    is_primary_email = Column(Boolean, default=False)
    dont_email = Column(Boolean, default=False)

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)

    __mapper_args__ = {"version_id_col": version}


class PersonAddress(Base):
    __tablename__ = "person_address"
    id = Column(BIGINT, primary_key=True, index=True)
    version = Column(Integer, nullable=False)
    person_id = Column(BIGINT, ForeignKey("person.id"), nullable=False)
    address_line1 = Column(String(30))
    address_line2 = Column(String(30))
    city = Column(String(20))
    district = Column(String(20))
    state = Column(String(20))
    country = Column(String(20))
    postal_code = Column(String(10))
    is_primary_address = Column(Boolean, default=False)

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)

    __mapper_args__ = {"version_id_col": version}


class Visit(Base):
    __tablename__ = "visit"
    id = Column(BIGINT, primary_key=True, index=True)
    version = Column(Integer, nullable=False)
    person_id = Column(BIGINT, ForeignKey("person.id"), nullable=False)
    location = Column(String(50))
    remarks = Column(String(100))
    tentative_check_in_date_time = Column(DateTime)
    tentative_check_out_date_time = Column(DateTime)
    actual_check_in_date_time = Column(DateTime)
    actual_check_out_date_time = Column(DateTime)
    pax = Column(Integer)  # no of persons in group
    accommodation = Column(String(100))

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)

    is_active = Column(Boolean, default=True)

    __mapper_args__ = {"version_id_col": version}


class Orientation(Base):
    __tablename__ = "orientation"

    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String(50))
    cultivator_id = Column(BIGINT)  # will be tour guide for persons whom cultivator is already assigned
    cultivator_assistant_id = Column(BIGINT)
    orienter_id = Column(BIGINT)
    orientation_date = Column(DateTime)
    venue = Column(String(30))

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)


class OrientationParticipants(Base):
    __tablename__ = "orientation_participants"

    id = Column(BIGINT, primary_key=True, index=True)
    orientation_id = Column(BIGINT, default=None)
    visit_id = Column(BIGINT, default=None)
    check_in_time = Column(Time)
    attended = Column(Boolean, default=False)


class PersonRelationships(Base):
    __tablename__ = "person_relationships"

    id = Column(BIGINT, primary_key=True, index=True)

    relationship_name = Column(String(50))
    person_primary_id = Column(BIGINT, ForeignKey("person.id"), default=None)
    person_secondary_id = Column(BIGINT, ForeignKey("person.id"), default=None)
    reverse_relationship_name = Column(String(50))

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)


class RelationshipNames(Base):
    __tablename__ = "relationship_names"

    id = Column(Integer, primary_key=True, index=True)
    relationship_name_wrt_primary_id = Column(String(50))
    relationship_name_wrt_secondary_id = Column(String(50))

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)
