# app/config/messages.py
MESSAGES = {
    "en": {
        "welcome": "🎉 *Welcome to Compounding Tracker Bot!*\nTrack your progress with ease. Set a target using /target or view settings with /settings.",
        "target_prompt": "Please enter your target in the format: *start_amount, target_amount, rate, mode*\nExample: *1500, 10000, 5, daily*",
        "target_exists": "❌ You already have a target. Edit it via /settings or reset with /reset.",
        "no_target": "❌ No target set. Use /target to set one.",
        "close_prompt": "Please enter today’s closing balance (e.g., *1500.50*).",
        "status_summary": "📊 *Your Progress Summary*",
        "settings_prompt": "Select an option to edit your settings:",
        "reset_prompt": "⚠️ Are you sure you want to reset all data? This cannot be undone.",
        "broadcast_prompt": "Please enter the message to broadcast to all users.",
        "language_prompt": "Please choose a language: *Hindi* (hi) or *English* (en).",
        "language_set": "✅ Language updated successfully!",
        "no_history": "❌ No history available to export.",
        "export_success": "✅ Your progress report has been generated!",
        "stoploss_alert": "🚨 *Stop-Loss Alert!* Your balance is below the stop-loss level!",
        "target_achieved": "🎉 *Congratulations!* You’ve achieved your target!",
        "reminder_prompt": "⏰ Time to record your balance! Use /close to enter today’s balance.",
        "cancel": "✅ Operation cancelled.",
        "unknown_command": "❌ Unknown command. Use /start to begin."
    },
    "hi": {
        "welcome": "🎉 *कंपाउंडिंग ट्रैकर बॉट में आपका स्वागत है!*\nअपनी प्रगति को आसानी से ट्रैक करें। /target से लक्ष्य सेट करें या /settings से सेटिंग्स देखें।",
        "target_prompt": "कृपया अपना लक्ष्य इस प्रारूप में दर्ज करें: *शुरुआती_राशि, लक्ष्य_राशि, दर, मोड*\nउदाहरण: *1500, 10000, 5, daily*",
        "target_exists": "❌ आपके पास पहले से एक लक्ष्य है। इसे /settings से संपादित करें या /reset से रीसेट करें।",
        "no_target": "❌ कोई लक्ष्य सेट नहीं है। /target का उपयोग करें।",
        "close_prompt": "कृपया आज का क्लोजिंग बैलेंस दर्ज करें (उदाहरण: *1500.50*)।",
        "status_summary": "📊 *आपकी प्रगति का सारांश*",
        "settings_prompt": "अपनी सेटिंग्स संपादित करने के लिए एक विकल्प चुनें:",
        "reset_prompt": "⚠️ क्या आप वाकई सभी डेटा रीसेट करना चाहते हैं? इसे पूर्ववत नहीं किया जा सकता।",
        "broadcast_prompt": "कृपया सभी उपयोगकर्ताओं को प्रसारित करने के लिए संदेश दर्ज करें।",
        "language_prompt": "कृपया एक भाषा चुनें: *हिंदी* (hi) या *अंग्रेजी* (en)।",
        "language_set": "✅ भाषा सफलतापूर्वक अपडेट की गई!",
        "no_history": "❌ निर्यात करने के लिए कोई इतिहास उपलब्ध नहीं।",
        "export_success": "✅ आपकी प्रगति रिपोर्ट जनरेट हो गई है!",
        "stoploss_alert": "🚨 *स्टॉप-लॉस अलर्ट!* आपका बैलेंस स्टॉप-लॉस स्तर से नीचे है!",
        "target_achieved": "🎉 *बधाई हो!* आपने अपना लक्ष्य हासिल कर लिया है!",
        "reminder_prompt": "⏰ बैलेंस दर्ज करने का समय! आज का बैलेंस दर्ज करने के लिए /close का उपयोग करें।",
        "cancel": "✅ ऑपरेशन रद्द किया गया।",
        "unknown_command": "❌ अज्ञात कमांड। शुरू करने के लिए /start का उपयोग करें।"
    }
}
