import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)

import sys, tty, termios, signal

######################
## Motor Establishment
######################

motorL = 0
motorR = 1
motorZ = 2

motorR_forward = 1000
motorR_backward = 1000
motorL_forward = 1000
motorL_backward = 1000
motorZ_forward = 1000
motorZ_backward = 1000


try:
  RPL.pinMode(motorL,RPL.SERVO)
  RPL.servoWrite(motorL,1500)
  RPL.pinMode(motorR,RPL.SERVO)
  RPL.servoWrite(motorR,1500)
  #RPL.pinMode(motorZ,RPL.SERVO)
  #RPL.servoWrite(motorZ,1500)
except:
  pass

######################
## Individual commands
######################

def forward():
  if mortorR == 1:
      RPL.servoWrite(motorR,motorR_forward)
  elif mortorR == 2:
      RPL.servoWrite(motorR,motorL_forward)
  elif mortorR == 3:
      RPL.servoWrite(motorR,motorZ_forward)

def reverse():
  RPL.servoWrite(motorL,motorL_backward)
  RPL.servoWrite(motorR,motorR_forward)

def print_speed():
  print '--FORWARD: Left Motor: ', motorL_forward, ' Right Motor: ', motorR_forward, '\r'
  print '  BACKWARD: Left Motor: ', motorR_backward, ' Right Motor: ', motorL_backward, '\r'

#legacy#

#def forwardSpeedChanges(change, mn = 400, mx = 2300):
#  global motorR_forward
#  global motorL_forward
#  motorR_forward += change
#  motorL_forward += change
#  motorR_forward = max(min(motorR_forward, mx), mn)
#  motorL_forward = max(min(motorL_forward, mx), mn)
#  print_speed()

def forwardSpeedChanges(change, mn = 400, mx = 2300):
  global motorR_forward
  global motorL_forward
  if mortorR == 1:
      motorR_forward += change
      motorR_forward = max(min(motorR_forward, mx), mn)
  elif mortorR == 2:
      motorL_forward += change
      motorL_forward = max(min(motorL_forward, mx), mn)
  elif mortorR == 3:
      motorZ_forward += change
      motorZ_forward = max(min(motorZ_forward, mx), mn)
  print_speed()



def forwardSpeedChangeReset():
    global motorR_forward
    global motorL_forward
    motorR_forward = 1000
    print_speed()

def print_motor():
    print motorR

def motorchange(change, mn = 0, mx = 5):
  global motorR
  motorR = change

  print_motor()

def stopAll():
  try:
    RPL.servoWrite(motorL,400)
    RPL.servoWrite(motorR,motorR_forward)
  except:
    print "error except"
    pass


fd = sys.stdin.fileno() # I don't know what this does
old_settings = termios.tcgetattr(fd) # this records the existing console settings that are later changed with the tty.setraw... line so that they can be replaced when the loop ends

######################################
## Other motor commands should go here
######################################

def interrupted(signum, frame): # this is the method called at the end of the alarm
  stopAll()

signal.signal(signal.SIGALRM, interrupted) # this calls the 'interrupted' method when the alarm goes off
tty.setraw(sys.stdin.fileno()) # this sets the style of the input

print "Ready To Drive! Press * to quit.\r"
## the SHORT_TIMEOUT needs to be greater than the press delay on your keyboard
## on your computer, set the delay to 250 ms with `xset r rate 250 20`
SHORT_TIMEOUT = 0.255 # number of seconds your want for timeout
while True:
  signal.setitimer(signal.ITIMER_REAL,SHORT_TIMEOUT) # this sets the alarm
  ch = sys.stdin.read(1) # this reads one character of input without requiring an enter keypress
  signal.setitimer(signal.ITIMER_REAL,0) # this turns off the alarm
  if ch == '*': # pressing the asterisk key kills the process
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) # this resets the console settings
    break # this ends the loop
  else:
    if ch == 'a':
      forwardSpeedChanges(60)
      forward()
    elif ch == "r":
      forwardSpeedChangeReset()
    elif ch == "d":
      forwardSpeedChanges(-60)
      reverse()
    elif ch == "1":
      motorchange(1)
    elif ch == "2":
      motorchange(2)
    elif ch == "3":
      motorchange(3)
    elif ch == "4":
      motorchange(4)
    else:
      stopAll()
