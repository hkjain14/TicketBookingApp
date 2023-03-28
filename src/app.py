from flask import Flask, render_template, redirect, request, url_for, session
from models import *

app = Flask(__name__)
db.init_app(app)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ticketDb.sqlite3"
app.config['SECRET_KEY'] = 'SecretKeyForSession'

### Root Routes
@app.route('/', methods = ['GET'])
def root():
    session.pop('username', None)
    return render_template('root_view.html')

@app.route('/', methods = ['POST'])
def postRoot():
    user_type = request.form.get('user_type')
    if user_type == "User Login":
        return redirect('/login/user')
    return redirect('/login/admin')



### Login Routes

@app.route('/login/user', methods = ['GET'])
def loginUser():
    return render_template('user_login.html')

@app.route('/login/user', methods = ['POST'])
def loginUserPost():
    login_type = request.form.get('login_type')
    if login_type == "Register":
        return redirect('/register')
    username = request.form.get('username')
    password = request.form.get('password')

    users = User.query.filter_by(user_username=username).all()
    if users != [] and users[0].user_password == password:
        # User logged in successfully.
        session['username'] = username
        return redirect('/user')
    # TODO : Show error that wrong credentials
    return redirect('/login/user')

@app.route('/register', methods = ['GET'])
def registerUser():
    return render_template('user_register.html')

@app.route('/register', methods = ['POST'])
def registerUserPost():
    username = request.form.get('username')
    password = request.form.get('password')

    users = User.query.filter_by(user_username=username).all()
    if users != []:
        # TODO : Show error that already registered credentials
        return redirect('/register')
    user = User(user_username = username, user_password = password)
    db.session.add(user)
    db.session.commit()
    return redirect('/login/user')

@app.route('/login/admin', methods = ['GET'])
def loginAdmin():
    return render_template('admin_login.html')

@app.route('/login/admin', methods = ['POST'])
def loginAdminPost():
    username = request.form.get('username')
    password = request.form.get('password')

    # Assumption is that there is a single admin of app
    admin = Admin.query.all()[0]
    if(username == admin.admin_username and password == admin.admin_password):
        session['username'] = username
        return redirect('/admin')
    # TODO: Show error that wrong credentials
    return redirect('/login/admin')


### Admin view
@app.route('/admin', methods = ['GET'])
def viewAdmin():
    venues = Venue.query.all()
    for venue in venues:
        venue.showsArr = Show.query.filter_by(show_venue_id=venue.venue_id).all()
    return render_template('admin_view.html', username=session['username'], venues=venues)

@app.route('/create/venue', methods = ['GET'])
def createVenue():
    return render_template('create_venue.html', username=session['username'])

@app.route('/create/venue', methods = ['POST'])
def postCreateVenue():
    venueName = request.form.get('venueName')
    place = request.form.get('place')
    location = request.form.get('location')
    capacity = int(request.form.get('capacity'))

    venue = Venue(venue_name=venueName, venue_place=place, venue_location=location, venue_capacity=capacity)
    db.session.add(venue)
    db.session.commit()
    return redirect('/admin')

@app.route('/edit/venue', methods = ['GET'])
def editVenue():
    venueId = request.args.get('venueId')
    return render_template('edit_venue.html', venueId=venueId, username=session['username'])

@app.route('/edit/venue', methods = ['POST'])
def postEditVenue():
    venueId = request.form.get('venueId')
    venue = Venue.query.get(venueId)
    oldCapacity = venue.venue_capacity
    newCapacity = int(request.form.get('capacity'))

    venue.venue_name = request.form.get('venueName')
    venue.venue_place = request.form.get('place')
    venue.venue_location = request.form.get('location')
    venue.venue_capacity = newCapacity

    # Update all corresponding shows if venue updates
    shows = Show.query.filter_by(show_venue_id=venueId).all()
    for show in shows:
        show.show_available_seats = max(0,show.show_available_seats + newCapacity - oldCapacity)

    db.session.commit()
    return redirect('/admin')

@app.route('/delete/venue', methods = ['POST'])
def deleteVenue():
    venueId = request.form.get('venueId')
    venue = db.session.query(Venue).filter(Venue.venue_id == venueId).first()
    db.session.delete(venue)
    # Venue.query.filter_by(venue_id=venueId).delete()
    db.session.commit()
    return redirect('/admin')

@app.route('/create/show', methods = ['GET'])
def createShow():
    venueId = request.args.get('venueId')
    return render_template('create_show.html', venueId=venueId, username=session['username'])

