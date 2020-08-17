from flask.cli import FlaskGroup
from project import run_app


cli = FlaskGroup(run_app())


if __name__ == "__main__":
    cli()
