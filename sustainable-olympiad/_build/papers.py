"""Past Round 1 papers (Online Knowledge Challenge) with mark schemes.

Text may use <sub>, <sup>, <b>, <i> and the entities &amp; &lt; &gt;. The same
markup is rendered on the website and in the PDFs. Every numerical answer is
checked by verify_papers.py, so run that after editing a calculation.

Part A: multiple choice, 2 marks each. Part B: structured problems.
"""
import re

CO2 = "CO<sub>2</sub>"
CH4 = "CH<sub>4</sub>"
N2O = "N<sub>2</sub>O"

DATA_SENIOR = [
    "Acceleration due to gravity: <i>g</i> = 9.81 m s<sup>−2</sup>",
    "Specific heat capacity of water: <i>c</i> = 4.18 kJ kg<sup>−1</sup> K<sup>−1</sup>; density of water 1.00 kg L<sup>−1</sup>",
    "1 kWh = 3.6 MJ; 0 °C = 273.15 K; 1 year = 8760 h",
    "Planck constant <i>h</i> = 6.63 × 10<sup>−34</sup> J s; speed of light <i>c</i> = 3.00 × 10<sup>8</sup> m s<sup>−1</sup>; 1 eV = 1.60 × 10<sup>−19</sup> J",
    "Stefan–Boltzmann constant σ = 5.67 × 10<sup>−8</sup> W m<sup>−2</sup> K<sup>−4</sup>",
    "Molar masses (g mol<sup>−1</sup>): H 1.008, C 12.01, N 14.01, O 16.00",
]

DATA_JUNIOR = [
    "1 kWh = 1000 Wh = 3.6 MJ; 1 tonne (t) = 1000 kg",
    "1 litre of water has a mass of 1 kg",
    "Heating 1 kg of water by 1 °C needs 4.18 kJ",
    "1 hectare (ha) = 10 000 m<sup>2</sup>; 1 km<sup>2</sup> = 100 ha",
]

