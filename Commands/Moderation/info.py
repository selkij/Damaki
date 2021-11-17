import discord
from discord.ext import commands

import datetime

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def info(self, ctx, member: discord.Member):
        infoEmbed = discord.Embed(title=f"{member.name}'s menu", description="Info menu", color=0x0557F1)
        infoEmbed.add_field(name="🕘 Joined server at:", value=member.joined_at(), inline=False)
        infoEmbed.add_field(name="➕ Created account at:", value=member.created_at, inline=False)

        await ctx.send(embed=infoEmbed)
    
    @info.error
    async def kickError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(error)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(error) #member view