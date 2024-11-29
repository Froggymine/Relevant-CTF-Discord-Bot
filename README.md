# Discord CTF ping bot

This bot takes the RSS feed for upcoming CTFs from ctftime.org, parses it for the ctfs relevant to my team, and sends a ping with the basic info to a discord channel in a server.

## Ping format example

========== @Role ===========
CTF: CTF Name
Links:  CTF Time,  Offical CTF Wepage
CTF Weight:  25.00
Date/Time (Adl):  Sat,  2024-12-14, 17:30  (in 14 days)
             to:  Sun,  2024-12-15, 17:30

========== @Role ===========

# Setup

- Setup a discord bot through the discord developer portal
- Pull this repo and run `setup.sh`
- Configure constants in `main.py` as needed (such as the channel id pings to be sent)
- Configure ping function in `main.py` to use the correct role id (the interger in the code)
- Add your discord bot private secret to the `secret.txt` (created by `setup.sh`)
- Run `start.sh`

## Troubleshoot

If you are not using `setup.sh`, ensure `pinglog.log` exists, otherwise the bot will not run.