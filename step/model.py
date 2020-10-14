from app import db


class Step(db.Model):
    __tablename__ = 'step'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflow.id"))
    workflow = db.relationship("Workflow", back_populates="steps", uselist=False)
