import {
  Client,
  GatewayIntentBits,
  ChannelType,
  PermissionFlagsBits,
  type Message,
  type TextChannel,
} from "discord.js";

// =============================================
// ĐẶT TOKEN BOT CỦA BẠN VÀO ĐÂY
const TOKEN = "TOKEN_CỦA_BẠN_Ở_ĐÂY";
// =============================================

const PREFIX = ">";

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

// =============================================
// DANH SÁCH KÊNH SẼ ĐƯỢC TẠO
const CHANNEL_LIST: string[] = [
  "𝙉𝙪𝙠𝙚-𝘽𝙮-𝙉𝙜𝙪𝙮ễ𝙣𝙆𝙝ô𝙞",
];
// =============================================

const nukeState = new Map<string, boolean>();

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function runUsermap(message: Message) {
  const guild = message.guild;
  if (!guild) return;

  const member = await guild.members.fetch(message.author.id).catch(() => null);
  if (!member?.permissions.has(PermissionFlagsBits.ManageChannels)) {
    await message.reply("❌ Bạn cần quyền **Quản lý Kênh** để dùng lệnh này.");
    return;
  }

  if (nukeState.get(guild.id)) {
    await message.reply("⚠️ Bot đang chạy rồi! Gõ `>stop nuke` để dừng.");
    return;
  }

  nukeState.set(guild.id, true);

  const statusMsg = await (message.channel as TextChannel).send(
    `🔁 Bắt đầu tạo kênh liên tục...\nGõ \`>stop nuke\` để dừng.`,
  );

  let count = 0;

  while (nukeState.get(guild.id)) {
    for (const name of CHANNEL_LIST) {
      if (!nukeState.get(guild.id)) break;
      try {
        await guild.channels.create({
          name,
          type: ChannelType.GuildText,
        });
        count++;
        if (count % 10 === 0) {
          await statusMsg.edit(
            `🔁 Đang tạo kênh... Đã tạo **${count}** kênh\nGõ \`>stop nuke\` để dừng.`,
          ).catch(() => {});
        }
      } catch (err: any) {
        if (err?.status === 429 || err?.httpStatus === 429) {
          const retryAfter = (err?.retryAfter ?? 1) * 1000;
          await sleep(retryAfter + 100);
        } else {
          await sleep(500);
        }
      }
      await sleep(50);
    }
  }

  await statusMsg.edit(
    `🛑 Đã dừng! Tổng cộng đã tạo **${count}** kênh.`,
  );
}

async function runStopNuke(message: Message) {
  const guild = message.guild;
  if (!guild) return;

  if (!nukeState.get(guild.id)) {
    await message.reply("⚠️ Bot không đang chạy.");
    return;
  }

  nukeState.set(guild.id, false);
  await message.reply("🛑 Đã ra lệnh dừng! Bot sẽ dừng sau khi hoàn thành kênh hiện tại.");
}

async function runHelp(message: Message) {
  await message.reply(
    `**🤖 Hướng dẫn sử dụng Bot**\n\n` +
    `\`>usermap\` — Tạo kênh liên tục cho đến khi dừng\n` +
    `\`>stop nuke\` — Dừng việc tạo kênh\n` +
    `\`>help\` — Hiện hướng dẫn này`,
  );
}

client.once("clientReady", () => {
  console.log(`✅ Bot online: ${client.user?.tag}`);
});

client.on("messageCreate", async (message) => {
  if (message.author.bot) return;
  if (!message.content.startsWith(PREFIX)) return;

  const content = message.content.slice(PREFIX.length).trim().toLowerCase();
  const args = content.split(/\s+/);
  const command = args[0];

  try {
    if (command === "usermap") {
      await runUsermap(message);
    } else if (command === "stop" && args[1] === "nuke") {
      await runStopNuke(message);
    } else if (command === "help") {
      await runHelp(message);
    }
  } catch (err) {
    await message.reply("❌ Đã xảy ra lỗi.").catch(() => {});
  }
});

client.login(TOKEN);