@app.route('/create/show', methods = ['POST'])
def postCreateShow():
    showName = request.form.get('showName')
    rating = request.form.get('rating')
    startTime = request.form.get('startTime')
    endTime = request.form.get('endTime')
    tags = request.form.get('tags')
    price = int(request.form.get('price'))
    venueId = request.form.get('venueId')
    venue = Venue.query.get(venueId)
    seats = venue.venue_capacity

    show = Show(show_name=showName, show_rating=rating, show_start_time=startTime, show_end_time=endTime, show_tags=tags, show_price=price, show_available_seats=seats, show_venue_id=venueId)
    venue.shows.append(show)
    db.session.add(show)
    db.session.commit()
    return redirect('/admin')

@app.route('/edit/show', methods = ['GET'])
def editShow():
    showId = request.args.get('showId')
    return render_template('edit_show.html', showId=showId, username=session['username'])

@app.route('/edit/show', methods = ['POST'])
def postEditShow():
    showId = request.form.get('showId')
    show = Show.query.get(showId)

    show.show_name = request.form.get('showName')
    show.show_rating = request.form.get('rating')
    show.show_start_time = request.form.get('startTime')
    show.show_end_time = request.form.get('endTime')
    show.show_tags = request.form.get('tags')
    show.show_price = request.form.get('price')

    db.session.commit()
    return redirect('/admin')

@app.route('/delete/show', methods = ['POST'])
def deleteShow():
    showId = request.form.get('showId')
    Show.query.filter_by(show_id=showId).delete()
    db.session.commit()
    return redirect('/admin')

@app.route('/summary', methods = ['GET'])
def summary():
    # TODO: Fill summary
    return render_template('summary.html', username=session['username'])


### User view
@app.route('/user', methods = ['GET'])
def viewUser():
    #TODO: Search by show/venue. Rating based should be >=rating, not exact
    venues = Venue.query.all()
    for venue in venues:
        venue.showsArr = Show.query.filter_by(show_venue_id=venue.venue_id).all()
    return render_template('user_view.html', username=session['username'], venues=venues)



@app.route('/book/show', methods = ['GET'])
def bookShow():
    showId = request.args.get('showId')
    show = Show.query.get(showId)
    venue = Venue.query.get(show.show_venue_id)
    return render_template('book_show.html', username=session['username'], showId=showId, showName=show.show_name, venueName=venue.venue_name, startTime=show.show_start_time, endTime=show.show_end_time, seats=show.show_available_seats, price=show.show_price)

@app.route('/book/show', methods = ['POST'])
def postBookShow():
    bookCount = int(request.form.get('bookCount'))
    showId = request.form.get('showId')
    username = session['username']
    userId = User.query.filter_by(user_username=username).all()[0].user_id
    # Create row in Booking table
    booking = Booking(booking_tickets_booked=bookCount, booking_show_id=showId, booking_user_id=userId)
    db.session.add(booking)
    # Update available seat count in Show table
    show = Show.query.get(showId)
    show.show_available_seats = show.show_available_seats - bookCount
    db.session.commit()
    return redirect('/bookings')

@app.route('/bookings', methods = ['GET'])
def bookings():
    #TODO: Rate view
    username = session['username']
    userId = User.query.filter_by(user_username=username).all()[0].user_id
    bookings = Booking.query.filter_by(booking_user_id=userId).all()

    for booking in bookings:
        showId = booking.booking_show_id
        show = Show.query.filter_by(show_id=showId).all()[0]
        venueId = show.show_venue_id
        venue = Venue.query.filter_by(venue_id=venueId).all()[0]
        booking.venueName = venue.venue_name
        booking.showName = show.show_name
        booking.startTime = show.show_start_time
        booking.endTime = show.show_end_time

    return render_template('bookings.html', username=session['username'], bookings=bookings)

@app.route('/profile', methods = ['GET'])
def profile():
    # TODO: Fill profile
    return render_template('profile.html', username=session['username'])

if __name__ == "__main__":
    db.create_all()
    admins = Admin.query.all()
    if admins == []:
        admin = Admin(admin_username='ashish', admin_password='gaba')
        db.session.add(admin)
        db.session.commit()
    app.run(debug=False)

# TODO: separate out routes in files (not that important)
# TODO: at end, check each page's title
# TODO: CORE: remova/deletion of show/venue : confirm button
# TODO: CORE: Deletion of show by admin should delete booking of user
# TODO: CORE: Deletion of venue by admin should delete booking of user
# TODO: CORE: Deletion of venue by admin should delete show
# TODO: Reset username in session when app restarts
# TODO: Check logged in user/admin before showing /user or /admin
# TODO: Show creation should not clash time with already created show (thoda complicated hai (compared to others))
# TODO: venue creation/db entry : multi lang support - utf8 explicit enable for db init
