from flask import Flask, render_template, redirect, request
from models import *

app = Flask(__name__)

db.init_app(app)
app.app_context().push()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabom.sqlite3"

@app.route('/sections', methods = ['GET','POST'])
def all_sections():
    sections = Section.query.all()
    return render_template('all_sections.html', sections = sections)

@app.route('/books', methods = ['GET', 'POST'])
def all_books():
    books = Book.query.all()
    return render_template('all_books.html', books = books)

@app.route('/<int:section_id>/books')
def sect_books(section_id):
    s1 = Section.query.get(section_id)
    books = Book.query.filter_by(sect= section_id).all()
    return render_template('section_books.html', books = books, s1 = s1)

@app.route('/create/section', methods = ['GET', 'POST'])
def create_section():
    if request.method == "POST":
        sect_name = request.form.get('s_name')
        s1 = Section(section_name = sect_name)
        db.session.add(s1)
        db.session.commit()
        return redirect('/sections')
    return render_template('create_section.html')

@app.route('/create/book/<int:section_id>', methods = ['GET', 'POST'])
def create_book(section_id):
    if request.method == "POST":
        b_name = request.form.get('b_name')
        b1 = Book(book_name = b_name, sect = section_id)
        db.session.add(b1)
        db.session.commit()
        return redirect(f'/{section_id}/books')
    return render_template('create_book.html', section_id = section_id)



if __name__ == "__main__":
    app.run(debug=True)

#OTHER CRUD OPERATIONS
# 3. ---UPDATE---
#update should take me to a form
# b1 = Book.query.get(2)
# b1.book_name = "<new_book_name>"
# b1.commit()
#then it should redirect to sections with updated names

# 4. ---DELETE---
# db.session.delete(b1)

