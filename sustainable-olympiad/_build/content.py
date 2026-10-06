"""Shared content for the Sustainable Olympiad site.

Everything that appears in more than one place (pages, PDFs, calendar file,
search index) lives here so it only has to be edited once. Run build.py after
changing anything in this file.
"""

EVENT = {
    "name": "Sustainable Olympiad",
    "edition": "2026",
    "edition_number": "7th",
    "tagline": "Young minds. Real solutions. One planet.",
    "finals_dates": "28–30 October 2026",
    "finals_iso": "2026-10-28T09:00:00-03:00",
    "finals_label": "28 October 2026 at 09:00 (Brasília time)",
    "registration_deadline": "9 October 2026",
    "registration_deadline_iso": "2026-10-09",
    "venue": "Lisbon (Portugal), Brazil and online",
}

# --------------------------------------------------------------------------
# Competition categories
# --------------------------------------------------------------------------
CATEGORIES = [
    {
        "id": "renewable-energy",
        "name": "Renewable Energy",
        "icon": "sun",
        "summary": "Design ways to generate, store or save clean energy in your school and community.",
        "description": (
            "Teams investigate how communities can move away from fossil fuels. Projects may range from "
            "a solar-powered phone charging station to an energy audit that cuts a school's electricity bill."
        ),
        "brief": "Reduce your school's energy use by at least 15% using low-cost, renewable or efficiency-based measures.",
        "examples": [
            "Small-scale solar, wind or micro-hydro prototypes",
            "Energy audits and behaviour-change campaigns",
            "Low-cost thermal insulation or passive cooling",
        ],
        "skills": "Physics, engineering, data analysis",
    },
    {
        "id": "waste-reduction",
        "name": "Waste Reduction & Circular Economy",
        "icon": "recycle",
        "summary": "Rethink how products are made, used and reused so less ends up in landfill.",
        "description": (
            "Teams tackle the full life cycle of materials, from reducing single-use plastics to turning "
            "food waste into compost, biogas or new products."
        ),
        "brief": "Cut the waste your school or neighbourhood sends to landfill and show measurable results over ten days.",
        "examples": [
            "Composting and food-waste recovery systems",
            "Repair cafés, swap shops and reuse schemes",
            "Biodegradable or upcycled materials",
        ],
        "skills": "Chemistry, biology, entrepreneurship",
    },
    {
        "id": "sustainable-design",
        "name": "Sustainable Design & Architecture",
        "icon": "leaf",
        "summary": "Create products, buildings and public spaces that do more with less.",
        "description": (
            "Teams apply eco-design principles to everyday objects, buildings or neighbourhoods, "
            "considering materials, energy, water and the wellbeing of the people who use them."
        ),
        "brief": "Redesign one space or product in your community so that it uses fewer resources and serves people better.",
        "examples": [
            "Green roofs, shading and natural ventilation",
            "Products designed for repair and disassembly",
            "Accessible, low-carbon public spaces",
        ],
        "skills": "Design, mathematics, art, technology",
    },
    {
        "id": "climate-solutions",
        "name": "Climate Solutions",
        "icon": "globe",
        "summary": "Measure, communicate and act on climate change, locally and globally.",
        "description": (
            "Teams develop tools, campaigns or policy proposals that reduce emissions or help communities "
            "adapt to a changing climate, backed by sound data."
        ),
        "brief": "Calculate a real carbon footprint in your community and propose a credible plan to reduce it.",
        "examples": [
            "Carbon calculators and climate data dashboards",
            "Flood, heat or drought adaptation plans",
            "Climate communication and advocacy campaigns",
        ],
        "skills": "Geography, statistics, communication",
    },
    {
        "id": "water-oceans",
        "name": "Water & Oceans",
        "icon": "drop",
        "summary": "Protect fresh water and marine life through smart monitoring and conservation.",
        "description": (
            "New for 2026. Teams explore water scarcity, pollution and ocean health, building solutions "
            "that save, clean or protect water resources."
        ),
        "brief": "Monitor a local water source for one month and design an intervention that improves its quality or reduces its use.",
        "examples": [
            "Low-cost water quality sensors",
            "Rainwater harvesting and grey-water reuse",
            "Beach and river clean-up data projects",
        ],
        "skills": "Biology, chemistry, electronics",
    },
    {
        "id": "biodiversity-food",
        "name": "Biodiversity & Food Systems",
        "icon": "sprout",
        "summary": "Grow food sustainably and give nature space to thrive.",
        "description": (
            "Teams work on pollinator habitats, school gardens, urban farming or reducing the footprint "
            "of what we eat, combining field observation with practical action."
        ),
        "brief": "Increase biodiversity on your school grounds and document the change with a species survey.",
        "examples": [
            "Pollinator gardens and wildlife corridors",
            "Hydroponics and vertical farming",
            "Low-impact school menus",
        ],
        "skills": "Biology, ecology, nutrition",
    },
]

