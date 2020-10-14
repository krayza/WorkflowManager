import click

from flask.cli import AppGroup

from .model import Workflow
from step.model import Step
from app import app, db


workflow_cli = AppGroup('workflow', short_help="Manage workflows")


@workflow_cli.command('create')
@click.argument('name')
def create_workflow(name):
    """ Create a new workflow """

    if Workflow.query.filter_by(name=name).first() is not None:
        print("A workflow with this name already exists.")
        return

    workflow = Workflow(name=name)
    db.session.add(workflow)

    step1 = Step(name="Status 1", workflow=workflow)
    step2 = Step(name="Status 2", workflow=workflow)
    step3 = Step(name="Validated", workflow=workflow)
    step4 = Step(name="Finished", workflow=workflow)
    db.session.add(step1)
    db.session.add(step2)
    db.session.add(step3)
    db.session.add(step4)

    db.session.commit()


@workflow_cli.command('list')
def list_workflow():
    """ List the existing workflows """

    workflows = Workflow.query.all()
    if not workflows:
        print("You don't have any workflows.")
        return

    for worklow in workflows:
        print(worklow.name)


@workflow_cli.command('remove')
@click.argument('name')
def remove_workflow(name):
    """ Remove the given workflow """

    workflow = Workflow.query.filter_by(name=name).first()

    if not workflow:
        print(f"Couldn't find any workflows named {name}.")
        return

    db.session.delete(workflow)
    db.session.commit()


app.cli.add_command(workflow_cli)
