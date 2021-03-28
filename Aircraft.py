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
