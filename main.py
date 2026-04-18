import discord
from discord import app_commands
import aiohttp
import asyncio
import os
import uuid
from dotenv import load_dotenv
from aiohttp import web

load_dotenv()

intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Thông tin BIDV của bạn (thay bằng thông tin thật)
BANK_CODE = "BIDV"
ACCOUNT_NUMBER = "8818603303"   # Số tài khoản BIDV
ACCOUNT_NAME = "Huỳnh"

CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot {bot.user} đã online!")

# Lệnh tạo QR
@tree.command(name="qr", description="Tạo QR thanh toán")
@app_commands.describe(amount="Số tiền cần thanh toán (ví dụ: 40000)")
async def qr_command(interaction: discord.Interaction, amount: int):
    if amount < 1000:
        await interaction.response.send_message("❌ Số tiền tối thiểu là 1.000đ!", ephemeral=True)
        return

    order_code = f"DH{uuid.uuid4().hex[:10].upper()}"   # Mã đơn hàng duy nhất

    # Tạo link QR động (không cần API Key)
    qr_url = f"https://qr.sepay.vn/img?acc={ACCOUNT_NUMBER}&bank={BANK_CODE}&amount={amount}&des={order_code}&template=compact"

    embed = discord.Embed(title="💰 Yêu cầu thanh toán", color=0x00ff88)
    embed.add_field(name="Số tiền", value=f"**{amount:,} VNĐ**", inline=False)
    embed.add_field(name="Nội dung chuyển khoản", value=f"`{order_code}`", inline=False)
    embed.add_field(name="Hướng dẫn", value="Quét QR và chuyển khoản **đúng nội dung** ở trên.", inline=False)
    embed.set_image(url=qr_url)
    embed.set_footer(text="Bot sẽ tự thông báo khi thanh toán thành công.")

    await interaction.response.send_message(embed=embed)

# ==================== WEBHOOK NHẬN TỪ SEPAY ====================
async def webhook_handler(request):
    try:
        data = await request.json()

        if data.get("transferType") != "in":
            return web.Response(text="OK", status=200)

        amount = int(data.get("transferAmount", 0))
        content = data.get("content", "").strip()
        sender = data.get("accountName", "Người lạ")

        # Chỉ xử lý nếu nội dung bắt đầu bằng DH (mã do bot tạo)
        if content.startswith("DH") and CHANNEL_ID:
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                success = discord.Embed(title="✅ Thanh toán thành công!", color=0x00ff00)
                success.add_field(name="Số tiền", value=f"{amount:,} VNĐ", inline=True)
                success.add_field(name="Người chuyển", value=sender, inline=True)
                success.add_field(name="Nội dung", value=content, inline=False)
                success.add_field(name="Thời gian", value=data.get("transactionDate", "Ngay bây giờ"), inline=False)

                await channel.send(embed=success)

        return web.Response(text="OK", status=200)
    except Exception as e:
        print("Webhook lỗi:", e)
        return web.Response(text="Error", status=200)

# Chạy cả bot + web server
async def main():
    # Web server
    app = web.Application()
    app.router.add_post("/webhook/sepay", webhook_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()

    # Chạy Discord bot
    await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
