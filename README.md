# 🦾 Arduino Robotic Arm — Laptop Controlled

A 4-servo robotic arm controlled in real time from a laptop via USB serial using a Python GUI. Powered entirely by a power bank — no wall socket needed.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python) ![Arduino](https://img.shields.io/badge/Arduino-Uno%20R3-teal?logo=arduino) ![License](https://img.shields.io/badge/License-MIT-green)

---

##
<img width="960" height="1280" alt="WhatsApp Image 2026-06-09 at 12 51 29 AM (2)" src="https://github.com/user-attachments/assets/c5e7aa95-2a53-4c22-807e-679349b2cb52" />

<img width="1280" height="960" alt="WhatsApp Image 2026-06-09 at 12 51 29 AM (11)" src="https://github.com/user-attachments/assets/1c509b4f-1c31-420d-b1d1-667e534e9897" />
 Demo

> GUI running on laptop → USB serial → Arduino Uno R3 → 4 servo motors

```
Laptop (Python GUI)
      │
      │ USB Serial (9600 baud)
      ▼
Arduino Uno R3  ──── Pin 9  ──► Servo 1 (Base rotation)
                ──── Pin 10 ──► Servo 2 (Shoulder joint)
                ──── Pin 11 ──► Servo 3 (Elbow joint)
                ──── Pin 6  ──► Servo 4 (Gripper / Wrist)
                │
                └── Power bank (5V USB) ──► All servos VCC + Arduino 5V
```

---

## 🧰 Hardware Required

| Component | Quantity | Notes |
|---|---|---|
| Arduino Uno R3 | 1 | Main microcontroller |
| SG90 / MG90S Servo motor | 4 | MG90S recommended for base & shoulder |
| Power bank | 1 | 5V USB output, ≥ 2A |
| USB-A to bare wire cable | 1 | Strip red (+5V) and black (GND) |
| Mini breadboard | 1 | For shared 5V / GND power rails |
| Jumper wires | ~20 | Male-to-male and female-to-male |
| Servo horns / joints | 4 | Included in servo bags |

---

## 🔩 Joint & Horn Setup

| Arduino Pin | Servo | Joint | Horn Type |
|---|---|---|---|
| Pin 9 | Servo 1 | Base rotation | Round disc horn |
| Pin 10 | Servo 2 | Shoulder joint | Long single arm horn |
| Pin 11 | Servo 3 | Elbow joint | Cross / X horn |
| Pin 6 | Servo 4 | Gripper / Wrist | Short single arm horn |

---

## ⚡ Wiring Guide

### Power bank → Breadboard
| Power bank wire | Breadboard rail |
|---|---|
| Red (USB +5V) | + rail |
| Black (USB GND) | − rail |

### Breadboard → Arduino
| Breadboard rail | Arduino pin |
|---|---|
| + rail | 5V pin |
| − rail | GND pin |

### Each Servo → Breadboard + Arduino
| Servo wire colour | Connects to |
|---|---|
| Red | Breadboard + rail (5V) |
| Brown / Black | Breadboard − rail (GND) |
| Orange / Yellow | Arduino PWM pin (see table above) |

---

## 💻 Software Setup

### Requirements
- Python 3.x
- pyserial library

### Install dependencies
```bash
pip install pyserial
```

### Clone this repo
```bash
git clone https://github.com/yourusername/arduino-robotic-arm.git
cd arduino-robotic-arm
```

---

## 📂 Project Structure

```
arduino-robotic-arm/
│
├── arm_controller.py       # Python laptop GUI controller
├── arm_firmware/
│   └── arm_firmware.ino    # Arduino sketch
└── README.md
```

---

## 🔌 Arduino Sketch Upload

1. Open `arm_firmware/arm_firmware.ino` in Arduino IDE
2. Select board: **Arduino Uno**
3. Select port: **COMx** (your Arduino port)
4. Click **Upload**
5. Close Arduino IDE completely before running the Python script

```cpp
#include <Servo.h>

Servo s1, s2, s3, s4;

void setup() {
  Serial.begin(9600);
  s1.attach(9);
  s2.attach(10);
  s3.attach(11);
  s4.attach(6);
  s1.write(90); s2.write(90);
  s3.write(90); s4.write(90);
  Serial.println("ARM_READY");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd.length() >= 4 && cmd[0] == 'S') {
      int servoNum = cmd[1] - '0';
      int angle = cmd.substring(3).toInt();
      angle = constrain(angle, 0, 180);
      if      (servoNum == 1) s1.write(angle);
      else if (servoNum == 2) s2.write(angle);
      else if (servoNum == 3) s3.write(angle);
      else if (servoNum == 4) s4.write(angle);
      Serial.print("OK:"); Serial.println(cmd);
    }
  }
}
```

---

## 🖥️ Running the Laptop Controller

```bash
python arm_controller.py
```

1. Select your COM port from the dropdown
2. Click **Connect** — status turns green
3. Drag sliders to move each joint in real time
4. Use preset buttons for quick positions

### Preset positions
| Button | Servo 1 | Servo 2 | Servo 3 | Servo 4 |
|---|---|---|---|---|
| Home | 90° | 90° | 90° | 90° |
| Pick up | 90° | 45° | 120° | 30° |
| Release | — | — | — | 150° |

---

## 🔧 Troubleshooting

### PermissionError: Access is denied (COM3)
```
1. Close Arduino IDE completely
2. Kill any leftover python.exe via Task Manager
3. Unplug Arduino → wait 5 sec → replug
4. Run PowerShell as Administrator
5. Or reassign COM port number in Device Manager → Properties → Port Settings → Advanced
```

### COM port not showing in dropdown
```
Click the Refresh button in the GUI, or run:
python -c "import serial.tools.list_ports; [print(p.device, p.description) for p in serial.tools.list_ports.comports()]"
```

### Servos jittering or not moving
```
- Power bank must output ≥ 2A
- All servo GND wires must share the same GND as Arduino
- Keep power bank awake with a small dummy load (LED + 220Ω resistor)
```

### Power bank keeps switching off
```
Power banks auto-shutoff when current draw is too low.
Add a 220Ω resistor + LED across the 5V and GND rails to keep it awake.
```

---

## 📡 Serial Command Protocol

Commands are sent as plain text over serial at 9600 baud.

| Command | Action |
|---|---|
| `S1:90\n` | Move Servo 1 (Base) to 90° |
| `S2:45\n` | Move Servo 2 (Shoulder) to 45° |
| `S3:120\n` | Move Servo 3 (Elbow) to 120° |
| `S4:30\n` | Move Servo 4 (Gripper) to 30° |

Arduino replies with `OK:S1:90` as confirmation.

---

## 🛠️ Built With

- [Arduino](https://www.arduino.cc/) — microcontroller firmware
- [Python](https://www.python.org/) — laptop GUI
- [pyserial](https://pyserial.readthedocs.io/) — serial communication
- [tkinter](https://docs.python.org/3/library/tkinter.html) — GUI framework

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙋 Author

Made by **Abilash**  
Arduino + Python robotic arm project
