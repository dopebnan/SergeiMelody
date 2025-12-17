"""
kwanCore, a discord.py bot foundation.
Copyright (C) 2022  dopebnan

You should have received a copy of the GNU General Public License
along with kwanCore. If not, see <https://www.gnu.org/licenses/>.
"""

import asyncpraw
import random

from discord.ext import commands
import discord


class Memes(commands.Cog, name="Memes", description="Reddit and stuff"):
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger
        self.reddit = asyncpraw.Reddit(
            client_id=bot.config["reddit"]['client_id'],
            client_secret=bot.config["reddit"]['client_secret'],
            password=bot.config["reddit"]['password'],
            user_agent=bot.config["reddit"]['user_agent'],
            username=bot.config["reddit"]['username']
        )
        self.emojis = bot.config["emojis"]

    async def get_post_embed(self, subreddit, color=None, title="", timeout=100):
        """
        Get a random image from a subreddit

        :param subreddit:  str, the subreddit name
        :param color:  int, the embed color
            Default: None
        :param title:  str, the embed title
            Default: the title of the found submission
        :param timeout:  int, the post limit
            Default: 100
        """
        subreddit = await self.reddit.subreddit(subreddit)
        submissions = [post async for post in subreddit.hot(limit=100) if hasattr(post, "post_hint") and post.post_hint == "image"]

        if not submissions:
            raise TimeoutError()

        submission = random.choice(submissions)

        if not title:
            title = submission.title

        self.logger.log(
            "info", "get_post_embed",
            f"Found {submission.permalink} from r/{submission.subreddit}"
        )
        embed = discord.Embed(
            title=title,
            url=submission.shortlink,
            color=color
        )
        embed.set_image(url=submission.url)
        embed.add_field(
            name=f"{self.emojis['upvote']} {submission.score} {self.emojis['downvote']}",
            value="\u200b"
        )
        embed.set_footer(text=f"Posted by u/{submission.author} in r/{submission.subreddit}")
        return embed

    @commands.command(name="random_image", brief="Gets a random image post from a subreddit")
    async def random_image(self, ctx, subreddit):
        async with ctx.typing():
            embed = await self.get_post_embed(subreddit, discord.Color.random())
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Memes(bot))
