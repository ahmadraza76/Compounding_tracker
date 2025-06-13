# app/config/messages.py
MESSAGES = {
    "en": {
        "welcome": """🎉 *Welcome to Compounding Tracker Bot!*

📈 Track your financial compounding progress with advanced features:

🎯 *Key Features:*
• Set compounding targets with custom rates
• Daily balance tracking with visual progress
• Stop-loss alerts for risk management
• Beautiful progress cards with your profile
• Excel export for detailed analysis
• Multi-language support (Hindi/English)
• Daily reminders to stay on track

🚀 *Quick Start:*
1. Use /target to set your goal
2. Use /close daily to record balance
3. Use /status to view progress

Type /help for complete command guide.""",

        "target_prompt": """🎯 *Set Your Compounding Target*

Please enter your target in this format:
*start_amount, target_amount, rate, mode*

📝 *Example:* `1500, 10000, 5, daily`

💡 *Parameters:*
• Start Amount: Your initial investment
• Target Amount: Your goal amount
• Rate: Percentage return (e.g., 5 for 5%)
• Mode: `daily` or `monthly`""",

        "target_exists": "❌ You already have a target set. Edit it via /settings or reset with /reset.",
        "no_target": "❌ No target set yet. Use /target to set your compounding goal.",
        
        "close_prompt": """💰 *Record Today's Balance*

Please enter your current closing balance:

📝 *Example:* `1650.50`

💡 This will update your progress and check against your target.""",

        "status_summary": "📊 *Your Progress Summary*",
        
        "settings_prompt": "⚙️ Select an option to edit your settings:",
        
        "reset_prompt": """⚠️ *Reset Confirmation*

Are you sure you want to reset ALL data?

This will permanently delete:
• Your target settings
• All balance history
• Progress tracking data

*This action cannot be undone!*""",

        "broadcast_prompt": "📢 *Broadcast Message*\n\nPlease enter the message to send to all users:",
        
        "language_prompt": """🌐 *Choose Language*

Please select your preferred language:

🇬🇧 *English* - Type: `en` or `english`
🇮🇳 *हिंदी* - Type: `hi` or `hindi`""",

        "language_set": "✅ Language updated successfully!",
        "no_history": "❌ No history available to export. Start tracking with /close command.",
        "export_success": "✅ Your detailed progress report has been generated and sent!",
        
        "stoploss_alert": """🚨 *STOP-LOSS ALERT!*

⚠️ Your current balance has fallen below your stop-loss threshold!

Please review your strategy and consider your next steps carefully.""",

        "target_achieved": """🎉 *CONGRATULATIONS!*

🏆 You've successfully achieved your compounding target!

🎯 Your disciplined approach to daily tracking has paid off!""",

        "reminder_prompt": """⏰ *Daily Balance Reminder*

Time to record today's closing balance!

Use /close to enter your current balance and track your progress.""",

        "cancel": "✅ Operation cancelled successfully.",
        "unknown_command": "❌ Unknown command. Use /help to see all available commands.",

        "help_text": """📚 *Compounding Tracker Bot - Complete Guide*

🎯 *MAIN COMMANDS:*

/start - Initialize bot and view welcome
/target - Set your compounding goal
/close - Record daily closing balance
/status - View progress with visual card
/settings - Access all bot settings
/export - Download Excel progress report
/language - Switch between Hindi/English
/help - Show this help guide
/reset - Reset all data (with confirmation)

💡 *HOW TO USE:*

*1. Set Target:*
Use: `/target`
Format: `start_amount, target_amount, rate, mode`
Example: `1500, 10000, 5, daily`

*2. Daily Tracking:*
Use: `/close`
Example: `1650.50`

*3. View Progress:*
Use: `/status` - See beautiful progress card

*4. Settings:*
Use: `/settings` - Edit all configurations

🎨 *FEATURES:*
• 📊 Visual progress cards with your photo
• 📈 Real-time compounding calculations
• 📉 Stop-loss alerts for risk management
• ⏰ Daily reminders (8 PM IST)
• 📋 Excel export for analysis
• 🌐 Hindi/English support
• 💰 Custom currency symbols

💰 *COMPOUNDING MODES:*
• `daily` - Daily compounding
• `monthly` - Monthly compounding

🔧 *SETTINGS OPTIONS:*
• Edit target parameters
• Set stop-loss percentage
• Change name and currency
• Toggle daily reminders
• Reset all data

📊 *PROGRESS TRACKING:*
• Daily balance vs expected
• Profit/loss calculations
• Visual status indicators
• Historical data export

Need help? Contact support or check /settings for more options!""",

        "profile_card_title": "📊 Daily Progress Card",
        "day_label": "Day",
        "target_label": "Target",
        "start_label": "Start",
        "rate_label": "Rate",
        "expected_label": "Expected",
        "current_label": "Current",
        "profit_goal_label": "Profit Goal",
        "stoploss_label": "Stop-Loss",
        "status_label": "Status",
        "progress_label": "Progress",
        "not_set": "Not Set",
        "status_image_error": "Sorry, there was an error generating your status image. Please try again later.",
        "status_data_error": """⚠️ Your status cannot be displayed due to a data issue:

{error_details}

Please check your target settings or use /reset if the issue persists."""
    },
    
    "hi": {
        "welcome": """🎉 *कंपाउंडिंग ट्रैकर बॉट में आपका स्वागत है!*

📈 उन्नत सुविधाओं के साथ अपनी वित्तीय कंपाउंडिंग प्रगति को ट्रैक करें:

🎯 *मुख्य विशेषताएं:*
• कस्टम दरों के साथ कंपाउंडिंग लक्ष्य सेट करें
• विज़ुअल प्रगति के साथ दैनिक बैलेंस ट्रैकिंग
• जोखिम प्रबंधन के लिए स्टॉप-लॉस अलर्ट
• आपकी प्रोफाइल के साथ सुंदर प्रगति कार्ड
• विस्तृत विश्लेषण के लिए एक्सेल एक्सपोर्ट
• बहु-भाषा समर्थन (हिंदी/अंग्रेजी)
• ट्रैक पर रहने के लिए दैनिक रिमाइंडर

🚀 *त्वरित शुरुआत:*
1. अपना लक्ष्य सेट करने के लिए /target का उपयोग करें
2. बैलेंस रिकॉर्ड करने के लिए दैनिक /close का उपयोग करें
3. प्रगति देखने के लिए /status का उपयोग करें

पूर्ण कमांड गाइड के लिए /help टाइप करें।""",

        "target_prompt": """🎯 *अपना कंपाउंडिंग लक्ष्य सेट करें*

कृपया अपना लक्ष्य इस प्रारूप में दर्ज करें:
*शुरुआती_राशि, लक्ष्य_राशि, दर, मोड*

📝 *उदाहरण:* `1500, 10000, 5, daily`

💡 *पैरामीटर:*
• शुरुआती राशि: आपका प्रारंभिक निवेश
• लक्ष्य राशि: आपकी लक्ष्य राशि
• दर: प्रतिशत रिटर्न (जैसे 5% के लिए 5)
• मोड: `daily` या `monthly`""",

        "target_exists": "❌ आपके पास पहले से एक लक्ष्य सेट है। इसे /settings से संपादित करें या /reset से रीसेट करें।",
        "no_target": "❌ अभी तक कोई लक्ष्य सेट नहीं है। अपना कंपाउंडिंग लक्ष्य सेट करने के लिए /target का उपयोग करें।",
        
        "close_prompt": """💰 *आज का बैलेंस रिकॉर्ड करें*

कृपया अपना वर्तमान क्लोजिंग बैलेंस दर्ज करें:

📝 *उदाहरण:* `1650.50`

💡 यह आपकी प्रगति को अपडेट करेगा और आपके लक्ष्य के विरुद्ध जांच करेगा।""",

        "status_summary": "📊 *आपकी प्रगति का सारांश*",
        
        "settings_prompt": "⚙️ अपनी सेटिंग्स संपादित करने के लिए एक विकल्प चुनें:",
        
        "reset_prompt": """⚠️ *रीसेट पुष्टि*

क्या आप वाकई सभी डेटा रीसेट करना चाहते हैं?

यह स्थायी रूप से हटा देगा:
• आपकी लक्ष्य सेटिंग्स
• सभी बैलेंस इतिहास
• प्रगति ट्रैकिंग डेटा

*इस क्रिया को पूर्ववत नहीं किया जा सकता!*""",

        "broadcast_prompt": "📢 *प्रसारण संदेश*\n\nकृपया सभी उपयोगकर्ताओं को भेजने के लिए संदेश दर्ज करें:",
        
        "language_prompt": """🌐 *भाषा चुनें*

कृपया अपनी पसंदीदा भाषा चुनें:

🇬🇧 *English* - टाइप करें: `en` या `english`
🇮🇳 *हिंदी* - टाइप करें: `hi` या `hindi`""",

        "language_set": "✅ भाषा सफलतापूर्वक अपडेट की गई!",
        "no_history": "❌ निर्यात करने के लिए कोई इतिहास उपलब्ध नहीं। /close कमांड के साथ ट्रैकिंग शुरू करें।",
        "export_success": "✅ आपकी विस्तृत प्रगति रिपोर्ट जनरेट और भेजी गई है!",
        
        "stoploss_alert": """🚨 *स्टॉप-लॉस अलर्ट!*

⚠️ आपका वर्तमान बैलेंस आपके स्टॉप-लॉस थ्रेशहोल्ड से नीचे गिर गया है!

कृपया अपनी रणनीति की समीक्षा करें और अपने अगले कदमों पर सावधानी से विचार करें।""",

        "target_achieved": """🎉 *बधाई हो!*

🏆 आपने सफलतापूर्वक अपना कंपाउंडिंग लक्ष्य हासिल कर लिया है!

🎯 दैनिक ट्रैकिंग के लिए आपका अनुशासित दृष्टिकोण सफल रहा है!""",

        "reminder_prompt": """⏰ *दैनिक बैलेंस रिमाइंडर*

आज का क्लोजिंग बैलेंस रिकॉर्ड करने का समय!

अपना वर्तमान बैलेंस दर्ज करने और अपनी प्रगति ट्रैक करने के लिए /close का उपयोग करें।""",

        "cancel": "✅ ऑपरेशन सफलतापूर्वक रद्द किया गया।",
        "unknown_command": "❌ अज्ञात कमांड। सभी उपलब्ध कमांड देखने के लिए /help का उपयोग करें।",

        "help_text": """📚 *कंपाउंडिंग ट्रैकर बॉट - पूर्ण गाइड*

🎯 *मुख्य कमांड:*

/start - बॉट को इनिशियलाइज़ करें और स्वागत देखें
/target - अपना कंपाउंडिंग लक्ष्य सेट करें
/close - दैनिक क्लोजिंग बैलेंस रिकॉर्ड करें
/status - विज़ुअल कार्ड के साथ प्रगति देखें
/settings - सभी बॉट सेटिंग्स एक्सेस करें
/export - एक्सेल प्रगति रिपोर्ट डाउनलोड करें
/language - हिंदी/अंग्रेजी के बीच स्विच करें
/help - यह सहायता गाइड दिखाएं
/reset - सभी डेटा रीसेट करें (पुष्टि के साथ)

💡 *उपयोग कैसे करें:*

*1. लक्ष्य सेट करें:*
उपयोग: `/target`
प्रारूप: `शुरुआती_राशि, लक्ष्य_राशि, दर, मोड`
उदाहरण: `1500, 10000, 5, daily`

*2. दैनिक ट्रैकिंग:*
उपयोग: `/close`
उदाहरण: `1650.50`

*3. प्रगति देखें:*
उपयोग: `/status` - सुंदर प्रगति कार्ड देखें

*4. सेटिंग्स:*
उपयोग: `/settings` - सभी कॉन्फ़िगरेशन संपादित करें

🎨 *विशेषताएं:*
• 📊 आपकी फोटो के साथ विज़ुअल प्रगति कार्ड
• 📈 रियल-टाइम कंपाउंडिंग गणना
• 📉 जोखिम प्रबंधन के लिए स्टॉप-लॉस अलर्ट
• ⏰ दैनिक रिमाइंडर (शाम 8 बजे IST)
• 📋 विश्लेषण के लिए एक्सेल एक्सपोर्ट
• 🌐 हिंदी/अंग्रेजी समर्थन
• 💰 कस्टम मुद्रा प्रतीक

💰 *कंपाउंडिंग मोड:*
• `daily` - दैनिक कंपाउंडिंग
• `monthly` - मासिक कंपाउंडिंग

🔧 *सेटिंग्स विकल्प:*
• लक्ष्य पैरामीटर संपादित करें
• स्टॉप-लॉस प्रतिशत सेट करें
• नाम और मुद्रा बदलें
• दैनिक रिमाइंडर टॉगल करें
• सभी डेटा रीसेट करें

📊 *प्रगति ट्रैकिंग:*
• दैनिक बैलेंस बनाम अपेक्षित
• लाभ/हानि गणना
• विज़ुअल स्थिति संकेतक
• ऐतिहासिक डेटा निर्यात

सहायता चाहिए? समर्थन से संपर्क करें या अधिक विकल्पों के लिए /settings देखें!""",

        "profile_card_title": "📊 दैनिक प्रगति कार्ड",
        "day_label": "दिन",
        "target_label": "लक्ष्य",
        "start_label": "शुरुआत",
        "rate_label": "दर",
        "expected_label": "अपेक्षित",
        "current_label": "वर्तमान",
        "profit_goal_label": "लाभ लक्ष्य",
        "stoploss_label": "स्टॉप-लॉस",
        "status_label": "स्थिति",
        "progress_label": "प्रगति",
        "not_set": "सेट नहीं",
        "status_image_error": "क्षमा करें, आपकी स्थिति छवि बनाने में कोई त्रुटि हुई। कृपया बाद में पुनः प्रयास करें।",
        "status_data_error": """⚠️ डेटा समस्या के कारण आपकी स्थिति प्रदर्शित नहीं की जा सकती:

{error_details}

कृपया अपनी लक्ष्य सेटिंग जांचें या यदि समस्या बनी रहती है तो /reset का उपयोग करें।"""
    }
}