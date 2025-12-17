"""
kwanCore, a discord.py bot foundation.
Copyright (C) 2022  dopebnan

You should have received a copy of the GNU General Public License
along with kwanCore. If not, see <https://www.gnu.org/licenses/>.
"""

import json
import random

import discord
from discord.ext import commands

with open("usercontent/settings.json") as file:
    settings = json.load(file)
with open("usercontent/quotes.json", encoding="utf-8") as file:
    quotes = json.load(file)


class General(commands.Cog, name="General", description="General user commands"):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.logger = bot.logger

    @commands.command(name="quote", brief="Sends a quote from the database")
    async def quote(self, ctx):
        test = discord.SyncWebhook.from_url(self.config["pin_link"])
        p = random.choice(list(quotes.values()))
        msg = random.choice(p["quotes"])
        test.send(msg, username=p["name"], avatar_url=p["pfp"])


async def setup(bot):
    await bot.add_cog(General(bot))
