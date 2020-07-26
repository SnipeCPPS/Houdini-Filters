from houdini import handlers
from houdini.handlers import XTPacket
from houdini.plugins import IPlugin
from houdini.handlers.play.moderation import moderator_ban,moderator_kick

import os
import re
import asyncio

# Get blacklisted words text file
directory = os.path.dirname(os.path.realpath(__file__))
blacklist = os.path.join(directory, 'blacklist.txt')
whitelist = os.path.join(directory, 'whitelist.txt')

# Read blacklisted words
with open(blacklist) as badwords:
    bannedwords = [word for line in badwords for word in line.split()]

# Read whitelisted words
with open(whitelist) as goodwords:
    allowedwords = [word for line in goodwords for word in line.split()]

class Filters(IPlugin):
    author = "Snipe"
    description = "Word Filter"
    version = "1"
    
    def __init__(self, server):
        super().__init__(server)

    async def ready(self):
        self.server.logger.info('Word Filters Loaded!')
	
    @handlers.handler(XTPacket('m', 'sm'))
    async def handle_send_message(self, p, penguin_id: int, message: str):
        # Use regular expressions to look for patterns in the words and make it case insensitive.
        if re.findall(r"(?!("+'|'.join(allowedwords)+r"))"r"(\b(?=("+'|'.join(bannedwords)+r"))\b)", message, flags=re.IGNORECASE):
            print(f"Successfully filtered bad word! Message: {message}")
            await p.room.send_xt('mm', message, p.id, f=lambda px: px.moderator)
            await moderator_kick(p, p.id)
        else:
            return
