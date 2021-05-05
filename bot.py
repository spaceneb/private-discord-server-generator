import discord, yaml, os
from discord.ext import commands, tasks
bot = commands.Bot(intents=discord.Intents.all(),command_prefix="/")
with open(f"{os.getcwd()}/config.yml","r") as file:
    botConfig = yaml.safe_load(file)
async def createServer():
    guild = await bot.create_guild(name=f"{bot.user.name} Server")
    channels = await guild.fetch_channels()
    for channel in channels:
        await channel.delete()
    await guild.create_role(name="root",permissions=discord.Permissions.all())
    await guild.create_role(name="Server Owner",permissions=discord.Permissions.all())
    channel = await guild.create_text_channel('invite')
    invite = await channel.create_invite(max_age=0,max_uses=0)
    return invite
@bot.command()
async def grantRoles(ctx):
    owner = await bot.is_owner(user=ctx.author)
    if owner and ctx.guild.owner_id == bot.user.id:
        await ctx.author.add_roles(ctx.guild.roles[len(ctx.guild.roles) - 1])
        await ctx.send(embed=discord.Embed(title="Success!", description=f"The `root` role has been granted to <@!{ctx.author.id}>!",color=discord.Color.blurple()))
@bot.command()
async def deleteGuild(ctx):
    owner = await bot.is_owner(user=ctx.author)
    if owner and ctx.guild.owner_id == bot.user.id:
        await ctx.guild.delete()
@bot.command()
async def joinNotifications(ctx):
    owner = await bot.is_owner(user=ctx.author)
    if owner and ctx.guild.owner_id == bot.user.id:
        flags = ctx.guild.system_channel_flags
        flags.join_notifications = not flags.join_notifications
        await ctx.guild.edit(system_channel_flags=flags)
        await ctx.send(embed=discord.Embed(title="Success!", description=f"Updated Join Notifications to be `{flags.join_notifications}`",color=discord.Color.blurple()))
@bot.command()
async def premiumSubscriptions(ctx):
    owner = await bot.is_owner(user=ctx.author)
    if owner and ctx.guild.owner_id == bot.user.id:
        flags = ctx.guild.system_channel_flags
        flags.premium_subscriptions = not flags.premium_subscriptions
        await ctx.guild.edit(system_channel_flags=flags)
        await ctx.send(embed=discord.Embed(title="Success!", description=f"Updated Premium Subscriptions to be `{flags.premium_subscriptions}`",color=discord.Color.blurple()))
@bot.command()
async def createPrivateServer(ctx):
    owner = await bot.is_owner(user=ctx.author)
    if owner and not ctx.author.bot and isinstance(ctx.channel, discord.DMChannel):
        invite = await createServer()
        await ctx.send(content=invite,embed=discord.Embed(title="Success!",description="Created a new private server!",color=discord.Color.blurple()))
@bot.event
async def on_ready():
    print("Ready!")
bot.run(botConfig['bot']['token'])