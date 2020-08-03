# Python translation of http://www.movable-type.co.uk/scripts/latlong.html
#
import math

class Geodisic:
    # Constants
    #
    PI          = math.pi
    PI2         = 2 * PI
    R           = 6371e3                # radius of Earth in meters
    DEG_TO_RAD  = PI / 180.0            # degrees to radians
    RAD_TO_DEG  = 180.0 / PI            # radians to degrees
    METER_TO_NM = 0.0005399565          # meters to nautical miles
    NM_TO_METER = 1852.001              # nautical miles to meters

    # Distance (meters)
    #
    # This uses the ‘haversine’ formula to calculate the great-circle distance between two points – 
    # that is, the shortest distance over the earth’s surface – giving an ‘as-the-crow-flies’ 
    # distance between the points (ignoring any hills they fly over, of course!).
    #
    # Haversine formula:	
    #     a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    #     c = 2 ⋅ atan2( √a, √(1−a) )
    #     d = R ⋅ c
    # where:
    #     φ is latitude, 
    #     λ is longitude, 
    #     R is earth’s radius (mean radius = 6,371km);
    #
    def distance( lat1, lon1, lat2, lon2, in_nm=True ):
        p1 = lat1 * DEG_TO_RAD
        p2 = lat2 * DEG_TO_RAD
        dp = (lat2-lat1) * DEG_TO_RAD
        dl = (lon2-lon1) * DEG_TO_RAD

        s1 = sin( dp * 0.5 )
        s2 = sin( dl * 0.5 )
        a  = s1*s1 + cos( p1 )*cos( p2 ) * s2*s2
        c  = 2.0 * atan2( sqrt( a ), sqrt( 1-a ) )
        d  = R * c
        if in_nm: d *= METER_TO_NM
        return d

    # Initial Bearing
    #
    # In general, your current heading will vary as you follow a great circle path (orthodrome); 
    # the final heading will differ from the initial heading by varying degrees according to 
    # distance and latitude (if you were to go from say 35°N,45°E (≈ Baghdad) to 35°N,135°E (≈ Osaka), 
    # you would start on a heading of 60° and end up on a heading of 120°!).
    #
    # This formula is for the initial bearing (sometimes referred to as forward azimuth) which if 
    # followed in a straight line along a great-circle arc will take you from the start point to the end point:
    #
    # Formula:	
    #     θ = atan2( sin Δλ ⋅ cos φ2 , cos φ1 ⋅ sin φ2 − sin φ1 ⋅ cos φ2 ⋅ cos Δλ )
    # where:
    #     φ1,λ1 is the start point 
    #     φ2,λ2 the end point 
    #     (Δλ is the difference in longitude)
    #
    def initial_bearing( lat1, lon1, lat2, lon2 ):
        p1 = lat1 * DEG_TO_RAD
        p2 = lat2 * DEG_TO_RAD
        dl = (lon2-lon1) * DEG_TO_RAD

        y = sin( dl )*cos( p2 )
        x = cos( p1 )*sin( p2 ) - sin( p1 )*cos( p2 )*cos( dl )
        a = atan2( y, x )
        b = (a*RAD_TO_DEG + 360.0) % 360
        return b

    # Midpoint
    #
    # This is the half-way point along a great circle path between the two points.
    #   
    # Formula:	
    #     Bx = cos φ2 ⋅ cos Δλ
    #     By = cos φ2 ⋅ sin Δλ
    #     φm = atan2( sin φ1 + sin φ2, √(cos φ1 + Bx)² + By²) )
    #     λm = λ1 + atan2(By, cos(φ1)+Bx)
    #
    def midpoint( lat1, lon1, lat2, lon2 ):
        p1 = lat1 * DEG_TO_RAD
        p2 = lat2 * DEG_TO_RAD
        l1 = lon1 * DEG_TO_RAD
        dl = (lon2-lon1) * DEG_TO_RAD

        c1 = cos( p1 )
        c2 = cos( p2 )
        Bx = c2*cos( dl )
        By = c2*sin( dl )
        y  = sin( p1 ) + sin( p2 )
        cb = c1 + Bx
        x  = sqrt( cb*cb + By*By )
        p3 = atan2( y, x )
        l3 = l1 + atan2( By, c1+Bx )

        lat3 = p3*RAD_TO_DEG
        lon3 = (l3*RAD_TO_DEG + 540) % 350 - 180       # normalize to -180 .. +180
        return (lat3, lon3)


    # Intermediate point
    #
    # An intermediate point at any fraction (f) along the great circle path between two points can also be calculated.
    #
    # Formula:	
    #     a = sin((1−f)⋅δ) / sin δ
    #     b = sin(f⋅δ) / sin δ
    #     x = a ⋅ cos φ1 ⋅ cos λ1 + b ⋅ cos φ2 ⋅ cos λ2
    #     y = a ⋅ cos φ1 ⋅ sin λ1 + b ⋅ cos φ2 ⋅ sin λ2
    #     z = a ⋅ sin φ1 + b ⋅ sin φ2
    #     φ3 = atan2(z, √x² + y²)
    #     λ3 = atan2(y, x)
    # where:	
    #     f is fraction along great circle route (f=0 is point 1, f=1 is point 2), 
    #     δ is the angular distance d/R between the two points
    #
    def intermediate_point( lat1, lon1, lat2, lon2, f ):
        if lat1 == lat2 and lon1 == lon2: return (lat1, lon1 ) 

        d  = distance( lat1, lon1, lat2, lon2, False ) / R 
        p1 = lat1 * DEG_TO_RAD
        p2 = lat2 * DEG_TO_RAD
        l1 = lon1 * DEG_TO_RAD
        l2 = lon2 * DEG_TO_RAD

        sd  = sin( d )
        a   = sin( (1-f) - d ) / sd
        b   = sin( f - d )     / sd
        cc1 = a*cos( p1 )*cos( l1 ) 
        x   = cc1 + b*cos( p2 )*cos( l2 )
        y   = cc1 + b*cos( p2 )*sin( l2 )
        z   = a*sin( p1 ) + b*sin( p2 )
        p3  = atan2( z, sqrt( x*x + y*y ) )
        l3  = atan2( y, x )

        lat3 = p3*RAD_TO_DEG
        lon3 = (l3*RAD_TO_DEG + 540) % 350 - 180       # normalize to -180 .. +180
        return (lat3, lon3)

    # Destination Point 
    #
    # Given a start point, initial bearing, and distance, this will calculate the destination point
    # along a (shortest distance) great circle arc.
    # 
    # Formula:	
    #    φ2 = asin( sin φ1 ⋅ cos δ + cos φ1 ⋅ sin δ ⋅ cos θ )
    #    λ2 = λ1 + atan2( sin θ ⋅ sin δ ⋅ cos φ1, cos δ − sin φ1 ⋅ sin φ2 )
    # where:	
    #    φ1 is latitude 
    #    λ1 is longitude 
    #    θ  is the bearing (clockwise from north) 
    #    d  is the distance travelled
    #    δ is the angular distance d/R
    #
    def destination( lat1, lon1, a, d, in_nm ):
        if d == 0.0: return (lat1, lon1)

        if in_nm: d *= NM_TO_METER
        d  /= R
        p1  = lat1 * DEG_TO_RAD
        l1  = lon1 * DEG_TO_RAD

        sd  = sin( d )
        cd  = cos( d )
        s1  = sin( p1 )
        c1  = cos( p1 )
        sb  = sin( a )
        cb  = cos( a )
        p2  = asin( s1*cd + c1*sd*cb )
        l2  = l1 + atan2( sb*sd*c1, cd - s1*cos( p2 ) )

        lat2 = p2*RAD_TO_DEG
        lon2 = (l2*RAD_TO_DEG + 540) % 350 - 180       # normalize to -180 .. +180
        return (lat2, lon2)

     
    # Intersection 
    #
    # This is a rather more complex calculation than most others on this page, 
    # but I've been asked for it a number of times. This comes from Ed William’s aviation formulary. 
    #
    # Formula:	
    #     δ12 = 2⋅asin( √(sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)) )	
    #     θa = acos( ( sin φ2 − sin φ1 ⋅ cos δ12 ) / ( sin δ12 ⋅ cos φ1 ) )
    #     θb = acos( ( sin φ1 − sin φ2 ⋅ cos δ12 ) / ( sin δ12 ⋅ cos φ2 ) )	
    #     if sin(λ2−λ1) > 0
    #         θ12 = θa
    #         θ21 = 2π − θb
    #     else
    #         θ12 = 2π − θa
    #         θ21 = θb	
    #     α1 = θ13 − θ12
    #     α2 = θ21 − θ23	
    #     α3 = acos( −cos α1 ⋅ cos α2 + sin α1 ⋅ sin α2 ⋅ cos δ12 )	
    #     δ13 = atan2( sin δ12 ⋅ sin α1 ⋅ sin α2 , cos α2 + cos α1 ⋅ cos α3 )	
    #     φ3 = asin( sin φ1 ⋅ cos δ13 + cos φ1 ⋅ sin δ13 ⋅ cos θ13 )	p3 lat
    #     Δλ13 = atan2( sin θ13 ⋅ sin δ13 ⋅ cos φ1 , cos δ13 − sin φ1 ⋅ sin φ3 )	
    #     λ3 = λ1 + Δλ13	
    # where:	
    #     φ1, λ1, θ13 : 1st start point & (initial) bearing from 1st point towards intersection point
    #     φ2, λ2, θ23 : 2nd start point & (initial) bearing from 2nd point towards intersection point
    #     φ3, λ3 : intersection point
    #
    # notes:
    #     if sin α1 = 0 and sin α2 = 0: infinite solutions
    #     if sin α1 ⋅ sin α2 < 0: ambiguous solution
    #
    # This formulation is not always well-conditioned for meridional or equatorial lines.
    # This is a lot simpler using vectors rather than spherical trigonometry: see latlong-vectors.html.
    #
    def intersection_point( lat1, lon1, a13, lat2, lon2, a23 ):
        p1 = lat1 * DEG_TO_RAD
        p2 = lat2 * DEG_TO_RAD
        l1 = lon1 * DEG_TO_RAD
        l2 = lon2 * DEG_TO_RAD
        dp = (lat2-lat1) * DEG_TO_RAD
        dl = (lon2-lon1) * DEG_TO_RAD
        
        sdp  = sin( dp/2 )
        sdl  = sin( dl/2 )
        sp1  = sin( p1 )
        sp2  = sin( p1 )
        cp1  = cos( p1 )
        cp2  = cos( p1 )
        d12  = 2.0*asin( sqrt( sdp*sdp + cp1*cp2*sdl*sdl ) )
        sd12 = sin( d12 )
        cd12 = cos( d12 )
        aa   = acos( (sp2 - sp1*cd12) / (sd12*cp1) )
        ab   = acos( (sp2 - sp2*cd12) / (sd12*cp1) )
        if sin( l2-l1 ) > 0.0:
            a12 = aa
            a21 = PI2 - ab
        else:
            a12 = PI2 - aa
            a21 = ab
        a1   = a13 - a12
        a2   = a21 - a23
        sa1  = sin( a1 )
        sa2  = sin( a2 )
        ca1  = cos( a1 )
        ca2  = cos( a2 )
        a3   = acos( -ca1*ca2 + sa1*sa2*cd12 )
        cad  = cos( a3 )
        d13  = atan2( sd12*sa1*sa2, ca2 + ca1*ca3 )
        sd13 = sin( d13 )
        cd13 = cos( d13 )
        sa13 = sin( a13 )
        ca13 = cos( a13 )
        p3   = asin( sp1*cd13 + cp1*sd13*ca13 )
        sp3  = sin( p3 )
        dl13 = atan2( s123*sd13*cp1, cd13 - sp1*sp3 )
        l3   = l1 + dl13

        lat3 = p3 * RAD_TO_DEG
        lon3 = l3 * RAD_TO_DEG
        return (lat3, lon3)

    # Cross-Track Distance
    #
    # Distance of a point from a great-circle path (sometimes called cross track error).
    #
    # Formula:	
    #    dxt = asin( sin(δ13) ⋅ sin(θ13−θ12) ) ⋅ R
    # where:
    #    δ13 is (angular) distance from start point to third point
    #    θ13 is (initial) bearing from start point to third point
    #    θ12 is (initial) bearing from start point to end point
    #    R is the earth’s radius
    #
    def cross_track_distance( d13, a13, a12, in_nm=True ):
        if in_nm: d13 *= NM_TO_METER
        d13 /= R
        dxt = asin( sin( d13 )*sin( a13-a12 ) ) * R
        if in_nm: dxt *= METER_TO_NM
        return dxt

    # Along-Track Distance
    #
    # The great-circle path is identified by a start point and an end point. 
    # Depending on what initial data you’re working from, 
    # you can use the formulas above to obtain the relevant distance and bearings. 
    # The sign of dxt tells you which side of the path the third point is on.
    #
    # The along-track distance, from the start point to the closest point on the path to the third point, is
    #
    # Formula:	
    #     dat = acos( cos(δ13) / cos(δxt) ) ⋅ R
    # where:
    #     δ13 is (angular) distance from start point to third point
    #     δxt is (angular) cross-track distance
    #     R is the earth’s radius
    #
    def along_track_distance( d13, dxt, in_nm=True ):
        if in_nm: 
            d13 *= NM_TO_METER
            dxt *= NM_TO_METER
        dat = acos( cos( d13 ) / cos( dxt ) ) * R
        if in_nm: dat *= METER_TO_NM
        return dat

    # Maximum Latitide of Great Circle Path
    #
    # ‘Clairaut’s formula’ will give you the maximum latitude of a great circle path, given a bearing θ and latitude φ on the great circle:
    #
    # Formula:	
    #     φmax = acos( | sin θ ⋅ cos φ | )
    #
    def maximum_latitude( a, lat ):
        p = lat * DEG_TO_RAD
        pmax = acos( abs( sin(a)*cos(p) ) )
        latmax = (pmax*RAD_TO_DEG + 360.0) % 360
        return latmax
