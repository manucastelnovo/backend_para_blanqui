from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, EmailField, PasswordField, SubmitField


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'chupetess'
db = SQLAlchemy(app)


#para los input
class RegisterForm(FlaskForm):
    username = StringField()
    email= EmailField()
    password = PasswordField()
    submit = SubmitField('para que se yo')

class LoginForm(FlaskForm):
    email= EmailField()
    password = PasswordField()
    submit = SubmitField('join')

#modelo de tabla
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))

#se crea,se acepta
with app.app_context():
    db.create_all()


#pagina registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    #form es un diccionario que tiene string en forma de etiquetas input en cada propiedad
    print(form.username)

    if form.validate_on_submit():
        new_user= User(name=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return 'se registro'
    return render_template('register.html',perrito=form)
    

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        if form.password.data == user.password:
            return user.name

    return render_template('login.html',perrito=form)
