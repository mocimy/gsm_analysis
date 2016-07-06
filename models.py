from gsm_analysis import db


class Cell(db.Model):
    cell_ID = db.Column(db.Integer, primary_key=True)
    bts_name = db.Column(db.String(20))
    area_name = db.Column(db.String(10))
    lac = db.Column(db.Integer)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    direction = db.Column(db.Integer)
    bcch = db.Column(db.Integer)
