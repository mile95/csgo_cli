import typer
from tabulate import tabulate
from typing import Optional

app = typer.Typer()

data = [
    {
        "NAME":"Retake01",
        "MAP": "de_dust2",
        "PLAYERS": 6,
        "MAX_PLAYERS":10
    },
    {
        "NAME":"Retake02",
        "MAP": "de_dust2",
        "PLAYERS": 0,
        "MAX_PLAYERS":10
    },
    {
        "NAME":"Retake03",
        "MAP": "de_inferno",
        "PLAYERS": 2,
        "MAX_PLAYERS":10
    },
    {
        "NAME":"Retake04",
        "MAP": "de_mirage",
        "PLAYERS": 10,
        "MAX_PLAYERS":10
    }   
]

def get_data():
    # TODO: Read game favorite server ips from file.
    # TODO: Convert IP to CSGO info.
    return data

def start_csgo():
   # TODO: Start CSGO
   # https://stackoverflow.com/questions/50848226/running-stardew-valley-from-python-on-windows
   # webbrowser.open('steam://rungameid/{}'.format(game['appid']))



@app.command()
def servers():
    """
    List your favorite GSGO servers
    """
    data = get_data()
    if data == []:
        typer.echo('No registered favorite servers.')

    output = []
    for index, server in enumerate(data):
        server['Index'] = index
        output.append(server)

    table = tabulate(output, headers="keys")
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
        if server_index > len(data):
            typer.echo(f"No server with index {server_index} exists.")
            return
        server = data[server_index]
        # TODO: Start CSGO and enter 'server'
        typer.echo(f"Starting CSGO and joining server {server['NAME']} ...")
        return

if __name__ == "__main__":
    app()