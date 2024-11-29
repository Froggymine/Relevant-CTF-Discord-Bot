# Discord CTF ping bot

This bot takes the RSS feed for upcoming CTFs from ctftime.org, parses it for the ctfs relevant to my team, and sends a ping with the basic info to a discord channel in a server.

## Setup

Pull the repo and run `setup.sh`. Configure constants in `main.py` as needed (such as the channel id pings to be sent)

Add your discord bot private secret to the `secret.txt` that would have been added by `setup.sh`

If you are not using `setup.sh`, ensure `pinglog.log` exists, otherwise the bot will not run.

Now, run `start.sh`