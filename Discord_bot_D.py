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
            name="`코로나`", value="코로나에 대한 정보를 알려줍니다.", inline=False)
        Help_embed.add_field(
            name="`서버`", value="서버 대한 정보를 알려줍니다.", inline=False)
        Help_embed.add_field(
            name="`내정보`", value="내정보에 대한 정보를 알려줍니다.", inline=False)
        Help_embed.add_field(
            name="`롤전적`", value="해당 유저의 롤전적을 알려줍니다.", inline=False)
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
            name="`완치환자(격리해제)`", value=statNum[1] + "(" + beforeNum[1] + ")", inline=False)
        Covid_19_embed.add_field(
            name="`치료중(격리 중)`", value=statNum[2] + "(" + beforeNum[2] + ")", inline=True)
        Covid_19_embed.add_field(
            name="`사망`", value=statNum[3] + "(" + beforeNum[3] + ")", inline=False)
        Covid_19_embed.add_field(name="`최신 브리핑`\n" +
                                 briefTasks[0][0], value=f"[링크]({briefTasks[0][1]})", inline=False)
        Covid_19_embed.add_field(name="`최신 브리핑`\n" +
                                 briefTasks[1][0], value=f"[링크]({briefTasks[1][1]})", inline=False)
        Covid_19_embed.set_footer(
            text=f"Latest data refred time | {latestupdateTime[0]}월 {latestupdateTime[1]}일 {latestupdateTime[2]}")
        Covid_19_embed.set_thumbnail(
            url="https://mohw.go.kr/images/react/homeimg.png")
        await message.channel.send("**Covid-19 Virus Korea Status**", embed=Covid_19_embed)

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

    if message.content.startswith(f"{prefix}롤전적"):
        await message.delete()
        try:
            if len(message.content.split(" ")) == 1:
                embed = discord.Embed(
                    title="소환사 이름이 입력되지 않았습니다!", description="", color=0x5CD1E5)
                embed.add_field(name="Summoner name not entered",
                                value=f"{prefix}롤전적 (Summoner Nickname)", inline=False)
                embed.set_footer(text=str(now.year) + "." + str(now.month) +
                                 "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
                await message.channel.send("**Error : Incorrect command usage**", embed=embed)
            else:
                playerNickname = ''.join((message.content).split(' ')[1:])
                # Open URL
                checkURLBool = urlopen(
                    opggsummonersearch + quote(playerNickname))
                bs = BeautifulSoup(checkURLBool, 'html.parser')

                # 자유랭크 언랭은 뒤에 '?image=q_auto&v=1'표현이없다

                # Patch Note 20200503에서
                # Medal = bs.find('div', {'class': 'ContentWrap tabItems'}) 이렇게 바꾸었었습니다.
                # PC의 설정된 환경 혹은 OS플랫폼에 따라서 ContentWrap tabItems의 띄어쓰기가 인식이

                Medal = bs.find('div', {'class': 'SideContent'})
                RankMedal = Medal.findAll('img', {'src': re.compile(
                    '\/\/[a-z]*\-[A-Za-z]*\.[A-Za-z]*\.[A-Za-z]*\/[A-Za-z]*\/[A-Za-z]*\/[a-z0-9_]*\.png')})
                # Variable RankMedal's index 0 : Solo Rank
                # Variable RankMedal's index 1 : Flexible 5v5 rank

                # for mostUsedChampion
                mostUsedChampion = bs.find('div', {'class': 'ChampionName'})
                mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})

                # 솔랭, 자랭 둘다 배치가 안되어있는경우 -> 사용된 챔피언 자체가 없다. 즉 모스트 챔피언 메뉴를 넣을 필요가 없다.

                # Scrape Summoner's Rank information
                # [Solorank,Solorank Tier]
                solorank_Types_and_Tier_Info = deleteTags(
                    bs.findAll('div', {'class': {'RankType', 'TierRank'}}))
                # [Solorank LeaguePoint, Solorank W, Solorank L, Solorank Winratio]
                solorank_Point_and_winratio = deleteTags(
                    bs.findAll('span', {'class': {'LeaguePoints', 'wins', 'losses', 'winratio'}}))
                # [Flex 5:5 Rank,Flexrank Tier,Flextier leaguepoint + W/L,Flextier win ratio]
                flexrank_Types_and_Tier_Info = deleteTags(bs.findAll('div', {
                    'class': {'sub-tier__rank-type', 'sub-tier__rank-tier', 'sub-tier__league-point',
                              'sub-tier__gray-text'}}))
                # ['Flextier W/L]
                flexrank_Point_and_winratio = deleteTags(
                    bs.findAll('span', {'class': {'sub-tier__gray-text'}}))

                # embed.set_imag()는 하나만 들어갈수 있다.

                # 솔랭, 자랭 둘다 배치 안되어있는 경우 -> 모스트 챔피언 출력 X
                if len(solorank_Point_and_winratio) == 0 and len(flexrank_Point_and_winratio) == 0:
                    embed = discord.Embed(
                        title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=f"[링크]({opggsummonersearch + playerNickname})",
                                    inline=False)
                    embed.add_field(name="Ranked Solo : Unranked",
                                    value="Unranked", inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked",
                                    value="Unranked", inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    embed.set_footer(text=str(now.year) + "." + str(now.month) +
                                     "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
                    await message.channel.send("**소환사 " + playerNickname + "님의 전적**", embed=embed)

                # 솔로랭크 기록이 없는경우
                elif len(solorank_Point_and_winratio) == 0:

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find(
                        'div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[
                        0]
                    mostUsedChampionWinRate = bs.find(
                        'div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + \
                        ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + \
                        " /" + flexrank_Types_and_Tier_Info[-1]
                    embed = discord.Embed(
                        title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=f"[링크]({opggsummonersearch + playerNickname})",
                                    inline=False)
                    embed.add_field(name="Ranked Solo : Unranked",
                                    value="Unranked", inline=False)
                    embed.add_field(
                        name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " +
                                    " WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    embed.set_footer(text=str(now.year) + "." + str(now.month) +
                                     "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
                    await message.channel.send("**소환사 " + playerNickname + "님의 전적**", embed=embed)

                # 자유랭크 기록이 없는경우
                elif len(flexrank_Point_and_winratio) == 0:

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find(
                        'div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[
                        0]
                    mostUsedChampionWinRate = bs.find(
                        'div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    SoloRankTier = solorank_Types_and_Tier_Info[0] + \
                        ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    embed = discord.Embed(
                        title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=f"[링크]({opggsummonersearch + playerNickname})",
                                    inline=False)
                    embed.add_field(
                        name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Flex 5:5 Rank : Unranked",
                                    value="Unranked", inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " +
                                    "WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    embed.set_footer(text=str(now.year) + "." + str(now.month) +
                                     "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
                    await message.channel.send("**소환사 " + playerNickname + "님의 전적**", embed=embed)
                # 두가지 유형의 랭크 모두 완료된사람
                else:
                    # 더 높은 티어를 thumbnail에 안착
                    solorankmedal = RankMedal[0]['src'].split(
                        '/')[-1].split('?')[0].split('.')[0].split('_')
                    flexrankmedal = RankMedal[1]['src'].split(
                        '/')[-1].split('?')[0].split('.')[0].split('_')

                    # Make State
                    SoloRankTier = solorank_Types_and_Tier_Info[0] + \
                        ' : ' + solorank_Types_and_Tier_Info[1]
                    SoloRankPointAndWinRatio = solorank_Point_and_winratio[0] + "/ " + solorank_Point_and_winratio[
                        1] + " " + solorank_Point_and_winratio[2] + " /" + solorank_Point_and_winratio[3]
                    FlexRankTier = flexrank_Types_and_Tier_Info[0] + \
                        ' : ' + flexrank_Types_and_Tier_Info[1]
                    FlexRankPointAndWinRatio = flexrank_Types_and_Tier_Info[2] + \
                        " /" + flexrank_Types_and_Tier_Info[-1]

                    # most Used Champion Information : Champion Name, KDA, Win Rate
                    mostUsedChampion = bs.find(
                        'div', {'class': 'ChampionName'})
                    mostUsedChampion = mostUsedChampion.a.text.strip()
                    mostUsedChampionKDA = bs.find('span', {'class': 'KDA'})
                    mostUsedChampionKDA = mostUsedChampionKDA.text.split(':')[
                        0]
                    mostUsedChampionWinRate = bs.find(
                        'div', {'class': "Played"})
                    mostUsedChampionWinRate = mostUsedChampionWinRate.div.text.strip()

                    cmpTier = tierCompare(solorankmedal[0], flexrankmedal[0])
                    embed = discord.Embed(
                        title="소환사 전적검색", description="", color=0x5CD1E5)
                    embed.add_field(name="Summoner Search From op.gg", value=f"[링크]({opggsummonersearch + playerNickname})",
                                    inline=False)
                    embed.add_field(
                        name=SoloRankTier, value=SoloRankPointAndWinRatio, inline=False)
                    embed.add_field(
                        name=FlexRankTier, value=FlexRankPointAndWinRatio, inline=False)
                    embed.add_field(name="Most Used Champion : " + mostUsedChampion,
                                    value="KDA : " + mostUsedChampionKDA + " / " +
                                    " WinRate : " + mostUsedChampionWinRate,
                                    inline=False)
                    if cmpTier == 0:
                        embed.set_thumbnail(url='https:' + RankMedal[0]['src'])
                    elif cmpTier == 1:
                        embed.set_thumbnail(url='https:' + RankMedal[1]['src'])
                    else:
                        if solorankmedal[1] > flexrankmedal[1]:
                            embed.set_thumbnail(
                                url='https:' + RankMedal[0]['src'])
                        elif solorankmedal[1] < flexrankmedal[1]:
                            embed.set_thumbnail(
                                url='https:' + RankMedal[0]['src'])
                        else:
                            embed.set_thumbnail(
                                url='https:' + RankMedal[0]['src'])

                    embed.set_footer(text=str(now.year) + "." + str(now.month) +
                                     "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
                    await message.channel.send("**소환사 " + playerNickname + "님의 전적**", embed=embed)
        except HTTPError as e:
            embed = discord.Embed(title="소환사 전적검색 실패",
                                  description="", color=0x5CD1E5)
            embed.add_field(
                name="", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
            embed.set_footer(text=str(now.year) + "." + str(now.month) +
                             "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
            await message.channel.send("**Wrong Summoner Nickname**")

        except UnicodeEncodeError as e:
            embed = discord.Embed(title="소환사 전적검색 실패",
                                  description="", color=0x5CD1E5)
            embed.add_field(
                name="", value="올바르지 않은 소환사 이름입니다. 다시 확인해주세요!", inline=False)
            embed.set_footer(text=str(now.year) + "." + str(now.month) +
                             "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
            await message.channel.send("**Wrong Summoner Nickname**", embed=embed)

        except AttributeError as e:
            embed = discord.Embed(title="존재하지 않는 소환사",
                                  description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 소환사가 존재하지 않습니다.",
                            value="소환사 이름을 확인해주세요", inline=False)
            embed.set_footer(text=str(now.year) + "." + str(now.month) +
                             "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute))
            await message.channel.send("**Error : Non existing Summoner**", embed=embed)

client.run(token)
