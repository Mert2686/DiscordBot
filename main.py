import random
import discord
from discord.ext import commands
from Oyunlar import *
import sqlite3
from random import *
from datetime import *
import locale
import datetime
import asyncio
import random

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

emoji = "<:4555minecraftglow:947558987514130492>"
emoji_2 = "<:3621gold:947567448708771921>"
emoji_3 = "<:puff:947572046794194944>"
#yeşil = 0x2ecc71
#kırmız = 0xe74c3c
#sarı = 0xf1c40f
@Bot.event
async def on_ready():
    await Bot.change_presence(activity=discord.Game(name="Adalances Towny"))
    print("Ben Hazırım")


@Bot.command()
@commands.has_role("Yönetici")
async def kayıt(ctx, member: discord.Member, mcnick, bakiye):
    discord_id = member.id
    user = get_user_or_false(discord_id)
    if user:
        kullancı_var = discord.Embed(color=0xe74c3c)
        kullancı_var.add_field(name="Kayıt Yapılamadı!", value="Kullanıcı zaten kayıtlı")
        await ctx.send(embed=kullancı_var)
    else:
        imlec.execute("INSERT INTO kullanıcılar VALUES('{}','{}','{}')".format(discord_id, mcnick, bakiye))
        bağlantı.commit()
        imlec.execute("SELECT * FROM kullanıcılar WHERE id='{}'".format(discord_id))
        kullanıcı_var = discord.Embed(color=0xf1c40f)
        for veri in imlec.fetchall():

            ad = veri[1]
            bakiye = veri[2]
            kullanıcı_kayıt = discord.Embed(color=0xf1c40f)
            kullanıcı_kayıt.add_field(name="**Kayıt Yapıldı**", value=f"{emoji_3}**Kullanıcı**: {member.mention}\n{emoji}**Minecraft Adı**: {ad}\n{emoji_2}**Bakiyesi**: {bakiye} Altın")


            await ctx.send(embed=kullanıcı_kayıt)

@Bot.command()
async def bakiye(ctx, member: discord.Member):
    discord_id = member.id
    user = get_user_or_false(discord_id)
    kullancı_yok = discord.Embed(color=0xe74c3c)
    kullancı_yok.add_field(name="Kullanıcı Bulunamadı!", value="Böyle bir kullanıcı sisteme kayıtlı değil")
    if user:
        imlec.execute("SELECT * FROM kullanıcılar WHERE id='{}'".format(discord_id))
        kullanıcı_var = discord.Embed(color=0xf1c40f)
        for veri in imlec.fetchall():
            ad = veri[1]
            bakiye = veri[2]
            kullanıcı_var.add_field(name=f"**Bakiye Sorgu!**",
                                    value=f"{emoji_3}**Kullanıcı**: {member.mention}\n{emoji}**Minecraft Adı**: {ad}\n{emoji_2}**Bakiyesi**: {bakiye} Altın")
            await ctx.send(embed=kullanıcı_var)

    else:
        await ctx.send(embed=kullancı_yok)

ödüller = ["1 Chunk", "20 Altın", "10 Altın", "5 Altın", "Bok", "1 Netherite", "10 Demir", "Öpücük"]
@Bot.command()
async def sandık(ctx):
    discord_id = ctx.message.author.id
    user = get_user_or_false(discord_id)
    if user:
        ödül = random.choice(ödüller)
        await ctx.send(f"Tebrikler '{ödül}' kazandın {ctx.message.author.mention}")
        channel = Bot.get_channel(962091943863668746)
        imlec.execute("SELECT * FROM kullanıcılar WHERE id='{}'".format(discord_id))
        for veri in imlec.fetchall():
            ad = veri[1]
            bakiye = veri[2]
        await channel.send(f"------------\nDc nick:{ctx.message.author.name}\nMc nick:{ad}\nKazandığı: {ödül}\n------------")



    else:
        kullancı_yok = discord.Embed(color=0xe74c3c)
        kullancı_yok.add_field(name="Kullanıcı Bulunamadı!", value="Böyle bir kullanıcı sisteme kayıtlı değil")
        await ctx.send(embed=kullancı_yok)


@Bot.command()
@commands.has_role("Yönetici")
async def bakiye_yükle(ctx, member: discord.Member, amount=0):
    discord_yol = ctx.message.mentions
    discord_id = member.id
    user = get_user_or_false(discord_id)
    if user:
        imlec.execute("SELECT * FROM kullanıcılar WHERE id='{}'".format(discord_id))
        for veri in imlec.fetchall():
            ad = veri[1]
            bakiye = veri[2]
            yeni_para = int(bakiye) + amount
            imlec.execute("UPDATE kullanıcılar SET money = '{}' WHERE id = '{}'".format(yeni_para, discord_id))
            bağlantı.commit()
            kullanıcı_var = discord.Embed(color=0x2ecc71)
            kullanıcı_var.add_field(name=f"**Bakiye Yüklendi!**",
                                    value=f"{emoji_3}**Kullanıcı**: {member.mention}\n{emoji}**Minecraft Adı**: {ad}\n{emoji_2}**Yeni Bakiyesi**: {yeni_para} Altın")
            await ctx.send(embed=kullanıcı_var)

    else:
        kullancı_yok = discord.Embed(color=0xe74c3c)
        kullancı_yok.add_field(name="Kullanıcı Bulunamadı!", value="Böyle bir kullanıcı sisteme kayıtlı değil")
        await ctx.send(embed=kullancı_yok)


