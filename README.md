 python -m venv venv
 #if venv not activated
 .\venv\Scripts\Activate.ps1
 #install required packages
 pip install flask flask-login flask-mysqldb mysql-connector-python firebase-admin python-dotenv werkzeug
 #verify installation
 pip list
mysqlclient              2.2.8
pip                      25.2
proto-plus               1.28.0
protobuf                 7.35.1
pyasn1                   0.6.3
pyasn1_modules           0.4.2
pycparser                3.0
PyJWT                    2.13.0
python-dotenv            1.2.2
requests                 2.34.2
typing_extensions        4.16.0
urllib3                  2.7.0
Werkzeug                 3.1.8

#generate the requirement.txtfile
pip freeze > requirements.txt
#this is required only when yhe people clone and run in thier local system ,just run 
   pip install -r requirements.txt

SQLAlchemy → ORM (Object Relational Mapper)
Flask-Migrate → Manage database schema changes

Flask-SQLAlchemy → Connects Flask to PostgreSQL.
Flask-Migrate → Creates and manages database migrations.
psycopg2-binary → PostgreSQL driver for Python.

hash passwords using Werkzeug


----------------------------
Backend: Flask
Database: PostgreSQL
ORM: SQLAlchemy
Migrations: Flask-Migrate
Authentication: Flask-Login
Cloud Storage: Firebase Storage
Frontend: HTML + CSS + Bootstrap + JavaScript
Deployment: Docker
-----------------------------

