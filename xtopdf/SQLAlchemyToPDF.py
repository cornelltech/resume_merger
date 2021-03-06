
# SQLAlchemyToPDF.py
# Program to read database data via SQLAlchemy 
# and publish it to PDF. This is a demo.
# Author: Vasudev Ram - http://www.dancingbison.com
# Copyright 2013 Vasudev Ram
# Version 0.1

from PDFWriter import PDFWriter
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=False)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    email = Column(String)

    def __init__(self, name, fullname, email):
        self.name = name
        self.fullname = fullname
        self.email = email

Base.metadata.create_all(engine) 

a_user = User('A', 'A 1', 'A1@gmail.com')
b_user = User('B', 'B 2', 'B2@yahoo.com')
c_user = User('C', 'C 3', 'C3@hotmail.com')

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

session = Session()

for user in (a_user, b_user, c_user):
    session.add(user)

pw = PDFWriter('users.pdf')
pw.setFont("Courier", 12)
pw.setHeader("SQLAlchemyToPDF - User table report")
pw.setFooter("Generated by xtopdf using Reportlab and Python")

users = session.query(User)
for user in users:
    pw.writeLine(user.name + "|" + user.fullname + "|" + user.email)

pw.savePage()
pw.close()

