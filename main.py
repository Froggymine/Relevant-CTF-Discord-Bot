import datetime
import time
import feedparser
import discord
from discord.ext import tasks

PING_LOG_LOCATION = "pinglog.log"
SECRET_LOCATION = "secret.txt"
RSS_URL = "https://ctftime.org/event/list/upcoming/rss/"
CHANNEL_ID = 1309395368475230238 # band-stuff
PING_CYCLE_TIME = 30 # seconds

feed = feedparser.parse(RSS_URL) 

# -------- Functions --------

def get_secret():
    with open(SECRET_LOCATION) as secret:
        return secret.read()

# Check if for the CTF time formated date if the start time is in two weeks or less than now
def check_date_two_weeks_from_now(date):
    date_with_no_time = date[:8] # Remove the time information, leaving just the date
    ctf_date = datetime.datetime.strptime(date_with_no_time, "%Y%m%d") # Parse the date into a datetime object
    two_weeks_time_delta = datetime.timedelta(weeks=2) # Get a timedelta for 2 weeks
    present = datetime.datetime.now() # Get the present datetime object
    # Check if the ctf start time is less than or equal to the the time two weeks from now 
    return True if ctf_date.date() <= (present + two_weeks_time_delta).date() else False

def generate_countdown(datetime_string):
    datetime_object = datetime.datetime.strptime(datetime_string, "%Y%m%dT%H%M%S")
    return "<t:" + str(int(time.mktime(datetime_object.timetuple()))) + ":R>"

def check_ping_logs_for_ctf(ctf_title):
    with open(PING_LOG_LOCATION) as ping_log:
        return True if ctf_title in ping_log.read() else False

def update_ping_logs_for_ctf(ctf_title):
    with open(PING_LOG_LOCATION, 'a') as ping_log:
        ping_log.write(ctf_title + "\n")

def date_time_string_to_local_datetime_string(datetime_string):
    datetime_object = datetime.datetime.strptime(datetime_string, "%Y%m%dT%H%M%S")
    return datetime_object.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).strftime("%a,  %Y-%m-%d, %H:%M")

async def ping_for_new_ctf(ctf, channel):
    ''' Possible ones ['title', 'title_detail', 'links', 'link', 'summary', 'summary_detail', 'id', 'guidislink', 
    'start_date', 'finish_date', 'logo_url', 'href', 'ctftime_url', 'format', 'format_text', 'public_votable', 
    'weight', 'live_feed', 'restrictions', 'location', 'onsite', 'organizers', 'ctf_id', 'ctf_name'] '''

    print("Ping!")
    await channel.send("<@&1311949816644767775> New CTF!")

    embed=discord.Embed(title=f"{ctf.title}", color=0x8000ff)

    embed_img = f"https://ctftime.org{ctf.logo_url}"
    # print(embed_img)
    embed.set_thumbnail(url=embed_img)

    embed.add_field(name="Links:", value=f"[CTF Time]({ctf.link}) | [Official CTF Webpage]({ctf.href})", inline=True)
    embed.add_field(name="CTF Weight:", value=f"{ctf.weight}", inline=True)
    embed.add_field(name="Date/Time (Adl):", value=f"**from: **{date_time_string_to_local_datetime_string(ctf.start_date)} ({generate_countdown(ctf.start_date)})\n**to:** {date_time_string_to_local_datetime_string(ctf.finish_date)}", inline=False)

    await channel.send(embed=embed)

@tasks.loop(seconds=PING_CYCLE_TIME)
async def discord_ping_cycle(channel):
    for ctf in feed["entries"]:
        # Filters for ctfs that are not onsite, are jeopardy, and are open to anyone
        if ctf.onsite == 'False' and ctf.format_text == "Jeopardy" and ctf.restrictions == "Open":
            if check_date_two_weeks_from_now(ctf.start_date):
                if not check_ping_logs_for_ctf(ctf.title):
                    await ping_for_new_ctf(ctf, channel)
                    update_ping_logs_for_ctf(ctf.title)

# -------- Running --------

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(CHANNEL_ID)
    discord_ping_cycle.start(channel)

client.run(get_secret())
