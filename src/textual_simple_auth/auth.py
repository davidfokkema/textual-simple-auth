import base64
import hashlib
import os
import pathlib
from dataclasses import dataclass

import click
import platformdirs
from rich import box, print
from rich.prompt import Prompt
from rich.table import Table


@dataclass
class User:
    name: str
    salt: bytes
    hash: bytes


@click.group()
def auth():
    """Manage user authentication."""


@auth.command()
@click.pass_context
def show(ctx):
    """Show passwords file contents and location."""
    path = get_passwords_path(ctx)
    print(f"Looking for passwords file at '{path}'.")
    if path.exists():
        print()
        print("Contents:")
        print(path.read_text())
    else:
        print("[red]Passwords file does not yet exist.[/]")


@auth.command()
@click.pass_context
def list(ctx):
    """List users."""
    users = parse_passwords(ctx)
    table = Table(title="Registered users", box=box.SIMPLE)
    table.add_column("Username")
    table.add_column("Salt (base64 encoded)")
    table.add_column("Password hash (base64 encoded)")
    print()
    for user in users.values():
        table.add_row(
            user.name,
            base64.b64encode(user.salt).decode(),
            base64.b64encode(user.hash).decode(),
        )
    print(table)


@auth.command()
@click.pass_context
@click.argument("username")
def add(ctx, username):
    """Add user or update password."""
    password = Prompt.ask("Password", password=True).encode()
    salt = os.urandom(18)
    hash = hashlib.pbkdf2_hmac(
        "sha256", password=password, salt=salt, iterations=500_000
    )

    users = parse_passwords(ctx)
    users[username] = User(name=username, salt=salt, hash=hash)
    save_passwords(ctx, users)


@auth.command()
def remove():
    """Remove user."""
    ...


def get_passwords_path(ctx: click.Context) -> pathlib.Path:
    """Get path to password file."""
    app_name = ctx.obj["app_name"]
    app_author = ctx.obj["app_author"]
    if not app_name:
        raise RuntimeError("Providing app_name is required.")
    return pathlib.Path(platformdirs.user_data_dir(app_name, app_author)) / "shadow"


def parse_passwords(ctx: click.Context) -> dict[str, User]:
    try:
        contents = get_passwords_path(ctx).read_bytes()
    except FileNotFoundError:
        contents = ""

    users = {}
    for line in contents.splitlines():
        name_, salt, hash = line.split(b"$")
        name = name_.decode()
        users[name] = User(
            name=name, salt=base64.b64decode(salt), hash=base64.b64decode(hash)
        )
    return users


def save_passwords(ctx: click.Context, users: dict[str, User]) -> None:
    path = get_passwords_path(ctx)

    contents = b"\n".join(
        [
            b"$".join(
                [
                    user.name.encode(),
                    base64.b64encode(user.salt),
                    base64.b64encode(user.hash),
                ]
            )
            for user in users.values()
        ]
    )

    path.parent.mkdir(exist_ok=True, parents=True)
    path.write_bytes(contents)
