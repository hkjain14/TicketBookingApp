from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Admin(db.Model):
    admin_id = db.Column(db.Integer(), primary_key = True)
    admin_username = db.Column(db.String(50), nullable=False)
    admin_password = db.Column(db.String(50), nullable = False)
    def __repr__(self):
        return "<Admin %r>" %self.admin_username

class User(db.Model):
    user_id = db.Column(db.Integer(), primary_key = True)
    user_username = db.Column(db.String(50), nullable=False)
    user_password = db.Column(db.String(50), nullable = False)
    bookings = db.relationship("Booking", backref = "user", cascade="all, delete")
    def __repr__(self):
        return "<Users %r>" %self.user_username

class Venue(db.Model):
    venue_id = db.Column(db.Integer(), primary_key = True)
    venue_name = db.Column(db.String(50), nullable=False)
    venue_place = db.Column(db.String(50), nullable=False)
    venue_location = db.Column(db.String(50), nullable = False)
    venue_capacity = db.Column(db.Integer(), nullable = False)
    shows = db.relationship("Show", backref = "venue", cascade="all, delete")
    def __repr__(self):
        return "<Users %r>" %self.user_name

class Show(db.Model):
    show_id = db.Column(db.Integer(), primary_key=True)
    show_name = db.Column(db.String(50), nullable=False)
    show_rating = db.Column(db.String(50), nullable=False)
    show_start_time = db.Column(db.String(50), nullable=False)
    show_end_time = db.Column(db.String(50), nullable=False)
    show_tags = db.Column(db.String(50), nullable=False)
    show_price = db.Column(db.Integer(), nullable=False)
    show_available_seats = db.Column(db.Integer(), nullable=False)
    show_venue_id = db.Column(db.Integer(), db.ForeignKey("venue.venue_id"), nullable=False)
    bookings = db.relationship("Booking", backref="show", cascade="all, delete")
    def __repr__(self):
        return "<Show %r>" %self.show_name

class Booking(db.Model):
    booking_id = db.Column(db.Integer(), primary_key=True)
    booking_tickets_booked = db.Column(db.Integer(), nullable=False)
    booking_show_id = db.Column(db.Integer(), db.ForeignKey("show.show_id"), nullable=False)
    booking_user_id = db.Column(db.Integer(), db.ForeignKey("user.user_id"), nullable=False)
    def __repr__(self):
        return "<Show %r>" %self.show_name

