import typer

from app.cli.commands.seed import seed_command

app = typer.Typer()


# N.B. with one command, Typer treats it as the main CLI
#  adding a callback tells Typer to keep it as a subcommand
# https://typer.tiangolo.com/tutorial/commands/one-or-multiple/#one-command-and-one-callback
@app.callback()
def callback() -> None:
    pass


app.command("seed")(seed_command)