DIVISIONS = [
    ("Junior", "Ages 12–14"),
    ("Senior", "Ages 15–18"),
    ("University", "Ages 18–25, undergraduate students"),
]

JUDGING = [
    ("Environmental impact", "30%", "How much measurable good does the solution do for people and the planet?"),
    ("Innovation", "25%", "Is the idea original, or does it apply an existing idea in a new way?"),
    ("Feasibility", "20%", "Could the solution realistically be built, funded and scaled?"),
    ("Scientific rigour", "15%", "Are the data, methods and conclusions sound?"),
    ("Communication", "10%", "Is the project explained clearly to a non-specialist audience?"),
]

# --------------------------------------------------------------------------
# Timeline (dates are ISO yyyy-mm-dd; "end" is optional)
# --------------------------------------------------------------------------
TIMELINE = [
    {"id": "registration-opens", "start": "2026-08-03", "title": "Registration opens",
     "desc": "Teams of 2–5 students and a supervising mentor can register online, free of charge.", "kind": "Registration"},
    {"id": "teacher-webinar", "start": "2026-08-20", "title": "Information webinar for teachers and mentors",
     "desc": "A one-hour live session on the format, categories and judging. A recording is published afterwards.", "kind": "Event"},
    {"id": "early-bird", "start": "2026-09-15", "title": "Early-bird deadline",
     "desc": "Teams registered by this date receive a printed starter kit with sensors and seeds for their project.", "kind": "Deadline"},
    {"id": "registration-deadline", "start": "2026-10-09", "title": "Registration deadline",
     "desc": "Registration closes at 23:59 Brasília time. Team details can be edited until Round 1 starts.", "kind": "Deadline"},
    {"id": "round-1", "start": "2026-10-10", "title": "Round 1: Online Knowledge Challenge",
     "desc": "A 90-minute online quiz on sustainability science, taken by each team from their own school.", "kind": "Competition round"},
    {"id": "round-1-results", "start": "2026-10-13", "title": "Round 1 results",
     "desc": "The top teams in each category and division advance to the Project Challenge.", "kind": "Results"},
    {"id": "round-2", "start": "2026-10-14", "end": "2026-10-23", "title": "Round 2: Project Challenge",
     "desc": "Teams have ten days to build and test a real solution, then submit a report and a three-minute video.", "kind": "Competition round"},
    {"id": "finalists", "start": "2026-10-24", "title": "Finalists announced",
     "desc": "Up to 60 finalist teams are invited to the Global Finals, in person or online.", "kind": "Results"},
    {"id": "finals", "start": "2026-10-28", "end": "2026-10-29", "title": "Global Finals",
     "desc": "Finalists present their projects to an international jury in Lisbon (Portugal), in Brazil and online, with both venues linked live.", "kind": "Finals"},
    {"id": "awards", "start": "2026-10-30", "title": "Awards Ceremony",
     "desc": "Gold, silver and bronze medals in every category, plus the Planet Award for the best overall project. Streamed live.", "kind": "Ceremony"},
]

