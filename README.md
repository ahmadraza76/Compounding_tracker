# 🚀 Compounding Tracker Telegram Bot

A powerful, feature-rich Telegram bot for tracking financial compounding progress with advanced analytics, beautiful visualizations, and comprehensive multi-language support.

## ✨ Features

### 🎯 Core Functionality
- **Smart Target Setting**: Set compounding goals with custom rates and modes
- **Daily Balance Tracking**: Easy balance recording with progress monitoring
- **Visual Progress Cards**: Beautiful profile cards with user photos and progress bars
- **Stop-Loss Protection**: Automatic alerts when balance drops below thresholds
- **Excel Export**: Comprehensive progress reports in Excel format

### 🎨 Advanced UI/UX
- **Beautiful Profile Cards**: Professional-looking cards with gradients and progress bars
- **Multi-language Support**: Complete Hindi and English translations
- **Interactive Settings**: Inline keyboard for easy configuration
- **Status Indicators**: Color-coded progress badges (🟢🟡🔴)
- **Rich Formatting**: Emojis, bold text, and proper spacing throughout

### 🔧 Smart Features
- **Daily Reminders**: Scheduled notifications at 8 PM IST
- **Compounding Calculations**: Support for daily and monthly compounding
- **Data Security**: Thread-safe JSON storage with backup protection
- **Error Handling**: Comprehensive error management and logging
- **Owner Controls**: Broadcast messaging for bot administrators

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Telegram Bot Token from [@BotFather](https://t.me/botfather)

### Local Development

1. **Clone and Setup**:
```bash
git clone <your-repo-url>
cd Compounding_tracker
pip install -r requirements.txt
```

2. **Configure Environment**:
```bash
cp .env.example .env
# Edit .env with your bot token
```

3. **Update Owner ID** in `app/config/constants.py`:
```python
OWNER_ID = "your_telegram_user_id"
```

4. **Run the Bot**:
```bash
python -m app.main
```

## 🌐 Render Deployment

### One-Click Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment

1. **Fork this repository** to your GitHub account

2. **Create a new Web Service** on [Render](https://render.com):
   - Connect your GitHub repository
   - Choose "Python" environment
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m app.main`

3. **Set Environment Variables**:
   - `TELEGRAM_BOT_TOKEN`: Your bot token from BotFather

4. **Deploy**: Click "Create Web Service"

### Render Configuration Files
- `render.yaml`: Service configuration
- `Procfile`: Process definition
- `runtime.txt`: Python version specification
- `requirements.txt`: Dependencies

## 📱 Bot Commands

### User Commands
- `/start` - Initialize bot with welcome card
- `/target` - Set compounding goal
- `/close` - Record daily balance
- `/status` - View progress with visual card
- `/settings` - Access all bot settings
- `/export` - Download Excel report
- `/language` - Switch Hindi/English
- `/help` - Complete command guide
- `/reset` - Reset all data

### Admin Commands (Owner Only)
- `/broadcast` - Send message to all users

## 🎯 Usage Examples

### Setting a Target
```
/target
1500, 10000, 5, daily
```
- Start: ₹1,500
- Target: ₹10,000
- Rate: 5% daily
- Mode: Daily compounding

### Recording Balance
```
/close
1650.50
```

### Viewing Progress
```
/status
```
Shows beautiful progress card with:
- Profile photo
- Progress bars
- Status indicators
- Detailed metrics

## 🏗️ Project Structure

```
Compounding_tracker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main application
│   ├── config/
│   │   ├── constants.py        # Configuration
│   │   └── messages.py         # Multi-language messages
│   ├── handlers/               # Command handlers
│   │   ├── start_handler.py
│   │   ├── target_handler.py
│   │   ├── status_handler.py
│   │   ├── settings_handler.py
│   │   └── ...
│   ├── conversations/          # Conversation flows
│   │   ├── target_conversation.py
│   │   ├── close_conversation.py
│   │   └── ...
│   └── utils/                  # Utility functions
│       ├── data_utils.py       # Data management
│       ├── image_utils.py      # Image generation
│       ├── calculation_utils.py # Math functions
│       └── ...
├── assets/
│   └── fonts/                  # Font files
├── requirements.txt            # Dependencies
├── render.yaml                 # Render config
├── Procfile                    # Process definition
├── runtime.txt                 # Python version
└── README.md                   # This file
```

## 🎨 Visual Features

### Profile Cards
- **Gradient Backgrounds**: Beautiful color transitions
- **Circular Profile Photos**: User avatars with borders
- **Progress Bars**: Visual representation of goal completion
- **Status Badges**: Color-coded indicators
- **Professional Layout**: Clean, modern design

### Multi-language Support
- **Complete Translations**: All text in Hindi and English
- **Unicode Support**: Proper rendering of Hindi text
- **Language Switching**: Easy toggle between languages
- **Localized Formatting**: Currency and number formatting

## 🔧 Configuration

### Environment Variables
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### Constants (app/config/constants.py)
```python
OWNER_ID = "your_telegram_user_id"
CURRENCY = "₹"
REMINDER_HOUR = 20  # 8 PM IST
```

## 📊 Features in Detail

### Compounding Calculations
- **Daily Mode**: Compounds daily with annual rate
- **Monthly Mode**: Compounds monthly with annual rate
- **Progress Tracking**: Real-time vs expected balance
- **Profit Goals**: Daily profit targets

### Data Management
- **Thread-Safe Storage**: Concurrent access protection
- **Backup System**: Automatic backup of corrupted files
- **Error Recovery**: Graceful handling of data issues
- **Export Functionality**: Excel reports with charts

### Security Features
- **Owner Verification**: Admin commands restricted
- **Input Validation**: Comprehensive data validation
- **Error Logging**: Detailed error tracking
- **Safe Defaults**: Fallback values for all settings

## 🐛 Troubleshooting

### Common Issues

1. **Bot Not Responding**:
   - Check TELEGRAM_BOT_TOKEN is correct
   - Verify bot is started with /start command

2. **Profile Photos Not Loading**:
   - Check bot has permission to access user photos
   - Verify network connectivity

3. **Reminders Not Working**:
   - Check timezone settings
   - Verify scheduler is running

4. **Data Loss**:
   - Check user_data.json file exists
   - Look for .backup files

### Logs
Check application logs for detailed error information:
```bash
# Local development
python -m app.main

# Render deployment
Check Render dashboard logs
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/Compounding_tracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/Compounding_tracker/discussions)
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [Pillow](https://pillow.readthedocs.io/) - Image processing
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel file generation
- [APScheduler](https://apscheduler.readthedocs.io/) - Task scheduling

## ⚠️ Disclaimer

This bot is for educational and tracking purposes only. It does not provide financial advice. Always consult with financial professionals for investment decisions.

---

Made with ❤️ for the trading community