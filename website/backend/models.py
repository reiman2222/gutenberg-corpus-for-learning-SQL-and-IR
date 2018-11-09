from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#================================================================================================

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class Book(BaseModel, db.Model):
    """Model for the stations table"""
    __tablename__ = 'Book'

    gutenberg_id = db.Column(db.Text, primary_key = True)
    release_date = db.Column(db.DateTime)
    full_text = db.Column(db.Text)
    language = db.Column(db.Text)
    title = db.Column(db.Text)



class Author(BaseModel, db.Model):
    __tablename__ = 'Author'

    author_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    middle_name = db.Column(db.Text)
    suffix = db.Column(db.Text)
    prefix = db.Column(db.Text)

class WrittenBy(BaseModel, db.Model):
    __tablename__ = 'Written_By'

    author_id = db.Column(db.Integer, primary_key = True)
    gutenberg_id = db.Column(db.Integer, primary_key = True)





