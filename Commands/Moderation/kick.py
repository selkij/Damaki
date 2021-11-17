import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member: discord.Member, *reason):
        if ctx.author.top_role.position >= member.top_role.position:
            moderator = ctx.author
            reason = " ".join(reason)

            kickedEmbed = discord.Embed(title="🚪 Kicked 🚪", description=f"You got kicked for `{reason}` by **{moderator}** in **{ctx.guild.name}**", color=0x05B8F1)
            kickedEmbed.set_footer(text=f"Damaki © 2021 | Kicked by {moderator}", icon_url=member.avatar_url)

            await member.send(embed=kickedEmbed)
            await ctx.guild.kick(member)
            await ctx.send(f"> ✅ **{member.mention}** has been kicked for `{reason}` by **{moderator}**", delete_after=5)
        else:
            await ctx.send("> ⛔ You can't kick a moderator.", delete_after=5)
    
    @kick.error
    async def kickError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("> ⛔ Please enter someone to kick", delete_after=5)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()
            await ctx.send("> ⛔ You don't have the required permission `administrator` to perform this command", delete_after=5)
