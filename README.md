# 🤖 Line Following Robot – Academic Final Project

Welcome to our repository!

This project was developed as part of our academic semester's **final exam**. As a team, we created a small **line-following robot** using:

-  **Pi Maker RP2040 Pico** microcontroller
-  **Infrared (IR) sensors** for black line detection
-  A robot **chassis kit** that includes motors, wheels, screws, cables, and a battery case

---

## 📦 Components Used

### 1. Raspberry Pi Pico (RP2040)
We used the **Pi Maker RP2040 Pico** as the central controller to manage sensors and motors.


---

### 2. IR Sensors
Two **infrared sensors** detect the presence of a black line on a white surface to guide the robot’s path.


---

### 3. Robot Chassis Kit
The robot chassis kit included:
- Battery case
- Screws and mounting hardware
- 2x DC motors
- 2x Wheels
- Wires and connecting cables
- Acrylic chassis base



---

## 💰 Cost Breakdown

| Component           | Unit Price (EURO) | Notes                  |
|--------------------|------------------|------------------------|
| RP2040 Board       | *14.90*   | Microcontroller        |
| IR Sensor Pair     | *1*   | Line detection         |
| Chassis Kit        | *0.93*   | Includes all hardware  |

---

## 🧠 How It Works

The robot continuously reads input from the IR sensors. Depending on whether the black line is detected on the left or right, it adjusts motor power to steer appropriately.

```python
from machine import Pin, PWM
from utime import sleep as delay

SensorR = Pin(26, Pin.IN)
SensorL = Pin(2, Pin.IN)

IN1 = Pin(9, Pin.OUT)
IN2 = Pin(8, Pin.OUT)
IN3 = Pin(11, Pin.OUT)
IN4 = Pin(10, Pin.OUT)

motorEsq1 = PWM(IN1)
motorEsq2 = PWM(IN2)
motorDir1 = PWM(IN3)
motorDir2 = PWM(IN4)

motorEsq1.freq(250)
motorEsq2.freq(250)
motorDir1.freq(250)
motorDir2.freq(250)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def pulsoMotor(speed):
    return map(speed, 0, 100, 0, 65534)

def parar():
    motorEsq1.duty_u16(0)
    motorDir1.duty_u16(0)
    motorEsq2.duty_u16(0)
    motorDir2.duty_u16(0)

parar()
delay(2)

while True:
    valSensorE = SensorL.value()
    valSensorD = SensorR.value()
    
    if not valSensorD and not valSensorE:
        motorEsq1.duty_u16(pulsoMotor(50))
        motorDir1.duty_u16(pulsoMotor(50))
        print("➡️ Moving forward")

    elif not valSensorE and valSensorD:
        motorEsq1.duty_u16(pulsoMotor(0))
        motorDir1.duty_u16(pulsoMotor(50))
        print("↪️ Turning right")

    elif valSensorE and not valSensorD:
        motorDir1.duty_u16(pulsoMotor(0))
        motorEsq1.duty_u16(pulsoMotor(50))
        print("↩️ Turning left")

    else:
        motorEsq1.duty_u16(pulsoMotor(0))
        motorDir1.duty_u16(pulsoMotor(0))
        print("🛑 Stopping")

    delay(0.01)

```
---
# ⚠️ Challenges Faced

During the development of our line-following robot, we encountered several practical and technical challenges:

- 🔧 **Sensor Alignment**: Even small misalignments in the IR sensors led to inaccurate detection of the line.
- ⚡ **Power Distribution**: Ensuring stable power to both the motors and the controller board required careful battery management.
- 🛞 **Motor Tuning**: Speed inconsistencies between motors resulted in the robot veering off its intended path.
- 🔩 **Mechanical Assembly**: Properly securing the components to the chassis was critical to avoid vibration and misbehavior.

These challenges helped us develop better problem-solving, collaboration, and hardware debugging skills.

---

# 👥 Team Members

| Name         | Role / Responsibility         |
|--------------|-------------------------------|
| **Dimitris Iatroy** | Hardware engineer              |
| **[Name 2]** | [Your Role Here]              |
| **[Name 3]** | [Your Role Here]              |
| **[Name 4]** | [Your Role Here]              |


---

# 🙏 Thank You!

Thank you for checking out our project! We had a great time building it and hope you enjoyed reading about it as much as we enjoyed making it.



![Robot Victory](https://media.giphy.com/media/IThjAlJnD9WNO/giphy.gif)

---


