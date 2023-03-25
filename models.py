#ONE-TO-MANY--> Book & Sections, A section can have multiple books but a book can only belong to one section/
#Example-2--> A parent can have multiple children but a child can have only one parent

from flask import Flask
#Since here we're not running any server therefore we don't need FLask here
from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__) This line is also not required
#Configuring one to many database with our application

db = SQLAlchemy()

class Section(db.Model):  #db.Model is a class which is inherited by class Section
    section_id = db.Column(db.Integer(), primary_key = True)
    section_name = db.Column(db.String(50), nullable = False)
    books = db.relationship("Book", backref = "section", cascade="all, delete") #By this line we can do s1.books...it is just giving us privilege to add all the books to a partivular section
    #Cascade- it makes sure if the parent element gets deleted all its children are also deleted

    def __repr__(self):
        return "<Section %r>" %self.section_name


class Book(db.Model):
    book_id = db.Column(db.Integer(), primary_key=True)
    book_name = db.Column(db.String(50), nullable=False)
    sect = db.Column(db.Integer(), db.ForeignKey("section.section_id"), nullable=False) #creating another column to define the one-to-many relationship bw books and sections
#If classname is Section----> table name would be "section"


    def __repr__(self):
        return "<Book %r>" %self.book_name


#In the language of MVC, the file where classes & tables are present is called model.
#Therefore we're changing the filename from models.py to models.py

#The part that we want to work as an application should be called controller
#Here the file that we're gonna work as controller we're going to rename as app.py