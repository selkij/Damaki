from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"> 🏓 Pong! `{round(self.bot.latency * 1000)} ms`")
        print(f"Ping command issued by {ctx.author} \nId: {ctx.author.id} \nGuild: {ctx.guild.id}\n--------")
