# Omega-bot

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), [Python3.5](https://www.python.org/downloads/release/python-350/) and [discord-py](https://github.com/Rapptz/discord.py) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone git@github.com:Brinnyman/omega-bot

# Go into the repository
$ cd omega-bot

# Run the app
$ python3.5 bot.py
```

## Configuration

```bash
# Go into the config directory
$ cd config

# Configure the bot in config.ini
[Credentials]
token = discord-api-token

[Chat]
prefix = !

[Permission]
ownerid = discord-user-id
permitted = discord-role-id

[Channel]
logchannel = discord-channel-id

# Set the command permissions in permission.ini
[Member]
commandwhitelist = command

[Mod]
commandwhitelist = command
```

## Bot commands

The extensions "members", "moderator", "help" are loaded by default.

```bash
!help   Shows bot commands.
!load   Load extension.
!unload   Unload extension.
!reload   Reload extension.
```
