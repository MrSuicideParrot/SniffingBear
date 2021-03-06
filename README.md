# :honey_pot:  &nbsp; SniffingBear  &nbsp; :honey_pot:

------------------------------------------------------------------------

### :honeybee:  &nbsp; Introduction  &nbsp; :honeybee:

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

------------------------------------------------------------------------

## :sparkles:  &nbsp; Contributors  &nbsp; :sparkles:

<table><tr><td align="center"><a href="https://github.com/andreluis034"><img src="https://avatars3.githubusercontent.com/u/5006716?s=400&v=4" width="100px;" alt="André Brandão"/><br /><sub><b>André Brandão</b></sub></a> </td> <td align="center"><a href="https://github.com/FabioFreitas9"><img src="https://avatars3.githubusercontent.com/u/22847090?s=400&v=4" width="100px;" alt="Fábio Freitas"/><br /><sub><b>Fábio Freitas</b></sub></a></td> <td align="center"> <a href="https://github.com/0xSmiley"><img src="https://avatars3.githubusercontent.com/u/34580831?s=400&v=4" width="100px;" alt="Nuno Lopes"/><br /><sub><b>Nuno Lopes</b></sub></a> 
 </td></tr></table>


