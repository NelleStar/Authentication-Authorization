from flask import Flask, render_template, redirect, session, flash
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///authenticate_authorize"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.app_context().push()

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """redirects to user login"""

    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username

        flash("Welcome! You have successfully created an account!")
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back, {user.username}!")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form)

@app.route('/users/<string:username>', methods=["GET", "POST"])
def show_user_page(username):
    """shows user profile"""

    if session.get('username') == None:
        flash('Please login or register first!')
        return redirect('/login')
    
    if session['username'] != username:
        flash("Incorrect User Name")
        return redirect(f'/users/{session["username"]}')
    
    user = User.query.get_or_404(username)
    feedbacks = user.feedbacks

    return render_template('user.html', user=user, feedbacks=feedbacks)

@app.route('/users/<string:username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):

    user = User.query.get_or_404(username)
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, user=user)
        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f'/users/{username}')
    
    return render_template('add_feedback.html', form=form, user=user)


@app.route('/users/<string:username>/delete', methods=["POST"])
def delete_user(username):
    """delete a user"""

    user = User.query.get_or_404(username)

    for feedback in user.feedbacks:
        db.session.delete(feedback)

    db.session.delete(user)
    db.session.commit()

    return redirect('/register')

@app.route('/feedback/<int:id>delete', methods=['POST'])
def delete_feedback(id):
    
    feedback = Feedback.query.get_or_404(id)
    user = User.query.get_or_404(feedback.username)

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.user.username}')

@app.route('/feedback/<int:id>/update', methods=["GET", "POST"])
def edit_feedback(id):

    if session.get('username') == None:
        flash('Please login or register first!')
        return redirect('/login')
    
    feedback = Feedback.query.get_or_404(id)
    username = session['username']
    
    if feedback.user.username != username:
        flash("You are not authorized to edit this feedback.")
        return redirect(f'/users/{username}')

    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback.title = title
        feedback.content = content
        
        db.session.commit()

        return redirect(f'/users/{feedback.user.username}')

    return render_template('edit_feedback.html', feedback=feedback, form=form, user=feedback.user)

@app.route('/logout')
def logout_user():
    session.pop('username')
    return redirect('/')






# if __name__ == "__main__":
#     app.run(debug=True)
