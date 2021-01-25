import discord
import random
import asyncio
import os
import urllib
import re
import warnings
import requests
import time
import json
from datetime import datetime
from discord.ext import commands
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote

token = "ODAxMzg4NDAzMDIyODg5MDIx.YAf9HA.iO6lAmh8P6reI0ueu6uXdb4skm0"
client = discord.Client()
now = datetime.now()
prefix = "$"


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}도움말"))
    print(client.user.name)

tierScore = {
    'default': 0,
    'iron': 1,
    'bronze': 2,
    'silver': 3,
    'gold': 4,
    'platinum': 5,
    'diamond': 6,
    'master': 7,
    'grandmaster': 8,
    'challenger': 9
}


def tierCompare(solorank, flexrank):
    if tierScore[solorank] > tierScore[flexrank]:
        return 0
    elif tierScore[solorank] < tierScore[flexrank]:
        return 1
    else:
        return 2


warnings.filterwarnings(action='ignore')

opggsummonersearch = 'https://www.op.gg/summoner/userName='


def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>', '', str(htmls[a]), 0).strip()
    return htmls


@client.event
async def on_message(message):

    if message.author.bot:
        return None

    if message.content.startswith(f"{prefix}도움말"):
        channel = message.channel
        await message.delete()
        Help_embed = discord.Embed(
            title="도움말", description=f"```접두사는 {prefix} 입니다.```", color=0xfafafa)
        Help_embed.add_field(
            name="`인증`", value="서버에 들어올려면 해야하는 인증입니다.", inline=False)
        Help_embed.add_field(
            name="`서버`", value="서버 대한 정보를 알려줍니다.", inline=False)
        Help_embed.add_field(
            name="`내정보`", value="내정보에 대한 정보를 알려줍니다.", inline=False)
        if message.author.id == 373669721746178049:
            Help_embed.add_field(
                name="`공지`", value="공지 채널에 공지를 올립니다.", inline=False)
        Help_embed.set_footer(text=str(now.year) + "." + str(now.month) +
                              "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
        await channel.send(embed=Help_embed)

    if message.content.startswith(f"{prefix}공지"):
        if message.author.id == 373669721746178049:
            await message.delete()
            msg = message.content.split()[1]
            Boradcast_embed = discord.Embed(
                title="공지", description=f"{msg}", color=0xfafafa)
            for i in client.guilds:
                for j in i.channels:
                    if "공지" in j.name:
                        await j.send(embed=Boradcast_embed)
                        return

    if message. content.startswith(f"{prefix}인증"):
        Verification_code = str(random.randint(100000, 999999))
        await message.delete()
        channel = message.author
        Join_embed = discord.Embed(
            title="Verification Code", color=0xfafafa)
        Join_embed.set_thumbnail(url=client.user.avatar_url)
        Join_embed.add_field(
            name="`확인코드`", value=Verification_code)
        Join_embed.set_footer(text="제한시간: 1분")
        Join_msg = await channel.send(embed=Join_embed)
        channel = client.get_channel(801706052244602900)
        Confirm_embed = discord.Embed(
            title="Verification Code", description="확인코드를 입력해주세요.", color=0xfafafa)
        Confirm_embed_msg = await channel.send(embed=Confirm_embed)

        def Confirm_check(m):
            return m.author == message.author and m.channel == channel
        try:
            Confirm_msg = await client.wait_for("message", timeout=60.0, check=Confirm_check)
        except:
            await Confirm_embed_msg.delete()
            Verification_code = str(random.randint(100000, 999999))
            Time_Out_embed = discord.Embed(
                title="Verification Code", description="Time Over", color=0xfafafa)
            Confirm_time_out = await channel.send(embed=Time_Out_embed)
            await asyncio.sleep(5)
            await Confirm_time_out.delete()
            return
        else:
            msg = Confirm_msg.content
            if Verification_code == msg:
                await Confirm_msg.delete()
                Clear_Confirm_embed = discord.Embed(
                    title="Verification Code", description="확인 완료", color=0xfafafa)
                role = discord.utils.get(
                    message.guild.roles, id=int(722006255136276492))
                await message.author.add_roles(role)
                Clear_Confirm_msg = await channel.send(embed=Clear_Confirm_embed)
            else:
                await Confirm_msg.delete()
                Clear_Confirm_embed = discord.Embed(
                    title="Verification Code", description="틀렸습니다.", color=0xfafafa)
                Clear_Confirm_msg = await channel.send(embed=Clear_Confirm_embed)
            await asyncio.sleep(5)
            await Confirm_embed_msg.delete()
            await Clear_Confirm_msg.delete()
            return

    if message.content.startswith(f"{prefix}내정보"):
        await message.delete()
        My_embed = discord.Embed(
            title=f"{message.author.name}", color=0x050505)
        My_embed.add_field(
            name="`Name`", value=f"{message.author}", inline=False)
        My_embed.add_field(
            name="`Nick`", value=f"{message.author.nick}", inline=False)
        My_embed.add_field(
            name="`ID`", value=f"{message.author.id}", inline=False)
        My_embed.add_field(
            name="`Join`", value=f"{(message.author.joined_at).year}.{(message.author.joined_at).month}.{(message.author.joined_at).day} {(message.author.joined_at).hour}:{(message.author.joined_at).minute}", inline=False)
        My_embed.set_footer(text=str(now.year) + "." + str(now.month) +
                            "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
        My_embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=My_embed)

    if message.content.startswith(f"{prefix}서버"):
        await message.delete()
        Server_embed = discord.Embed(
            title="서버", color=0x050505)
        Server_embed.add_field(
            name="`Name`", value=f"{message.author.guild}", inline=False)
        Server_embed.add_field(
            name="`ID`", value=f"{message.author.guild.id}", inline=False)
        Server_embed.add_field(
            name="`Server Age`", value=f"{now.year - message.author.guild.created_at.year}살", inline=False)
        Server_embed.add_field(
            name="`Member`", value=f"{message.author.guild.member_count}명", inline=False)
        Server_embed.set_footer(text=str(now.year) + "." + str(now.month) +
                                "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
        Server_embed.set_thumbnail(
            url=client.user.avatar_url)
        await message.channel.send(embed=Server_embed)

client.run(token)
