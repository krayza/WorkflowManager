from app import db


class Entity(db.Model):
    __tablename__ = 'entity'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflow.id"))
    workflow = db.relationship("Workflow", back_populates="entities", uselist=False)
    current_step = db.Column(db.Integer, default=0)
