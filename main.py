import machine 
import utime, time

open_close = machine.Pin(27,machine.Pin.IN,machine.Pin.PULL_DOWN)
full = machine.Pin(28,machine.Pin.IN,machine.Pin.PULL_DOWN)

#PWM for opening/close the trash 
servoTrash = machine.PWM(machine.Pin(15))

#Motor M1A,M2A,M1B,M2B
M1A = machine.Pin(10, machine.Pin.OUT)
M1B = machine.Pin(11, machine.Pin.OUT)
M2A = machine.Pin(12, machine.Pin.OUT)
M2B = machine.Pin(13, machine.Pin.OUT)

uart = machine.UART(0, baudrate=9600,bits=8, parity=None, stop=1)

def move_servo(pin):
    servoTrash.freq(100)
    servoTrash.duty_u16(0)
    if(open_close.value()==0):
        for i in range(65536):
          servoTrash.duty_u16(i)
        utime.sleep(2)
        for i in range(65536,0,-1):
          servoTrash.duty_u16(i)
        utime.sleep(1)
        
def is_trash_full(pin):
    if(full.value()==0):
        print("trash full")
    

def sendCMD_waitResp(cmd, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(timeout)
    print()
    
def waitResp(timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print(resp)

def sendCMD_waitRespLine(cmd, timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitRespLine(timeout)
    print()
    
def waitRespLine(timeout=2000):
    prvMills = utime.ticks_ms()
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            print(uart.readline())

def backward_move():
    M1A.value(1)
    M2A.value(1)
    
def forward_move():
    M1B.value(1)
    M2B.value(1)
    
def right_move():
    M1A.value(0)
    M2A.value(1)
    M1B.value(1)
    M2B.value(0)

def left_move():
    M1A.value(1)
    M2A.value(0)
    M1B.value(0)
    M2B.value(1)
    
def break_move():
    print("break")
    M1A.value(0)
    M2A.value(0)
    M1B.value(0)
    M2B.value(0)
 
def getCommand(command):
    if(command != ""):
        if "forward" in command: 
            forward_move()
            utime.sleep(0.02)
        elif "left" in command: 
            left_move()
            utime.sleep(0.02)
        elif "right" in command: 
            right_move()
            utime.sleep(0.02)
        elif "backward" in command: 
            backward_move()
            utime.sleep(0.02)
    else:
        break_move()
        return
    
open_close.irq(trigger=machine.Pin.IRQ_RISING, handler=move_servo)
full.irq(trigger=machine.Pin.IRQ_RISING, handler=is_trash_full)

utime.sleep(0.5)

while True:
    break_move()
    
    line = uart.readline()
    lineDecode =line.decode("utf-8")
    getCommand(lineDecode)
    
    utime.sleep(1)
