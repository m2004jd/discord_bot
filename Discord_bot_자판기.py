import discord
import random
import asyncio
from datetime import datetime
from discord.ext import commands
import os

token = "ODAxMzg4NDAzMDIyODg5MDIx.YAf9HA.G25LYpvpxPOjqVhPHWDv6lxQ-zI"
client = discord.Client()
now = datetime.now()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='$도움말'))


@client.event
async def on_message(message):

    if message.author.bot:
        return None

    if message.content == "$도움말":
        channel = message.channel
        await message.delete()
        helpembed = discord.Embed(
            title="Help", color=0x453a3a)
        helpembed.set_thumbnail(
            url=client.user.avatar_url)
        helpembed.add_field(
            name="`인증`", value="서버에 들어올려면 해야하는 인증입니다.", inline=False)
        await channel.send(embed=helpembed)

    if message.content == "$인증":
        Verification_code = str(random.randint(100000, 999999))
        await message.delete()
        channel = message.author
        Join_embed = discord.Embed(
            title="Verification Code", color=0x453a3a)
        Join_embed.set_thumbnail(url=client.user.avatar_url)
        Join_embed.add_field(
            name="`확인코드`", value=Verification_code)
        Join_embed.set_footer(text="제한시간: 1분")
        Join_msg = await channel.send(embed=Join_embed)
        channel = client.get_channel(801706052244602900)
        Confirm_embed = discord.Embed(
            title="Verification Code", description="확인코드를 입력해주세요.", color=0x453a3a)
        Confirm_embed_msg = await channel.send(embed=Confirm_embed)

        def Confirm_check(m):
            return m.author == message.author and m.channel == channel
        try:
            Confirm_msg = await client.wait_for("message", timeout=60.0, check=Confirm_check)
        except:
            await Confirm_embed_msg.delete()
            Verification_code = str(random.randint(100000, 999999))
            Time_Out_embed = discord.Embed(
                title="Verification Code", description="Time Over", color=0x453a3a)
            Confirm_time_out = await channel.send(embed=Time_Out_embed)
            await asyncio.sleep(5)
            await Confirm_time_out.delete()
            return
        else:
            msg = Confirm_msg.content
            if Verification_code == msg:
                await Confirm_msg.delete()
                Clear_Confirm_embed = discord.Embed(
                    title="Verification Code", description="확인 완료", color=0x453a3a)
                role = discord.utils.get(
                    message.guild.roles, id=int(722006255136276492))
                await message.author.add_roles(role)
                Clear_Confirm_msg = await channel.send(embed=Clear_Confirm_embed)
            else:
                await Confirm_msg.delete()
                Clear_Confirm_embed = discord.Embed(
                    title="Verification Code", description="틀렸습니다.", color=0x453a3a)
                Clear_Confirm_msg = await channel.send(embed=Clear_Confirm_embed)
            await asyncio.sleep(5)
            await Confirm_embed_msg.delete()
            await Clear_Confirm_msg.delete()
            return

client.run(token)
