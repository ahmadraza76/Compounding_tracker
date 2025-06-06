# app/utils/image_utils.py
from PIL import Image, ImageDraw, ImageFont
import io
from app.utils.calculation_utils import calculate_progress
from app.config.constants import CURRENCY

def generate_daily_profile_card(user_data: dict, profile_photo: bytes = None) -> bytes:
    """Generate Daily Profile Card as bytes."""
    width, height = 800, 600
    background_color = (30, 30, 30)  # Dark gray
    text_color = (255, 255, 255)     # White
    accent_color = (0, 200, 0)       # Green

    # Create blank image
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Load font
    try:
        font_path = "assets/fonts/DejaVuSans.ttf"
        font_large = ImageFont.truetype(font_path, 40)
        font_medium = ImageFont.truetype(font_path, 30)
        font_small = ImageFont.truetype(font_path, 20)
    except IOError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # User data
    language = user_data.get("language", "en")
    name = user_data.get("name", "User")
    currency = user_data.get("currency", CURRENCY)
    progress = calculate_progress(user_data)

    # Draw profile photo or default avatar
    photo_size = 150
    if profile_photo:
        try:
            photo = Image.open(io.BytesIO(profile_photo)).resize((photo_size, photo_size))
            mask = Image.new("L", (photo_size, photo_size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, photo_size, photo_size), fill=255)
            photo = photo.convert("RGBA")
            photo.putalpha(mask)
            image.paste(photo, (50, 50), photo)
        except Exception:
            draw.ellipse((50, 50, 50 + photo_size, 50 + photo_size), fill=(100, 100, 100))
    else:
        draw.ellipse((50, 50, 50 + photo_size, 50 + photo_size), fill=(100, 100, 100))

    # Draw text
    y_offset = 50
    draw.text((250, y_offset), f"{'Daily Profile' if language == 'en' else 'दैनिक प्रोफाइल'}", font=font_large, fill=text_color)
    y_offset += 60
    draw.text((250, y_offset), f"{'Name' if language == 'en' else 'नाम'}: {name}", font=font_medium, fill=text_color)
    y_offset += 50

    if user_data.get("target"):
        target = user_data["target"]
        draw.text((50, y_offset), f"{'Day' if language == 'en' else 'दिन'}: {progress['days_passed'] + 1}", font=font_small, fill=text_color)
        y_offset += 30
        draw.text((50, y_offset), f"{'Target' if language == 'en' else 'लक्ष्य'}: {currency}{float(target['target_amount']):,.2f}", font=font_small, fill=text_color)
        y_offset += 30
        draw.text((50, y_offset), f"{'Start' if language == 'en' else 'शुरुआत'}: {currency}{float(target['start_amount']):,.2f}", font=font_small, fill=text_color)
        y_offset += 30
        draw.text((50, y_offset), f"{'Rate' if language == 'en' else 'दर'}: {target['rate']}% {'per' if language == 'en' else 'प्रति'} {target['mode']}", font=font_small, fill=text_color)
        y_offset += 30
        draw.text((50, y_offset), f"{'Today\'s Target' if language == 'en' else 'आज का लक्ष्य'}: {currency}{progress['expected_balance']:,.2f}", font=font_small, fill=text_color)
        y_offset += 30
        draw.text((50, y_offset), f"{'Profit Goal' if language == 'en' else 'लाभ लक्ष्य'}: {currency}{progress['today_profit_goal']:,.2f}", font=font_small, fill=text_color)
        y_offset += 30
        stoploss_text = f"{progress['stoploss_level']:,.2f}" if progress['stoploss_level'] else ('Not set' if language == 'en' else 'सेट नहीं')
        draw.text((50, y_offset), f"{'Stop Loss' if language == 'en' else 'स्टॉप लॉस'}: {currency}{stoploss_text}", font=font_small, fill=text_color)
        y_offset += 30
        draw.text((50, y_offset), f"{'Balance' if language == 'en' else 'बैलेंस'}: {currency}{progress['current_balance']:,.2f}", font=font_small, fill=text_color)
        y_offset += 30
        draw.text((50, y_offset), f"{'Status' if language == 'en' else 'स्थिति'}: {progress['status_badge']}", font=font_small, fill=accent_color)
    else:
        draw.text((50, y_offset), f"{'No target set' if language == 'en' else 'कोई लक्ष्य सेट नहीं'}", font=font_small, fill=text_color)

    # Save to bytes
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()
