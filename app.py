""" 
there is an admin account used, to log in to it, use the regular login page and enter these credentials:
                    username: admin
                    password: not123
there is a logged in owner too, this will allow you to enquire about a property. To see this in full effect, make an enquiry to property 1.
Then sign into this account and go to the profile page:
                    username: bquinn129
                    password: iambrian
i would also recommend taking a look back at the home page after viewing a couple of properties to see a recently viewed page appear.
all properties have their own page, click the name of the property to view it
    
"""

from flask import Flask, render_template, url_for, redirect, session, g, request
from forms import ListingForm, RegisterForm, LoginForm, MortgageForm, RefineForm, ReviewForm, AddToWishlist, Enquiries, NewPasswordForm, NewUsernameForm, BidForm
from database import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from functools import wraps
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "a9094-5306-6752-6180"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.teardown_appcontext(close_db)
Session(app)

@app.before_request
def logged_in_user():
    g.user = session.get("username", None)
    g.admin = session.get("username", None)

def login_required(view):
    """add at start of routes where users need to be logged in to access"""
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

def admin_required(view):
    """add at start of routes where users admin needs to be logged in to access"""
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.admin != "admin":
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

def mortgage(price):
    """calculate a mortgage"""
    form = MortgageForm()
    period = form.period.data           #how long the mortgage is for
    monthly = price / 12 / int(period)  #get monthly installments
    monthly = monthly * 1.0315          #add interest
    monthly = round(monthly, 2)
    yearly = monthly * 12 * 1.032       #get yearly rate with APR + interest
    yearly = round(yearly, 2)
    total = yearly * int(period)        #get total + interest + APR
    total = round(total, 2)
    return monthly, yearly, total

def choices(option):
    """update choices in a SelectField/RadioField/etc. in forms.py"""
    db = get_db()
    choices = db.execute(f"""SELECT DISTINCT {option} FROM properties 
                             ORDER BY {option};""").fetchall()          #alphabetical order
    list_of_choices = []
    list_of_choices.append("Select Option")                             #set default to "Select Option"
    for dictionary in choices:
        for key in dictionary.keys():
            list_of_choices.append(dictionary[key])
    return list_of_choices

def save_image(image):
    """save an image into a folder"""
    #resource used:https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
    if image:
        # Save the image file to the images folder
        filename = image.filename
        image_path = os.path.join(app.root_path, 'static', 'images', filename)
        image.save(image_path)
        return filename
    
def create_reviews(database_name):
    """create a new database to hold a property's reviews"""
    #resource used:https://www.sqlite.org/schematab.html
    
    #check it table already exists i.e. reviews already submitted for that property
    db = get_db()
    table_exists = db.execute(f"""SELECT name FROM sqlite_master
                                  WHERE type='table' AND name=?;""", (database_name,)).fetchone()
    if not table_exists:
        db.execute(f"""CREATE TABLE {database_name}
                      (
                        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id VARCHAR(16) NOT NULL,
                        review TEXT NOT NULL);""")
        db.commit()

def update_view(property_id):
    """check to see if a property has been recently viewed by the user"""

    if "recently_viewed" not in session:
        session["recently_viewed"] = []

    #if it has, append it to the recently viewed list
    if property_id not in session["recently_viewed"]:
        session["recently_viewed"].append(property_id)

def recently_viewed():
    """fetches three of the recently viewed properties"""

    db = get_db()
    viewed_properties = []
    for property_id in session["recently_viewed"]:
        viewed_property = db.execute("""SELECT * FROM properties
                                          WHERE property_id = ?;""", (property_id,)).fetchone()
        viewed_properties.append(viewed_property)
    while len(viewed_properties) > 3:
        viewed_properties.pop(0)
    return viewed_properties

def delete_image(property_id):
    """deletes an image from the images folder"""

    db = get_db()
    image_row = db.execute("""SELECT photo FROM listings_for_approval
                              WHERE property_id = ?;""", (property_id,)).fetchone()
    image_name = image_row[0]
    image_path = os.path.join(app.root_path, 'static', 'images', image_name)
    os.remove(image_path)

@app.route("/clear_enquiry/<int:enquiry_id>")
@login_required
def clear_enquiry(enquiry_id):
    db = get_db()
    db.execute("""DELETE FROM enquiries 
                  WHERE enquiry_id = ?;""", (enquiry_id,))
    db.commit()
    return redirect(url_for('profile'))

@app.route("/")
def index():
    """home page"""

    viewed_properties = []
    if "recently_viewed" not in session:
        session["recently_viewed"] = []
    #show recently viewed on home page
    if session.get("username") is not None and session["recently_viewed"] != []:
        viewed_properties = recently_viewed()
    return render_template("index.html", viewed_properties=viewed_properties)

