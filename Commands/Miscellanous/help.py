import discord
from discord import Color
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help Menu",
                              description="Listing of all the available commands",
                              color=Color.blue()
                              )
        embed.add_field(name="🎈 Miscellanous", value="🏓 **$**ping \n 🗯 **$**say <message> \n ℹ **$**info (member)")
        embed.add_field(name="🛡 Moderation", value="🚫 **$**ban <member> (reason)\n ❌ **$**kick <member> (reason) \n ⚠ **$**warn <victim> (reason)\n    **$**warns (member)")
        embed.set_footer(text=f"Damaki © 2021 | Sent by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
