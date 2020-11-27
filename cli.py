import typer
import a2s
import vdf
import webbrowser
import logging
import socket
import typer
import subprocess
from tabulate import tabulate
from typing import Optional
from pathlib import Path

app = typer.Typer()
CONFIG_FILE = Path.home() / "csgo_cli.txt"

@app.command()
def configure(
    path: str = typer.Argument(None, help="Path to serverbrowser_hist.vdf, see github readme for more info.")
):
    """
    Configure path to favorite servers file
    """

    if not path:
        typer.echo("Please specify the path.")
        raise typer.Exit(1)
    
    if not Path(path).suffix == ".vdf":
        typer.echo("Not a valid path, must be a .vdf file.")
        raise typer.Exit(1)

    with open (CONFIG_FILE, 'w') as conf_file:
        conf_file.write(path)

    typer.echo(f"Added {path} to config file")


@app.command()
def servers():
    """
    List your favorite GSGO servers
    """
    servers = get_servers()
    if servers == {}:
        typer.echo('No registered favorite servers.')

    table = tabulate(servers, headers="keys")
    typer.echo(f"{table}\n")

@app.command()
def connect(
    server_index: int = typer.Argument(None, help="Connect to a server with the index given by 'csgo servers'"),
    ):
    """
    Start CSGO and connect to a specific game server.
    """
    if server_index is None:
        typer.echo("Please specify the server index")
        return

    if server_index >= 0:
        servers = get_servers()
        if server_index > len(servers):
            typer.echo(f"No server with index {server_index} exists.")
            return
        server = servers[server_index]
        typer.echo(f"Starting CSGO and joining server {server['NAME']} ...")
        start_csgo(server['ADDRESS'])
        return


def get_servers():
    try:
        with open(CONFIG_FILE, 'r') as f:
            PATH = f.readlines()[0]
    except FileNotFoundError:
        typer.echo("Config file not found, run 'csgo configure' to setup the config.")
        raise typer.Exit(1)

    try:
        serverbrowser = vdf.load(open(PATH))
    except FileNotFoundError:
        typer.echo("Path to favourite servers file not correct, change path by running 'csgo configure'")
        raise typer.Exit(1)

    favorite_servers = serverbrowser['Filters']['Favorites']

    server_infos = []
    for server in favorite_servers:
        server = favorite_servers[server]
        server_ip = server['address'].split(':')[0]
        server_port = int(server['address'].split(':')[1])
        address = (server_ip, server_port)
        try:
            info = a2s.info(address, timeout=a2s.defaults.DEFAULT_TIMEOUT, encoding=a2s.defaults.DEFAULT_ENCODING)
            server_info = {
                "INDEX": len(server_infos),
                "NAME": info.server_name,
                "MAP": info.map_name,
                "PLAYERS": f"{info.player_count}/{info.max_players}",
                "ADDRESS": f"{server_ip}:{server_port}",
            }
            server_infos.append(server_info)
        except socket.timeout as exp:
            logging.error(exp)

    return server_infos


def start_csgo(server_url):
   webbrowser.open(f'steam://connect/{server_url}')

if __name__ == "__main__":
    app()