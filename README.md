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

Supported commands in the client:

List all of the current honeypot modules
* `sb > list`

Brief explanation about the module in question
* `sb > description <moduleName>`

Scan and IP or a range of IP's with a given module (use 'all' if you want to run all of the modules), in a given port by default it scans all of the avaiable ports.
* `sb > scan <IP> <moduleName> -p<ports>`

 Example
* `sb > scan 192.168.1.0/24 amun -p20,21,22,23,24,25`

Scan and IP or a range of IP's with your custom module please provide de module url and follow our guide on how to create your own module.
* `sb > customScan <IP> <moduleUrl>`

------------------------------------------------------------------------

## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Server

Start the Server
* `server.py [-h] [ServerPort]`

------------------------------------------------------------------------

## &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Worker

Start the Worker
* `worker.py [-h] [WorkerPort] [ServerIp] [ServerPort]`

------------------------------------------------------------------------

All of the above components support a helping documentation when starting them.

* `python Client.py -h`
* `python Server.py -h`
* `python Worker.py -h`

------------------------------------------------------------------------

:warning: &nbsp; **Warning** &nbsp; :warning:

Use this tool at your own risk!
