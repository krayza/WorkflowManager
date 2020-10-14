from app import db


class Workflow(db.Model):
    __tablename__ = 'workflow'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    steps = db.relationship("Step", back_populates="workflow", cascade="all, delete")
    entities = db.relationship("Entity", back_populates="workflow", cascade="all, delete")
