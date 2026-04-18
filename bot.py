import discord
import asyncio
import os

# ✅ LẤY TOKEN TỪ ENV (Render)
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ Thiếu TOKEN trong Environment (Render)")

CHANNEL_LIST = [
    "𝙉𝙪𝙠𝙚-𝘽𝙮-𝙉𝙜𝙪𝙮ễ𝙣𝙆𝙝ô𝙞",
]

PREFIX = ">"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

client = discord.Client(intents=intents)
nuke_running = {}


@client.event
async def on_ready():
    print(f"✅ Bot online: {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if not message.content.startswith(PREFIX):
        return

    args = message.content[len(PREFIX):].strip().lower().split()
    command = args[0] if args else ""

    if command == "usermap":
        await run_usermap(message)
    elif command == "stop":
        await run_stop(message)
    elif command == "help":
        await run_help(message)
    elif command == "src":
        await run_src(message)


async def run_help(message):
    embed = discord.Embed(
        title="💣  N U K E",
        color=0xFF0000
    )
    embed.add_field(
        name="` >usermap `",
        value="╰ 🔴 Nuke Server",
        inline=False
    )
    embed.add_field(
        name="` >stop `",
        value="╰ 🟢 Stop Nuke",
        inline=False
    )
    embed.add_field(
        name="` >src `",
        value="╰ 📄 Lấy source code bot",
        inline=False
    )
    embed.add_field(
        name="⚠️",
        value="```Cần Quyền Để NuKe```",
        inline=False
    )
    embed.set_footer(text="by Nguyễn Khôi")
    await message.channel.send(embed=embed)


async def run_src(message):
    file_path = os.path.abspath(__file__)
    await message.channel.send(
        content="📄 **Source code bot:**",
        file=discord.File(file_path, filename="bot.py")
    )


async def run_usermap(message):
    guild = message.guild
    if not guild:
        return

    member = guild.get_member(message.author.id)
    if not member or not member.guild_permissions.manage_channels:
        await message.reply("❌ Bạn cần quyền **Quản lý Kênh** để dùng lệnh này.")
        return

    if nuke_running.get(guild.id):
        await message.reply("⚠️ Bot đang chạy rồi! Gõ `>stop` để dừng.")
        return

    nuke_running[guild.id] = True

    status_msg = await message.channel.send(
        "🔁 Bắt đầu tạo kênh liên tục...\nGõ `>stop` để dừng."
    )

    try:
        await guild.edit(name=CHANNEL_LIST[0])
    except Exception:
        pass

    count = 0

    while nuke_running.get(guild.id):
        for name in CHANNEL_LIST:
            if not nuke_running.get(guild.id):
                break
            try:
                await guild.create_text_channel(name)
                count += 1
                if count % 10 == 0:
                    try:
                        await status_msg.edit(content=f"🔁 Đã tạo **{count}** kênh\nGõ `>stop` để dừng.")
                    except Exception:
                        pass
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = float(e.response.headers.get("Retry-After", 1))
                    await asyncio.sleep(retry_after + 0.1)
                else:
                    await asyncio.sleep(0.5)
            await asyncio.sleep(0.05)

    try:
        await status_msg.edit(content=f"🛑 Đã dừng! Tổng cộng đã tạo **{count}** kênh.")
    except Exception:
        pass


async def run_stop(message):
    guild = message.guild
    if not guild:
        return

    if not nuke_running.get(guild.id):
        await message.reply("⚠️ Bot không đang chạy.")
        return

    nuke_running[guild.id] = False
    await message.reply("🛑 Đã dừng!")


client.run(TOKEN)
