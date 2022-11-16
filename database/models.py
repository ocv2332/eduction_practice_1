import enum

from sqlalchemy import Column, Integer, ForeignKey, Identity, Text, Date
from sqlalchemy import Enum, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Roles(enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

    @classmethod
    def list(cls):
        return list(map(lambda x: x.value, cls))


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    title = Column(Text, nullable=False, unique=True)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    group_id = Column(Integer, ForeignKey(Group.group_id, ondelete="RESTRICT"))
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    middle_name = Column(Text)
    birthday = Column(Date, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    login = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    role = Column(Enum(Roles), nullable=False)


class Subject(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    teacher_id = Column(Integer, ForeignKey(User.user_id, ondelete="RESTRICT"))
    group_id = Column(Integer, ForeignKey(Group.group_id, ondelete="RESTRICT"))
    title = Column(Text, nullable=False)


class SubjectItem(Base):
    __tablename__ = "subject_items"

    item_id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    subject_id = Column(Integer, ForeignKey(Subject.subject_id, ondelete="CASCADE"))
    title = Column(Text, nullable=False)
    date_event = Column(Date, nullable=False)
    comment = Column(Text)
    max_mark = Column(SmallInteger, nullable=False)


class Mark(Base):
    __tablename__ = "marks"

    mark_id = Column(Integer, Identity(start=1, always=True), primary_key=True)
    student_id = Column(Integer, ForeignKey(User.user_id, ondelete="CASCADE"))
    item_id = Column(Integer, ForeignKey(SubjectItem.item_id, ondelete="CASCADE"))
    mark = Column(SmallInteger, nullable=False)
