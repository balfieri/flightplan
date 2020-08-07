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

        # Performance 
        #
        'short_field_takeoff': [
            # weight
            2550, [
                # temp  MSL     ground  feet to clear
                #       ft      roll    50ft obstacle
                [ 0,    0,      860,    1465 ],
                [ 0,    1000,   940,    1600 ],        
                [ 0,    2000,   1025,   1755 ],        
                [ 0,    3000,   1125,   1925 ],        
                [ 0,    4000,   1235,   2120 ],        
                [ 0,    5000,   1355,   2345 ],        
                [ 0,    6000,   1495,   2605 ],        
                [ 0,    7000,   1645,   2910 ],        
                [ 0,    8000,   1820,   3265 ],        
            ],
        ],
    }
}

tails = { 
    # Wings of Carolina
    #
    'N53587': {
        'type':                 'C172S',
        'empty_weight':         1700.9,
        'empty_arm':            41.1
    },

    'N72675': {
        'type':                 'C172S',
        'empty_weight':         1679.0,
        'empty_arm':            40.4
    },

    'N972WW': {
        'type':                 'C172S',
        'empty_weight':         1665.4,
        'empty_arm':            40.88
    }
} 
