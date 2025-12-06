from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from config import Config
import json, re, datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)  # lines "name | qty"
    instructions = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class MealPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    week_start = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    plan_json = db.Column(db.Text, nullable=False)  # JSON string

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients (one per line, format: name | quantity)', validators=[DataRequired()])
    instructions = TextAreaField('Instructions')
    submit = SubmitField('Save')

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', recipes=recipes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username/password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken', 'warning')
            return render_template('register.html', form=form)
        u = User(username=form.username.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/recipes')
@login_required
def recipes():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipes/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        r = Recipe(title=form.title.data.strip(),
                   ingredients=form.ingredients.data.strip(),
                   instructions=form.instructions.data.strip(),
                   user_id=current_user.id)
        db.session.add(r)
        db.session.commit()
        flash('Recipe added', 'success')
        return redirect(url_for('recipes'))
    return render_template('add_recipe.html', form=form)

@app.route('/planner')
@login_required
def planner():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    today = datetime.date.today().isoformat()
    return render_template('planner.html', recipes=recipes, today=today)

@app.route('/shopping')
@login_required
def shopping_page():
    today = datetime.date.today().isoformat()
    return render_template('shopping.html', today=today)


@app.route('/api/save_plan', methods=['POST'])
@login_required
def save_plan():
    data = request.get_json()
    week_start = data.get('weekStart')
    plan = data.get('plan')
    if not week_start or plan is None:
        return jsonify({'error':'missing fields'}), 400
    mp = MealPlan.query.filter_by(user_id=current_user.id, week_start=week_start).first()
    if not mp:
        mp = MealPlan(user_id=current_user.id, week_start=week_start, plan_json=json.dumps(plan))
        db.session.add(mp)
    else:
        mp.plan_json = json.dumps(plan)
    db.session.commit()
    return jsonify({'status':'ok'})

@app.route('/api/get_shopping')
@login_required
def get_shopping():
    week_start = request.args.get('weekStart')
    if not week_start:
        return jsonify({'error':'weekStart required'}), 400
    mp = MealPlan.query.filter_by(user_id=current_user.id, week_start=week_start).first()
    if not mp:
        return jsonify({'shopping': {}})
    plan = json.loads(mp.plan_json)
    recipe_ids = set()
    for day, meals in plan.items():
        for meal, rid in meals.items():
            if rid:
                try:
                    recipe_ids.add(int(rid))
                except:
                    pass
    agg = {}
    for rid in recipe_ids:
        r = Recipe.query.get(rid)
        if not r: continue
        lines = r.ingredients.splitlines()
        for line in lines:
            line=line.strip()
            if not line: continue
            if '|' in line:
                parts=[p.strip() for p in line.split('|',1)]
                name=parts[0].lower(); qty=parts[1]
            else:
                name=line.lower(); qty=''
            agg.setdefault(name,[]).append(qty)
    shopping = {name: ', '.join([q for q in qtys if q]) or '1' for name, qtys in agg.items()}
    return jsonify({'shopping': shopping})

if __name__ == '__main__':
    app.run(debug=True)
