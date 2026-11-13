// ============================================
// CONFIGURATION - KidsFlix: Cartoon & Maths
// ============================================

const CONFIG = {
  // YouTube API Key (optional - site works with demo data)
  YOUTUBE_API_KEY: '',
  MAX_RESULTS: 12,
  MIN_DURATION_SECONDS: 60,

  DURATION_FILTERS: {
    '30s':  { min: 15, max: 45,    label: '~30 sec' },
    '1m':   { min: 45, max: 90,    label: '~1 min'  },
    '2m':   { min: 90, max: 150,   label: '~2 min'  },
    '3m':   { min: 150, max: 210,  label: '~3 min'  },
    '4m':   { min: 210, max: 270,  label: '~4 min'  },
    '5m':   { min: 270, max: 330,  label: '~5 min'  },
    'all':  { min: 0,   max: 99999, label: 'All'    }
  },

  SEARCH_QUERIES: {
    cartoon: {
      english: 'best cartoon episodes for kids 2026 english',
      hindi:   'cartoon hindi kids videos 2026',
      all:     'popular cartoon videos kids 2026'
    },
    maths: {
      english: 'basic maths for kids english learning 2026',
      hindi:   'maths for kids hindi basic sums 2026',
      all:     'maths learning kids 2026'
    }
  },

  // ============================================
  // DEMO / FALLBACK DATA - BIG VIDEOS
  // ============================================
  DEMO_VIDEOS: {
    cartoon: {
      english: [
        { id: 'V2iqyuoJlQ0', title: 'Peppa Pig Full Episodes — Season 1 🐷', channel: 'Peppa Pig Official', views: '45.2M', duration: '22:10', published: '1 day ago', thumbnail: '' },
        { id: 'Oj02jkbOHoQ', title: 'Cocomelon — JJ's Day Out Full Episode', channel: 'Cocomelon', views: '38.7M', duration: '30:15', published: '3 days ago', thumbnail: '' },
        { id: 'SrODRkTIOUo', title: 'Bluey — Full Episode Collection Vol. 1 🦴', channel: 'Bluey Official', views: '22.1M', duration: '28:40', published: '2 days ago', thumbnail: '' },
        { id: 'mDu2DuNFyRc', title: 'Tom and Jerry Classic Episodes 🐱🐭', channel: 'Tom & Jerry', views: '30.5M', duration: '25:33', published: '5 days ago', thumbnail: '' },
        { id: 'AyGtUhWAy0E', title: 'Paw Patrol Season 2 — Full Episodes 🐾', channel: 'Paw Patrol Official', views: '28.9M', duration: '35:20', published: '4 days ago', thumbnail: '' },
        { id: 'HQoRXvalfwI', title: 'Dora the Explorer — Map Adventure Full Episode', channel: 'Dora Official', views: '18.3M', duration: '22:45', published: '1 week ago', thumbnail: '' },
      ],
      hindi: [
        { id: '_OBlgSz8sSM', title: 'छोटा भीम — नई कहानी पूरा एपिसोड 🪄', channel: 'Chhota Bheem', views: '55.4M', duration: '24:30', published: '1 day ago', thumbnail: '' },
        { id: 'QH2-TGUlwu4', title: 'Motu Patlu — Full Episodes Hindi 😂', channel: 'Motu Patlu', views: '42.1M', duration: '26:15', published: '2 days ago', thumbnail: '' },
        { id: 'ktvTqknDobU', title: 'Doraemon Hindi — Nobita की नई कहानी', channel: 'Doraemon Hindi', views: '38.6M', duration: '22:00', published: '3 days ago', thumbnail: '' },
        { id: 'FTQbiNvZqaY', title: 'Shiva Hindi Cartoon — Full Episode 🏍️', channel: 'Shiva Official', views: '25.3M', duration: '28:50', published: '5 days ago', thumbnail: '' },
        { id: 'KeEbCInHKMY', title: 'Krishna Balram — Hindi Adventure Episode', channel: 'Krishna Balram', views: '19.8M', duration: '24:10', published: '4 days ago', thumbnail: '' },
        { id: 'Oj02jkbOHoQ', title: 'Singham Hindi Cartoon — Police Adventures', channel: 'Singham Official', views: '14.2M', duration: '26:40', published: '1 week ago', thumbnail: '' },
      ]
    },
    maths: {
      english: [
        { id: '0ZKisVMqMF4', title: 'Learn Addition for Kids — Full Lesson 1-20 ➕', channel: 'Math For Kids', views: '12.4M', duration: '15:30', published: '2 days ago', thumbnail: '' },
        { id: 'nTFEUsudhfs', title: 'Counting Numbers 1 to 100 — Kids Maths', channel: 'Number Blocks', views: '18.9M', duration: '20:15', published: '1 day ago', thumbnail: '' },
        { id: 'PVoiEHMR9WI', title: 'Shapes for Kids — Circle Square Triangle Star', channel: 'Kids Learning', views: '9.7M', duration: '12:45', published: '3 days ago', thumbnail: '' },
        { id: 'AYqhXaR5DaQ', title: 'Subtraction Made Easy for Grade 1 Kids ➖', channel: 'Maths Genie', views: '7.8M', duration: '18:20', published: '5 days ago', thumbnail: '' },
        { id: 'aBpHPPGKnco', title: 'Multiplication Tables 1 to 10 — Song & Tricks ✖️', channel: 'Times Tables', views: '22.3M', duration: '25:00', published: '4 days ago', thumbnail: '' },
        { id: 'DK4bSNNOZMI', title: 'Number Patterns and Basic Maths Fun', channel: 'Numberblocks', views: '11.5M', duration: '14:35', published: '1 week ago', thumbnail: '' },
      ],
      hindi: [
        { id: '3eWzRHm6kGY', title: 'गणित कैसे सीखें — 1 से 20 जोड़ना ➕', channel: 'Math Hindi', views: '8.2M', duration: '16:10', published: '2 days ago', thumbnail: '' },
        { id: 'L4EE19RbXpM', title: 'Hindi Maths — 1 से 100 गिनती सीखो', channel: 'Ginti Hindi', views: '14.6M', duration: '18:45', published: '1 day ago', thumbnail: '' },
        { id: 'ktvTqknDobU', title: 'घटाव कैसे करें — Class 1 के लिए ➖', channel: 'Kids Maths Hindi', views: '6.3M', duration: '13:30', published: '3 days ago', thumbnail: '' },
        { id: 'mDu2DuNFyRc', title: 'आकार सीखो — गोला चौकोर त्रिभुज', channel: 'Shape Hindi', views: '5.9M', duration: '11:20', published: '5 days ago', thumbnail: '' },
        { id: 'HQoRXvalfwI', title: 'पहाड़े याद करो — 2 से 10 ✖️', channel: 'Pahada Hindi', views: '19.4M', duration: '22:00', published: '4 days ago', thumbnail: '' },
        { id: 'SrODRkTIOUo', title: 'Hindi Maths Fun — Numbers and Patterns', channel: 'Maths Hindi Fun', views: '7.1M', duration: '15:55', published: '1 week ago', thumbnail: '' },
      ]
    }
  },

  // ============================================
  // DEMO / FALLBACK DATA - SHORTS
  // ============================================
  DEMO_SHORTS: {
    cartoon: {
      english: [
        { id: 'V2iqyuoJlQ0', title: 'Peppa Pig — Muddy Puddles 30 Sec 🐷', channel: 'Peppa Pig', views: '42.1M', duration: '0:30', durationSec: 30, published: '6 hours ago', thumbnail: '' },
        { id: 'Oj02jkbOHoQ', title: 'Cocomelon — Baby Shark Dance! 🦈', channel: 'Cocomelon', views: '85.3M', duration: '0:45', durationSec: 45, published: '1 day ago', thumbnail: '' },
        { id: 'SrODRkTIOUo', title: 'Bluey — Best Moments Compilation ✨', channel: 'Bluey', views: '18.9M', duration: '1:00', durationSec: 60, published: '2 days ago', thumbnail: '' },
        { id: 'mDu2DuNFyRc', title: 'Tom and Jerry — Funniest Chase! 😂', channel: 'Tom & Jerry', views: '31.7M', duration: '0:35', durationSec: 35, published: '12 hours ago', thumbnail: '' },
        { id: 'AyGtUhWAy0E', title: 'Paw Patrol — Chase Saves the Day! 🚔', channel: 'Paw Patrol', views: '14.2M', duration: '0:50', durationSec: 50, published: '3 days ago', thumbnail: '' },
        { id: 'HQoRXvalfwI', title: 'Dora — We Did It Song! 🎵', channel: 'Dora Official', views: '22.5M', duration: '0:40', durationSec: 40, published: '4 days ago', thumbnail: '' },
        { id: 'DK4bSNNOZMI', title: 'Numberblocks — All About 5! 🔢', channel: 'Numberblocks', views: '16.8M', duration: '1:15', durationSec: 75, published: '1 day ago', thumbnail: '' },
        { id: 'ktvTqknDobU', title: 'Mickey Mouse — Clubhouse Fun 🏠', channel: 'Mickey Mouse', views: '29.3M', duration: '2:00', durationSec: 120, published: '5 days ago', thumbnail: '' },
        { id: 'KeEbCInHKMY', title: 'SpongeBob — Krabby Patty Moment 🍔', channel: 'SpongeBob', views: '38.1M', duration: '2:30', durationSec: 150, published: '2 days ago', thumbnail: '' },
        { id: '_OBlgSz8sSM', title: 'Minions — Best Funny Moments! 💛', channel: 'Minions', views: '67.4M', duration: '3:00', durationSec: 180, published: '1 week ago', thumbnail: '' },
        { id: 'FTQbiNvZqaY', title: 'Cars Lightning McQueen Race! 🏎️', channel: 'Pixar Cars', views: '19.6M', duration: '4:00', durationSec: 240, published: '3 days ago', thumbnail: '' },
        { id: 'QH2-TGUlwu4', title: 'Frozen — Let It Go Animated Short ❄️', channel: 'Disney Shorts', views: '55.2M', duration: '5:00', durationSec: 300, published: '6 days ago', thumbnail: '' },
      ],
      hindi: [
        { id: '_OBlgSz8sSM', title: 'छोटा भीम — Kalia की मस्ती 30 Sec 😂', channel: 'Chhota Bheem Hindi', views: '48.3M', duration: '0:28', durationSec: 28, published: '5 hours ago', thumbnail: '' },
        { id: 'QH2-TGUlwu4', title: 'Motu Patlu — समोसे का कारनामा! 🥟', channel: 'Motu Patlu', views: '36.7M', duration: '0:45', durationSec: 45, published: '1 day ago', thumbnail: '' },
        { id: 'ktvTqknDobU', title: 'Doraemon — डोरा की गैजेट 1 min Hindi', channel: 'Doraemon Hindi', views: '27.9M', duration: '1:05', durationSec: 65, published: '2 days ago', thumbnail: '' },
        { id: 'FTQbiNvZqaY', title: 'Shiva — भागते लुटेरे हिंदी 2 min 🏍️', channel: 'Shiva Hindi', views: '18.4M', duration: '2:10', durationSec: 130, published: '3 days ago', thumbnail: '' },
        { id: 'KeEbCInHKMY', title: 'Krishna Balram — नई कहानी 3 min', channel: 'KB Hindi', views: '12.6M', duration: '3:15', durationSec: 195, published: '4 days ago', thumbnail: '' },
        { id: 'SrODRkTIOUo', title: 'Chacha Chaudhary — Comic Powers 4 min', channel: 'Chacha Hindi', views: '9.1M', duration: '4:00', durationSec: 240, published: '5 days ago', thumbnail: '' },
        { id: 'AyGtUhWAy0E', title: 'Little Singham — Action Short 5 min Hindi', channel: 'Singham Hindi', views: '21.3M', duration: '5:00', durationSec: 300, published: '1 week ago', thumbnail: '' },
        { id: 'mDu2DuNFyRc', title: 'Oggy and Cockroaches Hindi — Best Moments', channel: 'Oggy Hindi', views: '14.8M', duration: '0:55', durationSec: 55, published: '2 days ago', thumbnail: '' },
      ]
    },
    maths: {
      english: [
        { id: '0ZKisVMqMF4', title: '1+1=2 — Easy Addition Song for Kids ➕', channel: 'Maths Fun', views: '9.4M', duration: '0:30', durationSec: 30, published: '8 hours ago', thumbnail: '' },
        { id: 'nTFEUsudhfs', title: 'Count to 10 with Shapes! 🔢🔺🔵', channel: 'Numberblocks', views: '14.2M', duration: '0:45', durationSec: 45, published: '1 day ago', thumbnail: '' },
        { id: 'PVoiEHMR9WI', title: 'What Shape Am I? — Circle Square Triangle', channel: 'Kids Learning', views: '7.8M', duration: '0:38', durationSec: 38, published: '2 days ago', thumbnail: '' },
        { id: 'AQqhXaR5DaQ', title: '5-3=2 Subtraction — Super Easy for Kids ➖', channel: 'Maths Genie', views: '6.5M', duration: '1:00', durationSec: 60, published: '3 days ago', thumbnail: '' },
        { id: 'aBpHPPGKnco', title: '2 Times Table Song — Sing Along! ✖️', channel: 'Times Tables', views: '18.7M', duration: '1:15', durationSec: 75, published: '12 hours ago', thumbnail: '' },
        { id: 'DK4bSNNOZMI', title: 'Odd and Even Numbers — 1 Min Explained', channel: 'Math Explained', views: '5.3M', duration: '1:30', durationSec: 90, published: '4 days ago', thumbnail: '' },
        { id: '3eWzRHm6kGY', title: 'Big and Small — Comparing Numbers 2 Min', channel: 'Kids Maths', views: '4.9M', duration: '2:00', durationSec: 120, published: '5 days ago', thumbnail: '' },
        { id: 'L4EE19RbXpM', title: 'Count by 10s to 100! — Kids Number Song', channel: 'Counting Songs', views: '11.6M', duration: '2:30', durationSec: 150, published: '1 day ago', thumbnail: '' },
        { id: 'ktvTqknDobU', title: 'Fractions Made Fun! 1/2 1/4 3 Min Kids', channel: 'Math For Kids', views: '7.2M', duration: '3:10', durationSec: 190, published: '3 days ago', thumbnail: '' },
        { id: 'HQoRXvalfwI', title: 'Time on a Clock — Hour and Minute 4 Min', channel: 'Clock Kids', views: '8.4M', duration: '4:00', durationSec: 240, published: '2 days ago', thumbnail: '' },
        { id: 'mDu2DuNFyRc', title: 'Money Maths — Coins and Notes for Kids 5 Min', channel: 'Money Math', views: '6.1M', duration: '4:55', durationSec: 295, published: '1 week ago', thumbnail: '' },
        { id: 'SrODRkTIOUo', title: 'Patterns in Maths — Red Blue Red? 0:40 🔴🔵', channel: 'Pattern Play', views: '5.8M', duration: '0:40', durationSec: 40, published: '6 hours ago', thumbnail: '' },
      ],
      hindi: [
        { id: '3eWzRHm6kGY', title: '1+1=2 — जोड़ना सीखो आसान गाने से ➕', channel: 'Hindi Maths', views: '7.6M', duration: '0:35', durationSec: 35, published: '6 hours ago', thumbnail: '' },
        { id: 'L4EE19RbXpM', title: '1 से 10 गिनती — बच्चों के लिए 🔢', channel: 'Ginti Hindi', views: '12.3M', duration: '0:50', durationSec: 50, published: '1 day ago', thumbnail: '' },
        { id: 'mDu2DuNFyRc', title: 'आकार — गोला चौकोर त्रिभुज Hindi Shapes', channel: 'Shape Hindi', views: '5.4M', duration: '0:42', durationSec: 42, published: '2 days ago', thumbnail: '' },
        { id: 'HQoRXvalfwI', title: 'घटाव — 5-2=3 आसानी से सीखो ➖ 1 min', channel: 'Math Hindi', views: '6.8M', duration: '1:10', durationSec: 70, published: '3 days ago', thumbnail: '' },
        { id: 'ktvTqknDobU', title: 'पहाड़ा 2 का — गाते-गाते याद करो ✖️', channel: 'Pahade Hindi', views: '15.4M', duration: '1:30', durationSec: 90, published: '12 hours ago', thumbnail: '' },
        { id: 'FTQbiNvZqaY', title: 'सम और विषम संख्या — 2 Min Hindi', channel: 'Odd Even Hindi', views: '4.3M', duration: '2:00', durationSec: 120, published: '4 days ago', thumbnail: '' },
        { id: 'SrODRkTIOUo', title: 'बड़ा छोटा — तुलना करना सीखो 3 Min', channel: 'Comparison Hindi', views: '3.9M', duration: '3:05', durationSec: 185, published: '5 days ago', thumbnail: '' },
        { id: 'AyGtUhWAy0E', title: '1 से 100 तक गिनती गाना — Kids Song 4 Min', channel: 'Counting Hindi', views: '9.7M', duration: '4:15', durationSec: 255, published: '1 week ago', thumbnail: '' },
      ]
    }
  },

  // ============================================
  // FEATURED SECTIONS DATA
  // ============================================

  // Featured Maths Shorts (shown in dedicated section)
  MATHS_FEATURED: [
    { id: '0ZKisVMqMF4', title: '1+1=2 Addition Song 🎵', channel: 'Maths Fun', views: '9.4M', duration: '0:30', durationSec: 30, published: '8 hours ago', lang: 'english', thumbnail: '' },
    { id: 'nTFEUsudhfs', title: 'Count to 10 with Shapes! 🔺', channel: 'Numberblocks', views: '14.2M', duration: '0:45', durationSec: 45, published: '1 day ago', lang: 'english', thumbnail: '' },
    { id: 'aBpHPPGKnco', title: '2x Table Song — Sing Along! ✖️', channel: 'Times Tables', views: '18.7M', duration: '1:15', durationSec: 75, published: '12 hours ago', lang: 'english', thumbnail: '' },
    { id: 'PVoiEHMR9WI', title: 'Shapes: Circle Square Triangle', channel: 'Kids Learning', views: '7.8M', duration: '0:38', durationSec: 38, published: '2 days ago', lang: 'english', thumbnail: '' },
    { id: '3eWzRHm6kGY', title: 'जोड़ना सीखो — Hindi Addition Song ➕', channel: 'Hindi Maths', views: '7.6M', duration: '0:35', durationSec: 35, published: '6 hours ago', lang: 'hindi', thumbnail: '' },
    { id: 'L4EE19RbXpM', title: '1 से 10 गिनती बच्चों के लिए 🔢', channel: 'Ginti Hindi', views: '12.3M', duration: '0:50', durationSec: 50, published: '1 day ago', lang: 'hindi', thumbnail: '' },
    { id: 'DK4bSNNOZMI', title: 'Odd and Even Numbers — 1 Min!', channel: 'Math Explained', views: '5.3M', duration: '1:30', durationSec: 90, published: '4 days ago', lang: 'english', thumbnail: '' },
    { id: 'ktvTqknDobU', title: 'पहाड़ा 2 का — गाते याद करो ✖️', channel: 'Pahade Hindi', views: '15.4M', duration: '1:30', durationSec: 90, published: '12 hours ago', lang: 'hindi', thumbnail: '' },
  ],

  // Featured Cartoon Shorts (shown in dedicated section)
  CARTOON_FEATURED: [
    { id: 'V2iqyuoJlQ0', title: 'Peppa Pig — Muddy Puddles 30 Sec 🐷', channel: 'Peppa Pig', views: '42.1M', duration: '0:30', durationSec: 30, published: '6 hours ago', lang: 'english', thumbnail: '' },
    { id: 'Oj02jkbOHoQ', title: 'Cocomelon — Baby Shark Dance! 🦈', channel: 'Cocomelon', views: '85.3M', duration: '0:45', durationSec: 45, published: '1 day ago', lang: 'english', thumbnail: '' },
    { id: '_OBlgSz8sSM', title: 'छोटा भीम — Kalia की मस्ती 😂', channel: 'Chhota Bheem', views: '48.3M', duration: '0:28', durationSec: 28, published: '5 hours ago', lang: 'hindi', thumbnail: '' },
    { id: 'QH2-TGUlwu4', title: 'Motu Patlu — समोसे का कारनामा! 🥟', channel: 'Motu Patlu', views: '36.7M', duration: '0:45', durationSec: 45, published: '1 day ago', lang: 'hindi', thumbnail: '' },
    { id: 'mDu2DuNFyRc', title: 'Tom and Jerry — Funniest Chase! 😂', channel: 'Tom & Jerry', views: '31.7M', duration: '0:35', durationSec: 35, published: '12 hours ago', lang: 'english', thumbnail: '' },
    { id: 'SrODRkTIOUo', title: 'Bluey — Best Moments Compilation ✨', channel: 'Bluey', views: '18.9M', duration: '1:00', durationSec: 60, published: '2 days ago', lang: 'english', thumbnail: '' },
    { id: 'ktvTqknDobU', title: 'Doraemon — डोरा की गैजेट Hindi 🎒', channel: 'Doraemon Hindi', views: '27.9M', duration: '1:05', durationSec: 65, published: '2 days ago', lang: 'hindi', thumbnail: '' },
    { id: 'AyGtUhWAy0E', title: 'Paw Patrol — Chase Saves the Day! 🚔', channel: 'Paw Patrol', views: '14.2M', duration: '0:50', durationSec: 50, published: '3 days ago', lang: 'english', thumbnail: '' },
  ],

  // Fake comments for modal
  VIDEO_COMMENTS: [
    [
      { author: 'KidsMom2024', text: '😍 My kids absolutely love this! They watch it every day!', likes: '2.4K' },
      { author: 'TeacherJane', text: '🎓 Great educational content! Using this in my classroom.', likes: '1.8K' },
      { author: 'ParentPriya', text: '✨ So colorful and fun! My daughter asked to watch again!', likes: '956' },
    ],
    [
      { author: 'LearnerMom', text: '🌟 My son learned to count to 10 after just 3 watches!', likes: '3.1K' },
      { author: 'DadOfThree', text: '👏 Amazing way to make maths fun. No more boring worksheets!', likes: '2.2K' },
      { author: 'GrandmaHappy', text: '😊 Even grandma finds this easy to follow along!', likes: '1.4K' },
    ],
    [
      { author: 'CuriousKid007', text: '🤩 BEST VIDEO EVER!! More please!!', likes: '5.6K' },
      { author: 'HomeschoolHub', text: '📚 Perfect for our homeschool routine! Highly recommended.', likes: '2.9K' },
      { author: 'TinyTots', text: '🍎 My 3-year-old points at the screen and dances!', likes: '1.7K' },
    ],
  ]
};
