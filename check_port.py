import serial
import serial.tools.list_ports

print("=== Available ports ===")
for p in serial.tools.list_ports.comports():
    print(f"  {p.device} — {p.description}")

print("\n=== Trying to open COM3 ===")
try:
    s = serial.Serial("COM3", 9600, timeout=1)
    print("SUCCESS — COM3 opened fine!")
    s.close()
except Exception as e:
    print(f"FAILED — {e}")
    print("\nFix: Close Arduino IDE, run PowerShell as Admin, or try a different USB port.")