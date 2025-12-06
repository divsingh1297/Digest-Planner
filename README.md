 Digest Planner
A full-stack meal planning application with recipes, weekly planning, and automated shopping lists.
Built with Flask, SQLite, and a custom Material Design frontend.

 Overview
Digest Planner is a web application that simplifies meal planning by allowing users to:

Store and manage recipes

Organize weekly meal schedules with drag-and-drop

Automatically generate shopping lists based on planned meals

Enjoy a clean, responsive Material Design UI

This project demonstrates full-stack software engineering with a database-backed backend, interactive frontend, and user authentication.

 Features
 User Authentication
Secure login, logout, and registration using Flask-Login.

 Recipe Management
Create recipes with structured ingredients and view them in Material-styled cards.

 Weekly Meal Planner
Drag recipes into a weekly calendar (Breakfast/Lunch/Dinner) and save plans.

Shopping List Generator
Automatically merges all ingredients from planned meals into a complete shopping list.

 Material Design UI
Custom-designed teal color theme with ripple effects and floating action buttons.

 Folder Structure
project/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── recipes.html
│   ├── add_recipe.html
│   ├── planner.html
│   └── shopping.html
│
├── static/
│   ├── css/
│   │   └── material.css
│   ├── js/
│   │   ├── ripple.js
│   │   ├── planner_material.js
│   │   └── shopping_material.js
│   └── icons/
│
└── instance/
    └── digest.db

Getting Started
Follow these steps to run the project on any OS (Windows, macOS, Linux).

**1️** Install Python
Ensure Python 3.10+ is installed.

Check version:

python --version

**2** Clone the Repository
git clone https://github.com/<your-username>/digest_planner.git
cd digest_planner

**3️** Create a Virtual Environment
python -m venv venv
**4️** Activate the Environment
Windows (CMD):
venv\Scripts\activate
macOS & Linux:
source venv/bin/activate
You’ll see:

(venv)
**5️** Install Dependencies
pip install -r requirements.txt
**6️** Run the Application
python app.py
**7️** Open in Browser
Go to:

http://127.0.0.1:5000
 Your app is now running locally!

 Usage Guide
Add Recipes
Open Recipes

Click the floating “+” FAB

Enter title + ingredients (name | quantity format)

Plan Meals
Open Planner

Select week start date

Drag recipes into meal slots

Save the plan

Generate Shopping List
Open Shopping List

Choose starting week

Click Generate

 Technologies Used
Backend
Python

Flask

SQLAlchemy

Flask-Login

Flask-WTF

Frontend
HTML5

CSS (Material Design theme)

JavaScript

Material Icons

Database
SQLite 


