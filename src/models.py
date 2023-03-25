from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Section(db.Model):
    section_id = db.Column(db.Integer(), primary_key = True)
    section_name = db.Column(db.String(50), nullable = False)
    books = db.relationship("Book", backref = "section", cascade="all, delete")
    def __repr__(self):
        return "<Section %r>" %self.section_name

class Book(db.Model):
    book_id = db.Column(db.Integer(), primary_key=True)
    book_name = db.Column(db.String(50), nullable=False)
    sect = db.Column(db.Integer(), db.ForeignKey("section.section_id"), nullable=False)
    def __repr__(self):
        return "<Book %r>" %self.book_name