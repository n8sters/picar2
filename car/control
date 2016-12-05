import pi2go, time
import sys
import tty
import termios

UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

# Code taken from a StackOverflow tutorial on reading input from a keyboard, don't ask me how this works!
def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

# 0=Up, 1=Down, 2=Right, 3=Left arrows

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return ord(c3) - 65  

# End of keyboard code, now my stuff! 


speed = 50

pi2go.init()

# Motor control bit. 
try:
    while True:
        keyp = readkey()
        if keyp == 'w' or keyp == UP:
            pi2go.forward(speed)
        elif keyp == 's' or keyp == DOWN:
            pi2go.reverse(speed)
        elif keyp == 'd' or keyp == RIGHT:
            pi2go.spinRight(speed)
        elif keyp == 'a' or keyp == LEFT:
            pi2go.spinLeft(speed)
        elif keyp == ' ':
            pi2go.stop()
        elif ord(keyp) == 3:
            break

# press ctrl+c and it will stop the program
except KeyboardInterrupt:
    pi2go.cleanup()
