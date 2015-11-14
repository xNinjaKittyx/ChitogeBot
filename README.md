# ChitogeBot
A Python Bot for Discord. Powered by discord.py

# What is ChitogeBot?
ChitogeBot is a chatbot that is used for Discord servers.

It is using the python API wrapper, discord.py that wraps around the DiscordAPI.

# Commands
!help - Display this help message.

!cinfo - Channel Information

!who [user] - User Information

!wiki [topic] - Look for a wiki page\n

!listmusic - List all music files available on the bot

!lookup [Summoner] - Find Summoner on LoL

!next - Play the next song

!pause - Pause the song

!play [song] - Play a song

!resume - Resume the player

!stop - Stop the player - Currently not working

!roll - Roll a die

!uptime - Bot uptime

# Todo List
- !johncena - Find's author's voice channel and play johncena.
- !join [channel] - Join that voice channel.
- So i Found out discord.py doesn't support joining voice channels yet.
- Need to organize in different classes
- Need to organize HELP command
- !lookup - Find Rank Division
- A Json file to keep track of ignored servers.
- A json file to store a playlist (so in case of crash, it can return where it began
- This also means I need to put youtube API in here to autoplay it. (or use youtube-dl to grab an mp3 file and then play it.)
- !ignoreserver - Ignore the server (Only executable by those with permission)
