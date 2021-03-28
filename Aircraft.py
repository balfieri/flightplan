# Aircraft.py - Known Aircraft Types and Their Performance Characteristics
#               Overrides for Specific Tail Numbers
#
# Feel free to ADD your own types and tails to this.  
# Just don't delete what is already here.
#
types = { 
    'C172S': {
        'make':                 'Cessna',
        'model':                '172S',

        # Weight and Balance
        #
        'empty_weight':         1680,
        'empty_arm':            40.5,
        'fuel_gal_max':         53,             # unusable already counted in empty_weight
        'fuel_gal_weight':      6,
        'fuel_arm':             48,
        'row1_arm':             37,
        'row2_arm':             73,
        'baggage1_weight_max':  120,
        'baggage1_arm':         95,
        'baggage2_weight_max':  50,
        'baggage2_arm':         123,
        'baggage_weight_max':   120,
        'ramp_weight_max':      2558,
        'takeoff_weight_max':   2550,
        'landing_weight_max':   2550,
        'normal_cg': [
            # weight,   arm_min, arm_max
            [ 2550,     41.0,    47.3 ],
            [ 1950,     35.0,    47.3 ],
            [ 1500,     35.0,    47.3 ]
        ],

        # V-speeds (KIAS)
        #
        'Vne':  163,
        'Vno':  129,
        'Va': [
            [ 2550, 105 ],
            [ 2200, 98 ],
            [ 1900, 90 ]
        ],
        'Vfe': [
            [ 10,   110 ],
            [ 20,   85 ],
            [ 30,   85 ]
        ],
        'Vg':   68,
        'best_glide_ratio':     1.5,        # nm for each 1000 ft above terrain, Vg, prop windmilling, flaps up, zero wind

        # Performance 
        #
        'fuel_gal_taxi':        1.4,
        'fuel_gph':             10,         # temporary

        'airspeed_calibration': [  # normal static port
            # flaps
            0,  [
                # KIAS    KCAS
                [   50,    56 ],
                [   60,    62 ],
                [   70,    70 ],
                [   80,    78 ],
                [   90,    87 ],
                [  100,    97 ],
                [  110,   107 ],
                [  120,   117 ],
                [  130,   127 ],
                [  140,   137 ],
                [  150,   147 ],
                [  160,   157 ],
                ],

            10, [
                # KIAS    KCAS
                [   40,    51 ],
                [   50,    57 ],
                [   60,    63 ],
                [   70,    71 ],
                [   80,    80 ],
                [   90,    89 ],
                [  100,    99 ],
                [  110,   109 ],
                ],

            30, [
                # KIAS    KCAS
                [   40,    50 ],
                [   50,    56 ],
                [   60,    63 ],
                [   70,    72 ],
                [   80,    81 ],
                [   85,    86 ],
                ],
        ],

        'short_field_takeoff_pct_decrease_per_knot_headwind': 10.0/9.0,
        'short_field_takeoff_pct_increase_per_knot_tailwind': 10.0/2.0,
        'short_field_takeoff_pct_increase_for_dry_grass':     15.0,     # ground roll only

        'short_field_landing_pct_decrease_per_knot_headwind': 10.0/9.0,
        'short_field_landing_pct_increase_per_knot_tailwind': 10.0/2.0,
        'short_field_landing_pct_increase_for_dry_grass':     45.0,     # ground roll only
        'short_field_landing_pct_increase_for_flaps_up':      35.0,     # assuming 9 KIAS faster approach speed

        'short_field_takeoff': [
            # weight
            2550, [
                # temp (C)
                0,  [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      860,    1465 ],
                    [ 1000,   940,    1600 ],        
                    [ 2000,   1025,   1755 ],        
                    [ 3000,   1125,   1925 ],        
                    [ 4000,   1235,   2120 ],        
                    [ 5000,   1355,   2345 ],        
                    [ 6000,   1495,   2605 ],        
                    [ 7000,   1645,   2910 ],        
                    [ 8000,   1820,   3265 ],        
                    ],

                10, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      925,    1575 ],
                    [ 1000,   1010,   1720 ],
                    [ 2000,   1110,   1890 ],
                    [ 3000,   1215,   2080 ],
                    [ 4000,   1335,   2295 ],
                    [ 5000,   1465,   2545 ],
                    [ 6000,   1615,   2830 ],
                    [ 7000,   1785,   3170 ],
                    [ 8000,   1970,   3575 ],
                    ],

                20, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      995,    1690 ],
                    [ 1000,   1090,   1850 ],
                    [ 2000,   1195,   2035 ],
                    [ 3000,   1310,   2240 ],
                    [ 4000,   1440,   2480 ],
                    [ 5000,   1585,   2755 ],
                    [ 6000,   1745,   3075 ],
                    [ 7000,   1920,   3440 ],
                    [ 8000,   2120,   3880 ],
                    ],

                30, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      1070,   1810 ],
                    [ 1000,   1170,   1990 ],
                    [ 2000,   1285,   2190 ],
                    [ 3000,   1410,   2420 ],
                    [ 4000,   1550,   2685 ],
                    [ 5000,   1705,   2975 ],
                    [ 6000,   1875,   3320 ],
                    [ 7000,   2065,   3730 ],
                    [ 8000,   2280,   4225 ],
                    ],

                40, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      1150,   1945 ],
                    [ 1000,   1260,   2135 ],
                    [ 2000,   1380,   2355 ],
                    [ 3000,   1515,   2605 ],
                    [ 4000,   1660,   2880 ],
                    [ 5000,   1825,   3205 ],
                    [ 6000,   2010,   3585 ],
                    [ 7000,   2215,   4045 ],
                    [ 8000,   2450,   4615 ],
                    ],
            ],

            2400, [
                # temp (C)
                0,  [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      745,    1275 ],
                    [ 1000,   810,    1390 ],
                    [ 2000,   885,    1520 ],
                    [ 3000,   970,    1665 ],
                    [ 4000,   1065,   1830 ],
                    [ 5000,   1170,   2015 ],
                    [ 6000,   1285,   2230 ],
                    [ 7000,   1415,   2470 ],
                    [ 8000,   1560,   2755 ],
                    ],

                10, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      800,    1370 ],
                    [ 1000,   875,    1495 ],
                    [ 2000,   955,    1635 ],
                    [ 3000,   1050,   1795 ],
                    [ 4000,   1150,   1975 ],
                    [ 5000,   1265,   2180 ],
                    [ 6000,   1390,   2410 ],
                    [ 7000,   1530,   2685 ],
                    [ 8000,   1690,   3000 ],
                    ],

                20, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      860,    1470 ],
                    [ 1000,   940,    1605 ],
                    [ 2000,   1030,   1760 ],
                    [ 3000,   1130,   1930 ],
                    [ 4000,   1240,   2130 ],
                    [ 5000,   1360,   2355 ],
                    [ 6000,   1500,   2610 ],
                    [ 7000,   1650,   2900 ],
                    [ 8000,   1815,   3240 ],
                    ],

                30, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      925,    1570 ],
                    [ 1000,   1010,   1720 ],
                    [ 2000,   1110,   1890 ],
                    [ 3000,   1215,   2080 ],
                    [ 4000,   1335,   2295 ],
                    [ 5000,   1465,   2530 ],
                    [ 6000,   1610,   2805 ],
                    [ 7000,   1770,   3125 ],
                    [ 8000,   1950,   3500 ],
                    ],

                40, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      995,    1685 ],
                    [ 1000,   1085,   1845 ],
                    [ 2000,   1190,   2030 ],
                    [ 3000,   1305,   2230 ],
                    [ 4000,   1430,   2455 ],
                    [ 5000,   1570,   2715 ],
                    [ 6000,   1725,   3015 ],
                    [ 7000,   1900,   3370 ],
                    [ 8000,   2095,   3790 ],
                    ],
            ],

            2200, [
                # temp (C)
                0,  [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      610,    1055 ],
                    [ 1000,   665,    1145 ],
                    [ 2000,   725,    1250 ],
                    [ 3000,   795,    1365 ],
                    [ 4000,   870,    1490 ],
                    [ 5000,   955,    1635 ],
                    [ 6000,   1050,   1800 ],
                    [ 7000,   1150,   1985 ],
                    [ 8000,   1270,   2195 ],
                    ],

                10, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      655,    1130 ],
                    [ 1000,   720,    1230 ],
                    [ 2000,   785,    1340 ],
                    [ 3000,   860,    1465 ],
                    [ 4000,   940,    1605 ],
                    [ 5000,   1030,   1765 ],
                    [ 6000,   1130,   1940 ],
                    [ 7000,   1245,   2145 ],
                    [ 8000,   1370,   2375 ],
                    ],

                20, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      705,    1205 ],
                    [ 1000,   770,    1315 ],
                    [ 2000,   845,    1435 ],
                    [ 3000,   925,    1570 ],
                    [ 4000,   1010,   1725 ],
                    [ 5000,   1110,   1900 ],
                    [ 6000,   1220,   2090 ],
                    [ 7000,   1340,   2305 ],
                    [ 8000,   1475,   2555 ],
                    ],

                30, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      760,    1290 ],
                    [ 1000,   830,    1410 ],
                    [ 2000,   905,    1540 ],
                    [ 3000,   995,    1685 ],
                    [ 4000,   1090,   1855 ],
                    [ 5000,   1195,   2035 ],
                    [ 6000,   1310,   2240 ],
                    [ 7000,   1435,   2475 ],
                    [ 8000,   1580,   2745 ],
                    ],

                40, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      815,    1380 ],
                    [ 1000,   890,    1505 ],
                    [ 2000,   975,    1650 ],
                    [ 3000,   1065,   1805 ],
                    [ 4000,   1165,   1975 ],
                    [ 5000,   1275,   2175 ],
                    [ 6000,   1400,   2395 ],
                    [ 7000,   1540,   2650 ],
                    [ 8000,   1695,   2950 ],
                    ],
            ],
        ],

        'short_field_landing': [
            # weight
            2550, [
                # temp (C)
                0,  [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      545,    1290 ],
                    [ 1000,   565,    1320 ],
                    [ 2000,   585,    1355 ],
                    [ 3000,   610,    1385 ],
                    [ 4000,   630,    1425 ],
                    [ 5000,   655,    1460 ],
                    [ 6000,   680,    1500 ],
                    [ 7000,   705,    1545 ],
                    [ 8000,   735,    1585 ],
                    ],

                10, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      565,    1320 ],
                    [ 1000,   585,    1350 ],
                    [ 2000,   610,    1385 ],
                    [ 3000,   630,    1425 ],
                    [ 4000,   655,    1460 ],
                    [ 5000,   680,    1500 ],
                    [ 6000,   705,    1540 ],
                    [ 7000,   730,    1585 ],
                    [ 8000,   760,    1630 ],
                    ],

                20, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      585,    1350 ],
                    [ 1000,   605,    1385 ],
                    [ 2000,   630,    1420 ],
                    [ 3000,   655,    1460 ],
                    [ 4000,   675,    1495 ],
                    [ 5000,   705,    1535 ],
                    [ 6000,   730,    1580 ],
                    [ 7000,   760,    1625 ],
                    [ 8000,   790,    1670 ],
                    ],

                30, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      605,    1380 ],
                    [ 1000,   625,    1420 ],
                    [ 2000,   650,    1455 ],
                    [ 3000,   675,    1495 ],
                    [ 4000,   700,    1535 ],
                    [ 5000,   725,    1575 ],
                    [ 6000,   755,    1620 ],
                    [ 7000,   785,    1665 ],
                    [ 8000,   815,    1715 ],
                    ],

                40, [
                    # press   ground  feet to clear
                    # alt     roll    50ft obstacle
                    [ 0,      625,    1415 ],
                    [ 1000,   650,    1450 ],
                    [ 2000,   670,    1490 ],
                    [ 3000,   695,    1530 ],
                    [ 4000,   725,    1570 ],
                    [ 5000,   750,    1615 ],
                    [ 6000,   780,    1660 ],
                    [ 7000,   810,    1705 ],
                    [ 8000,   840,    1755 ],
                    ],
            ],
        ],
    }
}

