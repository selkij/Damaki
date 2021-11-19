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

        if ctx.author.top_role.position >= member.top_role.position:

            memberId = member.id
            reason = " ".join(reason)

            datet = date.today()
            
            moderator = ctx.author
            cursor = self.db.cursor()

            warnCheckQuery = "SELECT MAX(ID) AS MaxID FROM warn"
            cursor.execute(warnCheckQuery)

            warnIdSQL = cursor.fetchone()[0]
            warnId = int(warnIdSQL) + 1

            if warnId == 10:
                warnId = 99167239
            elif warnId == 20:
                warnId = 99167240
            elif warnId == 30:
                warnId = 99167241
            elif warnId == 40:
                warnId = 99167241

            warn_query = f"INSERT INTO warn (ID, userID, reason, date, moderator) VALUES ('{warnId}', '{memberId}','{reason}', '{datet}', '{moderator.id}')"
            cursor.execute(warn_query)

            self.db.commit()

            await ctx.send(f"> ✅ **{member.mention}** has been warned for `{reason}` by **{moderator}**", delete_after=5)

            warnedEmbed = discord.Embed(title="⚠ Warned ⚠", description=f"You got warned for `{reason}` by **{moderator}** in **{ctx.guild.name}**", color=0xE0BA50)
            warnedEmbed.set_footer(text=f"Damaki © 2021 | Warned by {moderator}", icon_url=member.avatar_url)
            await member.send(embed=warnedEmbed)

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
    @commands.has_permissions(administrator = True)
    async def warns(self, ctx, member: discord.Member):
        cursor = self.db.cursor()
        warns_query = f"SELECT * FROM warn WHERE userID = '{member.id}';"
        cursor.execute(warns_query)
        result = cursor.fetchall()
        warnMessage = ""
        debounce = 1

        selfEmbed = discord.Embed(title="⚠ List of warns ⚠",
                                  description=f"Warns menu of {member.mention}",
                                  color=0xF19F05,
                                  image=ctx.author.avatar_url
                                  )
        for warns in result:
            warnedUser = await self.bot.fetch_user(warns[1])
            moderatorUser = await self.bot.fetch_user(warns[4])

            if warns[2] == "":
                warnMessage += f"**{debounce}**.\n > ❓ **Reason**: `No Reason`\n > 🚨 **Moderator**: {moderatorUser} | 🌐 **{warns[4]}**\n\n"
            else:
                warnMessage += f"**{debounce}**.\n > ❓ **Reason**: `{warns[2]}`\n > 🚨 **Moderator**: {moderatorUser} | 🌐 **{warns[4]}**\n\n"
                
            debounce += 1

        selfEmbed.add_field(name=f"Warn", value=warnMessage, inline=False)
        selfEmbed.set_footer(text=f"Damaki © 2021 | Sent by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=selfEmbed)

    @warns.error
    async def warnsError(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            cursor = self.db.cursor()
            warns_query = f"SELECT * FROM warn;"
            cursor.execute(warns_query)
            result = cursor.fetchall()
            warnMessage = ""
            debounce = 1

            selfEmbed = discord.Embed(title="⚠ List of warns ⚠",
                                      description=f"Warns menu",
                                      color=0xF19F05,
                                      image=ctx.author.avatar_url
                                      )
            for warns in result:
                warnedUser = await self.bot.fetch_user(warns[1])
                moderatorUser = await self.bot.fetch_user(warns[4])

                if warns[2] == "":
                    warnMessage += f"**{debounce}**.\n > 🙍‍♂️ **Member**: {warnedUser} | 🌐 **{warns[1]}**\n > ❓ **Reason**: `No Reason`\n > 🚨 **Moderator**: {moderatorUser} | 🌐 **{warns[4]}**\n\n"
                else:
                    warnMessage += f"**{debounce}**.\n > 🙍‍♂️ **Member**: {warnedUser} | 🌐 **{warns[1]}**\n > ❓ **Reason**: `{warns[2]}`\n > 🚨 **Moderator**: {moderatorUser} | 🌐 **{warns[4]}**\n\n"
                
                debounce += 1

            selfEmbed.add_field(name=f"Warn", value=warnMessage)
            selfEmbed.set_footer(text=f"Damaki © 2021 | Sent by {ctx.author}", icon_url=ctx.author.avatar_url)

            sendEmbed = await ctx.send(embed=selfEmbed)
            await sendEmbed.add_reaction("◀")
            await sendEmbed.add_reaction("▶")

            @commands.Cog.listener()
            async def on_reaction_add(self, playload):
                message = playload.message
                
                if playload.emoji == "◀":
                    await ctx.send("test")
            
            

