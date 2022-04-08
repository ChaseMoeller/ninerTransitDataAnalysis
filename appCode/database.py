from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask-SQLAlchemy extension instance
db = SQLAlchemy()


def db_init(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()