from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/afang8"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run()