@app.route("/register", methods=["GET", "POST"])
def register():
    """register a user in the database"""
    form = RegisterForm()
    if form.validate_on_submit():
        #collect user data
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password2 = form.password2.data
        db = get_db()

        #if user already exists
        clashing_email = db.execute("""SELECT * FROM users
                                       WHERE email = ?;""", (email,)).fetchone()
        clashing_user = db.execute("""SELECT * FROM users
                                    WHERE user_id = ?;""", (username,)).fetchone()
        if clashing_email is not None:
            form.email.errors.append("Username already exists")
        else:
            if clashing_user is not None:
                form.username.errors.append("Username already exists")
            else:
                db.execute("""INSERT INTO users (user_id, email, password)
                        VALUES (?, ?, ?);""", (username, email, generate_password_hash(password)))
                db.commit()
                return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """log in a user that is already registered in database"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()

        #check if user exists
        user_check = db.execute("""SELECT * FROM users
                                    WHERE user_id = ?;""", (username,)).fetchone()
        if user_check is None:
            form.username.errors.append("Username does not exist")

        #check if encrypted password doesn't match entered password associated with username
        elif not check_password_hash(user_check["password"], password):
            form.password.errors.append("Incorrect Password.")
        else:
            session.clear()
            session["username"] = username

            #return to previous page if there was one
            next_page = request.args.get("next")

            #otherwise return to homepage
            if not next_page:
                next_page = url_for("index")
            return redirect(next_page)
    return render_template("login.html", form=form)
            
@app.route("/logout")
def logout():
    """log a user out of their account and clear their session"""
    session.clear()
    return redirect(url_for("index"))

@app.route("/listing", methods=["GET", "POST"])
@login_required
def listing():
    """list a property"""

    form = ListingForm()
    message=""
    if form.validate_on_submit():
        #collect data
        full_name = form.full_name.data
        email = form.email.data
        address = form.address.data
        county = form.county.data
        post_code = form.post_code.data
        price = form.price.data
        house_type = form.house_type.data
        bedroom = form.bedrooms.data
        bathroom = form.bathrooms.data
        photo = form.photo.data
        filename = save_image(photo)
        description = form.description.data
        db = get_db()
        #check if property is already listed
        clashing_property = db.execute("""SELECT * FROM properties
                                    WHERE address = ?
                                    AND post_code = ?;""", (address, post_code)).fetchone()
        if clashing_property is not None:
            form.post_code.errors.append("Property already listed")
        else:
            #if not send it to the admin page to be verified
            db.execute("""INSERT INTO listings_for_approval (full_name, email, address, county, post_code, price, house_type, bedroom, bathroom, photo, description)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (full_name, email, address, county, post_code, price, house_type, bedroom, bathroom, filename, description))
            db.commit()
            message = "New property successfully submitted"
    return render_template("listing_form.html", form=form, message=message)

@app.route("/remove_from_wishlist/<int:property_id>")
@login_required
def remove_from_wishlist(property_id):
    """remove an item from a users wishlist"""

    if property_id in session["wishlist"]:
        session["wishlist"].remove(property_id)
    return redirect(url_for("wishlist"))

@app.route("/add_to_wishlist/<int:property_id>")
@login_required
def add_to_wishlist(property_id):
    """add an item to a users wishlist"""
    if "wishlist" not in session:
        session["wishlist"] = []
    if property_id not in session["wishlist"]:
        session["wishlist"].append(property_id)
    else:
        return redirect(url_for("property", property_id=property_id))
    return redirect(url_for("wishlist"))

@app.route("/wishlist")
@login_required
def wishlist():
    """show a user their wishlist"""

    if "wishlist" not in session:
        session["wishlist"] = []
    places = {}
    db = get_db()
    
    #display the information associated with the property id in their wishlist
    for property_id in session["wishlist"]:
        property = db.execute("""SELECT * from properties 
                                 WHERE property_id = ?;""", (property_id,)).fetchone()
        address = property["address"]
        places[property_id] = address
    return render_template("wishlist.html", wishlist=session["wishlist"], places=places)    

