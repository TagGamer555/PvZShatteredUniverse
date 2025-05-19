from math import sqrt, atan2, degrees, radians, cos, sin # ONLY IMPORT WHAT YOU NEED!! All hail the fast loading times.
# 11/05/2025 - damn, I haven't been here in a while...

def dist(x1, y1, x2, y2):
    return sqrt((x2 - x1)**2 + (y2 - y1)**2) # I almost forgot that sqrt() is faster than **0.5, but I did! :D

# function to calculate the angle between two points in degrees
def point2point_angle_degr(x1, y1, x2, y2):
    angle_rad = atan2(y2 - y1, x2 - x1)
    angle_deg = degrees(angle_rad)
    return angle_deg

# function to translate a point by a given distance in a specific direction (angle in degrees)
def translate_point_degr(x, y, distance, angle_deg):
    angle_rad = radians(angle_deg)
    x_new = x + distance * cos(angle_rad)
    y_new = y + distance * sin(angle_rad)
    return x_new, y_new

def point2point_slope(x1, y1, x2, y2):
    try: return (y2 - y1) / (x2 - x1)
    except ZeroDivisionError: return float('inf')

def in_range(x, low, hi):
    return low <= x <= hi
