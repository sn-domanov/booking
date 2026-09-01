import typer

from app.cli.commands.create_admin import create_admin_command
from app.cli.commands.seed import seed_command

app = typer.Typer()


app.command("create-admin")(create_admin_command)
app.command("seed")(seed_command)
