from discord.ext import commands
import discord

class Logs(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
    logChannel = None
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def logs(self, ctx, arg):
        logChannel = arg

        cursor = self.db.cursor()
        add_query = f"INSERT INTO logs (channel, guild) VALUES ('{logChannel}', '{ctx.guild.id}')"
        cursor.execute(add_query)

        self.db.commit()

        await ctx.send(f"> ✅ Log channel has been set to `{logChannel}`")
        print(f"Log channel set to {logChannel} in {ctx.guild}")

    @commands.Cog.listener()
    async def on_ready(self):
        logChannel = self.bot.get_channel(910979507324862515)
        embed = discord.Embed(title="✅ Online ✅", description="> Bot online", color=0x25ba0e)
        embed.set_footer(text=f"Damaki © 2021 | Bot ON")

        await logChannel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        logChannel = self.bot.get_channel(910979507324862515)
        embed = discord.Embed(title="🗑 Message deleted 🗑", color=0xb11e31)
        embed.add_field(name=f"Message deleted by {message.author}", value=f"`{message.content}` in <#{message.channel.id}>")
        embed.set_footer(text=f"Damaki © 2021 | Message deleted", icon_url=message.author.avatar_url)
        await logChannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        logChannel = self.bot.get_channel(910979507324862515)
        link = before.jump_url
        embed = discord.Embed(title="💭 Message edited 💭", color=0xffd966)
        embed.add_field(name=f"Last message:", value=f"`{before.content}`")
        embed.add_field(name=f"New message:", value=f"`{after.content}`")
        embed.add_field(name=f"Infos:", value=f"edited by: {after.author} \n channel: <#{after.channel.id}> \n [Link]({link})")
        embed.set_footer(text=f"Damaki © 2021 | Message edited", icon_url=after.author.avatar_url)
        await logChannel.send(embed=embed)

    @logs.error
    async def logsError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            pass
        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.delete()                          
            await ctx.send("> ⛔ You don't have the required permission `administrator` to perform this command", delete_after=5)