@app.route("/property/<int:property_id>", methods=["GET","POST"])
def property(property_id):
    """display info relating to a single property - mortgage, reviews, adding to wishlist, enquiries"""
    #resource used:https://www.reddit.com/r/flask/comments/b21bv7/multiple_forms_and_buttons_best_practices/

    #mortgage installments
    form = MortgageForm()
    monthly = 0
    yearly = 0
    total = 0

    #connect to DB
    db = get_db()

    #get all information associated with selected property
    property = db.execute("""SELECT * FROM properties
                             WHERE property_id = ?;""", (property_id,)).fetchone()
    
    #update properties view flag to True
    if session.get("username") is not None:
        update_view(property_id)

    #call mortgage function
    if form.submit.data and form.validate_on_submit():
        monthly, yearly, total = mortgage(property["price"])

    #reviewing a property
    form2 = ReviewForm()
    database_name = 'reviews_{}'.format(property_id)
    comment = ""
    table_exists = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (database_name,)).fetchone()
    if not table_exists:
        #if table does not exist - select blank database i.e. show no reviews
        reviews = db.execute("""SELECT * FROM reviews;""")
    else:
        #if table does exist - fetch reviews for that property
        reviews = db.execute(f"""SELECT * FROM {database_name} LIMIT 9;""").fetchall()

    if session.get("username"):
        #if user is logged in
        if form2.submit_review.data and form2.validate_on_submit():
            user_id = session["username"]
            review_text = form2.review.data
            #call function to create review DB for property
            create_reviews(database_name)
            if review_text != " " and review_text != "\n":
                db.execute(f"""INSERT INTO {database_name} (user_id, review)
                                VALUES (?, ?);""", (user_id, review_text))
                db.commit()
                comment = "Review successfully submitted"
            reviews = db.execute(f"""SELECT * FROM {database_name} ORDER BY review_id ASC LIMIT 9;""").fetchall()
    else:
        #user is not logged in
        form2.review.errors = list(form2.review.errors)
        form2.review.errors.append("Please login to review.")

    #adding to wishlist
    form3 = AddToWishlist()
    if form3.submit_wishlist.data and form3.validate_on_submit():
        return redirect(url_for("add_to_wishlist", property_id=property_id))
        
    #suggested properties
    suggested_properties = db.execute("""SELECT * FROM properties 
                                         WHERE county = (
                                            SELECT county FROM properties
                                            WHERE property_id = ?)
                                         AND property_id != ?;""", (property_id,property_id)).fetchall()

    #enquiries
    form4 = Enquiries()
    if form4.submit_enquiry.data and form4.validate_on_submit():
        full_name = form4.full_name.data
        email = form4.email.data
        enquiry = form4.enquiry.data

        #send a notification to the owner on their profile page
        owner_email = db.execute("""SELECT email FROM properties
                                    WHERE property_id = ?;""", (property_id,)).fetchone()
        db.execute("""INSERT INTO enquiries (email, full_name, enquiry, owner_email, property_name)
                      VALUES (?,?,?,?,?);""", (email, full_name, enquiry, owner_email[0], property["address"]))
        db.commit()

    return render_template("property.html", form=form, property=property, monthly=monthly, yearly=yearly, total=total, form2=form2, reviews=reviews, comment=comment, form3=form3, suggested_properties=suggested_properties, form4=form4)

def refine_search(county,min_price,max_price,bedroom,bathroom,house_type):
    """Function uses inputs from property form to refine the houses displayed on the properties page"""
    #opens connection to RefineForm
    form = RefineForm()

    db = get_db()
    #making sure fields that are left as "Select Option" do not return anything relating to that option
    if county == "Select Option" and house_type != "Select Option":
        filters = db.execute("""SELECT * FROM properties
                                WHERE bedroom <= ? AND bathroom <= ?
                                AND price BETWEEN ? AND ?
                                AND house_type = ?;""", (bedroom,bathroom,min_price,max_price,house_type)).fetchall()
    elif county != "Select Option" and house_type == "Select Option":
        filters = db.execute("""SELECT * FROM properties
                                WHERE county = ? AND bedroom <= ? AND bathroom <= ?
                                AND price BETWEEN ? AND ?;""", (county,bedroom,bathroom,min_price,max_price)).fetchall()
    elif county == "Select Option" and house_type == "Select Option":
        filters = db.execute("""SELECT * FROM properties
                                WHERE bedroom <= ? AND bathroom <= ?
                                AND price BETWEEN ? AND ?;""", (bedroom,bathroom,min_price,max_price)).fetchall()
    else:
        filters = db.execute("""SELECT * FROM properties
                                WHERE county = ? AND bedroom <= ? AND bathroom <= ?
                                AND price BETWEEN ? AND ?
                                AND house_type = ?;""", (county,bedroom,bathroom,min_price,max_price,house_type)).fetchall()
    return filters

@app.route("/properties", methods=["GET", "POST"])
def properties():
    """Display full list of properties on website"""
    #opens connection to RefineForm
    form = RefineForm()

    #populating the SelectField choices in RefineForm
    counties = choices("county")
    form.county.choices = counties
    house_types = choices("house_type")
    form.house_type.choices = house_types
    bedrooms = choices("bedroom")
    form.bedrooms.choices = bedrooms
    bathrooms = choices("bathroom")
    form.bathrooms.choices = bathrooms

    if form.validate_on_submit():
        #populate variables with user's entry from form
        county = form.county.data
        min_price = form.min_price.data
        max_price = form.max_price.data
        bedroom = form.bedrooms.data
        bathroom = form.bathrooms.data
        house_type = form.house_type.data

        #call function to filter properties
        filters = refine_search(county,min_price,max_price,bedroom,bathroom,house_type)
    else:
        #return all properties
        db = get_db()
        filters = db.execute("""SELECT * FROM properties""") 
    return render_template("properties.html", filters=filters, form=form)

