import click

from flask.cli import AppGroup

from .model import Step
from workflow.model import Workflow
from app import app, db


step_cli = AppGroup('step', short_help="Manage steps")


@step_cli.command('list')
@click.argument('workflow_name')
def list_steps(workflow_name):
    """ List the steps of the given workflow """

    workflow = Workflow.query.filter_by(name=workflow_name).first()
    if workflow is None:
        print(f"Couldn't find any workflow named {workflow_name}.")
        return

    for step in workflow.steps:
        print(f"{step.name}")


@step_cli.command('rename')
@click.argument('workflow_name')
@click.argument('step_number')
@click.argument('new_status')
def rename_step(workflow_name, step_number, new_status):
    """ Rename the given step of the given workflow """

    try:
        step_number = int(step_number)
    except ValueError:
        print("Give a correct step number (1-3)")
        return

    if step_number < 1 or step_number > 3:
        print("Give a correct step number (1-3)")
        return

    step_number -= 1

    workflow = Workflow.query.filter_by(name=workflow_name).first()
    if workflow is None:
        print(f"Couldn't find any workflow named {workflow_name}.")
        return

    step = workflow.steps[step_number]
    step.name = new_status
    db.session.commit()


app.cli.add_command(step_cli)
