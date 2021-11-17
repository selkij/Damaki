from discord.ext import commands

class Join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await ctx.message.delete()
        await channel.connect()
    

class Leave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def leave(self, ctx):
        await ctx.message.delete()
        await ctx.voice_client.disconnect()

