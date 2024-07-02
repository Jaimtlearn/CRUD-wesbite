from App import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)

    def to_dict(self):
        return {"id" : self.id, "name" : self.name, "description" : self.description}
