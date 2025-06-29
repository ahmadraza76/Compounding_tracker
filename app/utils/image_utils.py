# app/utils/image_utils.py
from PIL import Image, ImageDraw, ImageFont
import io
import os
from app.utils.calculation_utils import calculate_progress
from app.config.constants import CURRENCY
from app.config.messages import MESSAGES
import logging

logger = logging.getLogger(__name__)

def get_font(size: int, bold: bool = False):
    """Get font with fallback to default."""
    try:
        if bold:
            font_path = os.path.join("assets", "fonts", "DejaVuSans-Bold.ttf")
        else:
            font_path = os.path.join("assets", "fonts", "DejaVuSans.ttf")
        
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
    except Exception as e:
        logger.warning(f"Could not load custom font: {e}")
    
    # Fallback to default font
    try:
        return ImageFont.load_default()
    except:
        # Ultimate fallback
        return ImageFont.load_default()

def draw_progress_bar(draw, x, y, width, height, progress, bg_color, fill_color):
    """Draw a progress bar."""
    try:
        # Background
        draw.rectangle([x, y, x + width, y + height], fill=bg_color, outline=(100, 100, 100))
        
        # Progress fill
        if progress > 0:
            fill_width = int(width * min(progress, 1.0))
            if fill_width > 0:
                draw.rectangle([x, y, x + fill_width, y + height], fill=fill_color)
        
        # Border
        draw.rectangle([x, y, x + width, y + height], outline=(150, 150, 150), width=2)
    except Exception as e:
        logger.error(f"Error drawing progress bar: {e}")

