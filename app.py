import click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from workflow import model
from step import model
from entity import model

db.create_all()


from workflow import actions
from entity import actions
from step import actions


def main():
    app.run()


if __name__ == '__main__':
    main()
