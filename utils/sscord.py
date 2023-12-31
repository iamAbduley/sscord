import discord
import datetime
from io import BytesIO
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageChops

turkish_to_english = {
    "ç": "c", "ğ": "g", "ı": "i", "i": "i", "ö": "o", "ş": "s", "ü": "u",
    "Ç": "C", "Ğ": "G", "İ": "I", "I": "I", "Ö": "O", "Ş": "S", "Ü": "U"
}

FONT_REGULAR_BIG = ImageFont.truetype("./fonts/gibson-regular.otf", 22)
FONT_MESSAGE = ImageFont.truetype("./fonts/Almarai-Light.ttf", 22)
FONT_SMALL = ImageFont.truetype(f"./fonts/Almarai-Bold.ttf", 15)

class SSCORD:
    def __init__(self, user: discord.Member, message: discord.Message):
        self.user = user
        self.message = message
        self.content = message.content

    def format_datetime(self, time: datetime.datetime):
        TURKIYE_ISTANBUL = ZoneInfo("Europe/Istanbul")

        if (time.day == datetime.datetime.now().day) and (time.month == datetime.datetime.now().month):
            time = time.astimezone(tz = TURKIYE_ISTANBUL)
            clock = time.strftime('%H:%M')
            return f"Today at {clock}"
        return time.strftime("%d/%m/%Y %H:%M")


    # Circle User Avatar
    def circle(self, pfp, size = (215,215)):
        pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")

        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill = 255)
        mask = mask.resize(pfp.size, Image.LANCZOS)
        mask = ImageChops.darker(mask, pfp.split()[-1])
        pfp.putalpha(mask)

        return pfp


    # Split text every 37 chars
    def format_text(self) -> str:
        # Split text every 37 chars
        result = '\n'.join(line.strip() for line in [self.content[i:i+37] for i in range(0, len(self.content), 37)])
        # Replace english chars instead of turkish chars
        result = ''.join(turkish_to_english.get(char, char) for char in result)

        return result
    
    # Row count in the text
    @property
    def row_count(self):
        return self.format_text().count('\n')

    # Create background
    def background(self):
        height = 300 + (10 * self.row_count) if self.row_count > 1 else 300 # Image height according to row count
        width = 500

        img = Image.new("RGBA", (width, height), "#313338")
        return img

    # Paste avatar, write texts ... (main)
    async def draw(self):
        img = self.background()
        draw = ImageDraw.Draw(img)

        # Username
        username = self.user.name

        username_len = draw.textlength(username, FONT_REGULAR_BIG)
        draw.text((93, 29), username, "#ffffff", FONT_REGULAR_BIG)
        
        # Time
        time = self.format_datetime(self.message.created_at)
        draw.text(((username_len + 105), 34), str(time), "#8f8f8f", FONT_SMALL)

        # Avatar
        pfp = self.user.avatar.replace(size = 256)
        data = BytesIO(await pfp.read())
        user_avatar = Image.open(data).convert("RGBA")

        user_avatar = self.circle(user_avatar,size = (213, 213))
        user_avatar = user_avatar.resize((51, 51), Image.LANCZOS)
        
        img.paste(user_avatar, (21, 24), user_avatar)

        # Message Content
        draw.text((93, 56), self.format_text(), "#ffffff", FONT_MESSAGE)

        return img
