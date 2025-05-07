import discord
from keep_alive import keep_alive
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests, io, os, json, asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
COUNTER_FILE = 'counter.json'
BACKGROUND_IMAGE = 'background.png'
FONT_PATH = 'arial.ttf'

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, 'w') as f:
        json.dump({"count": 1}, f)

def get_counter():
    with open(COUNTER_FILE, 'r') as f:
        return json.load(f)

def increment_counter():
    data = get_counter()
    data['count'] += 1
    with open(COUNTER_FILE, 'w') as f:
        json.dump(data, f)
    return data['count']

def draw_centered_text(draw, text, font, y, image_width, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (image_width - text_width) // 2
    draw.text((x, y), text, font=font, fill=color)

def create_welcome_image(username, avatar_url):
    bg = Image.open(BACKGROUND_IMAGE).convert("RGBA")
    image_width, image_height = bg.size

    response = requests.get(avatar_url)
    avatar_size = 370
    avatar = Image.open(io.BytesIO(response.content)).convert("RGBA").resize((avatar_size, avatar_size))

    # ماسك دائري
    mask = Image.new("L", (avatar_size, avatar_size), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, avatar_size, avatar_size), fill=255)
    avatar.putalpha(mask)

    # تموضع الصورة بدقة
    avatar_x = 214
    avatar_y = 312
    bg.paste(avatar, (avatar_x, avatar_y), avatar)

    # الاسم فقط داخل الصورة
    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype(FONT_PATH, 36)
    draw_centered_text(draw, username, font, avatar_y + avatar_size + 10, image_width, (255, 255, 255))

    return bg

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

invite_cache = {}

@bot.event
async def on_ready():
    global invite_cache
    for guild in bot.guilds:
        try:
            invite_cache[guild.id] = await guild.invites()
        except:
            invite_cache[guild.id] = []
    print(f"✅ Logged in as {bot.user.name}")
    bot.loop.create_task(handle_dashboard_commands())

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    count = increment_counter()
    avatar_url = member.display_avatar.url

    # محاولة معرفة من اللي دعاه
    inviter = None
    try:
        invites_before = invite_cache.get(member.guild.id, [])
        invites_after = await member.guild.invites()
        for invite in invites_after:
            for old_invite in invites_before:
                if invite.code == old_invite.code and invite.uses > old_invite.uses:
                    inviter = invite.inviter
                    break
        invite_cache[member.guild.id] = invites_after
    except:
        inviter = None

    image = create_welcome_image(member.display_name, avatar_url)

    with io.BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        file = discord.File(fp=image_binary, filename='welcome.png')

        mention_line = f"wlc : {member.mention}"
        by_line = f"by  : {inviter.mention if inviter else 'unknown'}"
        count_line = f"أنت العضو رقم {count} في السيرفر!"

        await channel.send(content=f"{mention_line}\n{by_line}", file=file)
        await channel.send(content=count_line)

# المهمة الخاصة بقراءة أوامر الداشبورد
async def handle_dashboard_commands():
    while True:
        await asyncio.sleep(2)
        command_file = "commands/clear_request.json"
        if os.path.exists(command_file):
            with open(command_file, 'r') as f:
                data = json.load(f)
            os.remove(command_file)

            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.purge(limit=data.get("amount", 5))
                print(f"🧹 Deleted {data['amount']} messages by dashboard")

keep_alive()
bot.run(TOKEN)
