import sqlite3
import discord
from discord.ext import commands

with sqlite3.connect("discordmain.db") as bağlantı:
    imlec = bağlantı.cursor()

    imlec.execute("CREATE TABLE IF NOT EXISTS kullanıcılar(id INT,mcad TEXT,money INT)")


    # imlec.execute("INSERT INTO kullanıcılar VALUES('{}','{}','{}')".format(id,ad,para))

    def get_user_or_false(discord_id):
        users = imlec.execute("SELECT * from kullanıcılar")
        for user in users:
            if discord_id in user:
                return user

        return False



bağlantı.commit()
