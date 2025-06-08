# Compounding Tracker Telegram Bot

A powerful Telegram bot for tracking financial compounding progress with advanced features like stop-loss alerts, daily reminders, and progress visualization.

## Features

- 🎯 **Target Setting**: Set compounding goals with start amount, target amount, rate, and mode (daily/monthly)
- 📊 **Progress Tracking**: Real-time progress monitoring with visual status indicators
- 📉 **Stop-Loss Alerts**: Automatic alerts when balance falls below set thresholds
- ⏰ **Daily Reminders**: Scheduled reminders to update your balance
- 📈 **Visual Reports**: Generate daily profile cards with progress visualization
- 📋 **Excel Export**: Export your progress history to Excel format
- 🌐 **Multi-language**: Support for English and Hindi
- 💰 **Currency Support**: Customizable currency symbols
- 🔒 **Data Security**: Local JSON storage with thread-safe operations

## Installation

### Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/YOUR_USERNAME/Compounding_tracker.git
cd Compounding_tracker
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp .env.example .env
```
Edit `.env` and add your Telegram Bot Token:
```
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
```

4. **Update owner ID** in `app/config/constants.py`:
```python
OWNER_ID = "your_telegram_user_id"  # Replace with your actual Telegram ID
```

5. **Run the bot**:
```bash
python -m app.main
```

## Usage

### Bot Commands

- `/start` - Initialize the bot and view welcome message
- `/target` - Set your compounding target
- `/close` - Record daily closing balance
- `/status` - View current progress with visual card
- `/settings` - Access bot settings and configurations
- `/export` - Export progress data to Excel
- `/language` - Change language (English/Hindi)
- `/reset` - Reset all data (with confirmation)
- `/broadcast` - Send message to all users (owner only)

### Setting Up Your First Target

1. Use `/target` command
2. Enter details in format: `start_amount, target_amount, rate, mode`
3. Example: `1500, 10000, 5, daily`

### Daily Usage

1. Use `/close` to record your daily balance
2. Use `/status` to check progress
3. Bot will send daily reminders at 8 PM IST (if enabled)

## Configuration

### Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your bot token from BotFather

### Constants Configuration

Edit `app/config/constants.py`:

- `OWNER_ID`: Your Telegram user ID for admin features
- `CURRENCY`: Default currency symbol

## Project Structure

```
Compounding_tracker/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main bot application
│   ├── config/
│   │   ├── constants.py        # Configuration constants
│   │   └── messages.py         # Multi-language messages
│   ├── handlers/               # Command handlers
│   ├── conversations/          # Conversation handlers
│   └── utils/                  # Utility functions
├── assets/
│   └── fonts/                  # Font files for image generation
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
└── LICENSE                    # MIT License
```

## Features in Detail

### Compounding Calculation

The bot supports two compounding modes:
- **Daily**: Compounds daily with annual rate
- **Monthly**: Compounds monthly with annual rate

### Stop-Loss Protection

Set a percentage-based stop-loss to get alerts when your balance drops below the threshold.

### Visual Progress Cards

Generate beautiful profile cards showing:
- User profile photo
- Current progress
- Target vs actual balance
- Status indicators

### Data Export

Export your complete progress history to Excel with:
- Date-wise balance tracking
- Expected vs actual balance
- Stop-loss status indicators

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/YOUR_USERNAME/Compounding_tracker/issues) page
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about the error and steps to reproduce

## Disclaimer

This bot is for educational and tracking purposes only. It does not provide financial advice. Always consult with financial professionals for investment decisions.