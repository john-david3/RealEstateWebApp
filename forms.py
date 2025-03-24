from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField, IntegerField, SelectField, EmailField, PasswordField, RadioField, TextAreaField
from wtforms.validators import InputRequired, DataRequired, EqualTo

class ListingForm(FlaskForm):
    full_name = StringField("Full Name:", validators=[InputRequired()])
    email = EmailField("Email Address:", validators=[DataRequired()])
    address = StringField("Address of Property:", validators=[InputRequired()])
    county = StringField("County:", validators=[InputRequired()])
    post_code = StringField("Postcode of Property:", validators=[InputRequired()])
    price = IntegerField("Listing Price:", validators=[InputRequired()])
    house_type = SelectField("House Type:", choices=["Detached House", "Semi-Detached House", "Terraced House", "Bungalow", "Apartment", "Duplex", "Studio"],validators=[InputRequired()])
    bedrooms = SelectField("Number of Bedrooms:", choices=[1,2,3,4,5,6,7,8], validators=[DataRequired()])
    bathrooms = SelectField("Number of Bathrooms:", choices=[1,2,3,4,5,6,7,8], validators=[DataRequired()])
    photo = FileField("Picture of Property:", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images Only!')])
    description = TextAreaField("Description of property:", validators=[InputRequired()])
    submit = SubmitField("List Property")

class RegisterForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    email = EmailField("Email:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class RefineForm(FlaskForm):
    county = SelectField("County:", choices=[])
    min_price = SelectField("Min. Price:", choices=[0, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1200000, 1400000, 1600000, 1800000, 2000000])
    max_price = SelectField("Max. Price:", choices=[0, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1200000, 1400000, 1600000, 1800000, 2000000], default=2000000)
    house_type = SelectField("House Type:", choices=[])
    bedrooms = SelectField("Max Bedrooms:", choices=[], default=4)
    bathrooms = SelectField("Max Bathrooms:", choices=[], default=4)
    submit = SubmitField("Show Results")

class MortgageForm(FlaskForm):
    period = RadioField("Period of Mortgage(in years):", choices=[5, 10, 15, 20, 25, 30, 35], default=5)
    submit = SubmitField("Calculate Mortgage")

class ReviewForm(FlaskForm):
    review = TextAreaField("Review:", validators=[InputRequired()])
    submit_review = SubmitField("Submit Review")

class AddToWishlist(FlaskForm):
    submit_wishlist = SubmitField("Add to wishlist")

class Enquiries(FlaskForm):
    full_name = StringField("Enter Full Name:", validators=[InputRequired()])
    email = EmailField("Enter Email", validators=[InputRequired()])
    enquiry = TextAreaField("Enquiries to owner:", validators=[InputRequired()])
    submit_enquiry = SubmitField("Submit Enquiry")

class NewPasswordForm(FlaskForm):
    new_password = PasswordField("Enter New Password:", validators = [InputRequired()])
    confirm_new_password = PasswordField("Confirm New Password:", validators=[InputRequired(), EqualTo("new_password")])
    submit_password = SubmitField("Save Changes")

class NewUsernameForm(FlaskForm):
    new_username = StringField("New Username:", validators=[InputRequired()])
    submit_username = SubmitField("Save Changes")
    
class BidForm(FlaskForm):
    bid_amount = IntegerField("Place a bid:", validators=[InputRequired()])
    submit = SubmitField("Place Bid")
    