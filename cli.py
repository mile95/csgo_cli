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

app = typer.Typer()

PATH = "/mnt/c/Program Files (x86)/Steam/userdata/160616678/7/remote/serverbrowser_hist.vdf"
serverbrowser = vdf.load(open(PATH))
favorite_servers = serverbrowser['Filters']['Favorites']


def get_servers():
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
   pass


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
        # TODO: Start CSGO and enter 'server'
        typer.echo(f"Starting CSGO and joining server {server['NAME']} ...")
        start_csgo(server['ADDRESS'])
        return

if __name__ == "__main__":
    app()