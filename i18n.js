/* LifeBridge Japan: lightweight UI translations (header, footer, home page).
 * Languages: English (en), Nepali (ne), Vietnamese (vi), Burmese (my).
 * The choice is stored in localStorage as "lb_lang" and applied on every page.
 * Elements opt in with data-i18n="key" (plain text), data-i18n-html="key"
 * (markup such as the hero title's line break), or data-i18n-placeholder="key".
 * Anything without a matching key stays in English.
 * JS-rendered text uses window.LBT.t(key) (English fallback, safe before load)
 * and re-renders on the "lb:lang" event. data-i18n-aria-label and
 * data-i18n-alt set the aria-label and alt attributes.
 */
(function () {
    "use strict";

    var STORE_KEY = "lb_lang";
    var SUPPORTED = ["en", "ne", "vi", "my"];

    var I18N = {
        en: {
            "nav.home": "Home",
            "nav.deadlines": "Deadlines",
            "footer.tagline": "Understand Japanese notices in your own language.",
            "hero.explain": "LifeBridge Lens",
            "topic.japanese.title": "Japanese",
            "journey.nav.dates": "Important Dates",
            "app.noDates": "No dates added yet.",
            "app.remove": "Remove",
            "app.removeDate": "Remove {t}",
            "doc.skip": "Skip to content",
            "doc.mainNavAria": "Main navigation",
            "doc.langAria": "Language",
            "doc.back": "← Home",
            "doc.explore": "Explore",
            "doc.copyright": "© 2026 LifeBridge Lens · Built for newcomers in Japan",
            "doc.backTop": "Back to top ↑",
            "money.trackerTitle": "Money Tracker",
            "dates.title": "Important Dates | LifeBridge Lens",
            "dates.lead": "Keep appointments and deadlines in one place. Dates are stored on this browser; notifications are not sent.",
            "dates.dateLabel": "Date",
            "explain.title": "LifeBridge Lens",
            "explain.eyebrow": "Scan & understand",
            "explain.lead": "Take a photo of a Japanese letter or notice. LifeBridge Lens tells you what it is, why you got it, and what to do next, in simple words.",
            "explain.step1": "<strong>1. Choose a photo of the notice</strong>",
            "explain.step2": "<strong>2. Choose your language</strong>",
            "explain.optNepali": "Nepali",
            "explain.optEnglish": "English",
            "explain.submit": "Scan notice",
            "explain.resultTitle": "Your explanation",
            "explain.hWhat": "What is this?",
            "explain.hWhy": "Why did you get it?",
            "explain.hImportance": "How important is it?",
            "explain.hNext": "What to do next",
            "explain.hDeadline": "Deadline",
            "explain.hAmount": "Amount",
            "explain.hCheck": "Things to check",
            "explain.needPhoto": "Please choose a photo first.",
            "explain.reading": "Reading your notice... this can take a few seconds.",
            "explain.failed": "Sorry, it did not work: {msg}",
            "explain.followTitle": "Ask a follow-up question",
            "explain.qDeadline": "What happens if I miss the deadline?",
            "explain.qWhere": "Where do I pay or do this?",
            "explain.qDocs": "What documents do I need?",
            "explain.qUrgent": "Is this urgent?",
            "explain.askPlaceholder": "Ask something else about this notice...",
            "explain.ask": "Ask",
            "tracker.title": "Money Tracker | LifeBridge Lens",
            "tracker.lead": "A simple record of what you earn, spend and save each month, and what you are saving for. Everything stays in this browser on your device.",
            "tracker.thisMonth": "This month",
            "tracker.monthLabel": "<strong>Month</strong>",
            "tracker.earned": "Earned",
            "tracker.spent": "Spent",
            "tracker.saved": "Saved",
            "tracker.left": "Left",
            "tracker.addEntry": "Add an entry",
            "tracker.type": "Type",
            "tracker.optIncome": "Income (earned)",
            "tracker.optExpense": "Expense (spent)",
            "tracker.optSaving": "Saving (put aside)",
            "tracker.amount": "Amount (¥)",
            "tracker.noteLabel": "What is it?",
            "tracker.notePlaceholder": "e.g. Sukiya salary, Rent, Food, Train",
            "tracker.savingFor": "Saving for",
            "tracker.addEntryBtn": "Add entry",
            "tracker.goalsTitle": "Savings goals",
            "tracker.newGoal": "New goal. What are you saving for?",
            "tracker.goalPlaceholder": "e.g. Ticket to Nepal, New laptop",
            "tracker.target": "Target amount (¥)",
            "tracker.addGoal": "Add goal",
            "tracker.entries": "Entries",
            "tracker.generalSavings": "General savings",
            "tracker.noGoals": "No goals yet. Add one below, for example a ticket home or a new laptop.",
            "tracker.goalProgress": "{saved} of {target} ({pct}%)",
            "tracker.noEntries": "No entries for this month yet.",
            "tracker.tagIncome": "Income",
            "tracker.tagExpense": "Expense",
            "tracker.tagSaving": "Saving",
            "tracker.forGoal": " · For: {name}",
            "tracker.delete": "Delete",
            "tracker.added": "Added.",
            "tracker.deleteGoal": "Delete goal",
            "tracker.deleteGoalConfirm": "Delete this goal? Your savings entries will stay.",
            "tracker.saveFailed": "Could not save. Your browser storage may be full or blocked.",
            "footer.disclaimer": "LifeBridge Lens is an independent student project and is not affiliated with any Japanese government agency. Information is summarized from official sources; always confirm with the office involved.",
            "doc.mobileNav": "Mobile",
            "doc.menu": "Menu",
            "nav.explainShort": "Lens",
            "explain.uploadTitle": "Tap to take or choose a photo",
            "explain.uploadHint": "A clear photo of the whole notice works best",
            "explain.askLabel": "Ask something else about this notice",
            "explain.explaining": "Reading your notice...",
            "explain.asking": "Asking...",
            "explain.badFormat": "The reply was unclear. Please try again with a clearer photo of the whole notice.",
            "explain.tooSlow": "The AI took too long. Please try again.",
            "explain.serverError": "Server error. Please try again.",
            "explain.sampleBtn": "Try a sample notice",
            "explain.sampleTag": "Sample",
            "explain.sample.what": "City notice: resident tax (住民税) payment notice",
            "explain.sample.why": "Yearly resident tax bill from the city office.",
            "explain.sample.importance": "High. Pay before the due date to avoid a late fee.",
            "explain.sample.next": "1. Check the amount and due date.\n2. Pay at a bank or convenience store.\n3. Keep the receipt.",
            "explain.sample.deadline": "February 1, 2027 (4th installment)",
            "explain.sample.amount": "12,340 yen",
            "explain.sample.staff": "この保険料の支払いについて相談したいです。",
            "explain.sample.staffMeaning": "I want to ask about paying this insurance bill.",
            "explain.sample.check": "Your name and address. The amount and due date.",
            "explain.saveDate": "Save deadline",
            "explain.dateSaved": "Saved to Important Dates.",
            "explain.dateExists": "Already in Important Dates.",
            "explain.viewDates": "View in Important Dates",
            "explain.viewDatesPage": "View Important Dates",
            "lens.title": "LifeBridge Lens",
            "lens.tagline": "Understand Japanese official notices in your language.",
            "lens.scan": "Scan a notice",
            "lens.dates": "My deadlines",
            "lens.money": "Money tracker",
            "index.hero": "Got a Japanese letter you cannot read? Take a photo and understand it in your language.",
            "index.exampleLabel": "Example",
            "index.exampleAfter": "This is your national health insurance bill, 4th installment. Pay 12,340 yen by November 30, 2026.",
            "index.sub": "City hall, tax, insurance and bill notices. Find out what to do and by when.",
            "index.note": "AI can make mistakes. Check the amount and date against the letter before paying.",
            "index.step1": "Take a photo",
            "index.step2": "Read it in your language",
            "index.step3": "Save the deadline",
            "explain.checkDate": "Check this date against the letter before saving.",
            "explain.confirmSave": "Confirm",
            "explain.addToCal": "Add to calendar",
            "explain.hStaff": "Show this to the staff",
            "explain.copy": "Copy",
            "explain.copied": "Copied.",
            "explain.note": "AI can make mistakes. Confirm important details with the office.",
            "explain.loadPrivacy": "Your photo is sent only to Meta AI and is not stored on our server.",
            "explain.daysLeft": "{n} days left",
            "explain.dayLeft": "1 day left",
            "explain.deadlinePassed": "Deadline passed",
            "explain.load1": "Reading the Japanese text",
            "explain.load2": "Understanding the notice",
            "explain.load3": "Writing it in your language",
            "explain.notShown": "Not shown",
            "explain.saveDateLabel": "Date to save",
            "explain.badDate": "Please pick a real date from the calendar.",
            "explain.privacyHint": "Your photo is sent to Meta AI. Cover details you don't need, like your residence card number.",
            "tracker.goalError": "Please enter a goal name and a target amount.",
            "tracker.deleteConfirm": "Delete this entry?",
            "net.offline": "You are offline. Connect to the internet and try again.",
            "chat.title": "Ask LifeBridge",
            "chat.placeholder": "Type your question...",
            "chat.send": "Send",
            "chat.open": "Open chat",
            "chat.close": "Close chat",
            "chat.online": "Online",
            "chat.offline": "Offline. Saved answers only",
            "net.banner": "You are offline. Saved deadlines, tracker and chat still work.",
            "nav.moneyShort": "Money",
            "index.step1d": "Use your phone camera to take a clear photo of the whole notice.",
            "index.step2d": "Get a simple explanation of what it means and what to do.",
            "index.step3d": "Keep the due date and amount saved so you never miss it.",
            "explain.eraLabel": "Japanese date",
            "explain.loadingTitle": "Reading your notice",
            "explain.loadingLang": "Language",
            "dates.upcoming": "Upcoming",
            "dates.past": "Past",
            "dates.completed": "Completed",
            "dates.markDone": "Mark done",
            "dates.reopen": "Reopen",
            "dates.prevMonth": "Previous month",
            "dates.nextMonth": "Next month",
            "dates.calendarTitle": "Calendar",
            "dates.today": "Today",
            "offline.title": "You are offline",
            "offline.lead": "Connect to the internet and try again.",
            "offline.retry": "Try again",
            "explain.hPayment": "How to pay",
            "explain.hConsequences": "If you miss the deadline",
            "explain.sample.payment": "Pay at a bank or convenience store with this slip. Keep the receipt.",
            "explain.sample.consequences": "A late fee may be added. If you cannot pay on time, ask the city office for advice."
        },
        ne: {
            "nav.home": "गृहपृष्ठ",
            "nav.deadlines": "म्यादहरू",
            "footer.tagline": "जापानी सूचनाहरू आफ्नै भाषामा बुझ्नुहोस्।",
            "hero.explain": "LifeBridge Lens",
            "topic.japanese.title": "जापानी",
            "journey.nav.dates": "महत्त्वपूर्ण मितिहरू",
            "app.noDates": "अहिलेसम्म कुनै मिति थपिएको छैन।",
            "app.remove": "हटाउनुहोस्",
            "app.removeDate": "{t} हटाउनुहोस्",
            "doc.skip": "सामग्रीमा जानुहोस्",
            "doc.mainNavAria": "मुख्य नेभिगेसन",
            "doc.langAria": "भाषा",
            "doc.back": "← गृहपृष्ठ",
            "doc.explore": "अन्वेषण",
            "doc.copyright": "© 2026 LifeBridge Lens · जापानमा नयाँ आउनेहरूका लागि बनाइएको",
            "doc.backTop": "माथि फर्कनुहोस् ↑",
            "money.trackerTitle": "पैसा ट्र्याकर",
            "dates.title": "महत्त्वपूर्ण मितिहरू | LifeBridge Lens",
            "dates.lead": "अपोइन्टमेन्ट र अन्तिम मितिहरू एकै ठाउँमा राख्नुहोस्। मितिहरू यो ब्राउजरमा भण्डार हुन्छन्; सूचना पठाइँदैन।",
            "dates.dateLabel": "मिति",
            "explain.title": "LifeBridge Lens",
            "explain.eyebrow": "स्क्यान गरेर बुझ्नुहोस्",
            "explain.lead": "जापानी चिठी वा सूचनाको फोटो खिच्नुहोस्। LifeBridge Lens ले त्यो के हो, तपाईंले किन पाउनुभयो, र अब के गर्ने भनेर सरल शब्दमा बुझाउँछ।",
            "explain.step1": "<strong>1. सूचनाको फोटो छान्नुहोस्</strong>",
            "explain.step2": "<strong>2. आफ्नो भाषा छान्नुहोस्</strong>",
            "explain.optNepali": "नेपाली",
            "explain.optEnglish": "अङ्ग्रेजी",
            "explain.submit": "सूचना स्क्यान गर्नुहोस्",
            "explain.resultTitle": "तपाईंको व्याख्या",
            "explain.hWhat": "यो के हो?",
            "explain.hWhy": "तपाईंले यो किन पाउनुभयो?",
            "explain.hImportance": "यो कत्तिको महत्त्वपूर्ण छ?",
            "explain.hNext": "अब के गर्ने",
            "explain.hDeadline": "अन्तिम मिति",
            "explain.hAmount": "रकम",
            "explain.hCheck": "जाँच्ने कुराहरू",
            "explain.needPhoto": "कृपया पहिले फोटो छान्नुहोस्।",
            "explain.reading": "तपाईंको सूचना पढ्दैछ... यसमा केही सेकेन्ड लाग्न सक्छ।",
            "explain.failed": "माफ गर्नुहोस्, काम भएन: {msg}",
            "explain.followTitle": "थप प्रश्न सोध्नुहोस्",
            "explain.qDeadline": "म्याद छुटेमा के हुन्छ?",
            "explain.qWhere": "कहाँ तिर्ने वा गर्ने?",
            "explain.qDocs": "कुन कागजातहरू चाहिन्छ?",
            "explain.qUrgent": "के यो जरुरी छ?",
            "explain.askPlaceholder": "सूचनाबारे अरू केही सोध्नुहोस्...",
            "explain.ask": "सोध्नुहोस्",
            "tracker.title": "पैसा ट्र्याकर | LifeBridge Lens",
            "tracker.lead": "हरेक महिना के कमाउनुहुन्छ, के खर्च गर्नुहुन्छ र के बचत गर्नुहुन्छ, र केका लागि बचत गर्दै हुनुहुन्छ भन्ने सरल रेकर्ड। सबै कुरा तपाईंको डिभाइसको यही ब्राउजरमा रहन्छ।",
            "tracker.thisMonth": "यो महिना",
            "tracker.monthLabel": "<strong>महिना</strong>",
            "tracker.earned": "कमाएको",
            "tracker.spent": "खर्च गरेको",
            "tracker.saved": "बचत गरेको",
            "tracker.left": "बाँकी",
            "tracker.addEntry": "प्रविष्टि थप्नुहोस्",
            "tracker.type": "प्रकार",
            "tracker.optIncome": "आम्दानी (कमाएको)",
            "tracker.optExpense": "खर्च (खर्च गरेको)",
            "tracker.optSaving": "बचत (छुट्याएको)",
            "tracker.amount": "रकम (¥)",
            "tracker.noteLabel": "यो के हो?",
            "tracker.notePlaceholder": "जस्तै: Sukiya तलब, भाडा, खाना, रेल",
            "tracker.savingFor": "केका लागि बचत",
            "tracker.addEntryBtn": "प्रविष्टि थप्नुहोस्",
            "tracker.goalsTitle": "बचत लक्ष्यहरू",
            "tracker.newGoal": "नयाँ लक्ष्य। केका लागि बचत गर्दै हुनुहुन्छ?",
            "tracker.goalPlaceholder": "जस्तै: नेपाल जाने टिकट, नयाँ ल्यापटप",
            "tracker.target": "लक्ष्य रकम (¥)",
            "tracker.addGoal": "लक्ष्य थप्नुहोस्",
            "tracker.entries": "प्रविष्टिहरू",
            "tracker.generalSavings": "सामान्य बचत",
            "tracker.noGoals": "अहिलेसम्म कुनै लक्ष्य छैन। तल एउटा थप्नुहोस्, जस्तै घर जाने टिकट वा नयाँ ल्यापटप।",
            "tracker.goalProgress": "{target} मध्ये {saved} ({pct}%)",
            "tracker.noEntries": "यो महिनाका लागि अहिलेसम्म कुनै प्रविष्टि छैन।",
            "tracker.tagIncome": "आम्दानी",
            "tracker.tagExpense": "खर्च",
            "tracker.tagSaving": "बचत",
            "tracker.forGoal": " · का लागि: {name}",
            "tracker.delete": "हटाउनुहोस्",
            "tracker.added": "थपियो।",
            "tracker.deleteGoal": "लक्ष्य हटाउनुहोस्",
            "tracker.deleteGoalConfirm": "यो लक्ष्य मेट्ने? तपाईंका बचत प्रविष्टिहरू रहनेछन्।",
            "tracker.saveFailed": "सेभ गर्न सकिएन। ब्राउजर स्टोरेज भरिएको वा ब्लक भएको हुन सक्छ।",
            "footer.disclaimer": "LifeBridge Lens स्वतन्त्र विद्यार्थी परियोजना हो र कुनै पनि जापानी सरकारी निकायसँग आबद्ध छैन। जानकारी आधिकारिक स्रोतहरूबाट सारांश गरिएको हो; सधैं सम्बन्धित कार्यालयसँग पक्का गर्नुहोस्।",
            "doc.mobileNav": "मोबाइल",
            "doc.menu": "मेनु",
            "nav.explainShort": "Lens",
            "explain.uploadTitle": "फोटो खिच्न वा छान्न ट्याप गर्नुहोस्",
            "explain.uploadHint": "पूरै सूचनाको स्पष्ट फोटो राम्रो हुन्छ",
            "explain.askLabel": "यो सूचनाबारे अरू केही सोध्नुहोस्",
            "explain.explaining": "सूचना पढ्दै...",
            "explain.asking": "सोध्दै...",
            "explain.badFormat": "जवाफ स्पष्ट भएन। पूरै सूचनाको स्पष्ट फोटो लिएर फेरि प्रयास गर्नुहोस्।",
            "explain.tooSlow": "AI लाई धेरै समय लाग्यो। कृपया फेरि प्रयास गर्नुहोस्।",
            "explain.serverError": "सर्भर त्रुटि। कृपया फेरि प्रयास गर्नुहोस्।",
            "explain.sampleBtn": "नमूना सूचना प्रयास गर्नुहोस्",
            "explain.sampleTag": "नमूना",
            "explain.sample.what": "सहरको सूचना: बासिन्दा कर (住民税) भुक्तानी सूचना",
            "explain.sample.why": "सहर कार्यालयबाट वार्षिक बासिन्दा करको बिल।",
            "explain.sample.importance": "उच्च। जरिवानाबाट बच्न म्यादअघि तिर्नुहोस्।",
            "explain.sample.next": "1. रकम र म्याद जाँच्नुहोस्।\n2. बैंक वा सुविधा पसलमा तिर्नुहोस्।\n3. रसिद राख्नुहोस्।",
            "explain.sample.deadline": "फेब्रुअरी 1, 2027 (चौथो किस्ता)",
            "explain.sample.amount": "12,340 येन",
            "explain.sample.staff": "この保険料の支払いについて相談したいです。",
            "explain.sample.staffMeaning": "म यो बिमा शुल्क तिर्ने बारेमा सोध्न चाहन्छु।",
            "explain.sample.check": "तपाईंको नाम र ठेगाना। रकम र म्याद।",
            "explain.saveDate": "म्याद सुरक्षित गर्नुहोस्",
            "explain.dateSaved": "महत्त्वपूर्ण मितिमा सेभ भयो।",
            "explain.dateExists": "पहिले नै महत्त्वपूर्ण मितिमा छ।",
            "explain.viewDates": "महत्त्वपूर्ण मितिमा हेर्नुहोस्",
            "explain.viewDatesPage": "महत्त्वपूर्ण मितिहरू हेर्नुहोस्",
            "lens.title": "LifeBridge Lens",
            "lens.tagline": "जापानी आधिकारिक सूचना आफ्नै भाषामा बुझ्नुहोस्।",
            "lens.scan": "सूचना स्क्यान गर्नुहोस्",
            "lens.dates": "मेरा म्यादहरू",
            "lens.money": "पैसा ट्र्याकर",
            "index.hero": "पढ्न नसकिने जापानी पत्र पाउनुभयो? फोटो खिच्नुहोस् र आफ्नै भाषामा बुझ्नुहोस्।",
            "index.exampleLabel": "उदाहरण",
            "index.exampleAfter": "यो तपाईंको राष्ट्रिय स्वास्थ्य बिमा शुल्कको बिल हो, चौथो किस्ता। नोभेम्बर 30, 2026 सम्म 12,340 येन तिर्नुहोस्।",
            "index.sub": "नगरपालिका, कर, बिमा र बिलका सूचनाहरू। के गर्ने र कहिलेसम्म गर्ने थाहा पाउनुहोस्।",
            "index.note": "AI ले गल्ती गर्न सक्छ। तिर्नुअघि रकम र मिति पत्रसँग मिलाउनुहोस्।",
            "index.step1": "फोटो खिच्नुहोस्",
            "index.step2": "आफ्नै भाषामा पढ्नुहोस्",
            "index.step3": "म्याद सुरक्षित गर्नुहोस्",
            "explain.checkDate": "सेभ गर्नुअघि यो मिति पत्रसँग भिडाउनुहोस्।",
            "explain.confirmSave": "पुष्टि गर्नुहोस्",
            "explain.addToCal": "पात्रोमा थप्नुहोस्",
            "explain.hStaff": "यो कर्मचारीलाई देखाउनुहोस्",
            "explain.copy": "प्रतिलिपि",
            "explain.copied": "प्रतिलिपि भयो।",
            "explain.note": "AI ले गल्ती गर्न सक्छ। महत्त्वपूर्ण कुरा कार्यालयसँग पक्का गर्नुहोस्।",
            "explain.loadPrivacy": "तपाईंको फोटो Meta AI लाई मात्र पठाइन्छ र हाम्रो सर्भरमा भण्डार गरिँदैन।",
            "explain.daysLeft": "{n} दिन बाँकी",
            "explain.dayLeft": "1 दिन बाँकी",
            "explain.deadlinePassed": "म्याद सकियो",
            "explain.load1": "जापानी पाठ पढ्दै",
            "explain.load2": "सूचना बुझ्दै",
            "explain.load3": "तपाईंको भाषामा लेख्दै",
            "explain.notShown": "देखाइएको छैन",
            "explain.saveDateLabel": "सेभ गर्ने मिति",
            "explain.badDate": "क्यालेन्डरबाट साँचो मिति छान्नुहोस्।",
            "explain.privacyHint": "तपाईंको फोटो Meta AI लाई पठाइन्छ। चाहिनेभन्दा बढी विवरण, जस्तै निवास कार्ड नम्बर, छोप्नुहोस्।",
            "tracker.goalError": "कृपया लक्ष्यको नाम र रकम लेख्नुहोस्।",
            "tracker.deleteConfirm": "यो प्रविष्टि मेट्ने?",
            "net.offline": "तपाईं अफलाइन हुनुहुन्छ। इन्टरनेट जोडेर फेरि प्रयास गर्नुहोस्।",
            "chat.title": "LifeBridge लाई सोध्नुहोस्",
            "chat.placeholder": "आफ्नो प्रश्न लेख्नुहोस्...",
            "chat.send": "पठाउनुहोस्",
            "chat.open": "च्याट खोल्नुहोस्",
            "chat.close": "च्याट बन्द गर्नुहोस्",
            "chat.online": "अनलाइन",
            "chat.offline": "अफलाइन। सेभ गरिएका जवाफ मात्र",
            "net.banner": "तपाईं अफलाइन हुनुहुन्छ। सेभ गरिएका मिति, ट्र्याकर र च्याट चल्छन्।",
            "nav.moneyShort": "पैसा",
            "index.step1d": "पूरै सूचनाको स्पष्ट फोटो फोन क्यामेराले खिच्नुहोस्।",
            "index.step2d": "यसको अर्थ के हो र के गर्ने भन्ने सरल व्याख्या पाउनुहोस्।",
            "index.step3d": "म्याद र रकम सेभ गरेर राख्नुहोस्, कहिल्यै नछुटाउनुहोस्।",
            "explain.eraLabel": "जापानी मिति",
            "explain.loadingTitle": "तपाईंको सूचना पढ्दै",
            "explain.loadingLang": "भाषा",
            "dates.upcoming": "आउँदै गरेका",
            "dates.past": "बितेका",
            "dates.completed": "पूरा भएका",
            "dates.markDone": "पूरा भयो",
            "dates.reopen": "फेरि खोल्नुहोस्",
            "dates.prevMonth": "अघिल्लो महिना",
            "dates.nextMonth": "अर्को महिना",
            "dates.calendarTitle": "पात्रो",
            "dates.today": "आज",
            "offline.title": "तपाईं अफलाइन हुनुहुन्छ",
            "offline.lead": "इन्टरनेट जोडेर फेरि प्रयास गर्नुहोस्।",
            "offline.retry": "फेरि प्रयास गर्नुहोस्",
            "explain.hPayment": "कसरी तिर्ने",
            "explain.hConsequences": "म्याद छुटेमा के हुन्छ",
            "explain.sample.payment": "यो पर्चीले बैंक वा सुविधा पसलमा तिर्नुहोस्। रसिद राख्नुहोस्।",
            "explain.sample.consequences": "ढिलो शुल्क लाग्न सक्छ। समयमा तिर्न नसके सहर कार्यालयसँग सल्लाह लिनुहोस्।"
        },
        vi: {
            "nav.home": "Trang chủ",
            "nav.deadlines": "Thời hạn",
            "footer.tagline": "Hiểu các thông báo tiếng Nhật bằng ngôn ngữ của bạn.",
            "hero.explain": "LifeBridge Lens",
            "topic.japanese.title": "Tiếng Nhật",
            "journey.nav.dates": "Ngày quan trọng",
            "app.noDates": "Chưa thêm ngày nào.",
            "app.remove": "Gỡ",
            "app.removeDate": "Gỡ {t}",
            "doc.skip": "Bỏ qua tới nội dung",
            "doc.mainNavAria": "Điều hướng chính",
            "doc.langAria": "Ngôn ngữ",
            "doc.back": "← Trang chủ",
            "doc.explore": "Khám phá",
            "doc.copyright": "© 2026 LifeBridge Lens · Dành cho người mới đến Nhật Bản",
            "doc.backTop": "Về đầu trang ↑",
            "money.trackerTitle": "Theo dõi tiền bạc",
            "dates.title": "Ngày quan trọng | LifeBridge Lens",
            "dates.lead": "Hãy giữ các cuộc hẹn và thời hạn ở một nơi. Các ngày được lưu trên trình duyệt này; không gửi thông báo.",
            "dates.dateLabel": "Ngày",
            "explain.title": "LifeBridge Lens",
            "explain.eyebrow": "Quét và hiểu",
            "explain.lead": "Hãy chụp ảnh một bức thư hoặc thông báo tiếng Nhật. LifeBridge Lens sẽ cho biết đó là gì, vì sao bạn nhận được và cần làm gì tiếp theo, bằng những từ đơn giản.",
            "explain.step1": "<strong>1. Chọn ảnh chụp thông báo</strong>",
            "explain.step2": "<strong>2. Chọn ngôn ngữ của bạn</strong>",
            "explain.optNepali": "Tiếng Nepal",
            "explain.optEnglish": "Tiếng Anh",
            "explain.submit": "Quét thông báo",
            "explain.resultTitle": "Lời giải thích của bạn",
            "explain.hWhat": "Đây là gì?",
            "explain.hWhy": "Vì sao bạn nhận được?",
            "explain.hImportance": "Nó quan trọng thế nào?",
            "explain.hNext": "Việc cần làm tiếp theo",
            "explain.hDeadline": "Thời hạn",
            "explain.hAmount": "Số tiền",
            "explain.hCheck": "Những điều cần kiểm tra",
            "explain.needPhoto": "Vui lòng chọn ảnh trước.",
            "explain.reading": "Đang đọc thông báo của bạn... việc này có thể mất vài giây.",
            "explain.failed": "Xin lỗi, không thành công: {msg}",
            "explain.followTitle": "Đặt câu hỏi tiếp theo",
            "explain.qDeadline": "Chuyện gì xảy ra nếu tôi trễ hạn?",
            "explain.qWhere": "Tôi nộp tiền hoặc làm việc này ở đâu?",
            "explain.qDocs": "Tôi cần những giấy tờ gì?",
            "explain.qUrgent": "Việc này có gấp không?",
            "explain.askPlaceholder": "Hỏi thêm điều gì khác về thông báo này...",
            "explain.ask": "Hỏi",
            "tracker.title": "Theo dõi tiền bạc | LifeBridge Lens",
            "tracker.lead": "Bản ghi đơn giản về những gì bạn kiếm được, chi tiêu và tiết kiệm mỗi tháng, cùng với mục tiêu bạn đang tiết kiệm. Mọi thứ được lưu trên trình duyệt này trong thiết bị của bạn.",
            "tracker.thisMonth": "Tháng này",
            "tracker.monthLabel": "<strong>Tháng</strong>",
            "tracker.earned": "Đã kiếm",
            "tracker.spent": "Đã chi",
            "tracker.saved": "Đã tiết kiệm",
            "tracker.left": "Còn lại",
            "tracker.addEntry": "Thêm một mục",
            "tracker.type": "Loại",
            "tracker.optIncome": "Thu nhập (đã kiếm)",
            "tracker.optExpense": "Chi tiêu (đã chi)",
            "tracker.optSaving": "Tiết kiệm (để dành)",
            "tracker.amount": "Số tiền (¥)",
            "tracker.noteLabel": "Đó là gì?",
            "tracker.notePlaceholder": "VD: lương Sukiya, tiền thuê nhà, ăn uống, tàu điện",
            "tracker.savingFor": "Tiết kiệm cho",
            "tracker.addEntryBtn": "Thêm mục",
            "tracker.goalsTitle": "Mục tiêu tiết kiệm",
            "tracker.newGoal": "Mục tiêu mới. Bạn đang tiết kiệm cho điều gì?",
            "tracker.goalPlaceholder": "VD: vé về Nepal, máy tính xách tay mới",
            "tracker.target": "Số tiền mục tiêu (¥)",
            "tracker.addGoal": "Thêm mục tiêu",
            "tracker.entries": "Các mục",
            "tracker.generalSavings": "Tiết kiệm chung",
            "tracker.noGoals": "Chưa có mục tiêu nào. Hãy thêm một mục tiêu bên dưới, ví dụ vé về quê hoặc máy tính xách tay mới.",
            "tracker.goalProgress": "{saved} trên {target} ({pct}%)",
            "tracker.noEntries": "Chưa có mục nào cho tháng này.",
            "tracker.tagIncome": "Thu nhập",
            "tracker.tagExpense": "Chi tiêu",
            "tracker.tagSaving": "Tiết kiệm",
            "tracker.forGoal": " · Cho: {name}",
            "tracker.delete": "Gỡ",
            "tracker.added": "Đã thêm.",
            "tracker.deleteGoal": "Xóa mục tiêu",
            "tracker.deleteGoalConfirm": "Xóa mục tiêu này? Các khoản tiết kiệm của bạn vẫn được giữ lại.",
            "tracker.saveFailed": "Không thể lưu. Bộ nhớ trình duyệt có thể đã đầy hoặc bị chặn.",
            "footer.disclaimer": "LifeBridge Lens là một dự án sinh viên độc lập và không liên kết với bất kỳ cơ quan chính phủ Nhật Bản nào. Thông tin được tóm tắt từ các nguồn chính thức; hãy luôn xác nhận với cơ quan liên quan.",
            "doc.mobileNav": "Di động",
            "doc.menu": "Menu",
            "nav.explainShort": "Lens",
            "explain.uploadTitle": "Chạm để chụp hoặc chọn ảnh",
            "explain.uploadHint": "Ảnh rõ nét toàn bộ thông báo sẽ cho kết quả tốt nhất",
            "explain.askLabel": "Hỏi thêm về thông báo này",
            "explain.explaining": "Đang đọc thông báo...",
            "explain.asking": "Đang hỏi...",
            "explain.badFormat": "Câu trả lời chưa rõ. Vui lòng thử lại với ảnh rõ nét hơn chụp toàn bộ thông báo.",
            "explain.tooSlow": "AI mất quá nhiều thời gian. Vui lòng thử lại.",
            "explain.serverError": "Lỗi máy chủ. Vui lòng thử lại.",
            "explain.sampleBtn": "Thử một thông báo mẫu",
            "explain.sampleTag": "Mẫu",
            "explain.sample.what": "Thông báo của thành phố: giấy nộp thuế cư trú (住民税)",
            "explain.sample.why": "Hóa đơn thuế cư trú hằng năm từ văn phòng thành phố.",
            "explain.sample.importance": "Cao. Hãy nộp trước hạn để tránh phí trễ hạn.",
            "explain.sample.next": "1. Kiểm tra số tiền và hạn nộp.\n2. Nộp tại ngân hàng hoặc cửa hàng tiện lợi.\n3. Giữ lại biên lai.",
            "explain.sample.deadline": "Ngày 1 tháng 2 năm 2027 (đợt 4)",
            "explain.sample.amount": "12.340 yên",
            "explain.sample.staff": "この保険料の支払いについて相談したいです。",
            "explain.sample.staffMeaning": "Tôi muốn hỏi về việc nộp khoản bảo hiểm này.",
            "explain.sample.check": "Tên và địa chỉ của bạn. Số tiền và hạn nộp.",
            "explain.saveDate": "Lưu thời hạn",
            "explain.dateSaved": "Đã lưu vào Ngày quan trọng.",
            "explain.dateExists": "Đã có trong Ngày quan trọng.",
            "explain.viewDates": "Xem trong Ngày quan trọng",
            "explain.viewDatesPage": "Xem Ngày quan trọng",
            "lens.title": "LifeBridge Lens",
            "lens.tagline": "Hiểu các thông báo chính thức của Nhật bằng ngôn ngữ của bạn.",
            "lens.scan": "Quét thông báo",
            "lens.dates": "Hạn của tôi",
            "lens.money": "Theo dõi tiền",
            "index.hero": "Nhận được thư tiếng Nhật mà bạn không đọc được? Hãy chụp ảnh và hiểu bằng ngôn ngữ của bạn.",
            "index.exampleLabel": "Ví dụ",
            "index.exampleAfter": "Đây là hóa đơn bảo hiểm y tế quốc dân của bạn, đợt 4. Hãy nộp 12.340 yên trước ngày 30 tháng 11 năm 2026.",
            "index.sub": "Thông báo của tòa thị chính, thuế, bảo hiểm và hóa đơn. Biết cần làm gì và trước khi nào.",
            "index.note": "AI có thể sai. Hãy đối chiếu số tiền và ngày với bức thư trước khi nộp.",
            "index.step1": "Chụp ảnh",
            "index.step2": "Đọc bằng ngôn ngữ của bạn",
            "index.step3": "Lưu thời hạn",
            "explain.checkDate": "Hãy đối chiếu ngày này với bức thư trước khi lưu.",
            "explain.confirmSave": "Xác nhận",
            "explain.addToCal": "Thêm vào lịch",
            "explain.hStaff": "Đưa cho nhân viên xem",
            "explain.copy": "Sao chép",
            "explain.copied": "Đã sao chép.",
            "explain.note": "AI có thể sai. Hãy xác nhận chi tiết quan trọng với văn phòng.",
            "explain.loadPrivacy": "Ảnh của bạn chỉ được gửi cho Meta AI và không lưu trên máy chủ của chúng tôi.",
            "explain.daysLeft": "Còn {n} ngày",
            "explain.dayLeft": "Còn 1 ngày",
            "explain.deadlinePassed": "Đã quá hạn",
            "explain.load1": "Đang đọc văn bản tiếng Nhật",
            "explain.load2": "Đang hiểu thông báo",
            "explain.load3": "Đang viết bằng ngôn ngữ của bạn",
            "explain.notShown": "Không có thông tin",
            "explain.saveDateLabel": "Ngày cần lưu",
            "explain.badDate": "Hãy chọn một ngày có thật từ lịch.",
            "explain.privacyHint": "Ảnh của bạn được gửi tới Meta AI. Hãy che các chi tiết không cần thiết, như số thẻ cư trú.",
            "tracker.goalError": "Vui lòng nhập tên mục tiêu và số tiền.",
            "tracker.deleteConfirm": "Xóa mục này?",
            "net.offline": "Bạn đang ngoại tuyến. Hãy kết nối internet rồi thử lại.",
            "chat.title": "Hỏi LifeBridge",
            "chat.placeholder": "Nhập câu hỏi...",
            "chat.send": "Gửi",
            "chat.open": "Mở trò chuyện",
            "chat.close": "Đóng trò chuyện",
            "chat.online": "Trực tuyến",
            "chat.offline": "Ngoại tuyến. Chỉ câu trả lời đã lưu",
            "net.banner": "Bạn đang ngoại tuyến. Hạn đã lưu, sổ tiền và trò chuyện vẫn dùng được.",
            "nav.moneyShort": "Tiền",
            "index.step1d": "Dùng camera điện thoại để chụp rõ toàn bộ tờ thông báo.",
            "index.step2d": "Nhận lời giải thích đơn giản về ý nghĩa và việc cần làm.",
            "index.step3d": "Lưu hạn nộp và số tiền để không bao giờ trễ hạn.",
            "explain.eraLabel": "Ngày theo lịch Nhật",
            "explain.loadingTitle": "Đang đọc thông báo",
            "explain.loadingLang": "Ngôn ngữ",
            "dates.upcoming": "Sắp đến",
            "dates.past": "Đã qua",
            "dates.completed": "Hoàn thành",
            "dates.markDone": "Đánh dấu xong",
            "dates.reopen": "Mở lại",
            "dates.prevMonth": "Tháng trước",
            "dates.nextMonth": "Tháng sau",
            "dates.calendarTitle": "Lịch",
            "dates.today": "Hôm nay",
            "offline.title": "Bạn đang ngoại tuyến",
            "offline.lead": "Hãy kết nối internet rồi thử lại.",
            "offline.retry": "Thử lại",
            "explain.hPayment": "Cách nộp tiền",
            "explain.hConsequences": "Nếu trễ hạn thì sao",
            "explain.sample.payment": "Hãy nộp tại ngân hàng hoặc cửa hàng tiện lợi bằng phiếu này. Giữ lại biên lai.",
            "explain.sample.consequences": "Bạn có thể bị cộng phí trễ hạn. Nếu không nộp kịp, hãy hỏi văn phòng thành phố."
        },
        my: {
            "nav.home": "ပင်မစာမျက်နှာ",
            "nav.deadlines": "သတ်မှတ်ရက်များ",
            "footer.tagline": "ဂျပန်အသိပေးစာများကို သင့်ဘာသာစကားဖြင့် နားလည်ပါ။",
            "hero.explain": "LifeBridge Lens",
            "topic.japanese.title": "ဂျပန်စာ",
            "journey.nav.dates": "အရေးကြီးသော ရက်စွဲများ",
            "app.noDates": "ရက်စွဲတစ်ခုမှ မထည့်ရသေးပါ။",
            "app.remove": "ဖယ်ရှားမယ်",
            "app.removeDate": "{t} ကို ဖယ်ရှားမယ်",
            "doc.skip": "အကြောင်းအရာဆီ ကျော်သွားမယ်",
            "doc.mainNavAria": "ပင်မ လမ်းညွှန်",
            "doc.langAria": "ဘာသာစကား",
            "doc.back": "← ပင်မစာမျက်နှာ",
            "doc.explore": "လေ့လာရန်",
            "doc.copyright": "© 2026 LifeBridge Lens · ဂျပန်ကို အခုမှရောက်လာသူတွေအတွက် ဖန်တီးထားသည်",
            "doc.backTop": "အပေါ်ဆုံးသို့ ပြန်သွားမယ် ↑",
            "money.trackerTitle": "ငွေကြေး မှတ်တမ်း",
            "dates.title": "အရေးကြီးသော ရက်စွဲများ | LifeBridge Lens",
            "dates.lead": "ရက်ချိန်းများနှင့် နောက်ဆုံးရက်စွဲများ တစ်နေရာတည်းတွင် ထားပါ။ ရက်စွဲများကို ဤဘရောင်ဇာတွင် သိမ်းထားပါသည်။ အကြောင်းကြားစာများ ပို့မည်မဟုတ်ပါ။",
            "dates.dateLabel": "ရက်စွဲ",
            "explain.title": "LifeBridge Lens",
            "explain.eyebrow": "စကင်န်ဖတ်ပြီး နားလည်ပါ",
            "explain.lead": "ဂျပန်စာ သို့မဟုတ် အကြောင်းကြားစာတစ်စောင် ဓာတ်ပုံရိုက်ပါ။ LifeBridge Lens က အဲဒါဘာလဲ၊ ဘာကြောင့်ရရှိတာလဲ၊ နောက်ဘာလုပ်ရမလဲဆိုတာ ရိုးရှင်းသောစကားလုံးများဖြင့် ပြောပြပေးပါမယ်။",
            "explain.step1": "<strong>1. အကြောင်းကြားစာဓာတ်ပုံ ရွေးပါ</strong>",
            "explain.step2": "<strong>2. သင့်ဘာသာစကား ရွေးပါ</strong>",
            "explain.optNepali": "နီပေါ",
            "explain.optEnglish": "အင်္ဂလိပ်",
            "explain.submit": "စကင်န်ဖတ်မယ်",
            "explain.resultTitle": "သင့်ရှင်းလင်းချက်",
            "explain.hWhat": "အဲဒါဘာလဲ?",
            "explain.hWhy": "ဘာကြောင့် ရရှိတာလဲ?",
            "explain.hImportance": "အဲဒါ ဘယ်လောက်အရေးကြီးလဲ?",
            "explain.hNext": "နောက်ဘာလုပ်ရမလဲ",
            "explain.hDeadline": "နောက်ဆုံးရက်စွဲ",
            "explain.hAmount": "ပမာဏ",
            "explain.hCheck": "စစ်ဆေးရမည့်အရာများ",
            "explain.needPhoto": "ကျေးဇူးပြု၍ ဦးစွာ ဓာတ်ပုံရွေးပါ။",
            "explain.reading": "သင့်အကြောင်းကြားစာ ဖတ်နေပါတယ်... စက္ကန့်အနည်းငယ် ကြာနိုင်ပါတယ်။",
            "explain.failed": "စိတ်မကောင်းပါဘူး၊ မအောင်မြင်ပါ: {msg}",
            "explain.followTitle": "နောက်ထပ်မေးခွန်းမေးပါ",
            "explain.qDeadline": "သတ်မှတ်ရက်ကျော်ရင် ဘာဖြစ်မလဲ?",
            "explain.qWhere": "ဘယ်မှာပေးချေရမလဲ၊ ဘယ်မှာလုပ်ရမလဲ?",
            "explain.qDocs": "ဘာစာရွက်စာတမ်းတွေလိုအပ်လဲ?",
            "explain.qUrgent": "ဒါ အရေးကြီးလား?",
            "explain.askPlaceholder": "ဒီအကြောင်းကြားစာအကြောင်း တခြားမေးစရာမေးပါ...",
            "explain.ask": "မေးပါ",
            "tracker.title": "ငွေကြေး မှတ်တမ်း | LifeBridge Lens",
            "tracker.lead": "လတိုင်း ဘာဝင်ငွေရတယ်၊ ဘာသုံးတယ်၊ ဘာစုတယ်ဆိုတာ, နဲ့ ဘာအတွက်စုနေတာလဲဆိုတာ ရိုးရှင်းစွာ မှတ်တမ်းထားပါ။ အားလုံးက သင့်စက်ရှိ ဤဘရောင်ဇာထဲမှာပဲ ရှိနေပါမယ်။",
            "tracker.thisMonth": "ဒီလ",
            "tracker.monthLabel": "<strong>လ</strong>",
            "tracker.earned": "ဝင်ငွေ",
            "tracker.spent": "အသုံးစရိတ်",
            "tracker.saved": "စုငွေ",
            "tracker.left": "ကျန်ငွေ",
            "tracker.addEntry": "မှတ်တမ်းထည့်မယ်",
            "tracker.type": "အမျိုးအစား",
            "tracker.optIncome": "ဝင်ငွေ (ရရှိသော)",
            "tracker.optExpense": "အသုံးစရိတ် (သုံးသော)",
            "tracker.optSaving": "စုငွေ (ဖယ်ထားသော)",
            "tracker.amount": "ပမာဏ (¥)",
            "tracker.noteLabel": "အဲဒါ ဘာလဲ?",
            "tracker.notePlaceholder": "ဥပမာ- Sukiya လစာ၊ အိမ်လခ၊ အစားအသောက်၊ ရထား",
            "tracker.savingFor": "ဘာအတွက်စုနေသလဲ",
            "tracker.addEntryBtn": "မှတ်တမ်း ထည့်မယ်",
            "tracker.goalsTitle": "စုငွေ ရည်မှန်းချက်များ",
            "tracker.newGoal": "ရည်မှန်းချက်အသစ်။ ဘာအတွက်စုနေသလဲ?",
            "tracker.goalPlaceholder": "ဥပမာ- နီပေါ ပြန်လက်မှတ်၊ လက်ပ်တော့အသစ်",
            "tracker.target": "ရည်မှန်းချက်ပမာဏ (¥)",
            "tracker.addGoal": "ရည်မှန်းချက် ထည့်မယ်",
            "tracker.entries": "မှတ်တမ်းများ",
            "tracker.generalSavings": "အထွေထွေစုငွေ",
            "tracker.noGoals": "ရည်မှန်းချက်တစ်ခုမှ မရှိသေးပါ။ အောက်မှာ တစ်ခုထည့်ပါ, ဥပမာ အိမ်ပြန်လက်မှတ် သို့မဟုတ် လက်ပ်တော့အသစ်။",
            "tracker.goalProgress": "{target} အနက် {saved} ({pct}%)",
            "tracker.noEntries": "ဒီလအတွက် မှတ်တမ်းတစ်ခုမှ မရှိသေးပါ။",
            "tracker.tagIncome": "ဝင်ငွေ",
            "tracker.tagExpense": "အသုံးစရိတ်",
            "tracker.tagSaving": "စုငွေ",
            "tracker.forGoal": " · အတွက်- {name}",
            "tracker.delete": "ဖယ်ရှားမယ်",
            "tracker.added": "ထည့်ပြီးပြီ။",
            "tracker.deleteGoal": "ပန်းတိုင် ဖယ်ရှားမယ်",
            "tracker.deleteGoalConfirm": "ဒီပန်းတိုင် ဖျက်မလား။ သင့်စုငွေမှတ်တမ်းတွေ ကျန်နေမယ်။",
            "tracker.saveFailed": "သိမ်းလို့မရပါ။ browser သိုလှောင်မှု ပြည့်နေတာ (သို့) ပိတ်ထားတာ ဖြစ်နိုင်တယ်။",
            "footer.disclaimer": "LifeBridge Lens သည် လွတ်လပ်သော ကျောင်းသားပရောဂျက် ဖြစ်ပြီး ဂျပန်အစိုးရအေဂျင်စီတစ်ခုခုနှင့် ဆက်စပ်မှုမရှိပါ။ အချက်အလက်များကို တရားဝင်ရင်းမြစ်များမှ အကျဉ်းချုပ်ထားပါသည်။ သက်ဆိုင်ရာရုံးနှင့် အမြဲအတည်ပြုပါ။",
            "doc.mobileNav": "မိုဘိုင်း",
            "doc.menu": "မီနူး",
            "nav.explainShort": "Lens",
            "explain.uploadTitle": "ဓာတ်ပုံရိုက်ရန် သို့မဟုတ် ရွေးရန် တို့ပါ",
            "explain.uploadHint": "အကြောင်းကြားစာတစ်ခုလုံးကို ရှင်းလင်းစွာရိုက်ထားသော ဓာတ်ပုံ အကောင်းဆုံးပါ",
            "explain.askLabel": "ဒီအကြောင်းကြားစာအကြောင်း နောက်ထပ်မေးပါ",
            "explain.explaining": "အကြောင်းကြားစာ ဖတ်နေပါသည်...",
            "explain.asking": "မေးနေပါသည်...",
            "explain.badFormat": "အဖြေ မရှင်းလင်းပါ။ အကြောင်းကြားစာတစ်ခုလုံးကို ရှင်းလင်းစွာရိုက်ပြီး ထပ်ကြိုးစားပါ။",
            "explain.tooSlow": "AI က အချိန်အကြာကြီးယူသည်။ ကျေးဇူးပြု၍ ထပ်စမ်းပါ။",
            "explain.serverError": "ဆာဗာအမှား။ ကျေးဇူးပြု၍ ထပ်စမ်းပါ။",
            "explain.sampleBtn": "နမူနာ အကြောင်းကြားစာ စမ်းကြည့်ပါ",
            "explain.sampleTag": "နမူနာ",
            "explain.sample.what": "မြို့တော်ရုံးအကြောင်းကြားစာ - နေထိုင်ခွန်အခွန် (住民税) ပေးချေရေးစာရွက်",
            "explain.sample.why": "မြို့တော်ရုံးမှ နှစ်စဉ်နေထိုင်ခွန်အခွန်ကျသင့်လွှာ။",
            "explain.sample.importance": "မြင့်မားပါတယ်။ နောက်ကျဒဏ်ကြေးမထိရန် သတ်မှတ်ရက်မတိုင်မီ ပေးပါ။",
            "explain.sample.next": "1. ပမာဏနှင့် သတ်မှတ်ရက်ကို စစ်ဆေးပါ။\n2. ဘဏ် သို့မဟုတ် ကွန်ဘိနိတွင် ပေးပါ။\n3. ပြေစာသိမ်းပါ။",
            "explain.sample.deadline": "၂၀၂၇ ဖေဖော်ဝါရီ ၁ (စတုတ္ထအရစ်ကျ)",
            "explain.sample.amount": "12,340 ယန်း",
            "explain.sample.staff": "この保険料の支払いについて相談したいです。",
            "explain.sample.staffMeaning": "ဒီအာမခံကြေးပေးချေရေးနဲ့ ပတ်သက်ပြီး မေးချင်ပါတယ်။",
            "explain.sample.check": "သင့်အမည်နှင့် လိပ်စာ။ ပမာဏနှင့် သတ်မှတ်ရက်။",
            "explain.saveDate": "သတ်မှတ်ရက်ကို သိမ်းပါ",
            "explain.dateSaved": "အရေးကြီးရက်စွဲများတွင် သိမ်းပြီးပြီ။",
            "explain.dateExists": "အရေးကြီးရက်စွဲများတွင် ရှိနှင့်ပြီးပြီ။",
            "explain.viewDates": "အရေးကြီးရက်စွဲများတွင် ကြည့်မယ်",
            "explain.viewDatesPage": "အရေးကြီးသော ရက်စွဲများ ကြည့်ရန်",
            "lens.title": "LifeBridge Lens",
            "lens.tagline": "ဂျပန်အစိုးရစာရွက်များကို သင့်ဘာသာစကားဖြင့် နားလည်ပါ။",
            "lens.scan": "စာရွက်စကင်န်ဖတ်ပါ",
            "lens.dates": "ကျွန်တော့်နောက်ဆုံးရက်များ",
            "lens.money": "ငွေစာရင်း",
            "index.hero": "မဖတ်တတ်သော ဂျပန်စာရရှိလား? ဓာတ်ပုံရိုက်ပြီး သင့်ဘာသာစကားဖြင့် နားလည်ပါ။",
            "index.exampleLabel": "ဥပမာ",
            "index.exampleAfter": "ဒါက သင့်အမျိုးသားကျန်းမာရေးအာမခံကြေးကျသင့်လွှာ၊ စတုတ္ထအရစ်ကျပါ။ ၂၀၂၆ နိုဝင်ဘာ ၃၀ မတိုင်မီ 12,340 ယန်း ပေးပါ။",
            "index.sub": "မြို့တော်ရုံး၊ အခွန်၊ အာမခံနဲ့ ဘေလ်စာရွက်များ။ ဘာလုပ်ရမယ်၊ ဘယ်တော့အထိလဲဆိုတာ သိပါ။",
            "index.note": "AI မှားနိုင်ပါတယ်။ မပေးခင် ပမာဏနဲ့ ရက်စွဲကို စာနဲ့ တိုက်စစ်ပါ။",
            "index.step1": "ဓာတ်ပုံရိုက်ပါ",
            "index.step2": "သင့်ဘာသာစကားနဲ့ ဖတ်ပါ",
            "index.step3": "သတ်မှတ်ရက်ကို သိမ်းပါ",
            "explain.checkDate": "မသိမ်းမီ ဤရက်စွဲကို စာရွက်နှင့် တိုက်စစ်ပါ။",
            "explain.confirmSave": "အတည်ပြုပါ",
            "explain.addToCal": "ပြက္ခဒိန်ထဲ ထည့်ပါ",
            "explain.hStaff": "ဝန်ထမ်းကို ဒါ ပြပါ",
            "explain.copy": "ကူးယူမယ်",
            "explain.copied": "ကူးယူပြီးပြီ။",
            "explain.note": "AI မှားနိုင်ပါတယ်။ အရေးကြီးတာတွေ ရုံးနဲ့ အတည်ပြုပါ။",
            "explain.loadPrivacy": "သင့်ဓာတ်ပုံကို Meta AI ဆီပဲ ပို့ပြီး ကျွန်တော်တို့ဆာဗာမှာ မသိမ်းပါဘူး။",
            "explain.daysLeft": "{n} ရက် ကျန်ပါတယ်",
            "explain.dayLeft": "1 ရက် ကျန်ပါတယ်",
            "explain.deadlinePassed": "သတ်မှတ်ရက် ကျော်သွားပါပြီ",
            "explain.load1": "ဂျပန်စာသားကို ဖတ်နေပါတယ်",
            "explain.load2": "အကြောင်းကြားစာကို နားလည်နေပါတယ်",
            "explain.load3": "သင့်ဘာသာစကားနဲ့ ရေးနေပါတယ်",
            "explain.notShown": "မပြထားပါ",
            "explain.saveDateLabel": "သိမ်းရမည့်ရက်",
            "explain.badDate": "ပြက္ခဒိန်မှ ရက်စွဲအမှန် ရွေးပါ။",
            "explain.privacyHint": "သင့်ဓာတ်ပုံကို Meta AI သို့ ပေးပို့ပါတယ်။ မလိုအပ်သော အသေးစိတ်များ၊ ဥပမာ နေထိုင်ခွင့်ကတ်နံပါတ်ကို ဖုံးအုပ်ပါ။",
            "tracker.goalError": "ပန်းတိုင်အမည်နှင့် ပမာဏ ထည့်ပေးပါ။",
            "tracker.deleteConfirm": "ဒီမှတ်တမ်း ဖျက်မလား။",
            "net.offline": "အင်တာနက် ပြတ်နေပါသည်။ ချိတ်ဆက်ပြီး ထပ်ကြိုးစားပါ။",
            "chat.title": "LifeBridge ကို မေးပါ",
            "chat.placeholder": "မေးခွန်း ရိုက်ထည့်ပါ...",
            "chat.send": "ပို့ပါ",
            "chat.open": "စကားပြောဖွင့်ပါ",
            "chat.close": "စကားပြောပိတ်ပါ",
            "chat.online": "အွန်လိုင်း",
            "chat.offline": "အော့ဖ်လိုင်း။ သိမ်းထားသော အဖြေများသာ",
            "net.banner": "အင်တာနက် ပြတ်နေပါသည်။ သိမ်းထားသော ရက်စွဲများ၊ ငွေစာရင်းနှင့် စကားပြော ရနေပါသည်။",
            "nav.moneyShort": "ငွေ",
            "index.step1d": "အကြောင်းကြားစာတစ်ခုလုံးကို ဖုန်းကင်မရာဖြင့် ရှင်းလင်းစွာ ရိုက်ပါ။",
            "index.step2d": "အဓိပ္ပာယ်နှင့် လုပ်ရမည့်အရာကို ရိုးရှင်းစွာ ရှင်းပြချက် ရယူပါ။",
            "index.step3d": "သတ်မှတ်ရက်နှင့် ပမာဏကို သိမ်းထားပြီး လုံးဝမလွတ်စေပါနဲ့။",
            "explain.eraLabel": "ဂျပန်ရက်စွဲ",
            "explain.loadingTitle": "သင့်စာကို ဖတ်နေပါတယ်",
            "explain.loadingLang": "ဘာသာစကား",
            "dates.upcoming": "လာမည့်",
            "dates.past": "ကုန်လွန်ခဲ့သော",
            "dates.completed": "ပြီးစီးသော",
            "dates.markDone": "ပြီးပြီအဖြစ် သတ်မှတ်ပါ",
            "dates.reopen": "ပြန်ဖွင့်ပါ",
            "dates.prevMonth": "ယခင်လ",
            "dates.nextMonth": "နောက်လ",
            "dates.calendarTitle": "ပြက္ခဒိန်",
            "dates.today": "ယနေ့",
            "offline.title": "သင် အော့ဖ်လိုင်းဖြစ်နေပါတယ်",
            "offline.lead": "အင်တာနက် ချိတ်ဆက်ပြီး ထပ်ကြိုးစားပါ။",
            "offline.retry": "ထပ်ကြိုးစားပါ",
            "explain.hPayment": "ဘယ်လိုပေးရမလဲ",
            "explain.hConsequences": "သတ်မှတ်ရက်ကျော်ရင် ဘာဖြစ်မလဲ",
            "explain.sample.payment": "ဤစာရွက်ဖြင့် ဘဏ် သို့မဟုတ် ကွန်ဘိနိတွင် ပေးပါ။ ပြေစာသိမ်းပါ။",
            "explain.sample.consequences": "နောက်ကျဒဏ်ကြေး ထပ်တိုးနိုင်ပါတယ်။ အချိန်မီမပေးနိုင်ပါက မြို့တော်ရုံးတွင် မေးပါ။"
        }
    };

    function getLang() {
        try {
            var saved = window.localStorage.getItem(STORE_KEY);
            if (SUPPORTED.indexOf(saved) !== -1) return saved;
        } catch (e) { /* private mode etc. - fall through to English */ }
        return "en";
    }

    function lookup(lang, key) {
        if (I18N[lang] && I18N[lang][key] !== undefined) return I18N[lang][key];
        return I18N.en[key];
    }

    // Current-language lookup with English fallback. Never throws, so classic
    // scripts running before this deferred file can call it unconditionally.
    function t(key) {
        try {
            var lang = getLang();
            if (I18N[lang] && I18N[lang][key] !== undefined) return I18N[lang][key];
            if (I18N.en[key] !== undefined) return I18N.en[key];
        } catch (e) { /* fall through to the key itself */ }
        return key;
    }

    function apply(lang) {
        if (SUPPORTED.indexOf(lang) === -1) lang = "en";
        document.documentElement.setAttribute("lang", lang);

        var i, el, key, value;

        var textEls = document.querySelectorAll("[data-i18n]");
        for (i = 0; i < textEls.length; i++) {
            el = textEls[i];
            key = el.getAttribute("data-i18n");
            value = lookup(lang, key);
            if (value !== undefined) el.textContent = value;
        }

        var htmlEls = document.querySelectorAll("[data-i18n-html]");
        for (i = 0; i < htmlEls.length; i++) {
            el = htmlEls[i];
            key = el.getAttribute("data-i18n-html");
            value = lookup(lang, key);
            if (value !== undefined) el.innerHTML = value;
        }

        var phEls = document.querySelectorAll("[data-i18n-placeholder]");
        for (i = 0; i < phEls.length; i++) {
            el = phEls[i];
            key = el.getAttribute("data-i18n-placeholder");
            value = lookup(lang, key);
            if (value !== undefined) el.setAttribute("placeholder", value);
        }

        var ariaEls = document.querySelectorAll("[data-i18n-aria-label]");
        for (i = 0; i < ariaEls.length; i++) {
            el = ariaEls[i];
            key = el.getAttribute("data-i18n-aria-label");
            value = lookup(lang, key);
            if (value !== undefined) el.setAttribute("aria-label", value);
        }

        var altEls = document.querySelectorAll("[data-i18n-alt]");
        for (i = 0; i < altEls.length; i++) {
            el = altEls[i];
            key = el.getAttribute("data-i18n-alt");
            value = lookup(lang, key);
            if (value !== undefined) el.setAttribute("alt", value);
        }

        var select = document.getElementById("lang-select");
        if (select) select.value = lang;

        try {
            document.dispatchEvent(new CustomEvent("lb:lang", { detail: { lang: lang } }));
        } catch (e) {
            try {
                var ev = document.createEvent("CustomEvent");
                ev.initCustomEvent("lb:lang", false, false, { lang: lang });
                document.dispatchEvent(ev);
            } catch (e2) { /* very old browser: JS re-render is skipped */ }
        }
    }

    function setLang(lang) {
        if (SUPPORTED.indexOf(lang) === -1) lang = "en";
        try {
            window.localStorage.setItem(STORE_KEY, lang);
        } catch (e) { /* ignore - translations still apply for this page view */ }
        apply(lang);
    }

    // ------------------------------------------------------------
    // Shared site chrome: current-page mark, mobile menu button,
    // profile link, bottom nav, theme and service worker.
    // This file loads on every page, so one place covers all pages.
    // ------------------------------------------------------------
    var THEME_KEY = "lb_theme";

    function currentPageName() {
        try {
            var name = window.location.pathname.split("/").pop() || "index.html";
            return name.split("?")[0].split("#")[0] || "index.html";
        } catch (e) {
            return "index.html";
        }
    }

    function markCurrentNav(page) {
        var links = document.querySelectorAll(".main-nav a");
        for (var i = 0; i < links.length; i++) {
            var href = String(links[i].getAttribute("href") || "").split("?")[0].split("#")[0];
            if (href === page) {
                links[i].setAttribute("aria-current", "page");
                if ((" " + links[i].className + " ").indexOf(" active ") === -1) {
                    links[i].className += (links[i].className ? " " : "") + "active";
                }
            } else {
                links[i].removeAttribute("aria-current");
                links[i].className = (" " + links[i].className + " ").replace(/ active /g, " ").replace(/^\s+|\s+$/g, "");
            }
        }
    }

    function addMenuButton() {
        var header = document.querySelector(".header-cnt");
        var nav = document.querySelector(".main-nav");
        if (!header || !nav || document.querySelector(".menu-btn")) return;
        nav.id = "main-nav";
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "menu-btn";
        btn.setAttribute("aria-expanded", "false");
        btn.setAttribute("aria-controls", "main-nav");
        var label = document.createElement("span");
        label.setAttribute("data-i18n", "doc.menu");
        label.textContent = "Menu";
        btn.appendChild(label);
        btn.addEventListener("click", function () {
            var isOpen = (" " + nav.className + " ").indexOf(" open ") !== -1;
            if (isOpen) {
                nav.className = (" " + nav.className + " ").replace(/ open /g, " ").replace(/^\s+|\s+$/g, "");
                btn.setAttribute("aria-expanded", "false");
            } else {
                nav.className += " open";
                btn.setAttribute("aria-expanded", "true");
            }
        });
        header.insertBefore(btn, nav);
    }

    function addBottomNav(page) {
        if (document.querySelector(".bottom-nav")) return;
        var nav = document.createElement("nav");
        nav.className = "bottom-nav";
        nav.setAttribute("data-i18n-aria-label", "doc.mobileNav");
        nav.setAttribute("aria-label", "Mobile");
        var items = [
            ["index.html", "nav.home", "Home", '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h5v-6h4v6h5V10"/>'],
            ["explain.html", "nav.explainShort", "Lens", '<circle cx="11" cy="11" r="7"/><path d="M16 16l5 5"/>'],
            ["dates.html", "nav.deadlines", "Deadlines", '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'],
            ["tracker.html", "nav.moneyShort", "Money", '<rect x="3" y="7" width="18" height="12" rx="2"/><path d="M3 10h18M16 15h2"/>']
        ];
        for (var i = 0; i < items.length; i++) {
            var a = document.createElement("a");
            a.href = items[i][0];
            var icon = document.createElement("span");
            icon.className = "nav-icon";
            icon.setAttribute("aria-hidden", "true");
            icon.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + items[i][3] + "</svg>";
            var label = document.createElement("span");
            label.setAttribute("data-i18n", items[i][1]);
            label.textContent = items[i][2];
            a.appendChild(icon);
            a.appendChild(label);
            if (items[i][0] === page) a.setAttribute("aria-current", "page");
            nav.appendChild(a);
        }
        document.body.appendChild(nav);
    }

    function themePreference() {
        try {
            var saved = window.localStorage.getItem(THEME_KEY);
            if (saved === "light" || saved === "dark") return saved;
        } catch (e) { /* fall through to system */ }
        try {
            if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
                return "dark";
            }
        } catch (e) { /* fall through to light */ }
        return "light";
    }

    function applyTheme() {
        document.documentElement.setAttribute("data-theme", themePreference());
    }

    window.LBTheme = {
        get: themePreference,
        set: function (theme) {
            if (theme !== "light" && theme !== "dark" && theme !== "system") theme = "system";
            try {
                if (theme === "system") {
                    window.localStorage.removeItem(THEME_KEY);
                } else {
                    window.localStorage.setItem(THEME_KEY, theme);
                }
            } catch (e) { /* private mode: apply for this view only */ }
            applyTheme();
        }
    };

    function registerWorker() {
        try {
            if ("serviceWorker" in navigator && window.location.protocol.indexOf("http") === 0) {
                window.addEventListener("load", function () {
                    navigator.serviceWorker.register("sw.js").catch(function () { /* offline stays off */ });
                });
            }
        } catch (e) { /* ignore */ }
    }

    function loadChatbot() {
        try {
            if (window.LBChat || document.querySelector('script[data-lb-chat]')) return;
            var script = document.createElement("script");
            script.src = "chatbot.js";
            script.defer = true;
            script.setAttribute("data-lb-chat", "1");
            document.head.appendChild(script);
        } catch (e) { /* chat stays unavailable */ }
    }

    function addOfflineBanner() {
        if (document.querySelector(".net-banner")) return;
        var banner = document.createElement("div");
        banner.className = "net-banner";
        banner.setAttribute("role", "status");
        banner.setAttribute("data-i18n", "net.banner");
        banner.textContent = "You are offline. Saved guides and chat still work.";
        banner.hidden = true;
        document.body.insertBefore(banner, document.body.firstChild);
        var update = function () {
            try {
                banner.hidden = typeof navigator === "undefined" || navigator.onLine !== false;
            } catch (e) { banner.hidden = true; }
        };
        window.addEventListener("online", update);
        window.addEventListener("offline", update);
        update();
    }

    function siteChrome() {
        try { document.documentElement.className += " js"; } catch (e) { /* ignore */ }
        var page = currentPageName();
        try { markCurrentNav(page); } catch (e) { /* ignore */ }
        try { addMenuButton(); } catch (e) { /* ignore */ }
        try { addBottomNav(page); } catch (e) { /* ignore */ }
        try { addOfflineBanner(); } catch (e) { /* ignore */ }
        try { applyTheme(); } catch (e) { /* ignore */ }
        try { registerWorker(); } catch (e) { /* ignore */ }
        try { loadChatbot(); } catch (e) { /* ignore */ }
    }

    document.addEventListener("DOMContentLoaded", function () {
        siteChrome();
        var select = document.getElementById("lang-select");
        if (select) {
            select.addEventListener("change", function () {
                setLang(select.value);
            });
        }
        apply(getLang());
    });

    window.LifeBridgeI18n = { apply: apply, set: setLang, get: getLang, t: t };
    window.LBT = {
        t: t,
        lang: getLang,
        onChange: function (fn) {
            try {
                document.addEventListener("lb:lang", function (event) {
                    var lang = getLang();
                    try {
                        if (event && event.detail && event.detail.lang) lang = event.detail.lang;
                    } catch (e) { /* keep getLang() value */ }
                    fn(lang);
                });
            } catch (e) { /* document unavailable: ignore */ }
        }
    };
})();