@Bot.command()
@commands.has_role("Yönetici")
async def bakiye_çek(ctx, member: discord.Member, amount=0):
    discord_id = member.id
    user = get_user_or_false(discord_id)
    if user:
        imlec.execute("SELECT * FROM kullanıcılar WHERE id='{}'".format(discord_id))
        for veri in imlec.fetchall():
            ad = veri[1]
            bakiye = veri[2]
            if amount > int(bakiye):
                yetersiz_altın = discord.Embed(color=0xe74c3c)
                yetersiz_altın.add_field(name="**Yetersiz Altın!**", value=f"{emoji_3}**Kullanıcı**: {member.mention}\n{emoji}**Minecraft Adı**: {ad}\n{emoji_2}**Bakiyesi**: {bakiye} Altın")
                ihtiyaç = amount - int(bakiye)
                yetersiz_altın.set_footer(text=f"Talep edilen bakiyenin çekilmesi için kullanıcının {ihtiyaç} Altına ihtiyacı var")
                await ctx.send(embed=yetersiz_altın)

            else:
                yeni_para = int(bakiye) - amount
                çekildi = discord.Embed(color=0x2ecc71)
                çekildi.add_field(name="**Bakiye Çekildi!**",
                                         value=f"{emoji_3}**Kullanıcı**: {member.mention}\n{emoji}**Minecraft Adı**: {ad}\n{emoji_2}**Bakiyesi**: {yeni_para} Altın")
                imlec.execute("UPDATE kullanıcılar SET money = '{}' WHERE id = '{}'".format(yeni_para, discord_id))
                bağlantı.commit()
                await ctx.send(embed=çekildi)
    else:
        kullancı_yok = discord.Embed(color=0xe74c3c)
        kullancı_yok.add_field(name="Kullanıcı Bulunamadı!", value="Böyle bir kullanıcı sisteme kayıtlı değil")
        await ctx.send(embed=kullancı_yok)


@Bot.command()
async def play(ctx, amount=0):
    import random
    discord_id = ctx.message.author.id
    user = get_user_or_false(discord_id)
    if user:
        imlec.execute("SELECT * FROM kullanıcılar WHERE id='{}'".format(discord_id))
        for veri in imlec.fetchall():
            bakiye = veri[2]
            if amount > int(bakiye):
                await ctx.send(f"Bu kadar altının yok senin bakiyen: {bakiye} Altın.")
            else:
                if amount > 100:
                    fuck_para = int(bakiye) - amount
                    imlec.execute("UPDATE kullanıcılar SET money = '{}' WHERE id = '{}'".format(fuck_para, discord_id))
                    bağlantı.commit()
                    await ctx.send(f"Kazanamadın yeni bakiyen: {fuck_para} Altın")
                else:
                    ğ = randint(1, 100)
                    if ğ % 4 == 0:
                        yeni_para = int(bakiye) + amount
                        imlec.execute(
                            "UPDATE kullanıcılar SET money = '{}' WHERE id = '{}'".format(yeni_para, discord_id))
                        bağlantı.commit()
                        await ctx.send(f"Tebrikler 1x yaptın yeni bakiyen: {yeni_para} Altın")
                    elif ğ % 10 == 0:
                        xxpara = amount * 2
                        orta_para = int(bakiye) + int(xxpara)
                        imlec.execute(
                            "UPDATE kullanıcılar SET money = '{}' WHERE id = '{}'".format(orta_para, discord_id))
                        bağlantı.commit()
                        await ctx.send(f"Tebrikler 2x yaptın yeni bakiyen: {orta_para} Altın")
                    elif ğ == 31:
                        çok_para = amount * 10
                        sj_para = int(bakiye) + int(çok_para)
                        imlec.execute(
                            "UPDATE kullanıcılar SET money = '{}' WHERE id = '{}'".format(sj_para, discord_id))
                        bağlantı.commit()
                        await ctx.send(f"Tebrikler 10x yaptın yeni bakiyen: {sj_para} Altın")
                    else:
                        eksi_para = int(bakiye) - amount
                        imlec.execute(
                            "UPDATE kullanıcılar SET money = '{}' WHERE id = '{}'".format(eksi_para, discord_id))
                        bağlantı.commit()
                        await ctx.send(f"Kazanamadın yeni bakiyen: {eksi_para} Altın")
    else:
        kullancı_yok = discord.Embed(color=0xe74c3c)
        kullancı_yok.add_field(name="Kullanıcı Bulunamadı!", value="Böyle bir kullanıcı sisteme kayıtlı değil")
        await ctx.send(embed=kullancı_yok)


