import uuid
from datetime import datetime
from decimal import Decimal
from config.config import db, ma


class Observation(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    time_zone_offset = db.Column(db.String(10), nullable=False)
    coordinates = db.Column(db.String(50), nullable=False)
    temperature_water = db.Column(db.Float, nullable=True)
    temperature_air = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    wind_speed = db.Column(db.Float, nullable=True)
    wind_direction = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)
    haze = db.Column(db.Float, nullable=True)
    becquerel = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Observation {self.id}>"

    @staticmethod
    def create(data):
        new_observation = Observation(
            date=data.get("date"),
            time=data.get("time"),
            time_zone_offset=data.get("time_zone_offset"),
            coordinates=data.get("coordinates"),
            temperature_water=data.get("temperature_water"),
            temperature_air=data.get("temperature_air"),
            humidity=data.get("humidity"),
            wind_speed=data.get("wind_speed"),
            wind_direction=data.get("wind_direction"),
            precipitation=data.get("precipitation"),
            haze=data.get("haze"),
            becquerel=data.get("becquerel"),
            notes=data.get("notes"),
        )
        db.session.add(new_observation)
        db.session.commit()
        return new_observation

    @staticmethod
    def get(observation_id):
        return Observation.query.get(observation_id)

    @staticmethod
    def get_all():
        return Observation.query.all()

    @staticmethod
    def update(observation_id, data):
        observation = Observation.query.get(observation_id)
        if observation:
            for key, value in data.items():
                if hasattr(observation, key) and key not in ["id", "created", "deleted"]:
                    setattr(observation, key, value)
            observation.updated = datetime.utcnow()
            db.session.commit()
            return observation
        return None
    
    @staticmethod
    def patch(observation_id, data):
        observation = Observation.query.get(observation_id)
        if observation:
            for key, value in data.items():
                if hasattr(observation, key) and key not in ["id", "created", "deleted"]:
                    setattr(observation, key, value)
            observation.updated = datetime.utcnow()
            db.session.commit()
            return observation
        return None


    @staticmethod
    def soft_delete(observation_id):
        observation = Observation.query.get(observation_id)
        if observation:
            observation.deleted = datetime.utcnow()
            db.session.commit()
            return observation
        return None

    @staticmethod
    def delete(observation_id):
        observation = Observation.query.get(observation_id)
        if observation:
            db.session.delete(observation)
            db.session.commit()
            return {"message": f"Observation {observation_id} permanently deleted."}
        return {"message": "Observation not found."}


class ObservationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Observation
        fields = (
            "id", "date", "time", "time_zone_offset", "coordinates",
            "temperature_water", "temperature_air", "humidity", "wind_speed",
            "wind_direction", "precipitation", "haze", "becquerel", "notes",
            "created", "updated", "deleted"
        )

observation_schema = ObservationSchema()
observations_schema = ObservationSchema(many=True)
