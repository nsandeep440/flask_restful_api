from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores' ## table name
    ## table columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        # return {'name': self.name, 'items': [item.json() for item in self.items]}
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }
        ## when used 'lazy=dynamic' .all() is used

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    ### this method is used to insert and update
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