@app.route("/admin")
@admin_required
def admin():
    """admin control page"""
    #display users - who can from there be banned
    db = get_db()
    users = db.execute("""SELECT * FROM users WHERE user_id != 'admin'""").fetchall()

    #verify a property listing form
    listings = db.execute("""SELECT * FROM listings_for_approval;""")
    return render_template("admin.html", users=users, listings=listings)

@app.route("/ban_user/<string:user_id>")
@admin_required
def ban_user(user_id):
    """ban a user"""

    db = get_db()
    db.execute("""DELETE FROM users WHERE user_id = ?;""", (user_id,))
    db.commit()
    return redirect(url_for("admin"))

@app.route("/approve/<int:property_id>")
@admin_required
def approve(property_id):
    """approve a submitted listing"""
    db = get_db()
    listing = db.execute("""SELECT * FROM listings_for_approval
                             WHERE property_id = ?;""", (property_id,)).fetchone()
    
    #transfer from the listing waiting list to the actual database to populate the properties page
    db.execute("""INSERT INTO properties (full_name, email, address, county, post_code, price, house_type, bedroom, bathroom, photo, description)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?);""", 
                    (listing["full_name"], listing["email"], listing["address"], listing["county"], listing["post_code"],
                     listing["price"], listing["house_type"], listing["bedroom"], listing["bathroom"], listing["photo"], 
                     listing["description"]))
    db.commit()

    #remove the listing for approval entry
    db.execute("""DELETE FROM listings_for_approval WHERE property_id = ?;""", (property_id,))
    db.commit()
    return redirect(url_for("admin"))

@app.route("/decline/<int:property_id>")
@admin_required
def decline(property_id):
    """decline a submitted listing"""
    
    delete_image(property_id)
    db = get_db()
    db.execute("""DELETE FROM listings_for_approval WHERE property_id = ?;""", (property_id,))
    db.commit()
    return redirect(url_for("admin"))

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """display the users profile page"""

    form = NewPasswordForm()
    form2 = NewUsernameForm()
    password_message = ""
    username_message = ""
    db = get_db()

    #show the list of enquiries on their property
    enquiries = db.execute("""SELECT * FROM enquiries
                              WHERE owner_email = (SELECT email FROM users
                                                   WHERE user_id = ?);""", (session["username"],)).fetchall()
    
    #change the users password
    if form.submit_password.data and form.validate_on_submit():
        new_password = form.new_password.data
        db.execute("""UPDATE users SET password = ?
                      WHERE user_id = ?;""", (generate_password_hash(new_password),session["username"]))
        db.commit()
        password_message = "Password Successfully Changed"
    
    #change the users username
    if form2.submit_username.data and form2.validate_on_submit():
        new_username = form2.new_username.data
        clashing_user = db.execute("""SELECT * FROM users
                                      WHERE user_id = ?;""", (new_username,)).fetchone()
        #check if username already exists
        if clashing_user is not None:
            form.new_password.errors.append("Error: Username already exists")
        else:
            db.execute("""UPDATE users SET user_id = ?
                          WHERE user_id = ?;""", (new_username, session["username"]))
            db.commit()
            username_message = "Username Successfully Changed"
            session.clear()
            session["username"] = new_username

    if "bid_amount" not in session:
        session["bid_amount"] = {}
    return render_template("profile.html",form=form,form2=form2,enquiries=enquiries,password_message=password_message,username_message=username_message, bids=session["bid_amount"])

@app.route("/bid/<int:property_id>", methods=["GET", "POST"])
@login_required
def bid(property_id):
    form = BidForm()
    message = ""
    db = get_db()
    current_highest_bid = db.execute("""SELECT bid_amount FROM properties 
                                            WHERE property_id = ?;""",  (property_id,)).fetchone()
    if form.validate_on_submit():
        bid_amount = form.bid_amount.data
        
        if bid_amount <= current_highest_bid[0]:
            form.bid_amount.errors.append("Bid must be higher than current highest bid")
        else:
            db.execute("""UPDATE properties SET bid_amount = ? 
                          WHERE property_id = ?;""", (bid_amount,property_id))
            db.commit()
            message = "Bid Successfully Placed"
            property_name = db.execute("""SELECT address FROM properties
                                          WHERE property_id = ?;""", (property_id,)).fetchone()
            session["bid_amount"] = {}
            session["bid_amount"]["property"] = property_name[0]
            session["bid_amount"]["amount"] = bid_amount
            print(session["bid_amount"])
    return render_template("bid.html", form=form, message=message, current_highest_bid=current_highest_bid[0])