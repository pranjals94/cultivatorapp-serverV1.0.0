import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, Time, BIGINT
from sqlalchemy.orm import relationship
from database import Base


# --------------one to many -------------------
class ParentOneToMany(Base):
    __tablename__ = "parent_table_one_2_many"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    children = relationship("ChildOneToMany", back_populates="parent", cascade="all, delete",
                            passive_deletes=True, )  # by back_populates we get all the children as array
    # cascade="all, delete":- when a “parent” object is marked for deletion, its related “child” objects should also
    # be marked for deletion


class ChildOneToMany(Base):
    __tablename__ = "child_table_one_2_many"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    parent_id = Column(Integer, ForeignKey("parent_table_one_2_many.id", ondelete="CASCADE"),
                       nullable=False)  # applying cascade delete to foreign key, Note* the Datatype should match the
    # parent datatype, here is Integer
    parent = relationship("ParentOneToMany", back_populates="children")
    # back populates means to get the parent ie to reverse, and also used to create new child for an existing parent

# --------------one to many end-------------------