# --------------------------------------------------------------------------
# Rulebook. Each section: (id, heading, [paragraphs], [bullet items])
# Inline <b> is allowed; it becomes <strong> on the website.
# --------------------------------------------------------------------------
RULES = [
    ("eligibility", "1. Eligibility", [
        "The Olympiad is open to students aged 12 to 25 who are enrolled in a school, college or university during 2026.",
    ], [
        "<b>Junior division:</b> students aged 12–14 on 1 August 2026.",
        "<b>Senior division:</b> students aged 15–18 on 1 August 2026.",
        "<b>University division:</b> undergraduate students aged 18–25.",
        "A team competes in the division of its oldest member.",
    ]),
    ("teams", "2. Teams and mentors", [
        "Each team has 2 to 5 students and one supervising mentor aged 21 or over, normally a teacher or lecturer.",
    ], [
        "Students may belong to only one team per edition.",
        "A mentor may supervise up to three teams.",
        "Mentors guide and support, but the work must be done by the students.",
        "Team members can be replaced until the Round 1 start date by contacting the organisers.",
    ]),
    ("registration", "3. Registration", [
        "Registration is free and is completed online by the team captain before the registration deadline.",
    ], [
        "Each team chooses one category when registering. The category can be changed until Round 1 starts.",
        "For students under 18, the mentor confirms that parental or guardian consent has been obtained.",
        "Schools may register more than one team.",
    ]),
    ("rounds", "4. Competition format", [
        "The Olympiad has three stages. Teams that do not advance still receive written feedback and a certificate of participation.",
    ], [
        "<b>Round 1, Online Knowledge Challenge:</b> a 90-minute multiple-choice and short-answer quiz taken together as a team.",
        "<b>Round 2, Project Challenge:</b> ten days to build and test a solution to the category brief, with a report of up to 3,000 words and a three-minute video.",
        "<b>Global Finals:</b> a ten-minute presentation and a ten-minute question-and-answer session with the jury, in person or online.",
    ]),
    ("submissions", "5. Project submissions", [
        "Round 2 submissions are uploaded through the participant portal before 23:59 Brasília time on the deadline date.",
    ], [
        "Reports are submitted as PDF and videos as MP4 or a public video link.",
        "Videos must include captions, and reports must use headings and alt text for images.",
        "All sources, data sets and tools, including AI tools, must be credited.",
        "Late submissions are accepted only in documented emergencies.",
    ]),
    ("judging", "6. Judging", [
        "Projects are scored by an independent jury of scientists, educators, engineers and entrepreneurs. Each project is reviewed by at least three judges.",
    ], [
        "Environmental impact: 30%",
        "Innovation: 25%",
        "Feasibility: 20%",
        "Scientific rigour: 15%",
        "Communication: 10%",
        "Judges declare any conflict of interest and do not score teams from their own institution.",
        "The jury's decisions are final.",
    ]),
    ("integrity", "7. Academic integrity", [
        "Teams must submit their own original work. Plagiarism, data fabrication or undisclosed outside help leads to disqualification.",
    ], [
        "AI tools may be used for research and editing, provided their use is described in the report.",
        "Projects must not have won another international competition before.",
    ]),
    ("safety", "8. Safety and ethics", [
        "Experiments must be carried out safely and under adult supervision where needed.",
    ], [
        "No project may harm people, animals or ecosystems.",
        "Research with human participants requires informed consent and must protect their privacy.",
        "Mains electricity, hazardous chemicals and power tools may be used only under a mentor's supervision.",
    ]),
    ("conduct", "9. Code of conduct", [
        "The Olympiad is an inclusive community. Participants, mentors, judges and volunteers treat each other with respect.",
    ], [
        "Harassment and discrimination of any kind are not tolerated.",
        "Concerns can be reported confidentially to the organisers at any time.",
    ]),
    ("accessibility-rules", "10. Accessibility and reasonable adjustments", [
        "We want everyone to be able to take part. Teams can request adjustments such as extra time, screen-reader-compatible quiz formats, sign language interpretation or step-free venue access.",
    ], [
        "Request adjustments in the registration form or by contacting us at least two weeks before the relevant round.",
    ]),
    ("ip", "11. Intellectual property and media", [
        "Teams keep full ownership of their ideas and projects.",
    ], [
        "By entering, teams allow the organisers to share project summaries, photos and videos to promote the Olympiad, with credit.",
        "Teams may opt out of photography at the Finals.",
    ]),
    ("prizes", "12. Prizes", [
        "Gold, silver and bronze medals are awarded in each category and division. The Planet Award goes to the best project overall.",
    ], [
        "Winning teams receive grants of up to €5,000 to develop their project further.",
        "All finalists receive certificates and mentoring from our partners.",
    ]),
]

GUIDELINES = [
    ("Before you register", [
        "Form a team of 2–5 students with a mix of skills: science, design, writing and presenting.",
        "Find a mentor, usually a teacher, who can meet with you regularly.",
        "Read the rulebook and choose the category that excites your team most.",
    ]),
    ("Preparing for Round 1", [
        "Review the sustainability topics in the study guide on our Resources page.",
        "Practise with past quizzes and agree how your team will divide questions.",
        "Test your internet connection and device the day before.",
    ]),
    ("Running your project in Round 2", [
        "Start with a clear problem statement and measure your baseline before you change anything.",
        "Keep a project log with dates, data, photos and decisions.",
        "Involve your community: interview the people affected by the problem.",
        "Make your report and video accessible, with headings, alt text and captions.",
    ]),
    ("Presenting at the Finals", [
        "Tell a story: the problem, what you tried, what you measured and what you learned.",
        "Show real evidence. Judges value honest results, including failures.",
        "Rehearse answering questions and share speaking time across the team.",
    ]),
]

