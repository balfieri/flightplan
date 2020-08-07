# Aircraft.py - Known Aircraft Types and Their Performance Characteristics
#               Overrides for Specific Tail Numbers
#
# Feel free to ADD your own types and tails to this.  
# Just don't delete what is already here.
#
types = { 
    'C172S': {
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
        'gross_weight_max':     2558,
        'takeoff_weight_max':   2550,
        'landing_weight_max':   2550,
        'normal_cg': [
            { 'weight':         2550,
              'arm_min':        41,
              'arm_max':        47.3 },
            { 'weight':         1950,
              'arm_min':        35,
              'arm_max':        47.3 },
            { 'weight':         1500,
              'arm_min':        35,
              'arm_max':        47.3 }
        ],
        'utility_cg': [
            { 'weight':         2200,
              'arm_min':        37.5,
              'arm_max':        40.5 },
            { 'weight':         1950,
              'arm_min':        35,
              'arm_max':        40.5 },
            { 'weight':         1500,
              'arm_min':        35,
              'arm_max':        40.5 }
        ],

        # V-speeds
        #
    }
}

tails = { 
    # Wings of Carolina:
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
