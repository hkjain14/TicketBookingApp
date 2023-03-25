#MANY-TO-MANY--> Book & Sections, A section can have multiple books but a book can only belong to one section/
#Example-2--> A parent can have multiple children but a child can have only one parent

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Configuring one to many database with our application
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabmm.sqlite3"

db = SQLAlchemy(app) #Create the db object of SQLAlchemy

class Section(db.Model):  #db.Model is a class which is inherited by class Section
    section_id = db.Column(db.Integer(), primary_key = True)
    section_name = db.Column(db.String(50), nullable = False)
    books = db.relationship("Book", backref = "section", secondary = 'association') #By this line we can do s1.books...it is just giving us privilege to add all the books to a partivular section
    #Here in many-to-many relationship secondary is required which says this m-to-m relationship is associated with this association table...here cascade is not required


    def __repr__(self):
        return "<Section %r>" %self.section_name


class Book(db.Model):
    book_id = db.Column(db.Integer(), primary_key=True)
    book_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Book %r>" %self.book_name

class Association(db.Model):
    section_id = db.Column(db.Integer(), db.ForeignKey("section.section_id"), primary_key = True)
    book_id = db.Column(db.Integer(), db.ForeignKey("book.book_id"), primary_key = True)
    #Here the unique combination of section_id & book_id acts as primary key of association table
