import base64
import hashlib
import os
import pathlib
import time
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
    path = get_passwords_path_using_context(ctx)
    print(f"Looking for passwords file: '{path}'.")
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
    users = get_passwords_using_context(ctx)
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
@click.argument("username", type=str)
def add(ctx, username):
    """Add user or update password."""
    password = Prompt.ask("Password", password=True).encode()
    salt = os.urandom(18)
    hash = hash_password(password, salt)

    users = get_passwords_using_context(ctx)
    users[username] = User(name=username, salt=salt, hash=hash)
    save_passwords(ctx, users)
    print(f"Added user {username} to passwords file.")


def hash_password(password: bytes, salt: bytes) -> bytes:
    """Hash password using pbkdf2_hmac."""
    return hashlib.pbkdf2_hmac(
        "sha256", password=password, salt=salt, iterations=500_000
    )


@auth.command()
@click.pass_context
@click.argument("username", type=str)
def remove(ctx, username):
    """Remove user."""
    users = get_passwords_using_context(ctx)
    try:
        del users[username]
    except KeyError:
        print(f"[red]User {username} not found in passwords file.[/]")
    else:
        save_passwords(ctx, users)
        print(f"Removed user {username} from passwords file.")


def get_passwords_path_using_context(ctx: click.Context) -> pathlib.Path:
    """Get path to password file."""
    app_name = ctx.obj["app_name"]
    app_author = ctx.obj["app_author"]
    return get_passwords_path(app_name, app_author)


def get_passwords_path(app_name: str, app_author: str | None = None) -> pathlib.Path:
    """Get path of the passwords file."""
    if not app_name:
        raise RuntimeError("Providing app_name is required.")
    return pathlib.Path(platformdirs.user_data_dir(app_name, app_author)) / "shadow"


def get_passwords_using_context(ctx: click.Context) -> dict[str, User]:
    """Get passwords using information from a click context object."""
    try:
        contents = get_passwords_path_using_context(ctx).read_bytes()
    except FileNotFoundError:
        contents = ""

    return parse_passwords(contents)


def parse_passwords(contents: bytes) -> dict[str, User]:
    """Parse passwords file contents."""
    users = {}
    for line in contents.splitlines():
        name_, salt, hash = line.split(b"$")
        name = name_.decode()
        users[name] = User(
            name=name, salt=base64.b64decode(salt), hash=base64.b64decode(hash)
        )
    return users


def save_passwords(ctx: click.Context, users: dict[str, User]) -> None:
    """Save passwords to passwords file."""
    path = get_passwords_path_using_context(ctx)

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


def verify_password(
    username: str, password: str, app_name: str, app_author: str | None = None
) -> bool:
    """Verify password by checking against password file."""
    try:
        contents = get_passwords_path(app_name, app_author).read_bytes()
    except FileNotFoundError:
        contents = ""
    users = parse_passwords(contents)

    try:
        user = users[username]
    except KeyError:
        return False

    hash = hash_password(password=password.encode(), salt=user.salt)
    if hash == user.hash:
        return True
    return False


def _time_hashing_passwords(N: int) -> float:
    t0 = time.monotonic()
    for _ in range(N):
        hash_password("mypassword".encode(), "mysalt".encode())
    return time.monotonic() - t0


if __name__ == "__main__":
    N = 50
    duration = _time_hashing_passwords(N)
    print(f"Hashing passwords takes {1000 * duration / N:.1f} ms per operation.")
