#"name",    "radius", "distance", "flattening", "rotperiod",       "eccentricity", "orbitperiod",
real_planets_data = [
["sun",     696342,   0,          0.000009,     25.1,              0,              0             ],
["mercury", 2440,     57909050,   0,            58.646,            0.20563,        87.9691       ],
["venus",   6052,     108208000,  0,            -243.0185,         0.0067,         224.701       ],
["earth",   6378,     149600000,  0.0033528,    0.99726968,        0.01671123,     365.256363004,],
["mars",    3396,     227939100,  0.00589,      1.025957,          0.0935,         686.971       ],
["jupiter", 71492,    778547200,  0.06487,      0.41354,           0.048775,       4332.59       ],
["saturn",  60268,    1433449370, 0.09796,      0.439583333333333, 0.0557,         10759.22      ],
["uranus",  25559,    2870671400, 0.0229,       0.71833,           0.04722,        30687.15      ],
["neptune", 24764,    4498542600, 0.0171,       0.6713,            0.008678,       60190.03      ]
]

# 0 name = name
# 1 radius = how big a planet is
# 2 distance = how far is it from Sun
# 3 flattening = how elliptic it's orbit is
# 4 rotperiod = how long it takes for it to rotate
# 5 eccentricity = how close the Sun is to orbite's centre
# 6 orbitperiod = how long it takes for planet to make a circle around the Sun
planets_data = [[i[0], int(i[1] / 350), i[2] / 4000000, i[3], i[4], i[5], i[6]] for i in real_planets_data]
planets_data[0][1] = int(planets_data[0][1] / 70)
