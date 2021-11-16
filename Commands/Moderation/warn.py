import discord

from discord.ext.commands.errors import MissingPermissions
from discord.ext.commands import MissingRequiredArgument
from discord.ext import commands

from dotenv import load_dotenv
from datetime import date

load_dotenv('config.env')

class Warn(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def warn(self, ctx, member: discord.Member, *reason):
        await ctx.message.delete()
        #FIXME: Can warn moderators
        memberId = member.id
        reason = " ".join(reason)
        datet = date.today()
        moderator = ctx.author

        await ctx.send(f"> ✅ **{member.mention}** has been warned for `{reason}` by **{moderator}**")

        cursor = self.db.cursor()
        warn_query = f"INSERT INTO warn (userID, reason, date, moderator) values ('{memberId}','{reason}', '{datet}', '{moderator}')"
        cursor.execute(warn_query)

        self.db.commit()
        await ctx.send("sent to database")
        print(f"Warn command issued by {ctx.author} \nId: {ctx.author.id}  \nfor {member} Id: {memberId} \nReason: {reason}\nGuild: {ctx.guild.id}\n--------")


    @warn.error
    async def warnError(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.message.delete()
            await ctx.send("> ⛔ Please enter someone to warn", delete_after=5)
        elif isinstance(error, MissingPermissions):
            await ctx.message.delete()
            await ctx.send("> ⛔ You don't have the required permission `administrator` to perform this command", delete_after=5)


#      LISTING OF WARNS
class Warns(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    

    @commands.command()
    async def warns(self, ctx, member: discord.Member):
        pass

    @warns.error
    async def warnsError(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            selfEmbed = discord.Embed(title="List of warns",
                                      description=f"Warns menu of {ctx.author.mention}",
                                      color=0xF19F05,
                                      image=ctx.author.avatar_url
                                      )
            selfEmbed.add_field(name="⚠ Warns ⚠", value="None")
            selfEmbed.set_footer(text=f"Damaki © 2021 | Sent by {ctx.author}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=selfEmbed)