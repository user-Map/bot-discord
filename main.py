# Thay thế phần async def main(): cũ bằng đoạn này

async def main():
    # Web server
    app = web.Application()
    app.router.add_post("/webhook/sepay", webhook_handler)
    app.router.add_get("/ping", lambda r: web.Response(text="pong"))  # Dùng để UptimeRobot ping

    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))          # Render dùng PORT = 10000
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"🚀 Web server đang chạy trên port {port}")

    # Chạy Discord bot
    await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
