#!/usr/bin/env python

import json
import subprocess
from pathlib import Path
import argparse
import os
import signal


def run_watchfors(
    base_path='/etc', 
    config_path="swatchdog/swatchdog.json", 
    watchfor_path="swatchdog/watchfor",
    debug=False):
    etc = Path(base_path)
    if debug: print(f"etc={etc.resolve()}")
    with open(etc / config_path) as swatchdog_json:
        swatchdog_config = json.load(swatchdog_json)
        for logfile in swatchdog_config["logfiles"]:
            logfile_directory = Path(logfile["directory"])
            if debug: print(f"logfile directory={logfile_directory}")
            if logfile_directory.is_dir():
                for f in logfile["files"]:
                    watchfor = etc / watchfor_path / f["watchfor"]
                    log = logfile_directory / f["name"]
                    if debug: print(f"watchfor={watchfor.resolve()}, log={log.resolve()}")
                    if log.exists() and watchfor.exists():
                        print(f"Started watching {log.resolve()} with {watchfor.resolve()}")
                        subprocess.run(["/usr/bin/swatchdog", "-c", watchfor, "-t", log, "--daemon" ])


def terminate_swatches(debug=False):
    p = subprocess.Popen(["pgrep", "swatch"], stdout=subprocess.PIPE)
    text, err = p.communicate()
    output = text.decode("utf-8").split("\n")[:-1]  # Skip extra newline
    for o in output:
        if debug: print(f"Terminating swatchdog process {o}")
        os.kill(int(o), signal.SIGKILL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--terminate', default=False, action='store_true')
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    args = parser.parse_args()

    if args.terminate:
        if args.debug: print("Terminating swatchdog processes")
        terminate_swatches(debug=args.debug)
    else:
        if args.debug: print("Starting watchfors for swatchdog")
        run_watchfors(debug=args.debug)