def generate_daily_profile_card(user_data: dict, progress_data: dict, profile_photo: bytes = None) -> bytes:
    """Generate enhanced Daily Profile Card with beautiful design."""
    try:
        width, height = 900, 700
        
        # Color scheme
        bg_gradient_start = (25, 25, 35)    # Dark blue-gray
        bg_gradient_end = (45, 45, 65)      # Lighter blue-gray
        card_bg = (255, 255, 255)           # White card background
        text_primary = (33, 37, 41)         # Dark text
        text_secondary = (108, 117, 125)    # Gray text
        accent_green = (40, 167, 69)        # Success green
        accent_red = (220, 53, 69)          # Danger red
        accent_yellow = (255, 193, 7)       # Warning yellow
        accent_blue = (0, 123, 255)         # Primary blue

        # Create image with gradient background
        image = Image.new("RGB", (width, height), bg_gradient_start)
        draw = ImageDraw.Draw(image)
        
        # Create gradient background
        for i in range(height):
            ratio = i / height
            r = int(bg_gradient_start[0] * (1 - ratio) + bg_gradient_end[0] * ratio)
            g = int(bg_gradient_start[1] * (1 - ratio) + bg_gradient_end[1] * ratio)
            b = int(bg_gradient_start[2] * (1 - ratio) + bg_gradient_end[2] * ratio)
            draw.line([(0, i), (width, i)], fill=(r, g, b))

        # Main card background with rounded corners effect
        card_margin = 30
        card_x = card_margin
        card_y = card_margin
        card_width = width - (2 * card_margin)
        card_height = height - (2 * card_margin)
        
        # Draw card shadow
        shadow_offset = 8
        draw.rectangle([card_x + shadow_offset, card_y + shadow_offset, 
                       card_x + card_width + shadow_offset, card_y + card_height + shadow_offset], 
                       fill=(0, 0, 0, 50))
        
        # Draw main card
        draw.rectangle([card_x, card_y, card_x + card_width, card_y + card_height], 
                       fill=card_bg, outline=(200, 200, 200), width=2)

        # Load fonts
        font_title = get_font(32, bold=True)
        font_large = get_font(24, bold=True)
        font_medium = get_font(20)
        font_small = get_font(16)
        font_tiny = get_font(14)

        # User data
        language = user_data.get("language", "en")
        name = user_data.get("name", "User")
        currency = user_data.get("currency", CURRENCY)

        # Check for errors from progress_data
        if progress_data.get("error"):
            # Simplified error card
            error_title_text = "Data Error" if language == "en" else "डेटा त्रुटि"
            error_message = progress_data["error"]

            # Error Title
            try:
                title_bbox = draw.textbbox((0, 0), error_title_text, font=font_title)
                title_width = title_bbox[2] - title_bbox[0]
                title_x_err = card_x + (card_width - title_width) / 2
                draw.text((title_x_err, card_y + 40), error_title_text, font=font_title, fill=accent_red)
            except:
                draw.text((card_x + 50, card_y + 40), error_title_text, font=font_title, fill=accent_red)

            # User Name
            name_text_err = f"User: {name}"
            try:
                name_bbox = draw.textbbox((0, 0), name_text_err, font=font_large)
                name_width = name_bbox[2] - name_bbox[0]
                name_x_err = card_x + (card_width - name_width) / 2
                draw.text((name_x_err, card_y + 100), name_text_err, font=font_large, fill=text_primary)
            except:
                draw.text((card_x + 50, card_y + 100), name_text_err, font=font_large, fill=text_primary)

            # Error Message
            error_lines = []
            max_chars_per_line = 50
            words = error_message.split()
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                try:
                    test_bbox = draw.textbbox((0, 0), test_line, font=font_medium)
                    test_width = test_bbox[2] - test_bbox[0]
                    if test_width <= card_width - 80:
                        current_line = test_line
                    else:
                        if current_line:
                            error_lines.append(current_line.strip())
                        current_line = word + " "
                except:
                    if len(current_line + word) <= max_chars_per_line:
                        current_line += word + " "
                    else:
                        if current_line:
                            error_lines.append(current_line.strip())
                        current_line = word + " "
            
            if current_line:
                error_lines.append(current_line.strip())

            err_y_offset = card_y + 160
            for line in error_lines:
                try:
                    line_bbox = draw.textbbox((0, 0), line, font=font_medium)
                    line_width = line_bbox[2] - line_bbox[0]
                    line_x_err = card_x + (card_width - line_width) / 2
                    draw.text((line_x_err, err_y_offset), line, font=font_medium, fill=accent_red)
                    err_y_offset += line_bbox[3] - line_bbox[1] + 5
                except:
                    draw.text((card_x + 50, err_y_offset), line, font=font_medium, fill=accent_red)
                    err_y_offset += 25

            # Footer
            footer_y_err = card_y + card_height - 40
            footer_text_err = "📊 Compounding Tracker Bot"
            try:
                footer_bbox = draw.textbbox((0, 0), footer_text_err, font=font_tiny)
                footer_width = footer_bbox[2] - footer_bbox[0]
                draw.text((card_x + (card_width - footer_width) // 2, footer_y_err),
                         footer_text_err, font=font_tiny, fill=text_secondary)
            except:
                draw.text((card_x + 50, footer_y_err), footer_text_err, font=font_tiny, fill=text_secondary)

            buffer = io.BytesIO()
            image.save(buffer, format="PNG", quality=95)
            buffer.seek(0)
            return buffer.getvalue()

        # Header section (if no error)
        header_y = card_y + 20
        
        # Profile photo section
        photo_size = 100
        photo_x = card_x + 30
        photo_y = header_y + 10
        
        if profile_photo:
            try:
                photo = Image.open(io.BytesIO(profile_photo)).resize((photo_size, photo_size))
                # Create circular mask
                mask = Image.new("L", (photo_size, photo_size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0, photo_size, photo_size), fill=255)
                
                # Apply mask
                photo = photo.convert("RGBA")
                photo.putalpha(mask)
                
                # Paste photo
                image.paste(photo, (photo_x, photo_y), photo)
                
                # Draw border around photo
                draw.ellipse([photo_x - 3, photo_y - 3, photo_x + photo_size + 3, photo_y + photo_size + 3], 
                            outline=accent_blue, width=4)
            except Exception as e:
                logger.warning(f"Error processing profile photo: {e}")
                # Default avatar
                draw.ellipse([photo_x, photo_y, photo_x + photo_size, photo_y + photo_size], 
                            fill=(150, 150, 150), outline=accent_blue, width=4)
                draw.text((photo_x + photo_size//2 - 10, photo_y + photo_size//2 - 15), "👤", 
                         font=get_font(30), fill=(255, 255, 255))
        else:
            # Default avatar
            draw.ellipse([photo_x, photo_y, photo_x + photo_size, photo_y + photo_size], 
                        fill=(150, 150, 150), outline=accent_blue, width=4)
            draw.text((photo_x + photo_size//2 - 10, photo_y + photo_size//2 - 15), "👤", 
                     font=get_font(30), fill=(255, 255, 255))

        # Title and name section
        title_x = photo_x + photo_size + 30
        title_y = header_y + 10
        
        title_text = MESSAGES[language]["profile_card_title"]
        draw.text((title_x, title_y), title_text, font=font_title, fill=accent_blue)
        
        name_y = title_y + 40
        draw.text((title_x, name_y), f"👤 {name}", font=font_large, fill=text_primary)

        # Main content area
        content_y = header_y + 140
        left_col_x = card_x + 30
        right_col_x = card_x + card_width // 2 + 20
        col_width = card_width // 2 - 50

        if user_data.get("target"):
            target = user_data["target"]
            
            # Left column - Target info
            y_offset = content_y
            
            # Day counter with highlight
            day_text = f"{MESSAGES[language]['day_label']} {progress_data['days_passed'] + 1}"
            day_bg_width = len(day_text) * 12 + 20
            draw.rectangle([left_col_x - 5, y_offset - 5, left_col_x + day_bg_width, y_offset + 25], 
                          fill=accent_blue, outline=accent_blue)
            draw.text((left_col_x, y_offset), day_text, font=font_medium, fill=(255, 255, 255))
            y_offset += 45

            # Target amount
            target_text = f"🎯 {MESSAGES[language]['target_label']}: {currency}{progress_data['target_amount_val']:,.2f}"
            draw.text((left_col_x, y_offset), target_text, font=font_medium, fill=text_primary)
            y_offset += 35

            # Start amount
            start_text = f"💰 {MESSAGES[language]['start_label']}: {currency}{progress_data['start_amount_val']:,.2f}"
            draw.text((left_col_x, y_offset), start_text, font=font_medium, fill=text_secondary)
            y_offset += 35

            # Rate and mode
            rate_text = f"📈 {MESSAGES[language]['rate_label']}: {target['rate']}% {target['mode']}"
            draw.text((left_col_x, y_offset), rate_text, font=font_medium, fill=text_secondary)
            y_offset += 50

            # Right column - Progress info
            y_offset = content_y

            # Expected balance
            expected_text = f"🎯 {MESSAGES[language]['expected_label']}: {currency}{progress_data['expected_balance']:,.2f}"
            draw.text((right_col_x, y_offset), expected_text, font=font_medium, fill=accent_blue)
            y_offset += 35

            # Current balance
            current_text = f"💼 {MESSAGES[language]['current_label']}: {currency}{progress_data['current_balance']:,.2f}"
            balance_color = accent_green if progress_data['current_balance'] >= progress_data['expected_balance'] else accent_red
            draw.text((right_col_x, y_offset), current_text, font=font_medium, fill=balance_color)
            y_offset += 35

            # Profit goal
            profit_text = f"💵 {MESSAGES[language]['profit_goal_label']}: {currency}{progress_data['today_profit_goal']:,.2f}"
            draw.text((right_col_x, y_offset), profit_text, font=font_medium, fill=text_secondary)
            y_offset += 35

            # Stop-loss
            if progress_data['stoploss_level']:
                stoploss_text = f"📉 {MESSAGES[language]['stoploss_label']}: {currency}{progress_data['stoploss_level']:,.2f}"
            else:
                stoploss_text = f"📉 {MESSAGES[language]['stoploss_label']}: {MESSAGES[language]['not_set']}"
            draw.text((right_col_x, y_offset), stoploss_text, font=font_medium, fill=text_secondary)
            y_offset += 50

            # Progress bar section
            progress_y = content_y + 200
            progress_label = f"{MESSAGES[language]['progress_label']}:"
            draw.text((left_col_x, progress_y), progress_label, font=font_medium, fill=text_primary)
            
            # Calculate progress percentage
            target_val = progress_data['target_amount_val']
            start_val = progress_data['start_amount_val']
            current_balance = progress_data['current_balance']
            
            if target_val > start_val:
                progress_percent = (current_balance - start_val) / (target_val - start_val)
            else:
                progress_percent = 0
            
            # Progress bar
            bar_y = progress_y + 30
            bar_width = card_width - 60
            bar_height = 25
            
            # Determine progress bar color
            if progress_percent >= 1.0:
                bar_color = accent_green
            elif progress_percent >= 0.7:
                bar_color = accent_blue
            elif progress_percent >= 0.3:
                bar_color = accent_yellow
            else:
                bar_color = accent_red
            
            draw_progress_bar(draw, left_col_x, bar_y, bar_width, bar_height, 
                             progress_percent, (240, 240, 240), bar_color)
            
            # Progress percentage text
            progress_text = f"{min(progress_percent * 100, 100):.1f}%"
            try:
                progress_bbox = draw.textbbox((0, 0), progress_text, font=font_small)
                text_width = progress_bbox[2] - progress_bbox[0]
                draw.text((left_col_x + bar_width - text_width, bar_y + bar_height + 10), 
                         progress_text, font=font_small, fill=text_primary)
            except:
                draw.text((left_col_x + bar_width - 50, bar_y + bar_height + 10), 
                         progress_text, font=font_small, fill=text_primary)

            # Status badge
            status_y = bar_y + bar_height + 40
            status_text = f"{MESSAGES[language]['status_label']}: {progress_data['status_badge']}"
            
            # Status background color
            if progress_data['status_badge'] == "🟢":
                status_bg = accent_green
            elif progress_data['status_badge'] == "🟡":
                status_bg = accent_yellow
            else:
                status_bg = accent_red
            
            status_width = len(status_text) * 10 + 20
            draw.rectangle([left_col_x - 5, status_y - 5, left_col_x + status_width, status_y + 25], 
                          fill=status_bg, outline=status_bg)
            draw.text((left_col_x, status_y), status_text, font=font_medium, fill=(255, 255, 255))

        else:
            # No target set
            no_target_y = content_y + 100
            no_target_text = MESSAGES[language]["no_target"]
            try:
                no_target_bbox = draw.textbbox((0, 0), no_target_text, font=font_large)
                text_width = no_target_bbox[2] - no_target_bbox[0]
                draw.text((card_x + (card_width - text_width) // 2, no_target_y), 
                         no_target_text, font=font_large, fill=accent_red)
            except:
                draw.text((card_x + 50, no_target_y), no_target_text, font=font_large, fill=accent_red)

        # Footer
        footer_y = card_y + card_height - 40
        footer_text = "📊 Compounding Tracker Bot"
        try:
            footer_bbox = draw.textbbox((0, 0), footer_text, font=font_tiny)
            text_width = footer_bbox[2] - footer_bbox[0]
            draw.text((card_x + (card_width - text_width) // 2, footer_y), 
                     footer_text, font=font_tiny, fill=text_secondary)
        except:
            draw.text((card_x + 50, footer_y), footer_text, font=font_tiny, fill=text_secondary)

        # Save to bytes
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", quality=95)
        buffer.seek(0)
        return buffer.getvalue()

    except Exception as e:
        logger.error(f"Error generating profile card: {e}")
        logger.error(f"Error details: {traceback.format_exc()}")
        raise e