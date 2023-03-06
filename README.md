# Swatchdog

This repo provides a simple - but useable and quite robust - solution for those who want log-file stimulated alerts.

In particular, it provides a way to alert to Slack.  Other systems can easily be added.

[`swatchdog`](https://github.com/ToddAtkins/swatchdog) is the base software for this.  It is written in Perl.  It's simple and high-performance.

## Installation

1. Clone the Repo

Place it in a convenient place.  We'll use $PREFIX to represent that directory.
```shell
git clone git@github.com:profitviews/swatchdog.git
```

2. Set Up Base Structure

Create: 
* `/etc/swatchdog`: copy all files from `$PREFIX/swatchdog/etc/swatchdog` into there with `sudo cp` 
* `/etc/swatchdog/watchfor`: similarly `sudo cp` from `$PREFIX/swatchdog/etc/swatchdog/watchfor`
* `/etc/systemd/system/swatchdog.service` as a copy of `$PREFIX/swatchdog/etc/systemd/system/swatchdog.service`.
  
Of course, you can (and should) do all of this via a staging directory.

3. Identify Log Files

For each log-file you need a `watchfor` file.  Duplicate, rename and adapt `/etc/swatchdog/watchfor/example.cfg` for this purpose.  The changes you will make are to the regular expression within the `/` bracketing characters on the `watchfor` line (i.e. change `RegularExpressionToFind` to that regexp):

```perl
watchfor /RegularExpressionToFind/
```

then change the form of the text to be generated:

```perl
      exec $python_executable /etc/swatchdog/swatchdog_slack.py test_server 'Message to send' "$0"
```

Change `test_server` to the server name that the log-file is associated with and `Message to send` to a prefix to the log-line that will be sent.

4. Specify Log File Locations

Adapt `/etc/swatchdog/swatchdog.json` specifying the directories and names of your log-files and their associated `watchfor` files (which you've adapted in `/etc/swatchdog/watchfor`)

5. Adjust `env` Values

Change `SLACK_TOKEN` and `SLACK_CHANNEL` to be correct for your system.  Read the [Slack API docs](https://api.slack.com/docs) on how to get your Slack API token.  Make sure the `PYTHON_EXECUTABLE` is correct.

6. Start the System

```shell
sudo systemctl daemon-reload
sudo systemctl enable swatchdog.service
sudo systemctl start swatchdog.service
```

This should result in a running system.  
