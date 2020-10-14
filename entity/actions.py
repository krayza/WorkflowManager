import click

from flask.cli import AppGroup

from .model import Entity
from workflow.model import Workflow
from app import app, db


entity_cli = AppGroup('entity', short_help="Manage entities")


@entity_cli.command()
@click.argument('workflow_name')
@click.argument('name')
def create_entity(workflow_name, name):
    """ Create a new entity that belongs to the given workflow """

    workflow = Workflow.query.filter_by(name=workflow_name).first()
    if workflow is None:
        print(f"Couldn't find any workflow named {workflow_name}.")
        return

    if Entity.query.filter_by(workflow_id=workflow.id, name=name).first() is not None:
        print("An Entity with this name already exists in this workflow.")
        return

    entity = Entity(name=name, workflow_id=workflow.id)
    db.session.add(entity)
    db.session.commit()


@entity_cli.command('forward')
@click.argument('workflow_name')
@click.argument('entity_name')
def forward(workflow_name, entity_name):
    """ Move the given entity to its next step """

    workflow = Workflow.query.filter_by(name=workflow_name).first()
    if workflow is None:
        print(f"Couldn't find any workflow named {workflow_name}.")
        return

    entity = Entity.query.filter_by(name=entity_name, workflow_id=workflow.id).first()
    if entity is None:
        print(f"Couldn't find {entity_name} in this workflow.")
        return

    if entity.current_step == 3:
        print(f"{entity_name} is already finished.")
        return

    entity.current_step += 1
    db.session.commit()


@entity_cli.command('backward')
@click.argument('workflow_name')
@click.argument('entity_name')
def backward(workflow_name, entity_name):
    """ Move the given entity to its previous step """

    workflow = Workflow.query.filter_by(name=workflow_name).first()
    if workflow is None:
        print(f"Couldn't find any workflow named {workflow_name}.")
        return

    entity = Entity.query.filter_by(name=entity_name, workflow_id=workflow.id).first()
    if entity is None:
        print(f"Couldn't find {entity_name} in this workflow.")
        return

    if entity.current_step == 0:
        print(f"{entity_name} is already at the first step.")
        return

    entity.current_step -= 1
    db.session.commit()


@entity_cli.command('status')
@click.argument('workflow_name')
@click.argument('entity_name')
def status(workflow_name, entity_name):
    """ Give the current status of the given entity """

    workflow = Workflow.query.filter_by(name=workflow_name).first()
    if workflow is None:
        print(f"Couldn't find any workflow named {workflow_name}.")
        return

    entity = Entity.query.filter_by(name=entity_name, workflow_id=workflow.id).first()
    if entity is None:
        print(f"Couldn't find {entity_name} in this workflow.")
        return
    entity_status = workflow.steps[entity.current_step].name

    print(f"{entity_name}'s status is {entity_status}.")


@entity_cli.command('list')
@click.argument('workflow_name')
def list_entities(workflow_name):
    """ List the entities belonging to the given workflow """

    workflow = Workflow.query.filter_by(name=workflow_name).first()
    if workflow is None:
        print(f"Couldn't find any workflow named {workflow_name}.")
        return

    if not workflow.entities:
        print("This workflow does not have any entities.")
        return

    for entity in workflow.entities:
        print(f"{entity.name}")


app.cli.add_command(entity_cli)
