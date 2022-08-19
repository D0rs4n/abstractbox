import datetime
import json
import secrets
from pathlib import Path

import jwt
import typer
from rich import print as pprint

app = typer.Typer()


def create_config() -> None:
    """Generate or overwrite a config file with a secure JWT secret."""
    with open("settings.json", "w") as f:
        config = {"jwt_secret": secrets.token_hex(32)}
        json.dump(config, f)


def generate_jwt(secret: str) -> str:
    """Generate a JWT with an expiry of 90 day using the provided secret."""
    return str(
        jwt.encode(
            {"type": "deploy", "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=90)},
            secret,
            algorithm="HS256",
        )
    )


@app.command()
def setup() -> None:
    """
    Generates a config file, with an appropriate secret, used for signing JWTs
    used for the authentication and authorization mechanism
    """
    # Check if a config file already exists, if not create a config file otherwise prompt the user
    pprint("[yellow]Generating settings.json...[/]")
    if Path("settings.json").is_file():
        typer.confirm("A config file already exists. Would you like to overwrite it?", abort=True)
    create_config()
    pprint("[green]Created configuration file.[/]")


@app.command()
def generate_deploy_token() -> None:
    """
    Generate a JWT deploy token, using the JWT secret in the config file.
    If the config does not exist, the generation process will be aborted.
    """
    if Path("settings.json").is_file():
        with open("settings.json") as f:
            config = json.load(f)
            if not (secret := config.get("jwt_secret", None)):
                pprint("[bold red] Incorrect config file, please generate a new one using the setup command[/]")
                return
            pprint(
                "[bold blue]Here's your signed deploy token: [/]"
                f"{generate_jwt(secret)}\n"
                "[bold red]Make sure to save it somewhere safe, you won't be able to see it again!"
            )
            return

    pprint("[bold red] Config file does not exists. Please generate one using the setup command[/]")


if __name__ == "__main__":
    app()
