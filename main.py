from machine import Pin, PWM
from utime import sleep as delay

# 🔍 Αισθητήρες
SensorR = Pin(26, Pin.IN)  # Δεξιός αισθητήρας IR
SensorL = Pin(2, Pin.IN)  # Αριστερός αισθητήρας IR

# ⚙️ Σύνδεση μοτέρ μέσω του Motor Driver
IN1 = Pin(9, Pin.OUT)  # IN1 για Αριστερό μοτέρ
IN2 = Pin(8, Pin.OUT)  # IN2 για Αριστερό μοτέρ
IN3 = Pin(11, Pin.OUT)  # IN3 για Δεξιό μοτέρ
IN4 = Pin(10, Pin.OUT)  # IN4 για Δεξιό μοτέρ

motorEsq1 = PWM(IN1)
motorEsq2 = PWM(IN2)
motorDir1 = PWM(IN3)
motorDir2 = PWM(IN4)

motorEsq1.freq(250)  # Συχνότητα PWM
motorEsq2.freq(250)  # Συχνότητα PWM
motorDir1.freq(250)  # Συχνότητα PWM
motorDir2.freq(250)  # Συχνότητα PWM

# 🌍 Εξισώσεις για το mapping των τιμών
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# 🚗 Εξάρτηση της ταχύτητας του μοτέρ από την τιμή 0-100
def pulsoMotor(speed):
    return map(speed, 0, 100, 0, 65534)

# 🛑 Σταμάτημα των μοτέρ
def parar():
    motorEsq1.duty_u16(0)
    motorDir1.duty_u16(0)
    motorEsq2.duty_u16(0)
    motorDir2.duty_u16(0)

def machine_reset():
    print("🔄 Επαναφορά μηχανήματος...")
    delay(1)
    reset()

# 🚦 Αρχική καθυστέρηση 2 δευτερολέπτων
parar()
delay(2)

while True:
    valSensorE = SensorL.value()  # Τιμή του αριστερού αισθητήρα
    valSensorD = SensorR.value()  # Τιμή του δεξιού αισθητήρα
    
    if not valSensorD and not valSensorE:
        # Αν οι δύο αισθητήρες ανιχνεύουν μαύρη γραμμή
        motorEsq1.duty_u16(pulsoMotor(50))  # Κινείται το αριστερό μοτέρ
        motorDir1.duty_u16(pulsoMotor(50))  # Κινείται το δεξί μοτέρ
        print("➡️ Κίνηση ευθεία πάνω στη μαύρη γραμμή")

    elif not valSensorE and valSensorD:
        # Αν ο αριστερός αισθητήρας είναι πάνω στη γραμμή και ο δεξιός αισθητήρας είναι πάνω σε άσπρο
        motorEsq1.duty_u16(pulsoMotor(0))   # Σταματά το αριστερό μοτέρ
        motorDir1.duty_u16(pulsoMotor(50))  # Κινείται το δεξί μοτέρ
        print("↪️ Στρίβει δεξιά (μαύρη γραμμή αριστερά)")

    elif valSensorE and not valSensorD:
        # Αν ο δεξιός αισθητήρας είναι πάνω στη γραμμή και ο αριστερός αισθητήρας είναι πάνω σε άσπρο
        motorDir1.duty_u16(pulsoMotor(0))   # Σταματά το δεξί μοτέρ
        motorEsq1.duty_u16(pulsoMotor(50))  # Κινείται το αριστερό μοτέρ
        print("↩️ Στρίβει αριστερά (μαύρη γραμμή δεξιά)")

    else:
        # Αν οι δύο αισθητήρες ανιχνεύουν άσπρο τραπέζι
        motorEsq1.duty_u16(pulsoMotor(0))   # Σταματά το αριστερό μοτέρ
        motorDir1.duty_u16(pulsoMotor(0))   # Σταματά το δεξί μοτέρ
        print("🛑 Σταματά (απομακρύνθηκε από τη γραμμή)")
    
    delay(0.01)
    # Μικρή καθυστέρηση για σταθερότητα