TIPS = [
    ("Energy", [
        "Switch off lights, screens and chargers when you leave a room.",
        "Use daylight where you can and choose LED bulbs.",
        "Lower the heating by 1 °C. It can cut heating energy use by up to 10%.",
    ]),
    ("Waste", [
        "Carry a reusable bottle, cup and lunch box.",
        "Repair, swap or donate before you throw away.",
        "Sort your recycling correctly. A contaminated bin can end up in landfill.",
    ]),
    ("Water", [
        "Take shorter showers and turn the tap off while brushing your teeth.",
        "Collect rainwater for plants.",
        "Report leaking taps and pipes at school.",
    ]),
    ("Food", [
        "Plan meals and use leftovers to reduce food waste.",
        "Eat more seasonal, local and plant-based food.",
        "Compost fruit and vegetable scraps.",
    ]),
    ("Transport", [
        "Walk, cycle, scoot or take public transport where you can.",
        "Share rides for longer journeys.",
        "Choose video calls when travelling is not necessary.",
    ]),
    ("Nature", [
        "Plant native flowers for pollinators.",
        "Leave a wild corner in gardens and school grounds.",
        "Join or organise a local clean-up.",
    ]),
]

DOWNLOADS = [
    ("rulebook", "Official Rulebook 2026", "sustainable-olympiad-rulebook-2026.pdf",
     "Eligibility, teams, format, judging, conduct and prizes.", "rules.html#rules"),
    ("guidelines", "Participant Guidelines", "sustainable-olympiad-participant-guidelines.pdf",
     "Practical advice for every stage, from registration to the Finals.", "rules.html#guidelines"),
    ("tips", "Sustainability Tips", "sustainable-olympiad-sustainability-tips.pdf",
     "18 everyday actions for students, schools and families.", "rules.html#tips"),
]

# --------------------------------------------------------------------------
# Sponsors / partners (illustrative names; replace with real partners)
# --------------------------------------------------------------------------
SPONSORS = {
    "Founding Partner": [
        ("Open Planet Foundation", "openplanet", "Funds the Olympiad's education programme and student grants."),
    ],
    "Gold Partners": [
        ("Verdalis Energy", "verdalis", "Provides solar starter kits for Renewable Energy teams."),
        ("Bluetide Water Lab", "bluetide", "Supports the new Water & Oceans category."),
    ],
    "Silver Partners": [
        ("Circulo Materials", "circulo", "Sponsors the Waste Reduction awards."),
        ("Heliora Mobility", "heliora", "Offsets travel for finalist teams."),
        ("Greenleaf Learning", "greenleaf", "Publishes our free classroom resources."),
    ],
    "Community Partners": [
        ("Youth Climate Network", "ycn", "Connects teams with local climate groups."),
        ("Makers Without Borders", "mwb", "Runs prototyping workshops for teams."),
        ("EduAccess Alliance", "eduaccess", "Advises on accessibility and inclusion."),
    ],
}

