from flask_script import Manager, prompt_bool, Command
from app import db

manager = Manager(usage="Perform database operations")

@manager.command
def drop():
    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()

@manager.command
def createdb():
    if prompt_bool("Do you wand to create database?"):
        db.create_all()

@manager.command
def recreate():
    if prompt_bool("Do you want to rebuild database?"):
        dropdb()
        createdb()

@manager.command
def init_data():
    pass
    print("Initialization completed")