tails = { 
    # Wings of Carolina Flying Club (WCFC, out of KTTA in Sanford, NC)
    #
    'N53587': {
        'type':                 'C172S',
        'home':                 'KTTA',
        'empty_weight':         1700.9,
        'empty_arm':            41.1,
        'magnetic_deviation': [
            [ 360, 359 ],
            [  30,  30 ],
            [  60,  51 ],
            [  90,  89 ],
            [ 120, 120 ],
            [ 150, 150 ],
            [ 180, 180 ],
            [ 210, 210 ],
            [ 240, 239 ],
            [ 270, 270 ],
            [ 300, 300 ],
            [ 330, 320 ],
        ],
    },

    'N72675': {
        'type':                 'C172S',
        'home':                 'KTTA',
        'empty_weight':         1679.0,
        'empty_arm':            40.4,
        'magnetic_deviation': [  # placeholder, don't have these numbers yet
            [ 360, 360 ],
            [  30,  28 ],
            [  60,  57 ],
            [  90,  87 ],
            [ 120, 120 ],
            [ 150, 151 ],
            [ 180, 182 ],
            [ 210, 214 ],
            [ 240, 245 ],
            [ 270, 275 ],
            [ 300, 303 ],
            [ 330, 332 ],
        ],
    },

    'N972WW': {
        'type':                 'C172S',
        'home':                 'KTTA',
        'empty_weight':         1665.4,
        'empty_arm':            40.88,
        'magnetic_deviation': [  
            [ 360, 357 ],
            [  30,  26 ],
            [  60,  55 ],
            [  90,  86 ],
            [ 120, 119 ],
            [ 150, 149 ],
            [ 180, 184 ],
            [ 210, 215 ],
            [ 240, 246 ],
            [ 270, 271 ],
            [ 300, 301 ],
            [ 330, 331 ],
        ],
    }
} 
