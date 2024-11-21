import uuid
from config.config import db, ma


class Observation(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    
    def __repr__(self):
        return "<Observation %r>" % self.id

    


class ObservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Observation
        fields = ("id")

observation_schema = ObservationSchema()
observations_schema = ObservationSchema(many=True)
