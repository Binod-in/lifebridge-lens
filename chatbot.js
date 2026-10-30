/* LifeBridge Japan offline chatbot.
 * Rule-based answers from the saved guides. No network needed.
 * Loaded on every page by i18n.js (deferred, cached by the service worker).
 * The knowledge base below is JSON-compatible (double quotes only) so the
 * Python test suite can parse and validate it. Keep it that way.
 */
(function () {
    "use strict";
    if (window.LBChat && window.LBChat.ready) return;

    var LB_CHAT_KB = [
        {
            "id": "greeting",
            "links": [],
            "keys": {
                "en": ["hello", "hey", "good morning", "good afternoon", "good evening", "namaste"],
                "ne": ["नमस्ते", "नमस्कार", "हेलो"],
                "vi": ["xin chao", "xin chào", "chào bạn", "hello"],
                "my": ["မင်္ဂလာပါ", "ဟယ်လို"],
                "ja": ["こんにちは"]
            },
            "answers": {
                "en": "Hello! Ask me about address, bank, jobs, health, transport, or emergencies. I answer from the saved guides, even offline.",
                "ne": "नमस्ते! ठेगाना, बैंक, काम, स्वास्थ्य, यातायात वा आपतकालबारे सोध्नुहोस्। सेभ गरिएका गाइडबाट जवाफ दिन्छु, अफलाइन पनि।",
                "vi": "Xin chào! Hãy hỏi về địa chỉ, ngân hàng, việc làm, sức khỏe, giao thông hoặc khẩn cấp. Tôi trả lời từ hướng dẫn đã lưu, kể cả khi ngoại tuyến.",
                "my": "မင်္ဂလာပါ! လိပ်စာ၊ ဘဏ်၊ အလုပ်၊ ကျန်းမာရေး၊ သယ်ယူပို့ဆောင်ရေး သို့မဟုတ် အရေးပေါ်အကြောင်း မေးပါ။ သိမ်းထားသော လမ်းညွှန်များမှ ဖြေပေးပါတယ်၊ အော့ဖ်လိုင်းလည်း ရပါတယ်။"
            }
        },
        {
            "id": "lost-residence",
            "links": [],
            "keys": {
                "en": ["lost residence card", "lost my residence card", "zairyu", "zairyu card", "reissue"],
                "ne": ["निवास कार्ड हरायो", "हराएको निवास कार्ड"],
                "vi": ["mất thẻ cư trú", "mat the cu tru"],
                "my": ["နေထိုင်ခွင့်ကတ် ပျောက်"],
                "ja": ["在留カード"]
            },
            "answers": {
                "en": "For a lost residence card, report to the police first, then apply at the immigration office for reissue within 14 days. Carry the police report.",
                "ne": "निवास कार्ड हराए पहिले प्रहरीमा रिपोर्ट गर्नुहोस्, अनि १४ दिनभित्र अध्यागमन कार्यालयमा पुनः बनाउन आवेदन दिनुहोस्। प्रहरी रिपोर्ट साथ लैजानुहोस्।",
                "vi": "Nếu mất thẻ cư trú, hãy báo cảnh sát trước, sau đó nộp đơn làm lại tại cục xuất nhập cảnh trong vòng 14 ngày. Mang theo biên bản báo mất.",
                "my": "နေထိုင်ခွင့်ကတ် ပျောက်ပါက အရင် ရဲစခန်းတွင် တိုင်ကြားပြီး ၁၄ ရက်အတွင်း လူဝင်မှုရုံးတွင် ပြန်လျှောက်ပါ။ ရဲတိုင်စာ ယူသွားပါ။"
            }
        },
        {
            "id": "lost-general",
            "links": [],
            "keys": {
                "en": ["lost", "lose", "missing", "stolen", "lost property", "lost and found", "koban", "police box"],
                "ne": ["हरायो", "हराएको", "चोरी", "हराएको सामान"],
                "vi": ["mất", "đánh mất", "đồ thất lạc"],
                "my": ["ပျောက်", "ပျောက်ဆုံး", "ပျောက်ဆုံးပစ္စည်း"],
                "ja": ["紛失", "なくし", "落とし物", "交番"]
            },
            "answers": {
                "en": "For lost items, report to the nearest police box (koban) or the station lost-and-found. Bring ID and describe what you lost.",
                "ne": "सामान हराए नजिकको प्रहरी बाकस (koban) वा स्टेसनको हराएको सामान काउन्टरमा रिपोर्ट गर्नुहोस्। परिचयपत्र लैजानुहोस् र के हरायो बताउनुहोस्।",
                "vi": "Nếu mất đồ, hãy báo cho đồn cảnh sát (koban) gần nhất hoặc quầy đồ thất lạc ở ga. Mang giấy tờ và mô tả món đồ đã mất.",
                "my": "ပစ္စည်းပျောက်ပါက အနီးဆုံး ရဲကင်း (koban) သို့မဟုတ် ဘူတာ ပျောက်ဆုံးပစ္စည်းကောင်တာတွင် တိုင်ကြားပါ။ မှတ်ပုံတင် ယူသွားပြီး ပျောက်သောပစ္စည်း ဖော်ပြပါ။"
            }
        },
        {
            "id": "emergency",
            "links": [],
            "keys": {
                "en": ["emergency", "police", "fire", "ambulance", "110", "119", "7119", "accident"],
                "ne": ["आपतकाल", "प्रहरी", "पुलिस", "दमकल", "एम्बुलेन्स", "११०", "११९", "दुर्घटना"],
                "vi": ["khẩn cấp", "khan cap", "cảnh sát", "cứu hỏa", "cấp cứu"],
                "my": ["အရေးပေါ်", "ရဲ", "မီးသတ်", "လူနာတင်"],
                "ja": ["緊急", "警察", "救急"]
            },
            "answers": {
                "en": "Police: 110. Ambulance or fire: 119. Medical advice: #7119. Foreign residents can call FRESC: 0570-011000 (weekdays). For visa/residence questions: 0570-013904. Details are in the Emergency guide.",
                "ne": "प्रहरी: ११०। एम्बुलेन्स वा दमकल: ११९। चिकित्सा सल्लाह: #7119। विदेशी बासिन्दाले FRESC मा फोन गर्न सक्छन्: 0570-011000 (हप्ताका दिन)। भिसा/बसोबासका प्रश्नका लागि: 0570-013904। विवरण Emergency गाइडमा छ।",
                "vi": "Cảnh sát: 110. Cấp cứu hoặc cứu hỏa: 119. Tư vấn y tế: #7119. Người nước ngoài cư trú có thể gọi FRESC: 0570-011000 (các ngày trong tuần). Câu hỏi về visa/cư trú: 0570-013904. Chi tiết trong hướng dẫn Emergency.",
                "my": "ရဲ - ၁၁၀။ လူနာတင် သို့မဟုတ် မီးသတ် - ၁၁၉။ ဆေးဘက်ဆိုင်ရာ အကြံဉာဏ် - #7119။ နိုင်ငံခြားသား နေထိုင်သူများ FRESC သို့ ဖုန်းဆက်နိုင်ပါတယ် - 0570-011000 (တနင်္လာမှ သောကြာ)။ ဗီဇာ/နေထိုင်ခွင့်မေးခွန်းများ - 0570-013904။ အသေးစိတ်ကို Emergency လမ်းညွှန်တွင် ကြည့်ပါ။"
            }
        },
        {
            "id": "address",
            "links": [],
            "keys": {
                "en": ["address", "register", "registration", "move in", "moving in", "moving-in", "tennyu", "ward office", "city office", "residence card"],
                "ne": ["ठेगाना", "दर्ता", "सर्ने", "वार्ड", "निवास कार्ड", "रेसिडेन्स"],
                "vi": ["địa chỉ", "dia chi", "đăng ký", "dang ky", "chuyển đến", "chuyển nhà", "thẻ cư trú", "the cu tru"],
                "my": ["လိပ်စာ", "မှတ်ပုံ", "ပြောင်းရွှေ့", "နေထိုင်ခွင့်ကတ်"],
                "ja": ["住所", "転入"]
            },
            "answers": {
                "en": "Register your address at the city or ward office within 14 days of moving in. Bring your residence card and passport.",
                "ne": "सरेको १४ दिनभित्र सिटी वा वार्ड कार्यालयमा ठेगाना दर्ता गर्नुहोस्। निवास कार्ड र राहदानी लैजानुहोस्।",
                "vi": "Đăng ký địa chỉ tại văn phòng thành phố hoặc quận trong 14 ngày sau khi chuyển đến. Mang thẻ cư trú và hộ chiếu.",
                "my": "ပြောင်းရွှေ့ပြီး ၁၄ ရက်အတွင်း မြို့ သို့မဟုတ် ရပ်ကွက်ရုံးတွင် လိပ်စာ မှတ်ပုံတင်ပါ။ နေထိုင်ခွင့်ကတ်နှင့် နိုင်ငံကူးလက်မှတ် ယူသွားပါ။"
            }
        },
        {
            "id": "pension",
            "links": [],
            "keys": {
                "en": ["pension", "nenkin", "retirement"],
                "ne": ["पेन्सन", "निवृत्तिभरण", "नेन्किन"],
                "vi": ["lương hưu", "luong huu", "nenkin", "hưu trí", "huu tri"],
                "my": ["ပင်စင်", "နန်ကင်း"],
                "ja": ["年金"]
            },
            "answers": {
                "en": "Almost everyone must join the pension system (nenkin). Employees pay through their company; others pay at banks and other financial institutions, post offices, or convenience stores with the payment slip, or by bank transfer / Pay-easy — never at the city/ward office counter. Students can apply for the student payment deferral (学生納付特例) at the ward office or pension office.",
                "ne": "लगभग सबैजना पेन्सन प्रणाली (नेन्किन) मा जोडिनुपर्छ। कर्मचारीले कम्पनीमार्फत तिर्छन्; अरूले भुक्तानी पर्चीले बैंक तथा वित्तीय संस्था, हुलाक वा सुविधा पसलमा तिर्छन्, वा बैंक ट्रान्सफर / Pay-easy बाट तिर्छन् — सहर/वार्ड कार्यालयको काउन्टरमा कहिल्यै तिर्न पाइँदैन। विद्यार्थीले विद्यार्थी भुक्तानी स्थगन (学生納付特例) का लागि वार्ड कार्यालय वा पेन्सन कार्यालयमा आवेदन दिन सक्छन्।",
                "vi": "Hầu như ai cũng phải tham gia bảo hiểm hưu trí (nenkin). Người đi làm đóng qua công ty; các trường hợp khác đóng tại ngân hàng và các tổ chức tài chính khác, bưu điện hoặc cửa hàng tiện lợi bằng phiếu nộp tiền, hoặc bằng chuyển khoản ngân hàng / Pay-easy — không bao giờ đóng tại quầy văn phòng thành phố/quận. Sinh viên có thể xin hoãn đóng theo diện sinh viên (学生納付特例) tại văn phòng quận hoặc văn phòng hưu trí.",
                "my": "လူတိုင်းနီးပါး ပင်စင်စနစ် (နန်ကင်း) တွင် ပါဝင်ရပါတယ်။ ဝန်ထမ်းများ ကုမ္ပဏီမှတစ်ဆင့် ပေးပြီး ကျန်သူများ ငွေပေးစာရွက်ဖြင့် ဘဏ်နှင့် အခြားဘဏ္ဍာရေးအဖွဲ့အစည်းများ၊ စာတိုက် သို့မဟုတ် ကွန်ဘိနိတွင် ပေးပြီး၊ သို့မဟုတ် ဘဏ်လွှဲ / Pay-easy ဖြင့် ပေးပါတယ် — မြို့/ရပ်ကွက်ရုံး ကောင်တာတွင် မပေးရပါ။ ကျောင်းသားများက ကျောင်းသားပေးချေမှုရွှေ့ဆိုင်းရေး (学生納付特例) ကို ရပ်ကွက်ရုံး သို့မဟုတ် ပင်စင်ရုံးတွင် လျှောက်ထားနိုင်ပါတယ်။"
            }
        },
        {
            "id": "bank",
            "links": [],
            "keys": {
                "en": ["bank", "banking", "bank app", "open account", "bank account", "salary", "remittance"],
                "ne": ["बैंक", "खाता", "तलब"],
                "vi": ["ngân hàng", "ngan hang", "tài khoản", "tai khoan", "lương", "luong"],
                "my": ["ဘဏ်", "အကောင့်", "လစာ"],
                "ja": ["銀行", "口座"]
            },
            "answers": {
                "en": "Choose a bank and open an account with your residence card and address proof. Ask about fees and language support. Some banks limit accounts for people who have lived in Japan for less than 6 months, so ask the bank first.",
                "ne": "बैंक छान्नुहोस् र निवास कार्ड र ठेगाना प्रमाणसहित खाता खोल्नुहोस्। शुल्क र भाषा सहयोगबारे सोध्नुहोस्। जापानमा 6 महिनाभन्दा कम बसेकालाई केही बैंकले खातामा सीमा लगाउँछन्, त्यसैले पहिले बैंकसँग सोध्नुहोस्।",
                "vi": "Chọn ngân hàng và mở tài khoản bằng thẻ cư trú và giấy tờ địa chỉ. Hỏi về phí và hỗ trợ ngôn ngữ. Một số ngân hàng hạn chế tài khoản đối với người sống ở Nhật dưới 6 tháng, vì vậy hãy hỏi ngân hàng trước.",
                "my": "ဘဏ်ရွေးပြီး နေထိုင်ခွင့်ကတ်နှင့် လိပ်စာအထောက်အထားဖြင့် အကောင့်ဖွင့်ပါ။ အခကြေးငွေနှင့် ဘာသာစကား အကူအညီအကြောင်း မေးပါ။ ဂျပန်တွင် ၆ လအောက် နေထိုင်သူများကို ဘဏ်အချို့က အကောင့်ကန့်သတ်ထားသဖြင့် ဦးစွာ ဘဏ်ကို မေးပါ။"
            }
        },
        {
            "id": "garbage",
            "links": [],
            "keys": {
                "en": ["garbage", "trash", "rubbish", "gomi", "burnable", "non-burnable", "recycle", "recycling", "sorting"],
                "ne": ["फोहोर", "गोमि", "जल्ने फोहोर", "रिसाइकल"],
                "vi": ["rác", "rac", "gomi", "phân loại rác", "tái chế", "tai che"],
                "my": ["အမှိုက်", "ဂိုမီ", "ခွဲခြား"],
                "ja": ["ごみ", "ゴミ", "分別", "燃えるごみ"]
            },
            "answers": {
                "en": "Sort garbage by your city's rules: burnable, non-burnable, and recyclables go out on different days. Check your city's garbage calendar or the ward office.",
                "ne": "आफ्नो सहरको नियमअनुसार फोहोर छुट्याउनुहोस्: जल्ने, नजल्ने र रिसाइकल फरक-फरक दिन जान्छ। सहरको फोहोर पात्रो वा वार्ड कार्यालयमा हेर्नुहोस्।",
                "vi": "Hãy phân loại rác theo quy định của thành phố: rác cháy được, rác không cháy được và rác tái chế đổ vào các ngày khác nhau. Xem lịch đổ rác hoặc hỏi văn phòng quận.",
                "my": "မြို့စည်းမျဉ်းအတိုင်း အမှိုက်ခွဲပါ - မီးလောင်နိုင်သော၊ မလောင်နိုင်သော၊ ပြန်လည်အသုံးပြုနိုင်သော အမှိုက်များကို မတူညီသောနေ့များတွင် စွန့်ပါ။ မြို့အမှိုက်ပြက္ခဒိန် သို့မဟုတ် ရပ်ကွက်ရုံးတွင် ကြည့်ပါ။"
            }
        },
        {
            "id": "tax",
            "links": [],
            "keys": {
                "en": ["tax", "taxes", "resident tax", "income tax", "tax office", "tax return", "nenmatsu", "year-end"],
                "ne": ["कर", "आयकर", "निवासी कर", "कर कार्यालय", "ट्याक्स"],
                "vi": ["thuế", "thue", "thuế thu nhập", "khai thuế", "cục thuế"],
                "my": ["အခွန်", "ဝင်ငွေခွန်", "အခွန်ရုံး"],
                "ja": ["税金", "住民税", "所得税", "確定申告"]
            },
            "answers": {
                "en": "Residents pay income tax and residence tax. Employees usually pay through their company; ask your employer or the ward office for your notice.",
                "ne": "बासिन्दाले आयकर र निवासी कर तिर्नुपर्छ। कर्मचारीले प्रायः कम्पनीमार्फत तिर्छन्; सूचना पत्रका लागि रोजगारदाता वा वार्ड कार्यालयसँग सोध्नुहोस्।",
                "vi": "Người dân đóng thuế thu nhập và thuế cư trú. Người đi làm thường đóng qua công ty; hãy hỏi công ty hoặc văn phòng quận về giấy báo thuế.",
                "my": "နေထိုင်သူများ ဝင်ငွေခွန်နှင့် နေထိုင်ခွန် ပေးရပါတယ်။ ဝန်ထမ်းများ ပုံမှန်အားဖြင့် ကုမ္ပဏီမှတစ်ဆင့် ပေးပါတယ်။ အခွန်စာရွက်အတွက် အလုပ်ရှင် သို့မဟုတ် ရပ်ကွက်ရုံးကို မေးပါ။"
            }
        },
        {
            "id": "visa",
            "links": [],
            "keys": {
                "en": ["visa", "renewal", "renew", "status of residence", "zairyu", "zairyu period", "zairyu card", "residence card", "immigration"],
                "ne": ["भिसा", "नवीकरण", "अध्यागमन", "भिसा थप्ने", "निवास कार्ड"],
                "vi": ["visa", "thị thực", "thi thuc", "gia hạn", "cục xuất nhập cảnh"],
                "my": ["ဗီဇာ", "သက်တမ်းတိုး", "လူဝင်မှု"],
                "ja": ["ビザ", "在留期間", "在留資格", "在留カード", "更新", "入国管理局"]
            },
            "answers": {
                "en": "You can apply from about 3 months before your period of stay expires. Apply to renew your visa at the immigration office before it expires. Bring your residence card, passport, a photo, and the application form. From October 1, 2026 the renewal fee depends on the period you get, for example ¥33,000 for 1 year (¥6,000 if you applied by September 30, 2026). Check the official ISA page for your case.",
                "ne": "बसाइँ अवधि सकिनुभन्दा करिब ३ महिनाअघिदेखि आवेदन दिन पाइन्छ। भिसा सकिनुअघि अध्यागमन कार्यालयमा नवीकरणका लागि आवेदन दिनुहोस्। निवास कार्ड, राहदानी, फोटो र आवेदन फारम लैजानुहोस्। अक्टोबर 1, 2026 देखि नवीकरण शुल्क पाउने अवधिअनुसार फरक हुन्छ, जस्तै 1 वर्षका लागि ¥33,000 (सेप्टेम्बर 30, 2026 सम्म आवेदन दिएको भए ¥6,000)। आफ्नो हकमा आधिकारिक ISA पृष्ठ हेर्नुहोस्।",
                "vi": "Bạn có thể nộp đơn từ khoảng 3 tháng trước khi thời gian lưu trú hết hạn. Hãy xin gia hạn visa tại cục xuất nhập cảnh trước khi hết hạn. Mang thẻ cư trú, hộ chiếu, một ảnh thẻ và đơn xin gia hạn. Từ ngày 1 tháng 10 năm 2026, lệ phí gia hạn tùy theo thời hạn bạn được cấp, ví dụ ¥33.000 cho 1 năm (¥6.000 nếu bạn nộp đơn trước ngày 30 tháng 9 năm 2026). Hãy xem trang ISA chính thức cho trường hợp của bạn.",
                "my": "နေထိုင်ခွင့်ကာလ မကုန်မီ ၃ လခန့်အလိုမှစ၍ လျှောက်ထားနိုင်ပါတယ်။ ဗီဇာမကုန်မီ လူဝင်မှုရုံးတွင် သက်တမ်းတိုးလျှောက်ပါ။ နေထိုင်ခွင့်ကတ်၊ နိုင်ငံကူးလက်မှတ်၊ ဓာတ်ပုံနှင့် လျှောက်လွှာပုံစံ ယူသွားပါ။ ၂၀၂၆ အောက်တိုဘာ ၁ ရက်မှစ၍ သက်တမ်းတိုးခက ရရှိသောကာလအလိုက် ကွဲပြားပြီး ဥပမာ ၁ နှစ်အတွက် ¥33,000 (၂၀၂၆ စက်တင်ဘာ ၃၀ ရက်မတိုင်မီ လျှောက်ထားပါက ¥6,000) ဖြစ်ပါတယ်။ သင့်အခြေအနေအတွက် တရားဝင် ISA စာမျက်နှာ ကြည့်ပါ။"
            }
        },
        {
            "id": "mynumber",
            "links": [],
            "keys": {
                "en": ["my number", "mynumber", "my-number", "individual number", "maina"],
                "ne": ["माई नम्बर", "माइ नम्बर", "व्यक्तिगत नम्बर"],
                "vi": ["my number", "mã số cá nhân", "ma so ca nhan", "thẻ my number"],
                "my": ["မိုင်နမ်ဘာ", "ကိုယ်ပိုင်နံပါတ်"],
                "ja": ["マイナンバー", "個人番号"]
            },
            "answers": {
                "en": "My Number is your personal ID number in Japan. Use your My Number card. If you do not have one, ask the office or employer which proof they accept (for example a residence certificate 住民票 that shows your number). The paper notice 個人番号通知書 is not accepted as proof of your number.",
                "ne": "माई नम्बर जापानमा तपाईंको व्यक्तिगत परिचय नम्बर हो। आफ्नो माई नम्बर कार्ड प्रयोग गर्नुहोस्। कार्ड छैन भने कुन प्रमाणपत्र चाहिन्छ भनेर कार्यालय वा रोजगारदातालाई सोध्नुहोस् (जस्तै नम्बर देखिने住民票 निवास प्रमाणपत्र)। कागजको सूचना 個人番号通知書 लाई नम्बरको प्रमाण मानिँदैन।",
                "vi": "My Number là mã số định danh cá nhân của bạn ở Nhật. Hãy dùng thẻ My Number của bạn. Nếu chưa có, hãy hỏi cơ quan hoặc công ty xem họ chấp nhận giấy tờ nào (ví dụ giấy chứng nhận cư trú 住民票 có ghi mã số). Tờ giấy báo 個人番号通知書 không được chấp nhận làm bằng chứng mã số.",
                "my": "မိုင်နမ်ဘာသည် ဂျပန်တွင် သင့်ကိုယ်ပိုင်မှတ်ပုံတင်နံပါတ် ဖြစ်ပါတယ်။ သင့် My Number ကတ် အသုံးပြုပါ။ ကတ်မရှိသေးပါက မည်သည့်အထောက်အထားကို လက်ခံသည်ကို ရုံး သို့မဟုတ် အလုပ်ရှင်အား မေးပါ (ဥပမာ နံပါတ်ပါသော 住民票 နေထိုင်မှုအထောက်အထားစာရွက်)။ စက္ကူအကြောင်းကြားစာ 個人番号通知書 ကို နံပါတ်အထောက်အထားအဖြစ် လက်မခံပါ။"
            }
        },
        {
            "id": "work",
            "links": [],
            "keys": {
                "en": ["job", "work", "part-time", "part time", "baito", "arubaito", "28 hours", "permission", "interview", "resume"],
                "ne": ["काम", "जागिर", "बैतो", "पार्ट", "अनुमति", "२८"],
                "vi": ["việc", "viec", "làm thêm", "lam them", "giấy phép", "giay phep", "28 giờ", "phỏng vấn"],
                "my": ["အလုပ်", "အချိန်ပိုင်း", "ခွင့်ပြုချက်", "၂၈"],
                "ja": ["仕事", "アルバイト", "許可"]
            },
            "answers": {
                "en": "Students need work permission before starting. During school terms the limit is 28 hours a week in total for all part-time jobs combined. During long school holidays set by the school, students can work up to 8 hours a day (40 hours a week). Check with your school.",
                "ne": "विद्यार्थीले काम सुरु गर्नुअघि अनुमति चाहिन्छ। पढाइ चल्दा सबै पार्ट-टाइम काम जोडेर हप्तामा जम्मा २८ घण्टाको सीमा छ। विद्यालयले तोकेको लामो बिदामा दिनमा ८ घण्टासम्म (हप्तामा ४० घण्टा) काम गर्न पाइन्छ। विद्यालयसँग बुझ्नुहोस्।",
                "vi": "Du học sinh cần giấy phép trước khi làm việc. Trong học kỳ, giới hạn là tổng cộng 28 giờ mỗi tuần cho mọi việc làm thêm cộng lại. Trong các kỳ nghỉ dài do trường quy định, sinh viên có thể làm tới 8 giờ mỗi ngày (40 giờ mỗi tuần). Hãy hỏi trường của bạn.",
                "my": "ကျောင်းသားများ အလုပ်မစမီ ခွင့်ပြုချက် လိုပါတယ်။ ကျောင်းဖွင့်ချိန်တွင် အချိန်ပိုင်းအလုပ်အားလုံးပေါင်း တစ်ပတ် စုစုပေါင်း ၂၈ နာရီ ကန့်သတ်ထားပါတယ်။ ကျောင်းသတ်မှတ်သည့် ပိတ်ရက်ရှည်များတွင် တစ်ရက် ၈ နာရီအထိ (တစ်ပတ် ၄၀ နာရီ) လုပ်နိုင်ပါတယ်။ ကျောင်းနှင့် မေးပါ။"
            }
        },
        {
            "id": "health",
            "links": [],
            "keys": {
                "en": ["insurance", "health", "hospital", "doctor", "sick", "clinic", "medicine"],
                "ne": ["बीमा", "स्वास्थ्य", "अस्पताल", "डाक्टर", "बिरामी"],
                "vi": ["bảo hiểm", "bao hiem", "sức khỏe", "suc khoe", "bệnh viện", "benh vien", "bác sĩ", "bac si", "ốm"],
                "my": ["အာမခံ", "ကျန်းမာရေး", "ဆေးရုံ", "ဆရာဝန်"],
                "ja": ["保険", "病院", "病気"]
            },
            "answers": {
                "en": "Join a health insurance plan through your city office, school, or employer. Bring your My Number health insurance card (マイナ保険証) or 資格確認書 (eligibility certificate) to the clinic.",
                "ne": "सिटी कार्यालय, विद्यालय वा रोजगारदातामार्फत स्वास्थ्य बीमामा जोडिनुहोस्। क्लिनिक जाँदा माई नम्बर स्वास्थ्य बीमा कार्ड (マイナ保険証) वा 資格確認書 (योग्यता प्रमाणपत्र) लैजानुहोस्।",
                "vi": "Tham gia bảo hiểm y tế qua văn phòng thành phố, trường học hoặc công ty. Khi đi khám, mang thẻ bảo hiểm y tế My Number (マイナ保険証) hoặc 資格確認書 (giấy chứng nhận đủ điều kiện).",
                "my": "မြို့ရုံး၊ ကျောင်း သို့မဟုတ် အလုပ်ရှင်မှတစ်ဆင့် ကျန်းမာရေးအာမခံတွင် ပါဝင်ပါ။ ဆေးခန်းသွားလျှင် My Number ကျန်းမာရေးအာမခံကတ် (マイナ保険証) သို့မဟုတ် 資格確認書 (အရည်အချင်းပြည့်မီရေး လက်မှတ်) ယူသွားပါ။"
            }
        },
        {
            "id": "transport",
            "links": [],
            "keys": {
                "en": ["ic card", "suica", "pasmo", "train", "bus", "station", "commute"],
                "ne": ["आईसी", "रेल", "बस", "स्टेसन"],
                "vi": ["thẻ ic", "the ic", "tàu", "tau", "xe buýt", "xe buyt", "ga"],
                "my": ["ic ကတ်", "ရထား", "ဘတ်စ်ကား", "ဘူတာ"],
                "ja": ["電車", "バス"]
            },
            "answers": {
                "en": "Get an IC card at station ticket machines. The card name differs by region (Suica, PASMO, ICOCA and others). Tap it on trains and buses.",
                "ne": "स्टेसनका टिकट मेसिनबाट आईसी कार्ड लिनुहोस्। क्षेत्रअनुसार कार्डको नाम फरक हुन्छ (Suica, PASMO, ICOCA र अन्य)। रेल र बसमा ट्याप गर्नुहोस्।",
                "vi": "Mua thẻ IC tại các máy bán vé ở ga. Tên thẻ khác nhau tùy vùng (Suica, PASMO, ICOCA và các loại khác). Quẹt thẻ khi đi tàu và xe buýt.",
                "my": "ဘူတာလက်မှတ်စက်များတွင် IC ကတ် ဝယ်ပါ။ ဒေသအလိုက် ကတ်အမည် မတူပါ (Suica, PASMO, ICOCA နှင့် အခြား)။ ရထားနှင့် ဘတ်စ်ကားတွင် တို့သုံးပါ။"
            }
        },
        {
            "id": "sim",
            "links": [],
            "keys": {
                "en": ["sim", "mobile", "phone", "smartphone"],
                "ne": ["सिम", "मोबाइल", "फोन"],
                "vi": ["sim", "điện thoại", "dien thoai"],
                "my": ["ဆင်းမ်", "ဖုန်း"],
                "ja": ["携帯"]
            },
            "answers": {
                "en": "You can get a SIM card at mobile shops and electronics stores. Bring your residence card and ask about monthly plans.",
                "ne": "मोबाइल पसल र इलेक्ट्रोनिक्स पसलबाट सिम कार्ड लिन सक्नुहुन्छ। निवास कार्ड लैजानुहोस् र मासिक योजनाबारे सोध्नुहोस्।",
                "vi": "Bạn có thể mua SIM tại cửa hàng di động và điện máy. Mang thẻ cư trú và hỏi về gói cước hàng tháng.",
                "my": "မိုဘိုင်းဆိုင်နှင့် လျှပ်စစ်ပစ္စည်းဆိုင်များတွင် ဆင်းမ်ကတ် ဝယ်နိုင်ပါတယ်။ နေထိုင်ခွင့်ကတ် ယူသွားပြီး လစဉ်ပက်ကေ့ချ်အကြောင်း မေးပါ။"
            }
        },
        {
            "id": "lost-phone",
            "links": [],
            "keys": {
                "en": ["lost", "lose", "missing", "stolen", "my phone", "find my"],
                "ne": ["हरायो", "हराएको", "चोरी", "फोन", "मोबाइल"],
                "vi": ["mất", "đánh mất", "điện thoại", "dien thoai"],
                "my": ["ပျောက်", "ပျောက်ဆုံး", "ဖုန်း"],
                "ja": ["紛失", "なくし", "携帯", "スマホ", "電話"]
            },
            "answers": {
                "en": "For a lost phone: lock it with Find My iPhone or Android, call your carrier to pause the line, and report to the police. Your carrier shop can reissue the SIM.",
                "ne": "फोन हराए: Find My iPhone वा Android बाट लक गर्नुहोस्, लाइन रोक्न क्यारियरलाई फोन गर्नुहोस्, अनि प्रहरीमा रिपोर्ट गर्नुहोस्। क्यारियर पसलबाट सिम फेरि निकाल्न सकिन्छ।",
                "vi": "Nếu mất điện thoại: khóa máy bằng Find My iPhone hoặc Android, gọi nhà mạng để tạm khóa, rồi báo cảnh sát. Cửa hàng nhà mạng có thể cấp lại SIM.",
                "my": "ဖုန်းပျောက်ပါက Find My iPhone သို့မဟုတ် Android ဖြင့် လော့ခ်ချပြီး လိုင်းရပ်ရန် အော်ပရေတာကို ဖုန်းဆက်ကာ ရဲစခန်းတွင် တိုင်ကြားပါ။ အော်ပရေတာဆိုင်တွင် ဆင်းမ်ကတ် ပြန်ထုတ်နိုင်ပါတယ်။"
            }
        },
        {
            "id": "lost-wallet",
            "links": [],
            "keys": {
                "en": ["lost", "lose", "missing", "stolen", "wallet", "my wallet", "purse", "bank card", "cash card"],
                "ne": ["हरायो", "हराएको", "चोरी", "वालेट", "पर्स", "बैंक कार्ड"],
                "vi": ["mất", "đánh mất", "ví", "vi", "thẻ ngân hàng"],
                "my": ["ပျောက်", "ပျောက်ဆုံး", "ပိုက်ဆံအိတ်", "ဘဏ်ကတ်"],
                "ja": ["紛失", "なくし", "財布", "キャッシュカード"]
            },
            "answers": {
                "en": "For a lost wallet or bank card: call your bank right away to stop the card, then report to the police. Bring ID to reissue the card.",
                "ne": "वालेट वा बैंक कार्ड हराए: कार्ड रोक्न तुरुन्त बैंकलाई फोन गर्नुहोस्, अनि प्रहरीमा रिपोर्ट गर्नुहोस्। कार्ड फेरि बनाउन परिचयपत्र लैजानुहोस्।",
                "vi": "Nếu mất ví hoặc thẻ ngân hàng: gọi ngay cho ngân hàng để khóa thẻ, rồi báo cảnh sát. Mang giấy tờ để làm lại thẻ.",
                "my": "ပိုက်ဆံအိတ် သို့မဟုတ် ဘဏ်ကတ် ပျောက်ပါက ကတ်ပိတ်ရန် ဘဏ်ကို ချက်ချင်းဖုန်းဆက်ပြီး ရဲစခန်းတွင် တိုင်ကြားပါ။ ကတ်ပြန်ထုတ်ရန် မှတ်ပုံတင် ယူသွားပါ။"
            }
        },
        {
            "id": "japanese",
            "links": [],
            "keys": {
                "en": ["japanese", "phrase", "speak", "talk", "say", "language"],
                "ne": ["जापानी", "वाक्य", "बोल्ने", "भाषा"],
                "vi": ["tiếng nhật", "tieng nhat", "mẫu câu", "mau cau", "nói"],
                "my": ["ဂျပန်", "စကားစု", "ပြော"],
                "ja": ["日本語"]
            },
            "answers": {
                "en": "Use the Japanese phrase helper: pick a situation, listen, copy, or save the phrase for later.",
                "ne": "जापानी वाक्य सहयोग प्रयोग गर्नुहोस्: अवस्था छान्नुहोस्, सुन्नुहोस्, कपी वा सेभ गर्नुहोस्।",
                "vi": "Hãy dùng công cụ mẫu câu tiếng Nhật: chọn tình huống, nghe, sao chép hoặc lưu mẫu câu.",
                "my": "ဂျပန်စကားစု အကူအညီ သုံးပါ - အခြေအနေ ရွေးပြီး နားထောင်၊ ကူး သို့မဟုတ် သိမ်းထားပါ။"
            }
        },
        {
            "id": "thanks",
            "links": [],
            "keys": {
                "en": ["thank", "thanks", "great", "good"],
                "ne": ["धन्यवाद", "राम्रो"],
                "vi": ["cảm ơn", "cam on", "hay"],
                "my": ["ကျေးဇူး", "ကောင်း"],
                "ja": ["ありがとう"]
            },
            "answers": {
                "en": "You are welcome! Ask anytime.",
                "ne": "तपाईंलाई स्वागत छ! जुनसुकै बेला सोध्नुहोस्।",
                "vi": "Không có gì! Hãy hỏi bất cứ lúc nào.",
                "my": "ရပါတယ်! အချိန်မရွေး မေးပါ။"
            }
        },
        {
            "id": "housing",
            "links": [],
            "keys": {
                "en": ["rent", "apartment", "room", "deposit", "key money"],
                "ne": ["भाडा", "कोठा", "अपार्टमेन्ट", "धरौटी"],
                "vi": ["thuê nhà", "thue nha", "căn hộ", "can ho", "phòng", "phong", "tiền cọc", "tien coc"],
                "my": ["ငှားခ", "အခန်း", "တိုက်ခန်း", "စပေါ်"],
                "ja": ["賃貸", "アパート", "部屋", "敷金", "礼金"]
            },
            "answers": {
                "en": "Decide your budget first: initial costs often equal 4 to 6 months of rent (deposit 敷金, key money 礼金, agent fee). Visit rooms in person, and register your new address at the ward office within 14 days of moving.",
                "ne": "पहिले बजेट तय गर्नुहोस्: सुरुका खर्च प्रायः ४ देखि ६ महिनाको भाडा बराबर हुन्छन् (धरौटी 敷金, key money 礼金, एजेन्ट शुल्क)। कोठा आफैं गएर हेर्नुहोस्, र सरेको १४ दिनभित्र वार्ड कार्यालयमा ठेगाना दर्ता गर्नुहोस्।",
                "vi": "Hãy quyết định ngân sách trước: chi phí ban đầu thường bằng 4 đến 6 tháng tiền thuê (tiền cọc 敷金, tiền lễ 礼金, phí môi giới). Đến xem phòng trực tiếp, và đăng ký địa chỉ mới tại văn phòng quận trong 14 ngày sau khi chuyển đến.",
                "my": "အရင်ဦးဆုံး ဘတ်ဂျက်သတ်မှတ်ပါ - အစပိုင်းကုန်ကျစရိတ်များသည် ပုံမှန်အားဖြင့် လခ ၄ လမှ ၆ လစာခန့် ရှိတတ်ပါသည် (စပေါ် 敷金၊ key money 礼金၊ ပွဲစားခ)။ အခန်းကို ကိုယ်တိုင်သွားကြည့်ပြီး ပြောင်းပြီး ၁၄ ရက်အတွင်း ရပ်ကွက်ရုံးတွင် လိပ်စာအသစ် မှတ်ပုံတင်ပါ။"
            }
        },
        {
            "id": "earthquake",
            "links": [],
            "keys": {
                "en": ["earthquake", "disaster", "typhoon", "tsunami", "quake"],
                "ne": ["भूकम्प"],
                "vi": ["động đất", "dong dat"],
                "my": ["ငလျင်"],
                "ja": ["地震", "台風"]
            },
            "answers": {
                "en": "In an earthquake, protect your head and move to a safe place first. Call 119 for fire or ambulance. Say your location clearly and follow official instructions.",
                "ne": "भूकम्प जाँदा पहिले टाउको जोगाउनुहोस् र सुरक्षित ठाउँमा जानुहोस्। दमकल वा एम्बुलेन्सका लागि 119 मा फोन गर्नुहोस्। ठेगाना स्पष्ट भन्नुहोस् र आधिकारिक निर्देशन पालना गर्नुहोस्।",
                "vi": "Khi động đất, trước tiên hãy bảo vệ đầu và di chuyển đến nơi an toàn. Gọi 119 cho cứu hỏa hoặc cấp cứu. Nói rõ vị trí của bạn và làm theo hướng dẫn chính thức.",
                "my": "ငလျင်လှုပ်လျှင် အရင် ဦးခေါင်းကာကွယ်ပြီး လုံခြုံသောနေရာသို့ရွှေ့ပါ။ မီးသတ်နှင့် လူနာတင်ယာဉ်အတွက် 119 ကိုခေါ်ပါ။ တည်နေရာကို ရှင်းလင်းစွာပြောပြီး တရားဝင်ညွှန်ကြားချက်များ လိုက်နာပါ။"
            }
        },
        {
            "id": "fallback",
            "links": [],
            "keys": {},
            "answers": {
                "en": "I answer from the saved guides. Try asking about address, bank, jobs, health, transport, or emergencies.",
                "ne": "म सेभ गरिएका गाइडबाट जवाफ दिन्छु। ठेगाना, बैंक, काम, स्वास्थ्य, यातायात वा आपतकालबारे सोध्नुहोस्।",
                "vi": "Tôi trả lời từ các hướng dẫn đã lưu. Hãy hỏi về địa chỉ, ngân hàng, việc làm, sức khỏe, giao thông hoặc khẩn cấp.",
                "my": "သိမ်းထားသော လမ်းညွှန်များမှ ဖြေပေးပါတယ်။ လိပ်စာ၊ ဘဏ်၊ အလုပ်၊ ကျန်းမာရေး၊ သယ်ယူပို့ဆောင်ရေး သို့မဟုတ် အရေးပေါ်အကြောင်း မေးပါ။"
            }
        }
    ];

    var LB_CHAT_SUGGEST = {
        "en": ["How do I register my address?", "How do I open a bank account?", "Can students work part-time?", "Emergency numbers?"],
        "ne": ["ठेगाना कसरी दर्ता गर्ने?", "बैंक खाता कसरी खोल्ने?", "विद्यार्थीले काम गर्न मिल्छ?", "आपतकालीन नम्बर?"],
        "vi": ["Đăng ký địa chỉ thế nào?", "Mở tài khoản ngân hàng thế nào?", "Du học sinh được làm thêm không?", "Số khẩn cấp?"],
        "my": ["လိပ်စာ ဘယ်လိုမှတ်ပုံတင်ရမလဲ။", "ဘဏ်အကောင့် ဘယ်လိုဖွင့်ရမလဲ။", "ကျောင်းသား အလုပ်လုပ်လို့ရလား။", "အရေးပေါ်ဖုန်းနံပါတ်။"]
    };

    function chatT(key, fallback) {
        try {
            if (window.LBT && typeof window.LBT.t === "function") {
                var value = window.LBT.t(key);
                if (typeof value === "string" && value !== "" && value !== key) return value;
            }
        } catch (e) { /* fall through */ }
        return fallback;
    }

    function chatLang() {
        try {
            if (window.LBT && typeof window.LBT.lang === "function") {
                var lang = window.LBT.lang();
                if (lang === "en" || lang === "ne" || lang === "vi" || lang === "my") return lang;
            }
            var htmlLang = document.documentElement.getAttribute("lang");
            if (htmlLang === "en" || htmlLang === "ne" || htmlLang === "vi" || htmlLang === "my") return htmlLang;
        } catch (e) { /* fall through */ }
        return "en";
    }

    function normalize(text) {
        var value = String(text || "");
        try {
            if (typeof value.normalize === "function") value = value.normalize("NFKC");
        } catch (e) { /* keep raw */ }
        // Punctuation becomes spaces, so "phone." still matches "phone".
        var noPunct = value.toLowerCase().replace(/[.,!?;:()\[\]"「」、。！？・]/g, " ");
        return " " + noPunct.replace(/\s+/g, " ").trim() + " ";
    }

    function findBest(input) {
        var text = normalize(input);
        var best = null;
        var bestScore = 0;
        for (var i = 0; i < LB_CHAT_KB.length; i++) {
            var intent = LB_CHAT_KB[i];
            if (!intent || intent.id === "fallback") continue;
            var score = 0;
            var groups = intent.keys || {};
            for (var lang in groups) {
                if (!Object.prototype.hasOwnProperty.call(groups, lang)) continue;
                var words = groups[lang] || [];
                // Latin-script keywords match whole words only, so "ga"
                // does not match inside "garbage". Other scripts keep
                // substring matching, since they don't use spaces.
                var wholeWords = (lang === "en" || lang === "vi");
                for (var w = 0; w < words.length; w++) {
                    var word = normalize(words[w]).replace(/^\s+|\s+$/g, "");
                    if (!word) continue;
                    if (wholeWords) {
                        if (text.indexOf(" " + word + " ") !== -1) score++;
                    } else if (text.indexOf(word) !== -1) {
                        score++;
                    }
                }
            }
            if (score > bestScore) {
                bestScore = score;
                best = intent;
            }
        }
        if (!best) {
            for (var j = 0; j < LB_CHAT_KB.length; j++) {
                if (LB_CHAT_KB[j] && LB_CHAT_KB[j].id === "fallback") return LB_CHAT_KB[j];
            }
        }
        return best;
    }

    function linkLabel(href) {
        var id = String(href || "").replace(/\.html$/, "");
        try {
            if (typeof guideData !== "undefined" && typeof guideTitle === "function") {
                for (var i = 0; i < guideData.length; i++) {
                    if (guideData[i] && guideData[i].id === id) return guideTitle(guideData[i]);
                }
            }
        } catch (e) { /* fall through */ }
        return id ? id.charAt(0).toUpperCase() + id.slice(1) : href;
    }

    function safeHref(href) {
        return /^([a-z-]+\.html)$/.test(String(href || "")) ? href : null;
    }

    var fab = null;
    var panel = null;
    var msgs = null;
    var chips = null;
    var form = null;
    var input = null;
    var sendBtn = null;
    var titleEl = null;
    var statusEl = null;
    var closeBtn = null;
    var backdrop = null;
    var greeted = false;

    function addMsg(text, who) {
        var div = document.createElement("div");
        div.className = who === "user" ? "chat-msg-user" : "chat-msg-bot";
        div.textContent = text;
        msgs.appendChild(div);
        var time = document.createElement("div");
        time.className = who === "user" ? "chat-time user" : "chat-time bot";
        try {
            time.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        } catch (e) { time.textContent = ""; }
        msgs.appendChild(time);
        msgs.scrollTop = msgs.scrollHeight;
    }

    function addLinks(links) {
        if (!links || !links.length) return;
        var row = document.createElement("div");
        row.className = "chat-links";
        for (var i = 0; i < links.length; i++) {
            var href = safeHref(links[i]);
            if (!href) continue;
            var a = document.createElement("a");
            a.className = "chat-link";
            a.href = href;
            a.textContent = linkLabel(href) + " →";
            row.appendChild(a);
        }
        if (row.childNodes.length) {
            msgs.appendChild(row);
            msgs.scrollTop = msgs.scrollHeight;
        }
    }

    function showSuggestions() {
        chips.replaceChildren();
        var list = LB_CHAT_SUGGEST[chatLang()] || LB_CHAT_SUGGEST.en;
        for (var i = 0; i < list.length; i++) {
            var btn = document.createElement("button");
            btn.type = "button";
            btn.className = "chip";
            btn.textContent = list[i];
            btn.addEventListener("click", function () {
                sendText(this.textContent);
            });
            chips.appendChild(btn);
        }
    }

    function answer(inputText) {
        var intent = findBest(inputText);
        if (!intent) return;
        var lang = chatLang();
        var answers = intent.answers || {};
        addMsg(answers[lang] || answers.en || "", "bot");
        addLinks(intent.links);
    }

    function sendText(text) {
        text = String(text || "").trim();
        if (!text) return;
        addMsg(text, "user");
        answer(text);
        showSuggestions();
    }

    function isOffline() {
        try {
            return typeof navigator !== "undefined" && navigator.onLine === false;
        } catch (e) { return false; }
    }

    function updateStatus() {
        if (isOffline()) {
            statusEl.textContent = chatT("chat.offline", "Offline — saved answers only");
        } else {
            statusEl.textContent = chatT("chat.online", "Online");
        }
    }

    function refreshChrome() {
        fab.setAttribute("aria-label", chatT("chat.open", "Open chat"));
        titleEl.textContent = chatT("chat.title", "Ask LifeBridge");
        updateStatus();
        closeBtn.setAttribute("aria-label", chatT("chat.close", "Close chat"));
        var ph = chatT("chat.placeholder", "Type your question...");
        input.setAttribute("placeholder", ph);
        input.setAttribute("aria-label", ph);
        sendBtn.textContent = chatT("chat.send", "Send");
        showSuggestions();
    }

    function togglePanel(force) {
        var show = typeof force === "boolean" ? force : panel.hidden;
        panel.hidden = !show;
        backdrop.hidden = !show;
        try {
            if (show) {
                document.body.style.top = (0 - (window.scrollY || 0)) + "px";
                document.documentElement.classList.add("chat-open");
            } else {
                document.documentElement.classList.remove("chat-open");
                var savedTop = document.body.style.top || "";
                document.body.style.top = "";
                if (savedTop) window.scrollTo(0, 0 - (parseInt(savedTop, 10) || 0));
            }
        } catch (e) { /* ignore */ }
        fab.setAttribute("aria-expanded", String(show));
        if (show && !greeted) {
            greeted = true;
            greet();
            showSuggestions();
        }
        if (show) {
            try { input.focus({ preventScroll: true }); } catch (e) { try { input.focus(); } catch (e2) { /* ignore */ } }
        }
    }

    function build() {
        fab = document.createElement("button");
        fab.type = "button";
        fab.className = "chat-fab";
        fab.setAttribute("aria-expanded", "false");
        fab.innerHTML = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>';

        panel = document.createElement("div");
        panel.className = "chat-panel";
        panel.hidden = true;
        panel.setAttribute("role", "dialog");
        panel.setAttribute("aria-modal", "true");

        backdrop = document.createElement("div");
        backdrop.className = "chat-backdrop";
        backdrop.hidden = true;

        var head = document.createElement("div");
        head.className = "chat-head";
        var avatar = document.createElement("span");
        avatar.className = "chat-avatar";
        avatar.setAttribute("aria-hidden", "true");
        avatar.textContent = "LB";
        var headText = document.createElement("span");
        headText.className = "chat-head-text";
        titleEl = document.createElement("strong");
        statusEl = document.createElement("span");
        statusEl.className = "chat-status";
        headText.append(titleEl, statusEl);
        closeBtn = document.createElement("button");
        closeBtn.type = "button";
        closeBtn.className = "chat-close";
        closeBtn.textContent = "×";
        head.append(avatar, headText, closeBtn);

        msgs = document.createElement("div");
        msgs.className = "chat-msgs";
        msgs.setAttribute("role", "log");
        msgs.setAttribute("aria-live", "polite");

        chips = document.createElement("div");
        chips.className = "chat-chips";

        form = document.createElement("form");
        form.className = "chat-form";
        input = document.createElement("input");
        input.type = "text";
        input.autocomplete = "off";
        input.maxLength = 500;
        sendBtn = document.createElement("button");
        sendBtn.type = "submit";
        sendBtn.className = "btn btn-prim";
        form.append(input, sendBtn);

        panel.append(head, msgs, chips, form);
        document.body.append(fab, backdrop, panel);

        fab.addEventListener("click", function () { togglePanel(); });
        backdrop.addEventListener("click", function () { togglePanel(false); });
        closeBtn.addEventListener("click", function () {
            togglePanel(false);
            fab.focus();
        });
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            sendText(input.value);
            input.value = "";
        });
        document.addEventListener("keydown", function (event) {
            if (panel.hidden) return;
            if (event.key === "Escape") {
                togglePanel(false);
                fab.focus();
                return;
            }
            if (event.key !== "Tab") return;
            var focusables = panel.querySelectorAll("button, input, a[href]");
            if (!focusables.length) return;
            var first = focusables[0];
            var last = focusables[focusables.length - 1];
            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault();
                first.focus();
            }
        });
        document.addEventListener("lb:lang", refreshChrome);
        window.addEventListener("online", updateStatus);
        window.addEventListener("offline", updateStatus);

        refreshChrome();
    }

    // First open shows the greeting intent from the KB.
    function greet() {
        var lang = chatLang();
        for (var i = 0; i < LB_CHAT_KB.length; i++) {
            if (LB_CHAT_KB[i] && LB_CHAT_KB[i].id === "greeting" && LB_CHAT_KB[i].answers) {
                var answers = LB_CHAT_KB[i].answers;
                addMsg(answers[lang] || answers.en || "", "bot");
                return;
            }
        }
    }

    function init() {
        build();
        window.LBChat = {
            ready: true,
            open: function () { togglePanel(true); },
            close: function () { togglePanel(false); }
        };
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
