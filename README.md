# tar_pyt
SSH tarpit implemented in Python 3.7 with asyncio

Essentially this is functional copy of [endlessh][es] by Chris Wellons, as suggested in his blog on that project. Asyncio is particularly  well suited to this application, and makes this program much simpler to implement than its C counterpart without sacrificing memory performance. The idea is to change your SSH port and leave this runnning on the default port 22, potentially trapping malicious connections and wasteing a small amout of their resources. I highly suggest you vist endlessh and the aforementioned blog for a more in-depth overview. 

## Usage
Run with `python3.7 tar_pyt`
Usage information is printed with `-h` or `-help`.

```
Usage: endlessh [-h] [-d MS] [-f CONFIG] [-l LEN] [-m LIMIT] [-p PORT] [-v]
  -d INT    Message millisecond delay [10000]
  -f        Set and load config file [NOT YET IMPLEMENTED]
  -h        Print this help message and exit
  -l INT    Maximum banner line length (3-255) [32]
  -m INT    Maximum number of clients [4096]
  -p INT    Listening port [2222]
  -v        Print diagnostics to standard output
```

Argument order does not matter and the configuration functionality is yet to be implemented. By default there is no log output, and it is enabled with `-v` and sent to standard output.

In order to list active connections and thier statitics, type `log` while the program  is running.

Keyboard interrupts shut down the program, type `CTRL` + `C`.

## Potential Issues

This must be run with python 3.7.

Usage on port 22 may require additional privledges depending on system and SSH configuration.

## Future Additions
Add configuration file support.

Potentially add primitive geolocaction for client connections.

potentially add HTTP serer support.

[es]: https://github.com/skeeto/endlessh