# --------------------------------------------------------------------------
# Participating schools and institutions (illustrative)
# (name, city, country, lat, lng, type)
# --------------------------------------------------------------------------
SCHOOLS = [
    ("Riverside Secondary School", "Lisbon", "Portugal", 38.72, -9.14, "Secondary school"),
    ("Escola Verde do Porto", "Porto", "Portugal", 41.15, -8.61, "Secondary school"),
    ("Northfield Academy", "Manchester", "United Kingdom", 53.48, -2.24, "Secondary school"),
    ("Harbourview College", "Cardiff", "United Kingdom", 51.48, -3.18, "College"),
    ("Lycée des Énergies Nouvelles", "Lyon", "France", 45.76, 4.84, "Secondary school"),
    ("Gymnasium am Stadtpark", "Hamburg", "Germany", 53.55, 9.99, "Secondary school"),
    ("Technical University Green Lab", "Delft", "Netherlands", 52.01, 4.36, "University"),
    ("Instituto Sol Naciente", "Valencia", "Spain", 39.47, -0.38, "Secondary school"),
    ("Liceo Scientifico Mare Blu", "Genoa", "Italy", 44.41, 8.93, "Secondary school"),
    ("Nordlys School", "Bergen", "Norway", 60.39, 5.32, "Secondary school"),
    ("Savanna Heights School", "Nairobi", "Kenya", -1.29, 36.82, "Secondary school"),
    ("Lagos Innovation College", "Lagos", "Nigeria", 6.52, 3.38, "College"),
    ("Cape Coast Eco School", "Cape Town", "South Africa", -33.92, 18.42, "Secondary school"),
    ("Colégio Mata Atlântica", "São Paulo", "Brazil", -23.55, -46.63, "Secondary school"),
    ("Universidad Andina Sostenible", "Bogotá", "Colombia", 4.71, -74.07, "University"),
    ("Lakeshore High School", "Toronto", "Canada", 43.65, -79.38, "Secondary school"),
    ("Bayside STEM Academy", "San Francisco", "United States", 37.77, -122.42, "Secondary school"),
    ("Prairie View Middle School", "Denver", "United States", 39.74, -104.99, "Middle school"),
    ("Sakura Science High School", "Osaka", "Japan", 34.69, 135.50, "Secondary school"),
    ("Monsoon International School", "Pune", "India", 18.52, 73.86, "Secondary school"),
    ("Banyan Tree Academy", "Chennai", "India", 13.08, 80.27, "Secondary school"),
    ("Coral Coast College", "Brisbane", "Australia", -27.47, 153.03, "College"),
    ("Kauri Grove School", "Auckland", "New Zealand", -36.85, 174.76, "Secondary school"),
    ("Mekong Future School", "Ho Chi Minh City", "Vietnam", 10.82, 106.63, "Secondary school"),
]

STATS = [
    ("6", "editions held"),
    ("62", "countries"),
    ("4,800+", "students"),
    ("1,150", "projects submitted"),
]

HISTORY = [
    ("2020", "The first Olympiad", "Three science teachers launch an online challenge for 40 teams from 14 countries during school closures."),
    ("2021", "Going global", "A free mentor programme opens, and participation triples to 120 teams."),
    ("2022", "First in-person Finals", "Finalists meet in Lisbon, and the University division is introduced."),
    ("2023", "Open Planet Foundation joins", "Student grants of up to €5,000 help winning teams turn prototypes into real projects."),
    ("2024", "Accessibility first", "Captioned sessions, screen-reader-compatible quizzes and travel support become standard, and the Climate Solutions category is introduced."),
    ("2025", "Sixth edition", "A record 280 teams from 62 countries take part; the winning team turns cafeteria waste into bioplastic."),
]

# --------------------------------------------------------------------------
# News
# --------------------------------------------------------------------------
NEWS = [
    {"id": "registration-2026-open", "date": "2026-08-03", "tag": "Announcement",
     "title": "Registration for the 2026 Olympiad is now open",
     "body": [
         "Teams from around the world can now register for the seventh Sustainable Olympiad. Registration is free and closes on 9 October 2026.",
         "Teams that register before 15 September receive a starter kit with a temperature and humidity sensor, a soil test kit and native wildflower seeds.",
     ]},
    {"id": "water-oceans-category", "date": "2026-08-10", "tag": "Competition",
     "title": "New for 2026: the Water & Oceans category",
     "body": [
         "Water scarcity and ocean pollution were the topics students asked about most in our 2025 survey. This year they get a category of their own.",
         "Teams will monitor a local water source for a month and design an intervention that improves its quality or reduces its use.",
     ]},
    {"id": "teacher-webinar", "date": "2026-08-10", "tag": "Event",
     "title": "Teachers' webinar: bringing the Olympiad to your classroom",
     "body": [
         "Join us online on 20 August for a one-hour introduction to the format, categories and judging, with time for questions.",
         "The session is captioned live, and the recording and slides will be shared afterwards.",
     ]},
    {"id": "open-planet-partnership", "date": "2026-07-10", "tag": "Partners",
     "title": "Open Planet Foundation renews founding partnership",
     "body": [
         "The Open Planet Foundation has renewed its support for another three editions, funding student grants and the mentor programme.",
         "The partnership also makes travel support available to every in-person finalist team that needs it.",
     ]},
    {"id": "2025-champions", "date": "2025-10-31", "tag": "Results",
     "title": "2025 champions turn cafeteria waste into bioplastic",
     "body": [
         "The Planet Award 2025 went to a Senior team from Nairobi. They turned food waste from their school cafeteria into a biodegradable packaging film.",
         "Their pilot diverted 1.2 tonnes of waste from landfill in a single term. The team will use their €5,000 grant to scale production with a local cooperative.",
     ]},
    {"id": "sixth-edition-numbers", "date": "2025-11-05", "tag": "Results",
     "title": "Our sixth edition in numbers",
     "body": [
         "1,140 students in 280 teams from 62 countries took part in the 2025 Olympiad, and 47% of participants were girls or young women.",
         "Together, the Round 2 projects reported savings of 410 MWh of energy and 2.3 million litres of water.",
     ]},
]

