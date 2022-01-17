from discord.ext import commands
import server
import discord
import os


# Load environment secrets
TOKEN = os.getenv('TOKEN')
PREFIX = os.getenv('PREFIX')
BADWORDS = os.getenv('BADWORDS').split(',')
hello = ['Hi', 'hi', 'Yo', 'yo', 'HI', 'Hello', 'HELLO']


bot = commands.Bot(command_prefix=PREFIX)


def make_name_pretty(name: str):
    return name[:name.index("#")]


@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    embed = discord.Embed(
        title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")


@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f" you have unmutedd from: - {ctx.guild.name}")
    embed = discord.Embed(
        title="unmute", description=f" unmuted-{member.mention}", colour=discord.Colour.light_gray())
    await ctx.send(embed=embed)


@bot.command(description="Bans a specified user. Needs ban permision to run.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:  discord.Member, *, reason=None):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself")
        return
    if reason == None:
        reason = "For being a jerk!"
    message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)
    await member.ban(reason=reason)
    await ctx.send(f"{member} is banned!")


@bot.command(description="Provides the latency between the bot and discord.")
async def ping(ctx):
    await ctx.send(f'Pong! Bot Latency: {round (bot.latency * 1000)} ms')


@bot.command(description="Unbans a specified user. Needs ban permision to run.")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"{user} Has been unbanned sucessfully")
        return


@bot.event
async def on_member_join(member):
    print(f' {member} has joined the server')


@bot.event
async def on_member_leave(member):
    print(f' {member} has left the server')


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

    await bot.change_presence(status=discord.Status.online, activity=discord.Game('?help\n Moderation ')


@ bot.event
async def on_message(message):     print(str(message.author) + ": " + message.content)
    words=message.content.split(' ')

    for word in words:
        if word in hello:
            await message.add_reaction('👋')

        if word in BADWORDS:
            await message.author.send(f'Hey {make_name_pretty(str(message.author))}! Swearing in the server is not allowed! Please do not continue with this behavior or else you may get banned or muted!')

            await message.delete()


    await bot.process_commands(message)

server.keep_alive()
bot.run(TOKEN)
