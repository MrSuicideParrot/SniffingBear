# SniffingBear

### Introduction

A modular and distributed tool developed in python to scan networks for honeypots

------------------------------------------------------------------------

### :inbox_tray: &nbsp; How to Install &nbsp; :inbox_tray:

Open the terminal and type following commands.

* `apt update`

* `apt install git`

* `git clone https://github.com/MrSuicideParrot/SniffingBear.git`

* `cd SniffingBear`

* `pip install -r requirements.txt`

------------------------------------------------------------------------

### :fire: &nbsp; How to Use &nbsp; :fire:

## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Client

Start the Client
* `python Client.py [ServerIp] [ServerPort]`

## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Server

Start the Server
* `server.py [-h] [ServerPort]`

## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Worker

Start the Worker
* `worker.py [-h] [WorkerPort] [ServerIp] [ServerPort]`

All of the above components support a helping documentation when starting them.

* `python Client.py -h`
* `python Server.py -h`
* `python Worker.py -h`

:warning: &nbsp; **Warning** &nbsp; :warning:

Use this tool at your own risk!