GALLERY = [
    ("solar", "Junior team members install a small solar panel array on their school roof.", "2025 Renewable Energy finalists, Lisbon"),
    ("wind", "Students test a hand-built wind turbine prototype on a hillside.", "Wind prototype testing, 2024"),
    ("recycling", "A team sorts collected waste into colour-coded recycling bins.", "Waste audit in Round 2, 2025"),
    ("trees", "Students plant native saplings along a school fence line.", "Biodiversity project, 2023"),
    ("ocean", "Volunteers on a small boat collect plastic from the water with a net.", "Ocean clean-up data project, 2025"),
    ("lab", "Students analyse water samples with a laptop and test tubes in a classroom lab.", "Water quality monitoring, 2024"),
    ("garden", "A rooftop garden with raised beds, solar panels and a rain barrel on a city building.", "Sustainable design winner, 2022"),
    ("awards", "Three teams stand on a podium holding a trophy as confetti falls.", "Awards Ceremony, Lisbon 2025"),
]

# --------------------------------------------------------------------------
# FAQ: (group, [(question, answer_html)])
# --------------------------------------------------------------------------
FAQ = [
    ("General", [
        ("What is the Sustainable Olympiad?",
         "An international competition where student teams develop real solutions to environmental challenges in six categories, from renewable energy to biodiversity. <a href=\"about.html\">Learn more about us</a>."),
        ("Who can take part?",
         "Students aged 12 to 25 who are enrolled in a school, college or university. Teams compete in the Junior (12–14), Senior (15–18) or University (18–25) division."),
        ("Does it cost anything to participate?",
         "No. Registration, all competition rounds and the starter resources are free. Travel support is available for in-person finalist teams."),
        ("Is the competition held in English?",
         "Yes, the Olympiad is run in English. Teams may use translation tools and should mention this in their report. Judges assess ideas, not language skills."),
    ]),
    ("Registration", [
        ("How do I register a team?",
         "The team captain completes the <a href=\"register.html\">online registration form</a> before 9 October 2026. You will need the details of every team member and your mentor."),
        ("Can I take part on my own?",
         "Teams need at least two students. If you cannot find teammates, <a href=\"contact.html\">contact us</a> and we will try to match you with other students from your region."),
        ("Can we change our category or team members after registering?",
         "Yes. Changes are allowed until Round 1 starts on 10 October 2026. Email us with your team name and the change."),
        ("Does our mentor have to be a teacher?",
         "Usually yes, but any responsible adult aged 21 or over with a connection to your school or university can act as mentor."),
    ]),
    ("Competition", [
        ("Do we need to travel to compete?",
         "No. Rounds 1 and 2 take place online from your school. The Global Finals are hybrid, so finalists can present in Lisbon (Portugal), in Brazil or online."),
        ("What equipment do we need?",
         "A computer with an internet connection is enough for Round 1. For Round 2, most projects use low-cost or recycled materials. Expensive equipment does not earn extra points."),
        ("Can we use AI tools?",
         "Yes, for research and editing, as long as you describe how you used them in your report. The ideas and the work must be your team's own."),
        ("Are past papers available?",
         "Yes. Round 1 papers from previous editions, with mark schemes and worked solutions, are on the "
         "<a href=\"past-papers.html\">Past Papers</a> page. You can practise online or download PDFs."),
        ("How are projects judged?",
         "By an independent jury using five weighted criteria: impact, innovation, feasibility, scientific rigour and communication. See the <a href=\"rules.html#judging\">judging criteria</a>."),
    ]),
    ("Support & Accessibility", [
        ("What accessibility support is available?",
         "We offer extra time, screen-reader-compatible quizzes, captioned sessions, sign language interpretation and step-free venues. Request adjustments when you register or <a href=\"contact.html\">contact us</a>."),
        ("How can my school become a partner or host an event?",
         "We would love to hear from you. Visit <a href=\"partners.html\">Partners</a> or <a href=\"contact.html?subject=partnership\">get in touch</a>."),
        ("How do you use our personal data?",
         "We use registration data only to run the competition, and we never sell it. Mentors confirm guardian consent for participants under 18. Data is deleted 12 months after each edition."),
    ]),
]