PAPERS = [
    # ======================================================================
    {
        "id": "2025-senior", "year": 2025, "division": "Senior", "ages": "15–18",
        "duration": 90,
        "topics": ["Solar and wind energy", "Thermodynamics and heat pumps", "Combustion chemistry",
                   "Population ecology", "Water management", "Radiative forcing"],
        "data": DATA_SENIOR + [
            "Radiative forcing of " + CO2 + ": Δ<i>F</i> = 5.35 ln(<i>C</i>/<i>C</i><sub>0</sub>) W m<sup>−2</sup>",
        ],
        "part_a": [
            {"q": "A rooftop solar module has an area of 1.6 m<sup>2</sup> and an efficiency of 20%. On a day equivalent to "
                  "4.5 peak sun hours at 1000 W m<sup>−2</sup>, approximately how much electrical energy does it produce?",
             "options": ["0.32 kWh", "1.44 kWh", "7.2 kWh", "14.4 kWh"], "answer": "B",
             "solution": "Power at peak irradiance: <i>P</i> = 1.6 m<sup>2</sup> × 0.20 × 1000 W m<sup>−2</sup> = 320 W. "
                         "Energy: 320 W × 4.5 h = 1440 Wh = <b>1.44 kWh</b>. Option A forgets the 4.5 hours."},
            {"q": "Over 20 years, the global warming potential (GWP) of methane is about 81, but over 100 years it is only about 28. "
                  "What is the main reason for this difference?",
             "options": ["Methane absorbs infrared radiation more strongly as its concentration rises",
                         "Methane has an atmospheric lifetime of only about 12 years, so most of its warming happens in the first decades",
                         "Methane is oxidised to " + CO2 + ", which has a higher GWP than methane",
                         "The 100-year GWP includes absorption of methane by the oceans"],
             "answer": "B",
             "solution": "GWP compares the warming caused by a pulse of gas with the same mass of " + CO2 + " over a chosen time horizon. "
                         "Methane is removed (mainly by OH radicals) with a lifetime of about 12 years. Averaged over 100 years, "
                         "its short, intense effect is diluted, while long-lived " + CO2 + " keeps warming. "
                         "Option C is false: the " + CO2 + " produced has a GWP of 1 by definition."},
            {"q": "According to Betz's law, what is the maximum fraction of the kinetic energy flux of the wind that an ideal "
                  "turbine can extract?",
             "options": ["1/3", "1/2", "16/27", "8/9"], "answer": "C",
             "solution": "Extracting all the energy would stop the air behind the rotor, so no more air could flow through. "
                         "Momentum theory gives an optimum when the wind is slowed to one third of its upstream speed, "
                         "giving a maximum power coefficient of <b>16/27 ≈ 59.3%</b>."},
            {"q": "The power available to a wind turbine is <i>P</i> = ½ρ<i>Av</i><sup>3</sup>. If the mean wind speed at a site "
                  "is 9.0 m s<sup>−1</sup> instead of 6.0 m s<sup>−1</sup>, by what factor does the available power increase?",
             "options": ["1.5", "2.25", "3.375", "4.5"], "answer": "C",
             "solution": "<i>P</i> ∝ <i>v</i><sup>3</sup>, so the factor is (9.0/6.0)<sup>3</sup> = 1.5<sup>3</sup> = <b>3.375</b>. "
                         "This is why turbines are placed on hilltops and offshore."},
            {"q": "The average pH of the surface ocean has fallen from about 8.2 to 8.1 since pre-industrial times. By approximately "
                  "what percentage has the hydrogen-ion concentration increased?",
             "options": ["1%", "10%", "26%", "100%"], "answer": "C",
             "solution": "pH = −log<sub>10</sub>[H<sup>+</sup>], so [H<sup>+</sup>]<sub>new</sub>/[H<sup>+</sup>]<sub>old</sub> = "
                         "10<sup>8.2 − 8.1</sup> = 10<sup>0.1</sup> ≈ 1.26, an increase of about <b>26%</b>."},
            {"q": "Producers in a grassland fix 50 000 kJ m<sup>−2</sup> yr<sup>−1</sup>. Assuming 10% of the energy is transferred "
                  "between successive trophic levels, how much energy is available to tertiary consumers?",
             "options": ["5000 kJ m<sup>−2</sup> yr<sup>−1</sup>", "500 kJ m<sup>−2</sup> yr<sup>−1</sup>",
                         "50 kJ m<sup>−2</sup> yr<sup>−1</sup>", "5 kJ m<sup>−2</sup> yr<sup>−1</sup>"],
             "answer": "C",
             "solution": "Producers 50 000 → primary consumers 5000 → secondary consumers 500 → tertiary consumers "
                         "<b>50 kJ m<sup>−2</sup> yr<sup>−1</sup></b>. Tertiary consumers are three transfers away from the producers."},
            {"q": "In a eutrophic lake, which process is most directly responsible for the sharp fall in dissolved oxygen after an "
                  "algal bloom?",
             "options": ["Algae absorbing oxygen through their cell walls during the day",
                         "Aerobic decomposition of dead algae by bacteria",
                         "Nitrogen fixation by cyanobacteria",
                         "An increase in oxygen solubility as the water cools"],
             "answer": "B",
             "solution": "When the bloom dies, the huge mass of organic matter is broken down by aerobic bacteria, whose respiration "
                         "consumes dissolved oxygen faster than it can be replaced. During the day algae photosynthesise and "
                         "release oxygen, and cooler water holds <i>more</i> oxygen, so A and D are wrong."},
            {"q": "Which of the following is a <b>negative</b> (stabilising) feedback in the climate system?",
             "options": ["The ice–albedo feedback",
                         "Release of methane from thawing permafrost",
                         "The water-vapour feedback",
                         "Increased emission of infrared radiation from a warmer surface"],
             "answer": "D",
             "solution": "By the Stefan–Boltzmann law, a warmer surface emits more radiation (∝ <i>T</i><sup>4</sup>), which "
                         "opposes further warming. This is the Planck response. The other three amplify an initial warming, "
                         "so they are positive feedbacks."},
            {"q": "A geothermal power plant takes heat from a reservoir at 180 °C and rejects heat to cooling water at 30 °C. "
                  "What is its maximum theoretical (Carnot) efficiency?",
             "options": ["17%", "33%", "67%", "83%"], "answer": "B",
             "solution": "Temperatures must be in kelvin: η = 1 − <i>T</i><sub>C</sub>/<i>T</i><sub>H</sub> = "
                         "1 − 303.15/453.15 = 0.331 ≈ <b>33%</b>. Options A and D come from wrongly using degrees Celsius."},
            {"q": "A heat pump with a coefficient of performance (COP) of 3.5 delivers 14 kW of heat to a building. "
                  "At what rate does it extract heat from the outside air?",
             "options": ["3.5 kW", "4.0 kW", "10 kW", "49 kW"], "answer": "C",
             "solution": "Electrical input = 14 kW / 3.5 = 4.0 kW. By conservation of energy, heat delivered = heat extracted + "
                         "work input, so heat extracted = 14 − 4.0 = <b>10 kW</b>."},
        ],
        "part_b": [
            {"title": "Decarbonising school heating",
             "stem": "A school needs 108 000 kWh of heat per year. The heat is supplied by a gas boiler with an efficiency of 90%. "
                     "Burning natural gas releases 0.20 kg " + CO2 + " per kWh of gas burned. The school is considering an "
                     "air-source heat pump with a seasonal COP of 3.0. Grid electricity has an emission factor of "
                     "0.25 kg " + CO2 + " per kWh.",
             "parts": [
                 {"text": "Calculate the annual " + CO2 + " emissions from the gas boiler, in tonnes.", "marks": 2,
                  "solution": "Gas burned = 108 000 / 0.90 = 120 000 kWh. Emissions = 120 000 × 0.20 = 24 000 kg = <b>24 t</b>.",
                  "scheme": "1 mark for dividing by the efficiency; 1 mark for the answer."},
                 {"text": "Calculate the annual " + CO2 + " emissions if the heat pump supplies all the heat.", "marks": 2,
                  "solution": "Electricity = 108 000 / 3.0 = 36 000 kWh. Emissions = 36 000 × 0.25 = 9000 kg = <b>9.0 t</b>.",
                  "scheme": "1 mark for the electricity used; 1 mark for the answer."},
                 {"text": "Calculate the percentage reduction in emissions.", "marks": 2,
                  "solution": "(24 − 9.0) / 24 × 100 = <b>62.5%</b>.",
                  "scheme": "Allow error carried forward from (a) and (b)."},
                 {"text": "Above what grid emission factor would the heat pump cause <i>more</i> " + CO2 + " than the boiler?",
                  "marks": 2,
                  "solution": "Break-even when 36 000 × <i>f</i> = 24 000, so <i>f</i> = <b>0.67 kg " + CO2 + " per kWh</b>. "
                              "This is roughly the factor of a grid that runs mostly on coal.",
                  "scheme": "1 mark for the equation; 1 mark for the answer."},
                 {"text": "Suggest two reasons why the real reduction might differ from your answer to (c).", "marks": 2,
                  "solution": "Any two of: the COP drops in very cold weather, exactly when heat demand is highest; the grid's "
                              "emission factor varies by hour and season; leaking refrigerant is a powerful greenhouse gas; "
                              "a poorly insulated building may need higher flow temperatures, lowering the COP; "
                              "extra demand may be met by fossil-fuel plants (marginal emissions).",
                  "scheme": "1 mark per valid, explained reason."},
             ]},
            {"title": "Fuels and combustion",
             "stem": "Model petrol as pure octane, C<sub>8</sub>H<sub>18</sub> (density 0.74 kg L<sup>−1</sup>, energy released "
                     "44.4 MJ kg<sup>−1</sup>). Ethanol, C<sub>2</sub>H<sub>5</sub>OH, releases 26.8 MJ kg<sup>−1</sup>.",
             "parts": [
                 {"text": "Write a balanced equation for the complete combustion of octane.", "marks": 2,
                  "solution": "<b>2C<sub>8</sub>H<sub>18</sub> + 25O<sub>2</sub> → 16" + CO2 + " + 18H<sub>2</sub>O</b> "
                              "(or C<sub>8</sub>H<sub>18</sub> + 12.5O<sub>2</sub> → 8" + CO2 + " + 9H<sub>2</sub>O).",
                  "scheme": "1 mark for correct products; 1 mark for balancing."},
                 {"text": "Calculate the mass of " + CO2 + " produced when 1.00 kg of octane burns completely.", "marks": 2,
                  "solution": "<i>M</i>(C<sub>8</sub>H<sub>18</sub>) = 8 × 12.01 + 18 × 1.008 = 114.22 g mol<sup>−1</sup>, so "
                              "1000 g is 8.755 mol. This gives 8 × 8.755 = 70.04 mol " + CO2 + ", and 70.04 × 44.01 = 3082 g ≈ <b>3.08 kg</b>.",
                  "scheme": "1 mark for the moles of octane; 1 mark for the mass of " + CO2 + "."},
                 {"text": "A car uses 6.0 L of petrol per 100 km. Calculate its " + CO2 + " emissions in g km<sup>−1</sup>.",
                  "marks": 2,
                  "solution": "Fuel per km = 0.060 L × 0.74 kg L<sup>−1</sup> = 0.0444 kg. " + CO2 + " = 0.0444 × 3.08 = "
                              "0.137 kg ≈ <b>137 g km<sup>−1</sup></b>.",
                  "scheme": "Allow error carried forward from (b)."},
                 {"text": "Calculate the mass of " + CO2 + " released per MJ of energy for octane and for ethanol. Then explain "
                           "why bioethanol can still reduce net emissions.", "marks": 2,
                  "solution": "Ethanol: <i>M</i> = 46.07 g mol<sup>−1</sup>. 1 kg is 21.71 mol, giving 43.41 mol " + CO2 + " = 1.91 kg. "
                              "Per MJ: octane 3.08/44.4 = <b>69 g MJ<sup>−1</sup></b>; ethanol 1.91/26.8 = <b>71 g MJ<sup>−1</sup></b>. "
                              "Ethanol releases slightly <i>more</i> " + CO2 + " per unit of energy. However, its carbon was absorbed "
                              "from the air by the crop only months earlier (biogenic carbon), so it is largely balanced by "
                              "photosynthesis. Net savings depend on fertiliser, farm energy and land-use change.",
                  "scheme": "1 mark for both values; 1 mark for the biogenic-carbon explanation."},
             ]},
            {"title": "Estimating and modelling a population",
             "stem": "To estimate a population of ground beetles, students capture 60 beetles, mark them harmlessly and release them. "
                     "A week later they capture 75 beetles, of which 15 are marked.",
             "parts": [
                 {"text": "Use the Lincoln–Petersen index to estimate the population size.", "marks": 2,
                  "solution": "<i>N</i> = <i>MC</i>/<i>R</i> = 60 × 75 / 15 = <b>300 beetles</b>.",
                  "scheme": "1 mark for the method; 1 mark for the answer."},
                 {"text": "State two assumptions of this method.", "marks": 2,
                  "solution": "Any two of: the population is closed (no births, deaths or migration between samples); marks are "
                              "not lost and do not affect behaviour or survival; marked individuals mix randomly with the "
                              "population; every individual is equally likely to be caught.",
                  "scheme": "1 mark each."},
                 {"text": "Chapman's less-biased estimator is <i>N</i> = (<i>M</i> + 1)(<i>C</i> + 1)/(<i>R</i> + 1) − 1. "
                          "Calculate this estimate.", "marks": 1,
                  "solution": "<i>N</i> = 61 × 76 / 16 − 1 = 289.75 − 1 = 288.75 ≈ <b>289 beetles</b>.",
                  "scheme": "1 mark."},
                 {"text": "The population grows logistically: d<i>N</i>/d<i>t</i> = <i>rN</i>(1 − <i>N</i>/<i>K</i>), with "
                          "<i>r</i> = 0.40 yr<sup>−1</sup> and <i>K</i> = 500. Calculate the growth rate when <i>N</i> = 300. "
                          "Then find the population size at which the growth rate is greatest, and that maximum rate.",
                  "marks": 3,
                  "solution": "At <i>N</i> = 300: 0.40 × 300 × (1 − 300/500) = <b>48 beetles per year</b>. The rate is a "
                              "quadratic in <i>N</i> with its maximum at <i>N</i> = <i>K</i>/2 = <b>250</b>, where "
                              "d<i>N</i>/d<i>t</i> = 0.40 × 250 × 0.5 = <b>50 beetles per year</b>.",
                  "scheme": "1 mark for 48; 1 mark for K/2 = 250; 1 mark for 50."},
             ]},
            {"title": "Rainwater harvesting",
             "stem": "A school has a roof area of 450 m<sup>2</sup>, and the annual rainfall is 750 mm. On average, 85% of the "
                     "rain landing on the roof can be collected. The 600 students each flush a toilet twice per school day, "
                     "using 6.0 L per flush, on 190 school days a year.",
             "parts": [
                 {"text": "Calculate the volume of rainwater collected per year, in m<sup>3</sup>.", "marks": 2,
                  "solution": "450 m<sup>2</sup> × 0.750 m × 0.85 = <b>287 m<sup>3</sup></b> (286.9 m<sup>3</sup>).",
                  "scheme": "1 mark for converting mm to m; 1 mark for the answer."},
                 {"text": "What percentage of the school's toilet-flushing water could rainwater supply?", "marks": 2,
                  "solution": "Demand = 600 × 2 × 6.0 L × 190 = 1 368 000 L = 1368 m<sup>3</sup>. "
                              "Fraction = 286.9 / 1368 = <b>21%</b>.",
                  "scheme": "1 mark for the demand; 1 mark for the percentage."},
                 {"text": "All the harvested water is pumped up 12 m to a header tank by a pump that is 50% efficient. "
                          "Calculate the electrical energy used per year, in kWh.", "marks": 3,
                  "solution": "Mass = 286 875 kg. <i>E</i><sub>p</sub> = <i>mgh</i> = 286 875 × 9.81 × 12 = 3.38 × 10<sup>7</sup> J. "
                              "Electrical energy = 3.38 × 10<sup>7</sup> / 0.50 = 6.75 × 10<sup>7</sup> J = <b>18.8 kWh</b>, "
                              "which is very small compared with the water saved.",
                  "scheme": "1 mark for mgh; 1 mark for the efficiency; 1 mark for the kWh conversion."},
             ]},
            {"title": "Carbon dioxide and global temperature",
             "stem": "The pre-industrial " + CO2 + " concentration was <i>C</i><sub>0</sub> = 280 ppm. Assume the equilibrium "
                     "temperature change is Δ<i>T</i> = λΔ<i>F</i>, with λ = 0.80 K per W m<sup>−2</sup>. Ignore all other "
                     "gases and aerosols.",
             "parts": [
                 {"text": "Calculate the radiative forcing and the equilibrium warming for a concentration of 420 ppm.", "marks": 2,
                  "solution": "Δ<i>F</i> = 5.35 ln(420/280) = 5.35 × 0.405 = <b>2.17 W m<sup>−2</sup></b>. "
                              "Δ<i>T</i> = 0.80 × 2.17 = <b>1.7 K</b>.",
                  "scheme": "1 mark each."},
                 {"text": "Calculate the equilibrium warming for a doubling of " + CO2 + " (the climate sensitivity in this model).",
                  "marks": 1,
                  "solution": "Δ<i>F</i> = 5.35 ln 2 = 3.71 W m<sup>−2</sup>, so Δ<i>T</i> = <b>3.0 K</b>.",
                  "scheme": "1 mark."},
                 {"text": "At what " + CO2 + " concentration would the equilibrium warming reach 1.5 K?", "marks": 2,
                  "solution": "Δ<i>F</i> = 1.5 / 0.80 = 1.875 W m<sup>−2</sup>, so <i>C</i> = 280 × e<sup>1.875/5.35</sup> = "
                              "280 × 1.42 = <b>398 ppm</b>, a level the atmosphere passed around 2014.",
                  "scheme": "1 mark for ΔF; 1 mark for C."},
                 {"text": "Observed warming is about 1.3 K, even though " + CO2 + " is above your answer to (c). Give two reasons.",
                  "marks": 2,
                  "solution": "The climate is not yet at equilibrium: the oceans' large heat capacity delays warming by decades. "
                              "Aerosol pollution reflects sunlight and masks part of the greenhouse warming. "
                              "(Other greenhouse gases add warming, so they do not explain the gap.)",
                  "scheme": "1 mark per valid reason."},
             ]},
        ],
    },
    # ======================================================================
    {
        "id": "2025-junior", "year": 2025, "division": "Junior", "ages": "12–14",
        "duration": 90,
        "topics": ["Energy saving", "Food chains", "Plastics and the ocean", "Biodiversity",
                   "Waste and composting", "Climate data"],
        "data": DATA_JUNIOR + ["Electricity: 0.25 kg " + CO2 + " per kWh (where needed)"],
        "part_a": [
            {"q": "A classroom replaces a 60 W filament bulb with an 8 W LED bulb that gives the same light. The light is on for "
                  "5 hours a day, 365 days a year. How much energy is saved in a year?",
             "options": ["9.5 kWh", "94.9 kWh", "109.5 kWh", "949 kWh"], "answer": "B",
             "solution": "Power saved = 60 − 8 = 52 W. Energy = 52 W × 5 h × 365 = 94 900 Wh = <b>94.9 kWh</b>. "
                         "Option C is the total energy used by the old bulb, not the saving."},
            {"q": "Which energy source does NOT originally come from sunlight?",
             "options": ["Wind", "Hydroelectric", "Wood", "Tidal"], "answer": "D",
             "solution": "The Sun heats the air unevenly (wind), evaporates water that later flows downhill (hydro) and powers "
                         "photosynthesis (wood). <b>Tides</b> are caused mainly by the Moon's gravity acting on a rotating Earth."},
            {"q": "In photosynthesis, 6" + CO2 + " + 6H<sub>2</sub>O → C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> + 6O<sub>2</sub>. "
                  "How many molecules of oxygen are released for each molecule of glucose made?",
             "options": ["1", "3", "6", "12"], "answer": "C",
             "solution": "The balanced equation shows <b>6</b> O<sub>2</sub> molecules for every one glucose molecule."},
            {"q": "In the food chain grass → grasshopper → frog → snake → hawk, the grass stores 100 000 kJ of energy. "
                  "If 10% of the energy passes from each level to the next, how much reaches the hawk?",
             "options": ["1000 kJ", "100 kJ", "10 kJ", "1 kJ"], "answer": "C",
             "solution": "100 000 → 10 000 (grasshopper) → 1000 (frog) → 100 (snake) → <b>10 kJ</b> (hawk). "
                         "There are four transfers, not five."},
            {"q": "Making a can from recycled aluminium instead of from bauxite ore saves about how much of the energy?",
             "options": ["About 10%", "About 40%", "About 70%", "About 95%"], "answer": "D",
             "solution": "Extracting aluminium from its ore needs huge amounts of electricity for electrolysis. Melting down "
                         "scrap needs only about 5% of that, saving about <b>95%</b>."},
            {"q": "Which greenhouse gas is the most abundant in Earth's atmosphere?",
             "options": ["Carbon dioxide", "Methane", "Water vapour", "Ozone"], "answer": "C",
             "solution": "<b>Water vapour</b> is the most abundant greenhouse gas. Its amount is controlled by temperature, so it "
                         "amplifies warming caused by " + CO2 + " rather than starting it."},
            {"q": "Seawater has a density of about 1.025 g cm<sup>−3</sup>. Which plastic will float in the sea?",
             "options": ["PET, a drinks bottle (1.38 g cm<sup>−3</sup>)", "PVC, a pipe (1.38 g cm<sup>−3</sup>)",
                         "Polypropylene, a bottle cap (0.90 g cm<sup>−3</sup>)", "Solid polystyrene, a CD case (1.05 g cm<sup>−3</sup>)"],
             "answer": "C",
             "solution": "Only materials less dense than seawater float: <b>polypropylene</b> (0.90 &lt; 1.025). This is why "
                         "bottle caps are often found on beaches while the bottles sink, unless air is trapped inside."},
            {"q": "A flight emits 0.15 kg " + CO2 + " per passenger per km. Lisbon to Paris is 1450 km. How much " + CO2 +
                  " is emitted for one passenger making a <b>return</b> trip?",
             "options": ["43.5 kg", "217.5 kg", "435 kg", "4350 kg"], "answer": "C",
             "solution": "Return distance = 2 × 1450 = 2900 km. 2900 × 0.15 = <b>435 kg</b>. "
                         "Option B is a one-way trip."},
            {"q": "Two meadows each contain 100 plants of the same 4 species. Meadow X has 25 of each species. Meadow Y has 97 of "
                  "one species and 1 of each of the others. Which statement is correct?",
             "options": ["Both have the same biodiversity because they have the same number of species",
                         "Meadow X has higher biodiversity because the species are more evenly spread",
                         "Meadow Y has higher biodiversity because one species is very successful",
                         "Biodiversity cannot be compared without knowing the area"],
             "answer": "B",
             "solution": "Biodiversity depends on <i>richness</i> (number of species) and <i>evenness</i> (how equally they are "
                         "represented). Richness is equal, but <b>X is far more even</b>, so it is more diverse."},
            {"q": "Why do tropical rainforest soils often become poor for farming only a few years after the forest is cleared?",
             "options": ["Tropical soils contain too much nitrogen",
                         "Most nutrients are stored in the living plants, and heavy rain washes the rest out of the thin soil",
                         "The soil becomes too cold without the trees",
                         "Earthworms eat all the organic matter"],
             "answer": "B",
             "solution": "In rainforests, nutrients are recycled quickly and held mainly in the vegetation. Once the trees are "
                         "removed, heavy rainfall <b>leaches</b> the few remaining nutrients from the thin topsoil."},
        ],
        "part_b": [
            {"title": "Computers left on",
             "stem": "A computer room has 12 computers. Each uses 120 W while in use and 60 W while idle. They are used for 6 hours "
                     "each school day but left idle for the other 18 hours instead of being switched off. There are 190 school "
                     "days a year. Electricity costs €0.20 per kWh, and each kWh causes 0.25 kg of " + CO2 + ".",
             "parts": [
                 {"text": "Calculate the energy wasted per school day, in kWh.", "marks": 2,
                  "solution": "12 × 60 W × 18 h = 12 960 Wh = <b>12.96 kWh</b>.",
                  "scheme": "1 mark for the method; 1 mark for converting to kWh."},
                 {"text": "Calculate the energy wasted per school year.", "marks": 2,
                  "solution": "12.96 × 190 = <b>2462 kWh</b> (2462.4 kWh).", "scheme": "Allow error carried forward."},
                 {"text": "How much money is wasted per year?", "marks": 2,
                  "solution": "2462.4 × €0.20 = <b>€492</b> (€492.48).", "scheme": "Allow error carried forward."},
                 {"text": "How much " + CO2 + " is caused by the wasted energy each year?", "marks": 2,
                  "solution": "2462.4 × 0.25 = <b>616 kg</b> (615.6 kg) of " + CO2 + ".", "scheme": "Allow error carried forward."},
             ]},
            {"title": "From food waste to compost",
             "stem": "A school canteen throws away 15 kg of food waste every school day (190 days a year). In a landfill, each kg of "
                     "food waste releases 0.05 kg of methane. Methane traps 28 times as much heat as the same mass of " + CO2 +
                     " over 100 years. Composting reduces the mass of the waste by 60%.",
             "parts": [
                 {"text": "Calculate the total food waste per year.", "marks": 1,
                  "solution": "15 × 190 = <b>2850 kg</b>.", "scheme": "1 mark."},
                 {"text": "What mass of compost would be produced?", "marks": 2,
                  "solution": "The mass falls by 60%, so 40% remains: 2850 × 0.40 = <b>1140 kg</b>.",
                  "scheme": "1 mark for using 40%; 1 mark for the answer."},
                 {"text": "Calculate the " + CO2 + "-equivalent emissions avoided each year by composting instead of using a "
                          "landfill. Ignore any emissions from the compost heap.", "marks": 3,
                  "solution": "Methane = 2850 × 0.05 = 142.5 kg. " + CO2 + "-equivalent = 142.5 × 28 = 3990 kg ≈ <b>4.0 t</b>.",
                  "scheme": "1 mark for methane; 1 mark for multiplying by 28; 1 mark for the answer."},
                 {"text": "Explain why a well-managed compost heap releases much less methane than a landfill.", "marks": 2,
                  "solution": "Methane is made by microbes that live <b>without oxygen</b> (anaerobic decomposition), as in "
                              "buried landfill waste. A compost heap that is turned regularly contains oxygen, so microbes break "
                              "the waste down aerobically into " + CO2 + " and water instead.",
                  "scheme": "1 mark for anaerobic conditions in landfill; 1 mark for oxygen/aerobic in the compost heap."},
             ]},
            {"title": "Cycling to school",
             "stem": "Ana lives 4.0 km from school. Each school day she is driven to school and back home (8.0 km in total). "
                     "The car emits 120 g of " + CO2 + " per km. There are 190 school days a year.",
             "parts": [
                 {"text": "Calculate the " + CO2 + " emitted by these journeys in a year, in kg.", "marks": 2,
                  "solution": "8.0 × 190 = 1520 km. 1520 × 0.120 kg = <b>182.4 kg</b>.",
                  "scheme": "1 mark for distance; 1 mark for the answer in kg."},
                 {"text": "30 students with the same journey start cycling instead. How much " + CO2 + " do they save in total?",
                  "marks": 2,
                  "solution": "30 × 182.4 = 5472 kg ≈ <b>5.5 t</b>.", "scheme": "Allow error carried forward."},
                 {"text": "The car averages 30 km/h and Ana cycles at 15 km/h. How many extra minutes per day does cycling take?",
                  "marks": 3,
                  "solution": "Car: 8.0/30 h = 16 min. Bike: 8.0/15 h = 32 min. Extra time = <b>16 minutes per day</b>.",
                  "scheme": "1 mark for each time; 1 mark for the difference."},
             ]},
            {"title": "Reading climate data",
             "stem": "Average " + CO2 + " concentration measured at Mauna Loa, Hawaii: 1960, 317 ppm; 1980, 339 ppm; "
                     "2000, 370 ppm; 2020, 414 ppm.",
             "parts": [
                 {"text": "Calculate the average rate of increase, in ppm per year, for each 20-year period.", "marks": 3,
                  "solution": "1960–1980: 22/20 = <b>1.10</b>; 1980–2000: 31/20 = <b>1.55</b>; "
                              "2000–2020: 44/20 = <b>2.20 ppm per year</b>.",
                  "scheme": "1 mark each."},
                 {"text": "Describe what your answers show.", "marks": 2,
                  "solution": "The concentration is not just rising: the <b>rate of increase is itself increasing</b> "
                              "(it doubled over the 60 years). The rise is accelerating.",
                  "scheme": "1 mark for increasing concentration; 1 mark for the increasing rate."},
                 {"text": "Predict the concentration in 2030 if the 2000–2020 rate continues.", "marks": 2,
                  "solution": "414 + 10 × 2.20 = <b>436 ppm</b>.", "scheme": "Allow error carried forward."},
             ]},
        ],
    },
    # ======================================================================
    {
        "id": "2024-senior", "year": 2024, "division": "Senior", "ages": "15–18",
        "duration": 90,
        "topics": ["Energy storage", "Photovoltaics", "Life-cycle assessment", "River pollution",
                   "Nitrogen and fertilisers", "Resource depletion"],
        "data": DATA_SENIOR + ["Solar constant <i>S</i> = 1361 W m<sup>−2</sup>; GWP<sub>100</sub> of " + N2O + " = 273"],
        "part_a": [
            {"q": "A home battery stores 13.5 kWh and has a round-trip efficiency of 90%. How much energy must be supplied while "
                  "charging so that it can deliver 13.5 kWh?",
             "options": ["12.2 kWh", "13.5 kWh", "15.0 kWh", "24.3 kWh"], "answer": "C",
             "solution": "Energy in × 0.90 = 13.5 kWh, so energy in = 13.5 / 0.90 = <b>15.0 kWh</b>. "
                         "Option A wrongly multiplies by 0.90."},
            {"q": "The band gap of crystalline silicon is 1.12 eV. What is the longest wavelength of light that can create an "
                  "electron–hole pair in silicon?",
             "options": ["443 nm", "700 nm", "1110 nm", "1550 nm"], "answer": "C",
             "solution": "λ = <i>hc</i>/<i>E</i> = (6.63 × 10<sup>−34</sup> × 3.00 × 10<sup>8</sup>) / (1.12 × 1.60 × 10<sup>−19</sup>) "
                         "= 1.11 × 10<sup>−6</sup> m = <b>1110 nm</b>, in the near infrared. Longer wavelengths pass straight through."},
            {"q": "What is the approximate maximum efficiency of a single-junction solar cell under ordinary sunlight "
                  "(the Shockley–Queisser limit)?",
             "options": ["15%", "33%", "59%", "86%"], "answer": "B",
             "solution": "Photons below the band gap are not absorbed, and the excess energy of high-energy photons is lost as "
                         "heat. Together these limit a single junction to about <b>33%</b>. 86% is the limit for an infinite "
                         "stack of junctions under concentrated light."},
            {"q": "Which organisms fix atmospheric nitrogen in the root nodules of legumes such as beans and clover?",
             "options": ["Nitrifying bacteria such as <i>Nitrosomonas</i>", "Denitrifying bacteria such as <i>Pseudomonas</i>",
                         "<i>Rhizobium</i> bacteria", "Mycorrhizal fungi"],
             "answer": "C",
             "solution": "<b><i>Rhizobium</i></b> lives symbiotically in root nodules and converts N<sub>2</sub> into ammonium using "
                         "the enzyme nitrogenase. Nitrifying bacteria oxidise ammonium to nitrate, and denitrifiers return "
                         "nitrogen to the air."},
            {"q": "A river sample has a high biochemical oxygen demand (BOD). This most likely indicates:",
             "options": ["a high concentration of dissolved oxygen",
                         "a large amount of biodegradable organic matter, for example from sewage",
                         "a low concentration of nitrate", "a high salinity"],
             "answer": "B",
             "solution": "BOD measures the oxygen that microorganisms consume while decomposing organic matter (usually over "
                         "5 days at 20 °C). A high BOD means <b>a lot of organic pollution</b>, which will lower dissolved oxygen."},
            {"q": "A pumped-storage reservoir holds 1.0 × 10<sup>6</sup> m<sup>3</sup> of water at an average height of 300 m "
                  "above the turbines. How much gravitational potential energy is stored?",
             "options": ["8.2 MWh", "82 MWh", "818 MWh", "8.2 GWh"], "answer": "C",
             "solution": "<i>m</i> = 1.0 × 10<sup>9</sup> kg. <i>E</i> = <i>mgh</i> = 1.0 × 10<sup>9</sup> × 9.81 × 300 = "
                         "2.94 × 10<sup>12</sup> J. Dividing by 3.6 × 10<sup>9</sup> J per MWh gives <b>818 MWh</b>."},
            {"q": "Global demand for a resource grows at 7% per year. Approximately how long does it take for demand to double?",
             "options": ["7 years", "10 years", "14 years", "70 years"], "answer": "B",
             "solution": "Doubling time = ln 2 / ln 1.07 = 10.2 years. This matches the 'rule of 70': 70/7 = <b>10 years</b>."},
            {"q": "Taking Earth's albedo as 0.30 and ignoring the atmosphere, what is Earth's effective radiating temperature?",
             "options": ["About −18 °C", "About 0 °C", "About +15 °C", "About +33 °C"], "answer": "A",
             "solution": "Absorbed = emitted: <i>S</i>(1 − α)/4 = σ<i>T</i><sup>4</sup>, so <i>T</i> = (1361 × 0.70 / (4 × 5.67 × "
                         "10<sup>−8</sup>))<sup>1/4</sup> = 255 K ≈ <b>−18 °C</b>. The actual average of +15 °C is 33 K warmer "
                         "because of the natural greenhouse effect."},
            {"q": "How much energy is needed to heat 150 L of water from 15 °C to 55 °C?",
             "options": ["0.70 kWh", "6.97 kWh", "25.1 kWh", "69.7 kWh"], "answer": "B",
             "solution": "<i>Q</i> = <i>mc</i>Δ<i>T</i> = 150 × 4.18 × 40 = 25 080 kJ. Dividing by 3600 kJ per kWh gives <b>6.97 kWh</b>. "
                         "Option C is the answer in MJ, not kWh."},
            {"q": "What is meant by 'green hydrogen'?",
             "options": ["Hydrogen made from natural gas, with the " + CO2 + " captured and stored",
                         "Hydrogen made by electrolysis of water using renewable electricity",
                         "Hydrogen made by gasifying coal",
                         "Hydrogen made by steam reforming of methane without carbon capture"],
             "answer": "B",
             "solution": "<b>Green</b> hydrogen comes from electrolysis powered by renewables. A is 'blue', C is 'brown/black' and "
                         "D is 'grey' hydrogen, which is how most hydrogen is made today."},
        ],
        "part_b": [
            {"title": "Reusable or single-use?",
             "stem": "Manufacturing a reusable glass bottle causes 0.40 kg " + CO2 + "e. Each use cycle (collection, washing and "
                     "refilling) adds 0.03 kg " + CO2 + "e. A single-use aluminium can causes 0.17 kg " + CO2 + "e per use, "
                     "including recycling.",
             "parts": [
                 {"text": "Find the minimum number of uses for the bottle's footprint per use to be lower than the can's.",
                  "marks": 3,
                  "solution": "Need (0.40 + 0.03<i>n</i>)/<i>n</i> &lt; 0.17, so 0.40 &lt; 0.14<i>n</i> and <i>n</i> &gt; 2.86. "
                              "The bottle must be used at least <b>3 times</b>.",
                  "scheme": "1 mark for the inequality; 1 mark for solving it; 1 mark for rounding up to a whole number."},
                 {"text": "Calculate the footprint per use if a bottle is used 20 times, and the percentage saving compared with the can.",
                  "marks": 2,
                  "solution": "(0.40 + 20 × 0.03)/20 = 1.00/20 = <b>0.050 kg</b> per use. "
                              "Saving = (0.17 − 0.050)/0.17 = <b>71%</b>.",
                  "scheme": "1 mark each."},
                 {"text": "In reality, after each use a bottle is returned with probability <i>p</i> = 0.90, otherwise it is lost. "
                          "Show that the expected number of uses is 1/(1 − <i>p</i>), and calculate the expected footprint per use.",
                  "marks": 4,
                  "solution": "A bottle is used exactly <i>k</i> times with probability <i>p</i><sup><i>k</i>−1</sup>(1 − <i>p</i>). "
                              "So E[<i>k</i>] = Σ <i>k p</i><sup><i>k</i>−1</sup>(1 − <i>p</i>) = (1 − <i>p</i>)/(1 − <i>p</i>)<sup>2</sup> "
                              "= 1/(1 − <i>p</i>) = <b>10 uses</b>. Footprint per use = (0.40 + 10 × 0.03)/10 = "
                              "<b>0.070 kg " + CO2 + "e</b>, still well below the can.",
                  "scheme": "1 mark for the geometric distribution; 1 mark for summing the series (or an equivalent "
                            "argument); 1 mark for 10 uses; 1 mark for 0.070 kg."},
             ]},
            {"title": "A solar farm",
             "stem": "A solar farm has a peak capacity of 50 MW and a capacity factor of 18%. An average household uses 3500 kWh of "
                     "electricity per year. Electricity from coal emits 0.95 kg " + CO2 + " per kWh.",
             "parts": [
                 {"text": "Calculate the farm's annual electricity output, in GWh.", "marks": 2,
                  "solution": "50 MW × 8760 h × 0.18 = 78 840 MWh = <b>78.8 GWh</b>.",
                  "scheme": "1 mark for the method; 1 mark for the answer."},
                 {"text": "How many average households could this supply?", "marks": 2,
                  "solution": "78 840 000 kWh / 3500 kWh = <b>about 22 500 households</b>.",
                  "scheme": "Allow error carried forward."},
                 {"text": "How much " + CO2 + " per year is avoided if this output replaces coal-fired electricity?", "marks": 2,
                  "solution": "78 840 000 × 0.95 = 7.49 × 10<sup>7</sup> kg ≈ <b>74 900 t</b> of " + CO2 + ".",
                  "scheme": "Allow error carried forward."},
                 {"text": "Give two reasons why the capacity factor of a solar farm is far below 100%.", "marks": 2,
                  "solution": "Any two of: no output at night; clouds; low sun angle in winter and in the early morning and evening; "
                              "panels lose efficiency when hot; dust and soiling; inverter and cable losses.",
                  "scheme": "1 mark each."},
             ]},
            {"title": "Sewage effluent in a river",
             "stem": "Upstream of a treatment plant, a river flows at 4.0 m<sup>3</sup> s<sup>−1</sup> with a BOD of 2.0 mg L<sup>−1</sup> "
                     "and dissolved oxygen (DO) of 9.0 mg L<sup>−1</sup>. The plant discharges 0.50 m<sup>3</sup> s<sup>−1</sup> of "
                     "effluent with a BOD of 60 mg L<sup>−1</sup> and DO of 2.0 mg L<sup>−1</sup>. Assume complete mixing.",
             "parts": [
                 {"text": "Calculate the BOD of the river just below the outlet.", "marks": 2,
                  "solution": "BOD = (4.0 × 2.0 + 0.50 × 60)/(4.0 + 0.50) = 38/4.5 = <b>8.4 mg L<sup>−1</sup></b>.",
                  "scheme": "1 mark for the flow-weighted mean; 1 mark for the answer."},
                 {"text": "Calculate the dissolved oxygen just below the outlet.", "marks": 2,
                  "solution": "DO = (4.0 × 9.0 + 0.50 × 2.0)/4.5 = 37/4.5 = <b>8.2 mg L<sup>−1</sup></b>.",
                  "scheme": "1 mark for the method; 1 mark for the answer."},
                 {"text": "Ignoring re-aeration, would the DO stay above 5.0 mg L<sup>−1</sup> (needed by most fish) once all the "
                          "BOD has been exerted? Explain.", "marks": 2,
                  "solution": "The oxygen demand (8.4) exceeds the oxygen available (8.2), so DO would fall to <b>zero</b>: "
                              "the river would become anoxic and fish would die.",
                  "scheme": "1 mark for comparing the values; 1 mark for the conclusion."},
                 {"text": "What is the maximum effluent BOD that would keep the DO at or above 5.0 mg L<sup>−1</sup>?",
                  "marks": 2,
                  "solution": "Allowed mixed BOD = 37/4.5 − 5.0 = 14.5/4.5 mg L<sup>−1</sup>. So (8.0 + 0.50<i>x</i>)/4.5 ≤ 14.5/4.5, "
                              "giving 0.50<i>x</i> ≤ 6.5 and <i>x</i> ≤ <b>13 mg L<sup>−1</sup></b>.",
                  "scheme": "1 mark for the inequality; 1 mark for the answer."},
             ]},
            {"title": "Fertilisers and nitrous oxide",
             "stem": "Ammonium nitrate (NH<sub>4</sub>NO<sub>3</sub>) and urea (CO(NH<sub>2</sub>)<sub>2</sub>) are common nitrogen "
                     "fertilisers.",
             "parts": [
                 {"text": "Calculate the percentage by mass of nitrogen in each fertiliser.", "marks": 2,
                  "solution": "NH<sub>4</sub>NO<sub>3</sub>: 28.02/80.05 = <b>35.0%</b>. Urea: 28.02/60.06 = <b>46.7%</b>.",
                  "scheme": "1 mark each."},
                 {"text": "A farmer applies 120 kg of nitrogen per hectare to 15 ha using urea. What mass of urea is needed?",
                  "marks": 2,
                  "solution": "N needed = 120 × 15 = 1800 kg. Urea = 1800/0.4665 = 3858 kg ≈ <b>3.86 t</b>.",
                  "scheme": "1 mark for total N; 1 mark for the answer."},
                 {"text": "1.0% of the applied nitrogen is emitted as nitrogen in " + N2O + ". Calculate the mass of " + N2O +
                          " and its " + CO2 + "-equivalent.", "marks": 3,
                  "solution": N2O + "–N = 18 kg. Mass of " + N2O + " = 18 × 44.02/28.02 = 28.3 kg. " + CO2 + "e = 28.3 × 273 = "
                              "7720 kg ≈ <b>7.7 t " + CO2 + "e</b>.",
                  "scheme": "1 mark for 18 kg; 1 mark for converting N to " + N2O + "; 1 mark for " + CO2 + "e."},
                 {"text": "Suggest one way to reduce these emissions without reducing crop yield.", "marks": 1,
                  "solution": "For example: split applications that match crop uptake; precision (variable-rate) spreading; "
                              "nitrification inhibitors; legumes in the rotation to fix nitrogen naturally.",
                  "scheme": "1 mark."},
             ]},
            {"title": "How long will it last?",
             "stem": "Known reserves of a metal are 880 Mt, and current annual consumption is 26 Mt.",
             "parts": [
                 {"text": "Calculate the static lifetime of the reserves.", "marks": 1,
                  "solution": "880/26 = <b>34 years</b> (33.8).", "scheme": "1 mark."},
                 {"text": "If consumption grows continuously at 3.0% per year, cumulative use after <i>t</i> years is "
                          "(<i>C</i><sub>0</sub>/<i>r</i>)(e<sup><i>rt</i></sup> − 1). Calculate when the reserves run out.",
                  "marks": 4,
                  "solution": "880 = (26/0.030)(e<sup>0.030<i>t</i></sup> − 1), so e<sup>0.030<i>t</i></sup> = 1 + 0.030 × 880/26 = 2.015. "
                              "Then <i>t</i> = ln(2.015)/0.030 = <b>23 years</b>. Steady 3% growth cuts the lifetime by a third.",
                  "scheme": "1 mark for setting up the equation; 1 mark for rearranging; 1 mark for the logarithm; 1 mark for the answer."},
                 {"text": "Give two reasons why the real lifetime could be longer than either estimate.", "marks": 2,
                  "solution": "Any two of: higher prices make lower-grade deposits economic, so reserves grow; new discoveries; "
                              "recycling; substitution by other materials; more efficient use.",
                  "scheme": "1 mark each."},
             ]},
        ],
    },
    # ======================================================================
    {
        "id": "2024-junior", "year": 2024, "division": "Junior", "ages": "12–14",
        "duration": 90,
        "topics": ["Energy at home", "The atmosphere", "Pollination", "Water use", "Sampling methods", "Transport"],
        "data": DATA_JUNIOR,
        "part_a": [
            {"q": "A 2000 W kettle is switched on for 3 minutes. How much energy does it use?",
             "options": ["0.01 kWh", "0.1 kWh", "6 kWh", "360 kWh"], "answer": "B",
             "solution": "3 minutes = 0.05 h. Energy = 2.0 kW × 0.05 h = <b>0.1 kWh</b> (360 000 J)."},
            {"q": "In which layer of the atmosphere is most of the ozone layer found?",
             "options": ["Troposphere", "Stratosphere", "Mesosphere", "Thermosphere"], "answer": "B",
             "solution": "About 90% of atmospheric ozone is in the <b>stratosphere</b>, roughly 15–35 km up, where it absorbs "
                         "harmful UV radiation."},
            {"q": "Which of these crops does NOT depend on insects for pollination?",
             "options": ["Apple", "Almond", "Wheat", "Strawberry"], "answer": "C",
             "solution": "<b>Wheat</b>, like other grasses, is wind-pollinated (and mostly self-pollinating). Apples, almonds and "
                         "strawberries need insects such as bees."},
            {"q": "A plant has plenty of water in its soil. What happens to its rate of transpiration on a hot, dry, windy day?",
             "options": ["It decreases, because wind closes the stomata",
                         "It increases, because water vapour diffuses away from the leaves faster",
                         "It stays the same", "It stops completely"],
             "answer": "B",
             "solution": "Heat, dry air and wind all steepen the water-vapour gradient between the leaf and the air, so "
                         "transpiration <b>increases</b>. Stomata close only when the plant is short of water."},
            {"q": "Last year a town produced 600 t of waste and recycled 30% of it. This year the waste fell by 10% and the "
                  "recycling rate rose to 40%. How much more waste was recycled this year?",
             "options": ["18 t", "36 t", "54 t", "60 t"], "answer": "B",
             "solution": "Last year: 0.30 × 600 = 180 t. This year: waste = 540 t, recycled = 0.40 × 540 = 216 t. "
                         "Difference = <b>36 t</b>."},
            {"q": "Making one cotton T-shirt uses about 2700 L of water. A class of 30 students each buys 2 fewer T-shirts this year. "
                  "How much water is saved?",
             "options": ["5400 L", "81 000 L", "162 000 L", "1 620 000 L"], "answer": "C",
             "solution": "30 × 2 × 2700 = <b>162 000 L</b>, about the volume of a small swimming pool."},
            {"q": "What causes coral bleaching?",
             "options": ["Corals expel the algae living in their tissues when the water becomes too warm",
                         "Strong sunlight bleaches the coral's pigment",
                         "Chlorine pollution from swimming pools",
                         "Fish eat the colourful algae on the reef"],
             "answer": "A",
             "solution": "Corals depend on algae called zooxanthellae for food and colour. Heat stress makes the corals "
                         "<b>expel the algae</b>, leaving the white skeleton visible. The coral may starve if it lasts too long."},
            {"q": "Which item takes the longest to break down in the sea?",
             "options": ["Paper bag", "Aluminium can", "Plastic bottle", "Glass bottle"], "answer": "D",
             "solution": "Estimates: paper, weeks; aluminium can, about 200 years; plastic bottle, about 450 years; "
                         "<b>glass</b>, up to a million years. Glass is inert, so it is far less harmful than plastic."},
            {"q": "On a 1:50 000 map, a forest is a rectangle 3 cm by 2 cm. What is its real area?",
             "options": ["6 ha", "15 ha", "150 ha", "1500 ha"], "answer": "C",
             "solution": "3 cm = 1.5 km and 2 cm = 1.0 km. Area = 1.5 km<sup>2</sup> = <b>150 ha</b>. Do not scale the area "
                         "by 50 000; the area scale is 50 000<sup>2</sup>."},
            {"q": "Which shows the energy transfers in a hydroelectric power station?",
             "options": ["Gravitational potential → kinetic → electrical", "Chemical → thermal → electrical",
                         "Kinetic → gravitational potential → electrical", "Thermal → kinetic → electrical"],
             "answer": "A",
             "solution": "Water stored high up has <b>gravitational potential</b> energy, which becomes kinetic energy as it falls, "
                         "turning the turbine and generator to produce electrical energy."},
        ],
        "part_b": [
            {"title": "A shorter shower",
             "stem": "Leo takes an 8-minute shower every day with a shower head that uses 12 L per minute. He switches to a "
                     "5-minute shower with an eco shower head that uses 8 L per minute. The water is heated from 15 °C to 40 °C.",
             "parts": [
                 {"text": "How much water does Leo save each day?", "marks": 2,
                  "solution": "Before: 8 × 12 = 96 L. After: 5 × 8 = 40 L. Saving = <b>56 L</b>.",
                  "scheme": "1 mark for both volumes; 1 mark for the saving."},
                 {"text": "How much water does he save in a year?", "marks": 2,
                  "solution": "56 × 365 = <b>20 440 L</b>.", "scheme": "Allow error carried forward."},
                 {"text": "Calculate the energy saved in a year by not heating this water, in kWh.", "marks": 4,
                  "solution": "Mass = 20 440 kg. Energy = 20 440 × 4.18 × 25 = 2 135 980 kJ. Dividing by 3600 kJ per kWh "
                              "gives <b>593 kWh</b>.",
                  "scheme": "1 mark for the mass; 1 mark for ΔT = 25 °C; 1 mark for kJ; 1 mark for converting to kWh."},
             ]},
            {"title": "Can trees cancel our emissions?",
             "stem": "A growing tree absorbs on average 22 kg of " + CO2 + " per year. A family's car and heating emit "
                     "7.5 t of " + CO2 + " per year. A forest has about 400 trees per hectare.",
             "parts": [
                 {"text": "How many trees are needed to absorb the family's emissions?", "marks": 2,
                  "solution": "7500 kg / 22 kg = 340.9, so <b>341 trees</b> (always round up).",
                  "scheme": "1 mark for converting tonnes to kg; 1 mark for the answer."},
                 {"text": "What area of forest is this, in hectares?", "marks": 2,
                  "solution": "341 / 400 = <b>0.85 ha</b> (8500 m<sup>2</sup>), larger than a football pitch.",
                  "scheme": "Allow error carried forward."},
                 {"text": "Give two reasons why planting trees alone is not a solution to climate change.", "marks": 3,
                  "solution": "Any two well-explained points: young trees absorb very little for many years; the carbon is "
                              "released again if the trees burn, die or are cut down; there is not enough land to offset "
                              "everyone's emissions; cutting emissions is faster and permanent.",
                  "scheme": "Up to 2 marks per reason (maximum 3)."},
             ]},
            {"title": "Counting daisies",
             "stem": "A field measures 50 m by 40 m. Students place ten 1 m<sup>2</sup> quadrats at random and count the daisies "
                     "in each: 4, 7, 3, 0, 6, 5, 8, 2, 5, 10.",
             "parts": [
                 {"text": "Calculate the area of the field.", "marks": 1,
                  "solution": "50 × 40 = <b>2000 m<sup>2</sup></b>.", "scheme": "1 mark."},
                 {"text": "Calculate the mean number of daisies per m<sup>2</sup>.", "marks": 2,
                  "solution": "Total = 50 daisies in 10 m<sup>2</sup>, so the mean is <b>5.0 per m<sup>2</sup></b>.",
                  "scheme": "1 mark for the total; 1 mark for the mean."},
                 {"text": "Estimate the total number of daisies in the field.", "marks": 2,
                  "solution": "5.0 × 2000 = <b>10 000 daisies</b>.", "scheme": "Allow error carried forward."},
                 {"text": "Why should the quadrats be placed at random, and why is it better to use more quadrats?", "marks": 2,
                  "solution": "Random placement avoids bias, such as choosing spots with lots of daisies. More quadrats give a "
                              "more reliable mean because daisies are not evenly spread.",
                  "scheme": "1 mark each."},
             ]},
            {"title": "Electric or petrol?",
             "stem": "An electric car uses 16 kWh per 100 km. Electricity costs €0.22 per kWh and causes 0.25 kg " + CO2 +
                     " per kWh. A petrol car uses 6.0 L per 100 km. Petrol costs €1.80 per litre, and burning 1 L releases "
                     "2.3 kg " + CO2 + ".",
             "parts": [
                 {"text": "Calculate the fuel cost per 100 km for each car.", "marks": 2,
                  "solution": "Electric: 16 × 0.22 = <b>€3.52</b>. Petrol: 6.0 × 1.80 = <b>€10.80</b>.",
                  "scheme": "1 mark each."},
                 {"text": "Calculate the " + CO2 + " per 100 km for each car.", "marks": 2,
                  "solution": "Electric: 16 × 0.25 = <b>4.0 kg</b>. Petrol: 6.0 × 2.3 = <b>13.8 kg</b>.",
                  "scheme": "1 mark each."},
                 {"text": "A family drives 12 000 km a year. How much money would they save on fuel with the electric car?",
                  "marks": 2,
                  "solution": "12 000 km = 120 × 100 km. Saving = 120 × (10.80 − 3.52) = 120 × 7.28 = <b>€873.60</b>.",
                  "scheme": "1 mark for the number of 100 km units or the difference per 100 km; 1 mark for the answer."},
                 {"text": "Give two reasons why the electric car's real climate impact is higher than your answer to (b) suggests.",
                  "marks": 2,
                  "solution": "Any two of: making the battery causes large emissions; some energy is lost while charging; "
                              "the grid's emissions vary with time and place; manufacturing the car itself.",
                  "scheme": "1 mark each."},
             ]},
        ],
    },
]


_UNIT = re.compile(r"(\d) (?=(?:°C|K|kWh|MWh|GWh|kW|MW|W|kg|g|t|L|m|km|mm|ppm|MJ|kJ|J|h|min|minutes|years|ha|nm|Mt|mg|eV)\b|°C|%)")


def nbsp(text):
    """Keep numbers and units together (non-breaking space) in HTML and PDF output."""
    return _UNIT.sub("\\1\u00a0", text)


def apply_nbsp():
    for p in PAPERS:
        p["data"] = [nbsp(d) for d in p["data"]]
        for q in p["part_a"]:
            q["q"], q["solution"] = nbsp(q["q"]), nbsp(q["solution"])
            q["options"] = [nbsp(o) for o in q["options"]]
        for q in p["part_b"]:
            q["stem"] = nbsp(q["stem"])
            for part in q["parts"]:
                for k in ("text", "solution", "scheme"):
                    part[k] = nbsp(part[k])


apply_nbsp()


def total_marks(p):
    return 2 * len(p["part_a"]) + sum(part["marks"] for q in p["part_b"] for part in q["parts"])


def part_b_marks(p):
    return sum(part["marks"] for q in p["part_b"] for part in q["parts"])
