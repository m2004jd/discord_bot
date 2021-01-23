import discord
import random
import asyncio
from datetime import datetime
from discord.ext import commands
import os
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re  # Regex for youtube link
import warnings
import requests
import time

token = "ODAxMzg4NDAzMDIyODg5MDIx.YAf9HA.iO6lAmh8P6reI0ueu6uXdb4skm0"
client = discord.Client()
now = datetime.now()
prefix = "$"


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{prefix}도움말"))
    print(client.user.name)


@client.event
async def on_message(message):

    if message.author.bot:
        return None

    if message.content.startswith(f"{prefix}도움말"):
        channel = message.channel
        await message.delete()
        helpembed = discord.Embed(
            title="도움말", description=f"```접두사는 {prefix} 입니다.```", color=0xfafafa)
        helpembed.add_field(
            name="`인증`", value="서버에 들어올려면 해야하는 인증입니다.", inline=False)
        helpembed.add_field(
            name="`코로나`", value="코로나에 대한 정보를 알려줍니다.", inline=False)
        await channel.send(embed=helpembed)

    if message.content.startswith(f"{prefix}인증"):
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

    if message.content.startswith(f"{prefix}코로나"):
        await message.delete()
        # 보건복지부 코로나 바이러스 정보사이트"
        covidSite = "http://ncov.mohw.go.kr/index.jsp"
        covidNotice = "http://ncov.mohw.go.kr"
        html = urlopen(covidSite)
        bs = BeautifulSoup(html, 'html.parser')
        latestupdateTime = bs.find('span', {'class': "livedate"}).text.split(',')[
            0][1:].split('.')
        statisticalNumbers = bs.findAll('span', {'class': 'num'})
        beforedayNumbers = bs.findAll('span', {'class': 'before'})

        # 주요 브리핑 및 뉴스링크
        briefTasks = []
        mainbrief = bs.findAll(
            'a', {'href': re.compile('\/tcmBoardView\.do\?contSeq=[0-9]*')})
        for brf in mainbrief:
            container = []
            container.append(brf.text)
            container.append(covidNotice + brf['href'])
            briefTasks.append(container)

        # 통계수치
        statNum = []
        # 전일대비 수치
        beforeNum = []
        for num in range(7):
            statNum.append(statisticalNumbers[num].text)
        for num in range(4):
            beforeNum.append(
                beforedayNumbers[num].text.split('(')[-1].split(')')[0])

        totalPeopletoInt = statNum[0].split(')')[-1].split(',')
        tpInt = ''.join(totalPeopletoInt)
        Covid_19_embed = discord.Embed(
            title="Covid-19 Virus Korea Status", color=0xfafafa)
        Covid_19_embed.add_field(name="Data source : Ministry of Health and Welfare of Korea",
                                 value="[링크](http://ncov.mohw.go.kr/index.jsp)", inline=False)
        Covid_19_embed.add_field(name="`확진환자(누적)`", value=statNum[0].split(
            ')')[-1]+"("+beforeNum[0]+")", inline=True)
        Covid_19_embed.add_field(
            name="`누적확진률`", value=statNum[6], inline=True)
        Covid_19_embed.add_field(
            name="`완치환자(격리해제)`", value=statNum[1] + "(" + beforeNum[1] + ")", inline=True)
        Covid_19_embed.add_field(
            name="`치료중(격리 중)`", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
        Covid_19_embed.add_field(
            name="`사망`", value=statNum[3] + "(" + beforeNum[3] + ")", inline=True)
        Covid_19_embed.add_field(name="`최신 브리핑`\n" +
                                 briefTasks[0][0], value=f"[링크]({briefTasks[0][1]})", inline=False)
        Covid_19_embed.add_field(name="`최신 브리핑`\n" +
                                 briefTasks[1][0], value=f"[링크]({briefTasks[1][1]})", inline=False)
        Covid_19_embed.set_footer(
            text=f"Latest data refred time | {latestupdateTime[0]}월 {latestupdateTime[1]}일 {latestupdateTime[2]}")
        Covid_19_embed.set_thumbnail(
            url="https://mohw.go.kr/images/react/homeimg.png")
        await message.channel.send("**Covid-19 Virus Korea Status**", embed=Covid_19_embed)

client.run(token)
