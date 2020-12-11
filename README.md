# CSGO Command Line Interface

CLI for starting CSGO and joining one of your favorite servers insanely fast.

Because why not?

# Usage

![](src/csgo_help.png)
![](src/csgo_connect.png)

# Current installation
```
git clone https://github.com/mile95/csgo_cli
cd csgo_cli
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
TODO: Make the CLI available via PyPI.

# Setup path to steam user data

Steam stores your favorite servers in a file called `serverbrowser_hist.vdf`. 

For me, this file was located at:
```/c/Program Files (x86)/Steam/userdata/160616678/7/remote/serverbrowser_hist.vdf"```.

![](src/csgo_configure.png)

When the `serverbrowser_hist.vdf` has been located, run: 
```
csgo configure {full_path_to_`serverbrowser_hist.vdf`}
```

Everything should now be set, enjoy!