@Bot.command()
@commands.has_role("Yönetici")
async def clear(ctx, amount=0):
    await ctx.channel.purge(limit=amount)


@Bot.command()
@commands.has_role("Yönetici")
async def kick(ctx, member: discord.Member):
    reason = "yok"
    await member.kick(reason=reason)
    await ctx.send("Kullanıcı kicklendi")


@Bot.command()
@commands.has_role("Yönetici")
async def ban(ctx, member: discord.Member):
    reason = "yok"
    await member.ban(reason=reason)
    await ctx.send("Kullanıcı banlandı")


@Bot.command()
async def yönetici(msg):
    await msg.send("Adminlerin oyun içi nickleri: DupeBerke, DupeCrucial_, DupeKiitsu, LooKT")


@Bot.command()
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Slowmode {seconds} saniye olarak ayarlandı")


@Bot.command()
async def kullanıcısil(ctx, user):
    discord_yol = ctx.message.mentions
    discord_id = discord_yol[0].id
    user = get_user_or_false(discord_id)
    if user:
        imlec.execute("delete from kullanıcılar where id= '{}'".format(discord_id))
        bağlantı.commit()
        await ctx.send("Kullanıcı sistemden silindi.")

    else:
        await ctx.send("Sisteme böyle biri zaten kayıtlı değil.")


@Bot.command()
@commands.has_permissions(manage_roles=True, administrator=True)
async def rolekle(ctx, user: discord.Member, rol):
    role = discord.utils.get(ctx.guild.roles, name="{}".format(rol))
    await user.add_roles(role)


@Bot.command()
@commands.has_permissions(manage_roles=True, administrator=True)
async def rolkaldır(ctx, user: discord.Member, rol):
    role = discord.utils.get(ctx.guild.roles, name="{}".format(rol))
    print(user)
    await user.remove_roles(role)


roly = "Vip"
@Bot.command()
async def vipal(ctx):
    role = discord.utils.get(ctx.guild.roles, name="{}".format(roly))
    userr = ctx.message.author
    discord_id = ctx.message.author.id
    user = get_user_or_false(discord_id)
    if user:
        if role in userr.roles:
            await ctx.send("Zaten Vip'sin")
        else:
            imlec.execute("SELECT * FROM kullanıcılar WHERE id='{}'".format(discord_id))
            for veri in imlec.fetchall():
                bakiye = veri[2]
                if 32 > int(bakiye):
                    await ctx.send(f"Vip olman için 32 Altına ihtiyacın var senin Altının: {bakiye}")
                else:
                    await userr.add_roles(role)
                    yeni_bakiye = int(bakiye) - 32
                    imlec.execute(
                        "UPDATE kullanıcılar SET money = '{}' WHERE id = '{}'".format(yeni_bakiye, discord_id))
                    bağlantı.commit()
                    await ctx.send(f"Başarıyla vip oldun yeni bakiyen: {yeni_bakiye} Altın")
    else:
        await ctx.send("Vip olmak için önce Town'a kaydolmanız lazım.")

@Bot.command()
async def map(msg):
    await msg.send("https://map.adalances.com/towny2#world;flat;-33475,64,-14131;4")

@Bot.command()
async def help(ctx):
    user = ctx.message.author
    pfp = user.avatar_url
    embed = discord.Embed(title="  CODT Bot Komutları", color=0x2ecc71)
    embed.add_field(name=" Admin Komutları\n-----------------------",
                    value="**kayıt** = Kullanıcıyı kayıt eder\n**bakiye_yükle** = Kullanıcıya bakiye yükler\n**bakiye_çek** = Kullanıcın bakiyesini çeker\n**kullanıcısil** = Kullanıcıyı veritabanından siler\n**kick** = Kullanıcıyı kickler\n**ban** = Kullanıcı banlar\n**slowmode** = kanalın Slowmodeunu ayarlar\n**clear** = mesajları siler")
    embed.add_field(name=" Genel Komutlar\n-----------------------",
                    value="**bakiye** = Kullanıcının bakiyesini sorgular- örnek kullanım:\n!bakiye @Berke\n**play** = şans oyunu oynar- örnek kullanım:\n!play 10\n**vipal** = Vip rolü alırsnız (32 altına)\n**yönetici** = Yöneticilerin oyun içi nicklerini verir\n**map** = Mapin linkini verir")
    embed.set_footer(text=f"{user} tarafından istendi", icon_url=pfp)

    await ctx.send(embed=embed)







Bot.run("OTQxNDI1MjExNjgzNzcwNTEw.YgVwjQ.FFxBbqXf5G94dsBGiIB4RCDQxg8")
