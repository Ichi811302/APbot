from flask.sansio.scaffold import T_url_value_preprocessor
from keep_alive import keep_alive

keep_alive()
import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を取得するため必要
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

#ユーザー別記録
user_stats = {}


@bot.event
async def on_ready():
    print(f"ログイン完了: {bot.user}")


@bot.event
async def on_ready():
    bot.active = True
    print(f"ログインおけ: {bot.user}")


@bot.event
async def on_message(message):
    if hasattr(bot, 'active') and not bot.active:
        if message.content.startswith("!開始"):
            await bot.process_commands(message)
        return

    if message.author == bot.user:
        return

    # Bot自身のメッセージには反応しない
    if message.author == bot.user:
        return

    targets = ["○", "×", "❌"]
    content = message.content.strip()

    #カウント
    if content in targets:
        user_id = message.author.id
        if user_id not in user_stats:
            user_stats[user_id] = {"○": 0, "×": 0, "❌": 0, "log": []}

        user_stats[user_id][content] += 1
        user_stats[user_id]["log"].append(content)

        #await message.channel.send(f"{message.author.display_name}:入力を受け付けました。"
        await message.add_reaction("🤡")

    await bot.process_commands(message)

    if "🤡" in message.content:
        await message.channel.send(f"🫷🤡🫸 💣{message.author.display_name}💣🫷🤡🫸")

    if "folern" in message.content:
        await message.channel.send(
            f"ｺﾝｽｨｰﾔwwﾚｯwﾄｩwwﾊwﾘｰwwﾃﾞｨwwwｲwﾃﾞｨwwkﾄwｴwﾗwwwｺｰｽﾞｨﾝwwwﾊﾟwwwﾃﾞｨwwｱwﾒｲwwwﾃﾞｨwwｼｭ↑wｶﾞｰwｺﾝﾌﾙｰｧwwwwﾚｯwwﾃｨwwwﾊwﾒｲｯwwwﾃｨwwwﾙｰﾝwwwﾔwwﾒwﾃﾞｨwｸﾗｷﾓwwwｲﾝwwﾅﾅｧ↑wwｲwwﾄwｷｨｨ↑↑ww"
        )

    if "theEmperror" in message.content:
        await message.channel.send(
            f"MY醤油PayPay二元論\nMY Defense ｽｳｨﾝｽｳｨﾝ グッバイｾｯ\nI 世間 天然 二元論")

    if "conflict" in message.content:
        await message.channel.send(
            f"ズォールヒ～～↑ｗｗｗｗヴィヤーンタースｗｗｗｗｗワース フェスツｗｗｗｗｗｗｗルオルｗｗｗｗｗプローイユクｗｗｗｗｗｗｗダルフェ スォーイヴォーｗｗｗｗｗスウェンネｗｗｗｗヤットゥ ヴ ヒェンヴガｒジョｊゴアｊガ オガオッガｗｗｗじゃｇｊｊ"
        )


@bot.command()
async def 集計(ctx):
    if not user_stats:
        await ctx.send("まだ0回ですよ🤡")
        return

    msg = "集計"
    perfect_game = []
    for user_id, stats in user_stats.items():
        member = ctx.guild.get_member(user_id)
        name = member.display_name if member else f"不明なユーザー"
        total = sum(v for k, v in stats.items() if k != "log")
        success = stats["○"]
        fail = stats["×"]
        fly = stats["❌"]
        success_rate = (success / total * 100) if total > 0 else 0
        msg += (f"\n-------------------------\n"
                f"{name}\n"
                f"回数: {total}回\n"
                f"AP: {success}回\n"
                f"ミス: {fail}回\n"
                f"飛び: {fly}回\n"
                f"勝率: {success_rate:.1f}%")

        if total > 0 and success_rate == 100:
            perfect_game.append(name)

    await ctx.send(msg)

    if perfect_game:
        names = "、".join(perfect_game)
        await ctx.send(f"🌈🌈{names}PG!!!🌈🌈")


@bot.command()
async def Reset(ctx):
    user_stats.clear()
    await ctx.send("回数リセットしました。")


@bot.command()
async def 開始(ctx):
    bot.active = True
    await ctx.send("こんにちはぁ🫲🤡🫱")


@bot.command()
async def 履歴(ctx):
    if not user_stats:
        await ctx.send("まだ0回ですよ🤡")
        return

    msg = "-------履歴-------\n"
    for user_id, stats in user_stats.items():
        member = ctx.guild.get_member(user_id)
        name = member.display_name if member else f"不明なユーザー"
        log_str = "".join(stats.get("log", []))
        msg += f"\n{name}：{log_str if log_str else '（まだなし）'}"

    await ctx.send(msg)


@bot.command()
async def 終わり(ctx):
    await ctx.send("ばいばい🫶🤡🫶(←腕四本あってえぐい)")
    bot.active = False


@bot.command()
async def ジョージ(ctx):
    await ctx.send(file=discord.File("hello.mov"))


bot.run(TOKEN)
