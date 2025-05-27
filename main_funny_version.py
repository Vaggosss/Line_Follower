import uasyncio as asyncio
from machine import Pin, PWM
import neopixel

# --- WS2812B setup ---
NUM_PIXELS = 2
np = neopixel.NeoPixel(Pin(18), NUM_PIXELS)

# --- Buzzer setup ---
buzzer = PWM(Pin(22))
buzzer.duty_u16(0)

# --- IR sensors ---
SensorR = Pin(26, Pin.IN)
SensorL = Pin(2, Pin.IN)

# --- Motor driver pins ---
IN1 = Pin(9, Pin.OUT)
IN2 = Pin(8, Pin.OUT)
IN3 = Pin(11, Pin.OUT)
IN4 = Pin(10, Pin.OUT)

motorEsq1 = PWM(IN1)
motorEsq2 = PWM(IN2)
motorDir1 = PWM(IN3)
motorDir2 = PWM(IN4)

for motor in (motorEsq1, motorEsq2, motorDir1, motorDir2):
    motor.freq(250)

# --- Helpers ---
def map_val(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def pulsoMotor(speed):
    return map_val(speed, 0, 100, 0, 65534)

def parar():
    motorEsq1.duty_u16(0)
    motorDir1.duty_u16(0)
    motorEsq2.duty_u16(0)
    motorDir2.duty_u16(0)

# --- HSV to RGB ---
def hsv_to_rgb(h):
    h = h % 360
    x = int(255 * (1 - abs((h / 60) % 2 - 1)))
    if h < 60: return (255, x, 0)
    elif h < 120: return (x, 255, 0)
    elif h < 180: return (0, 255, x)
    elif h < 240: return (0, x, 255)
    elif h < 300: return (x, 0, 255)
    else: return (255, 0, x)

# --- Rainbow animation ---
async def rainbow_fade():
    hue = 0
    while True:
        for i in range(NUM_PIXELS):
            offset = (hue + i * 60) % 360
            np[i] = hsv_to_rgb(offset)
        np.write()
        hue = (hue + 2) % 360
        await asyncio.sleep(0.03)

# --- Notes ---
# Octave 4 & 5 notes
NOTE_C4 = 261; NOTE_CS4 = 277; NOTE_D4 = 294; NOTE_DS4 = 311; NOTE_E4 = 329
NOTE_F4 = 349; NOTE_FS4 = 370; NOTE_G4 = 392; NOTE_GS4 = 415; NOTE_A4 = 440
NOTE_AS4 = 466; NOTE_B4 = 493

NOTE_C5 = 523; NOTE_CS5 = 554; NOTE_D5 = 587; NOTE_DS5 = 622; NOTE_E5 = 659
NOTE_F5 = 698; NOTE_FS5 = 740; NOTE_G5 = 784; NOTE_GS5 = 831; NOTE_A5 = 880
NOTE_AS5 = 932; NOTE_B5 = 988

NOTE_C6 = 1047
REST = 0
BEAT = 0.07  # Base beat

# --- Melody ---
melody = [
    NOTE_B4, NOTE_B4, NOTE_CS5, NOTE_B4, NOTE_CS5, NOTE_B4, NOTE_GS4, NOTE_A4,
    NOTE_B4, NOTE_CS5, NOTE_CS5, NOTE_DS5, NOTE_CS5, NOTE_DS5, NOTE_CS5, NOTE_A4, NOTE_B4,
    NOTE_CS5, NOTE_DS5, NOTE_DS5, NOTE_E5, NOTE_DS5, NOTE_B4, NOTE_CS5, NOTE_DS5,
    NOTE_CS5, NOTE_B4, NOTE_A4, NOTE_GS4, NOTE_GS4, NOTE_GS4, NOTE_GS4, NOTE_GS4,
    NOTE_GS4, NOTE_GS4, NOTE_GS4, NOTE_GS4
]

rhythm = [
    BEAT*4, BEAT*2, BEAT*2, BEAT*4, BEAT*4, BEAT*4, BEAT*4, BEAT*4,
    BEAT*4, BEAT*4, BEAT*2, BEAT*2, BEAT*4, BEAT*4, BEAT*4, BEAT*4,
    BEAT*4,
    BEAT*4, BEAT*4, BEAT*2, BEAT*2, BEAT*4, BEAT*4, BEAT*2, BEAT*2,
    BEAT*4, BEAT*4, BEAT*4, BEAT*2, BEAT*2, BEAT*2, BEAT*2, BEAT*2,
    BEAT*2, BEAT*2, BEAT*2, BEAT*4
]

# --- Play melody ---
async def play_melody_loop():
    while True:
        for note, duration in zip(melody, rhythm):
            if note == REST:
                buzzer.duty_u16(0)
            else:
                buzzer.freq(note)
                buzzer.duty_u16(32768)
            await asyncio.sleep(duration)
            buzzer.duty_u16(0)
            await asyncio.sleep(0.05)
        await asyncio.sleep(0.5)  # Small pause between loops

# --- Line following logic ---
async def line_following():
    await asyncio.sleep(2)  # Initial delay
    parar()
    while True:
        valSensorE = SensorL.value()
        valSensorD = SensorR.value()

        if not valSensorD and not valSensorE:
            motorEsq1.duty_u16(pulsoMotor(50))
            motorDir1.duty_u16(pulsoMotor(50))
        elif not valSensorE and valSensorD:
            motorEsq1.duty_u16(0)
            motorDir1.duty_u16(pulsoMotor(50))
        elif valSensorE and not valSensorD:
            motorDir1.duty_u16(0)
            motorEsq1.duty_u16(pulsoMotor(50))
        else:
            motorEsq1.duty_u16(0)
            motorDir1.duty_u16(0)

        await asyncio.sleep(0.01)

# --- Main ---
async def main():
    asyncio.create_task(rainbow_fade())
    asyncio.create_task(play_melody_loop())
    await line_following()

asyncio.run(main())