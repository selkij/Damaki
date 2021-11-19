from discord.ext import commands


class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *msg):
        msg = " ".join(msg)

        if "je suis bete" in msg.lower():
            msg = "Ont sait."
            await ctx.reply(msg)
        else:
            await ctx.message.delete()
            await ctx.send(msg)
        
        


        

        
