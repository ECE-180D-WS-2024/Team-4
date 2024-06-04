import math
import gravity

gravity_const = 9.8

def moonGravityChanger(m_bool):
    global gravity_const
    if(m_bool):
    
        gravity_const = 9.8 * 0.5
        
    else:
        gravity_const = 9.8


def ballPath(startx, starty, power, ang, time):
    global gravity_const
    angle = ang
    
    velx = math.cos(angle) * power
    vely = math.sin(angle) * power

    distX = velx * time
    distY = (vely * time) + ((-gravity_const * (time ** 2)) / 2)

    newx = round(distX + startx)
    newy = round(starty - distY)

    return (newx, newy)


def findPower(power, angle, time):
    global gravity_const
    velx = math.cos(angle) * power
    vely = math.sin(angle) * power

    vfy = vely + (-gravity_const * time)
    vf = math.sqrt((vfy**2) + (velx**2))

    return vf


def findAngle(power, angle):
    
    vely = math.sin(angle) * power
    velx = math.cos(angle) * power

    ang = math.atan(abs(vely) / abs(velx))

    return ang


def maxTime(power, angle):
    global gravity_const
    vely = math.sin(angle) * power
    time = ((power * -1) - (math.sqrt(power**2))) / -gravity_const

    return time / 2