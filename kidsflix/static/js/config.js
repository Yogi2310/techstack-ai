// ============================================
// CONFIGURATION - KidsFlix: 4 Categories
// ============================================

const CONFIG = {
  YOUTUBE_API_KEY: '',
  MAX_RESULTS: 12,

  DURATION_FILTERS: {
    '30s':  { min: 15,  max: 45,    label: '~30 sec' },
    '1m':   { min: 45,  max: 90,    label: '~1 min'  },
    '2m':   { min: 90,  max: 150,   label: '~2 min'  },
    '3m':   { min: 150, max: 210,   label: '~3 min'  },
    '4m':   { min: 210, max: 270,   label: '~4 min'  },
    '5m':   { min: 270, max: 330,   label: '~5 min'  },
    'all':  { min: 0,   max: 99999, label: 'All'     }
  },

  // Age groups mapped to tags in demo data
  AGE_GROUPS: {
    'toddler': 'Toddler (2–4)',
    'kids':    'Kids (5–8)',
    'tweens':  'Tweens (9–12)',
    'all':     'All Ages'
  },

  // ============================================
  // DEMO SHORTS — 4 categories
  // ============================================
  DEMO_SHORTS: {

    cartoon: {
      english: [
        { id: 'V2iqyuoJlQ0', title: 'Peppa Pig — Muddy Puddles 30 Sec 🐷', channel: 'Peppa Pig', views: '42.1M', duration: '0:30', durationSec: 30, published: '6 hours ago', age: 'toddler' },
        { id: 'Oj02jkbOHoQ', title: 'Cocomelon — Baby Shark Dance! 🦈', channel: 'Cocomelon', views: '85.3M', duration: '0:45', durationSec: 45, published: '1 day ago', age: 'toddler' },
        { id: 'SrODRkTIOUo', title: 'Bluey — Best Moments Compilation ✨', channel: 'Bluey', views: '18.9M', duration: '1:00', durationSec: 60, published: '2 days ago', age: 'kids' },
        { id: 'mDu2DuNFyRc', title: 'Tom and Jerry — Funniest Chase! 😂', channel: 'Tom & Jerry', views: '31.7M', duration: '0:35', durationSec: 35, published: '12 hours ago', age: 'kids' },
        { id: 'AyGtUhWAy0E', title: 'Paw Patrol — Chase Saves the Day! 🚔', channel: 'Paw Patrol', views: '14.2M', duration: '0:50', durationSec: 50, published: '3 days ago', age: 'toddler' },
        { id: 'HQoRXvalfwI', title: 'Dora — We Did It Song! 🎵', channel: 'Dora Official', views: '22.5M', duration: '0:40', durationSec: 40, published: '4 days ago', age: 'toddler' },
        { id: 'DK4bSNNOZMI', title: 'Numberblocks — All About 5! 🔢', channel: 'Numberblocks', views: '16.8M', duration: '1:15', durationSec: 75, published: '1 day ago', age: 'kids' },
        { id: 'ktvTqknDobU', title: 'Mickey Mouse — Clubhouse Fun 🏠', channel: 'Mickey Mouse', views: '29.3M', duration: '2:00', durationSec: 120, published: '5 days ago', age: 'toddler' },
        { id: 'KeEbCInHKMY', title: 'SpongeBob — Best Krabby Patty Moment 🍔', channel: 'SpongeBob', views: '38.1M', duration: '2:30', durationSec: 150, published: '2 days ago', age: 'tweens' },
        { id: '_OBlgSz8sSM', title: 'Minions — Best Funny Moments! 💛', channel: 'Minions', views: '67.4M', duration: '3:00', durationSec: 180, published: '1 week ago', age: 'kids' },
        { id: 'FTQbiNvZqaY', title: 'Cars Lightning McQueen Race! 🏎️', channel: 'Pixar Cars', views: '19.6M', duration: '4:00', durationSec: 240, published: '3 days ago', age: 'kids' },
        { id: 'QH2-TGUlwu4', title: 'Frozen — Let It Go Animated Short ❄️', channel: 'Disney Shorts', views: '55.2M', duration: '5:00', durationSec: 300, published: '6 days ago', age: 'tweens' },
      ],
      hindi: [
        { id: '_OBlgSz8sSM', title: 'छोटा भीम — Kalia की मस्ती 😂', channel: 'Chhota Bheem', views: '48.3M', duration: '0:28', durationSec: 28, published: '5 hours ago', age: 'kids' },
        { id: 'QH2-TGUlwu4', title: 'Motu Patlu — समोसे का कारनामा! 🥟', channel: 'Motu Patlu', views: '36.7M', duration: '0:45', durationSec: 45, published: '1 day ago', age: 'kids' },
        { id: 'ktvTqknDobU', title: 'Doraemon — डोरा की गैजेट Hindi 🎒', channel: 'Doraemon Hindi', views: '27.9M', duration: '1:05', durationSec: 65, published: '2 days ago', age: 'kids' },
        { id: 'FTQbiNvZqaY', title: 'Shiva — भागते लुटेरे हिंदी 🏍️', channel: 'Shiva Hindi', views: '18.4M', duration: '2:10', durationSec: 130, published: '3 days ago', age: 'tweens' },
        { id: 'KeEbCInHKMY', title: 'Krishna Balram — नई कहानी', channel: 'KB Hindi', views: '12.6M', duration: '3:15', durationSec: 195, published: '4 days ago', age: 'kids' },
        { id: 'SrODRkTIOUo', title: 'Chacha Chaudhary — Comic Powers', channel: 'Chacha Hindi', views: '9.1M', duration: '4:00', durationSec: 240, published: '5 days ago', age: 'tweens' },
        { id: 'AyGtUhWAy0E', title: 'Little Singham — Action Short Hindi', channel: 'Singham Hindi', views: '21.3M', duration: '5:00', durationSec: 300, published: '1 week ago', age: 'tweens' },
        { id: 'mDu2DuNFyRc', title: 'Oggy and Cockroaches Hindi — Best Moments', channel: 'Oggy Hindi', views: '14.8M', duration: '0:55', durationSec: 55, published: '2 days ago', age: 'kids' },
      ]
    },

    maths: {
      english: [
        { id: '0ZKisVMqMF4', title: '1+1=2 — Easy Addition Song for Kids ➕', channel: 'Maths Fun', views: '9.4M', duration: '0:30', durationSec: 30, published: '8 hours ago', age: 'toddler' },
        { id: 'nTFEUsudhfs', title: 'Count to 10 with Shapes! 🔢🔺🔵', channel: 'Numberblocks', views: '14.2M', duration: '0:45', durationSec: 45, published: '1 day ago', age: 'toddler' },
        { id: 'PVoiEHMR9WI', title: 'What Shape Am I? — Circle Square Triangle', channel: 'Kids Learning', views: '7.8M', duration: '0:38', durationSec: 38, published: '2 days ago', age: 'toddler' },
        { id: 'AQqhXaR5DaQ', title: '5-3=2 Subtraction — Super Easy for Kids ➖', channel: 'Maths Genie', views: '6.5M', duration: '1:00', durationSec: 60, published: '3 days ago', age: 'kids' },
        { id: 'aBpHPPGKnco', title: '2 Times Table Song — Sing Along! ✖️', channel: 'Times Tables', views: '18.7M', duration: '1:15', durationSec: 75, published: '12 hours ago', age: 'kids' },
        { id: 'DK4bSNNOZMI', title: 'Odd and Even Numbers — 1 Min Explained', channel: 'Math Explained', views: '5.3M', duration: '1:30', durationSec: 90, published: '4 days ago', age: 'kids' },
        { id: '3eWzRHm6kGY', title: 'Big and Small — Comparing Numbers 2 Min', channel: 'Kids Maths', views: '4.9M', duration: '2:00', durationSec: 120, published: '5 days ago', age: 'toddler' },
        { id: 'L4EE19RbXpM', title: 'Count by 10s to 100! — Kids Number Song', channel: 'Counting Songs', views: '11.6M', duration: '2:30', durationSec: 150, published: '1 day ago', age: 'kids' },
        { id: 'ktvTqknDobU', title: 'Fractions Made Fun! 1/2 and 1/4 Kids', channel: 'Math For Kids', views: '7.2M', duration: '3:10', durationSec: 190, published: '3 days ago', age: 'tweens' },
        { id: 'HQoRXvalfwI', title: 'Time on a Clock — Hour and Minute', channel: 'Clock Kids', views: '8.4M', duration: '4:00', durationSec: 240, published: '2 days ago', age: 'tweens' },
        { id: 'mDu2DuNFyRc', title: 'Money Maths — Coins and Notes for Kids', channel: 'Money Math', views: '6.1M', duration: '4:55', durationSec: 295, published: '1 week ago', age: 'tweens' },
        { id: 'SrODRkTIOUo', title: 'Patterns in Maths — Red Blue Red? 🔴🔵', channel: 'Pattern Play', views: '5.8M', duration: '0:40', durationSec: 40, published: '6 hours ago', age: 'toddler' },
      ],
      hindi: [
        { id: '3eWzRHm6kGY', title: '1+1=2 — जोड़ना सीखो आसान गाने से ➕', channel: 'Hindi Maths', views: '7.6M', duration: '0:35', durationSec: 35, published: '6 hours ago', age: 'toddler' },
        { id: 'L4EE19RbXpM', title: '1 से 10 गिनती — बच्चों के लिए 🔢', channel: 'Ginti Hindi', views: '12.3M', duration: '0:50', durationSec: 50, published: '1 day ago', age: 'toddler' },
        { id: 'mDu2DuNFyRc', title: 'आकार — गोला चौकोर त्रिभुज Hindi Shapes', channel: 'Shape Hindi', views: '5.4M', duration: '0:42', durationSec: 42, published: '2 days ago', age: 'toddler' },
        { id: 'HQoRXvalfwI', title: 'घटाव — 5-2=3 आसानी से सीखो ➖', channel: 'Math Hindi', views: '6.8M', duration: '1:10', durationSec: 70, published: '3 days ago', age: 'kids' },
        { id: 'ktvTqknDobU', title: 'पहाड़ा 2 का — गाते-गाते याद करो ✖️', channel: 'Pahade Hindi', views: '15.4M', duration: '1:30', durationSec: 90, published: '12 hours ago', age: 'kids' },
        { id: 'FTQbiNvZqaY', title: 'सम और विषम संख्या — 2 Min Hindi', channel: 'Odd Even Hindi', views: '4.3M', duration: '2:00', durationSec: 120, published: '4 days ago', age: 'kids' },
        { id: 'SrODRkTIOUo', title: 'बड़ा छोटा — तुलना करना सीखो 3 Min', channel: 'Comparison Hindi', views: '3.9M', duration: '3:05', durationSec: 185, published: '5 days ago', age: 'tweens' },
        { id: 'AyGtUhWAy0E', title: '1 से 100 तक गिनती गाना — Kids Song', channel: 'Counting Hindi', views: '9.7M', duration: '4:15', durationSec: 255, published: '1 week ago', age: 'tweens' },
      ]
    },

    stories: {
      english: [
        { id: 'V2iqyuoJlQ0', title: 'Cinderella — Short Story for Kids 🥿✨', channel: 'Fairy Tales', views: '22.1M', duration: '0:58', durationSec: 58, published: '1 day ago', age: 'toddler' },
        { id: 'Oj02jkbOHoQ', title: 'The Three Little Pigs — 1 Min Story 🐷', channel: 'Story Time', views: '17.4M', duration: '1:00', durationSec: 60, published: '2 days ago', age: 'toddler' },
        { id: 'SrODRkTIOUo', title: 'Goldilocks and the Three Bears 🐻', channel: 'Classic Tales', views: '11.9M', duration: '1:30', durationSec: 90, published: '3 days ago', age: 'toddler' },
        { id: 'mDu2DuNFyRc', title: 'The Ugly Duckling — Animated Short 🦢', channel: 'Bedtime Stories', views: '8.7M', duration: '2:00', durationSec: 120, published: '4 days ago', age: 'kids' },
        { id: 'AyGtUhWAy0E', title: 'Jack and the Beanstalk 🌱🏰', channel: 'Story Pals', views: '13.5M', duration: '2:30', durationSec: 150, published: '5 days ago', age: 'kids' },
        { id: 'HQoRXvalfwI', title: 'The Lion and the Mouse — Aesop Fable 🦁🐭', channel: 'Aesop Fables', views: '6.3M', duration: '0:45', durationSec: 45, published: '12 hours ago', age: 'kids' },
        { id: 'DK4bSNNOZMI', title: 'Brave Little Tailor — Brothers Grimm', channel: 'Grimm Tales', views: '5.8M', duration: '3:00', durationSec: 180, published: '2 days ago', age: 'tweens' },
        { id: 'ktvTqknDobU', title: 'The Tortoise and the Hare 🐢🐇 Race Story', channel: 'Animal Tales', views: '19.2M', duration: '1:10', durationSec: 70, published: '1 day ago', age: 'toddler' },
      ],
      hindi: [
        { id: '_OBlgSz8sSM', title: 'सिंडरेला — हिंदी में कहानी 🥿✨', channel: 'Hindi Tales', views: '16.4M', duration: '1:00', durationSec: 60, published: '1 day ago', age: 'toddler' },
        { id: 'QH2-TGUlwu4', title: 'तीन मछलियाँ — पंचतंत्र कहानी 🐟', channel: 'Panchatantra', views: '21.3M', duration: '0:50', durationSec: 50, published: '2 days ago', age: 'kids' },
        { id: 'ktvTqknDobU', title: 'अकलू और मकलू — चालाक खरगोश 🐇', channel: 'Desi Stories', views: '12.7M', duration: '1:30', durationSec: 90, published: '3 days ago', age: 'kids' },
        { id: 'FTQbiNvZqaY', title: 'राजा और मंत्री — Hindi Moral Story 👑', channel: 'Naitik Kathayen', views: '8.2M', duration: '2:00', durationSec: 120, published: '4 days ago', age: 'tweens' },
        { id: 'KeEbCInHKMY', title: 'बंदर और टोपीवाला — Funny Story 🐒🎩', channel: 'Hindi Kahani', views: '14.9M', duration: '0:45', durationSec: 45, published: '6 hours ago', age: 'toddler' },
        { id: 'SrODRkTIOUo', title: 'जादुई बांसुरी — Magical Flute Story 🪈', channel: 'Jaduai Kahani', views: '7.6M', duration: '3:00', durationSec: 180, published: '5 days ago', age: 'tweens' },
      ]
    },

    science: {
      english: [
        { id: '0ZKisVMqMF4', title: 'Why Is the Sky Blue? — Science for Kids 🌤️', channel: 'Science Fun', views: '11.4M', duration: '0:55', durationSec: 55, published: '1 day ago', age: 'kids' },
        { id: 'nTFEUsudhfs', title: 'How Do Plants Grow? — Seed to Tree 🌱', channel: 'Planet Earth Kids', views: '8.9M', duration: '1:00', durationSec: 60, published: '2 days ago', age: 'toddler' },
        { id: 'PVoiEHMR9WI', title: 'Planets of the Solar System — 1 Min! 🪐', channel: 'Space Kids', views: '24.7M', duration: '1:00', durationSec: 60, published: '3 days ago', age: 'kids' },
        { id: 'AQqhXaR5DaQ', title: 'Why Do We Have Day and Night? 🌙', channel: 'Earth Science', views: '9.3M', duration: '0:45', durationSec: 45, published: '4 days ago', age: 'kids' },
        { id: 'aBpHPPGKnco', title: 'Amazing Animals Facts — Elephants 🐘', channel: 'Wild Science', views: '16.2M', duration: '1:30', durationSec: 90, published: '5 days ago', age: 'kids' },
        { id: 'DK4bSNNOZMI', title: 'Volcano Experiment at Home 🌋🧪', channel: 'Mini Lab', views: '31.4M', duration: '2:00', durationSec: 120, published: '1 day ago', age: 'tweens' },
        { id: '3eWzRHm6kGY', title: 'How Do Rainbows Form? 🌈 Science Short', channel: 'Rainbow Science', views: '7.8M', duration: '0:50', durationSec: 50, published: '6 hours ago', age: 'kids' },
        { id: 'L4EE19RbXpM', title: 'Dinosaurs Facts for Kids — T-Rex! 🦖', channel: 'Dino World', views: '38.5M', duration: '1:15', durationSec: 75, published: '2 days ago', age: 'tweens' },
        { id: 'ktvTqknDobU', title: 'Human Body — Heart Beats! ❤️ Kids Science', channel: 'Body Science', views: '12.1M', duration: '2:30', durationSec: 150, published: '3 days ago', age: 'tweens' },
        { id: 'HQoRXvalfwI', title: 'What Is Gravity? — Easy Explanation 🍎', channel: 'Physics Pals', views: '18.6M', duration: '3:00', durationSec: 180, published: '4 days ago', age: 'tweens' },
      ],
      hindi: [
        { id: '3eWzRHm6kGY', title: 'आसमान नीला क्यों होता है? 🌤️ Hindi Science', channel: 'Vigyan Hindi', views: '9.4M', duration: '1:00', durationSec: 60, published: '1 day ago', age: 'kids' },
        { id: 'L4EE19RbXpM', title: 'ग्रह-नक्षत्र — सौरमंडल की जानकारी 🪐', channel: 'Akash Gyan', views: '7.2M', duration: '1:30', durationSec: 90, published: '2 days ago', age: 'kids' },
        { id: 'mDu2DuNFyRc', title: 'पानी का चक्र — बादल कैसे बनते हैं? ☁️', channel: 'Mausam Hindi', views: '5.8M', duration: '0:55', durationSec: 55, published: '3 days ago', age: 'kids' },
        { id: 'HQoRXvalfwI', title: 'डायनासोर — T-Rex की कहानी 🦖 Hindi', channel: 'Dino Hindi', views: '13.7M', duration: '2:00', durationSec: 120, published: '4 days ago', age: 'tweens' },
        { id: 'ktvTqknDobU', title: 'घर पर प्रयोग — ज्वालामुखी बनाओ 🌋', channel: 'Vigyan Lab', views: '22.4M', duration: '2:30', durationSec: 150, published: '5 days ago', age: 'tweens' },
        { id: 'FTQbiNvZqaY', title: 'मानव शरीर — दिल कैसे काम करता है ❤️', channel: 'Sharir Vigyan', views: '8.9M', duration: '3:00', durationSec: 180, published: '1 week ago', age: 'tweens' },
      ]
    }
  },

  // ============================================
  // FEATURED SECTIONS
  // ============================================
  MATHS_FEATURED: [
    { id: '0ZKisVMqMF4', title: '1+1=2 Addition Song 🎵', channel: 'Maths Fun', views: '9.4M', duration: '0:30', durationSec: 30, published: '8 hours ago', lang: 'english', age: 'toddler' },
    { id: 'nTFEUsudhfs', title: 'Count to 10 with Shapes! 🔺', channel: 'Numberblocks', views: '14.2M', duration: '0:45', durationSec: 45, published: '1 day ago', lang: 'english', age: 'toddler' },
    { id: 'aBpHPPGKnco', title: '2x Table Song — Sing Along! ✖️', channel: 'Times Tables', views: '18.7M', duration: '1:15', durationSec: 75, published: '12 hours ago', lang: 'english', age: 'kids' },
    { id: 'PVoiEHMR9WI', title: 'Shapes: Circle Square Triangle', channel: 'Kids Learning', views: '7.8M', duration: '0:38', durationSec: 38, published: '2 days ago', lang: 'english', age: 'toddler' },
    { id: '3eWzRHm6kGY', title: 'जोड़ना सीखो — Hindi Addition Song ➕', channel: 'Hindi Maths', views: '7.6M', duration: '0:35', durationSec: 35, published: '6 hours ago', lang: 'hindi', age: 'toddler' },
    { id: 'L4EE19RbXpM', title: '1 से 10 गिनती बच्चों के लिए 🔢', channel: 'Ginti Hindi', views: '12.3M', duration: '0:50', durationSec: 50, published: '1 day ago', lang: 'hindi', age: 'toddler' },
  ],
  CARTOON_FEATURED: [
    { id: 'V2iqyuoJlQ0', title: 'Peppa Pig — Muddy Puddles 30 Sec 🐷', channel: 'Peppa Pig', views: '42.1M', duration: '0:30', durationSec: 30, published: '6 hours ago', lang: 'english', age: 'toddler' },
    { id: 'Oj02jkbOHoQ', title: 'Cocomelon — Baby Shark Dance! 🦈', channel: 'Cocomelon', views: '85.3M', duration: '0:45', durationSec: 45, published: '1 day ago', lang: 'english', age: 'toddler' },
    { id: '_OBlgSz8sSM', title: 'छोटा भीम — Kalia की मस्ती 😂', channel: 'Chhota Bheem', views: '48.3M', duration: '0:28', durationSec: 28, published: '5 hours ago', lang: 'hindi', age: 'kids' },
    { id: 'QH2-TGUlwu4', title: 'Motu Patlu — समोसे का कारनामा! 🥟', channel: 'Motu Patlu', views: '36.7M', duration: '0:45', durationSec: 45, published: '1 day ago', lang: 'hindi', age: 'kids' },
    { id: 'mDu2DuNFyRc', title: 'Tom and Jerry — Funniest Chase! 😂', channel: 'Tom & Jerry', views: '31.7M', duration: '0:35', durationSec: 35, published: '12 hours ago', lang: 'english', age: 'kids' },
    { id: 'SrODRkTIOUo', title: 'Bluey — Best Moments Compilation ✨', channel: 'Bluey', views: '18.9M', duration: '1:00', durationSec: 60, published: '2 days ago', lang: 'english', age: 'kids' },
  ],
  STORIES_FEATURED: [
    { id: 'V2iqyuoJlQ0', title: 'Cinderella — Short Story 🥿✨', channel: 'Fairy Tales', views: '22.1M', duration: '0:58', durationSec: 58, published: '1 day ago', lang: 'english', age: 'toddler' },
    { id: 'ktvTqknDobU', title: 'Tortoise and the Hare 🐢🐇', channel: 'Animal Tales', views: '19.2M', duration: '1:10', durationSec: 70, published: '1 day ago', lang: 'english', age: 'toddler' },
    { id: 'HQoRXvalfwI', title: 'The Lion and the Mouse 🦁🐭', channel: 'Aesop Fables', views: '6.3M', duration: '0:45', durationSec: 45, published: '12 hours ago', lang: 'english', age: 'kids' },
    { id: '_OBlgSz8sSM', title: 'सिंडरेला — हिंदी कहानी 🥿', channel: 'Hindi Tales', views: '16.4M', duration: '1:00', durationSec: 60, published: '1 day ago', lang: 'hindi', age: 'toddler' },
    { id: 'QH2-TGUlwu4', title: 'तीन मछलियाँ — पंचतंत्र 🐟', channel: 'Panchatantra', views: '21.3M', duration: '0:50', durationSec: 50, published: '2 days ago', lang: 'hindi', age: 'kids' },
    { id: 'KeEbCInHKMY', title: 'बंदर और टोपीवाला 🐒🎩', channel: 'Hindi Kahani', views: '14.9M', duration: '0:45', durationSec: 45, published: '6 hours ago', lang: 'hindi', age: 'toddler' },
  ],
  SCIENCE_FEATURED: [
    { id: 'PVoiEHMR9WI', title: 'Planets of the Solar System 🪐', channel: 'Space Kids', views: '24.7M', duration: '1:00', durationSec: 60, published: '3 days ago', lang: 'english', age: 'kids' },
    { id: 'aBpHPPGKnco', title: 'Amazing Elephants Facts 🐘', channel: 'Wild Science', views: '16.2M', duration: '1:30', durationSec: 90, published: '5 days ago', lang: 'english', age: 'kids' },
    { id: 'DK4bSNNOZMI', title: 'Volcano Experiment at Home 🌋', channel: 'Mini Lab', views: '31.4M', duration: '2:00', durationSec: 120, published: '1 day ago', lang: 'english', age: 'tweens' },
    { id: 'L4EE19RbXpM', title: 'Dinosaurs Facts — T-Rex! 🦖', channel: 'Dino World', views: '38.5M', duration: '1:15', durationSec: 75, published: '2 days ago', lang: 'english', age: 'tweens' },
    { id: '3eWzRHm6kGY', title: 'आसमान नीला क्यों? 🌤️ Hindi', channel: 'Vigyan Hindi', views: '9.4M', duration: '1:00', durationSec: 60, published: '1 day ago', lang: 'hindi', age: 'kids' },
    { id: 'ktvTqknDobU', title: 'घर पर ज्वालामुखी बनाओ 🌋', channel: 'Vigyan Lab', views: '22.4M', duration: '2:30', durationSec: 150, published: '5 days ago', lang: 'hindi', age: 'tweens' },
  ],

  VIDEO_COMMENTS: [
    [
      { author: 'KidsMom2024',  text: '😍 My kids absolutely love this! They watch it every day!', likes: '2.4K' },
      { author: 'TeacherJane',  text: '🎓 Great educational content! Using this in my classroom.', likes: '1.8K' },
      { author: 'ParentPriya',  text: '✨ So colorful and fun! My daughter asked to watch again!', likes: '956' },
    ],
    [
      { author: 'LearnerMom',   text: '🌟 My son learned to count to 10 after just 3 watches!', likes: '3.1K' },
      { author: 'DadOfThree',   text: '👏 Amazing way to make maths fun. No more boring worksheets!', likes: '2.2K' },
      { author: 'GrandmaHappy', text: '😊 Even grandma finds this easy to follow along!', likes: '1.4K' },
    ],
    [
      { author: 'CuriousKid007',  text: '🤩 BEST VIDEO EVER!! More please!!', likes: '5.6K' },
      { author: 'HomeschoolHub',  text: '📚 Perfect for our homeschool routine! Highly recommended.', likes: '2.9K' },
      { author: 'TinyTots',       text: '🍎 My 3-year-old points at the screen and dances!', likes: '1.7K' },
    ],
  ]
};
