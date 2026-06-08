import tkinter as tk
import serial
import serial.tools.list_ports
import time

class ArmController:
    def __init__(self, root):
        self.root = root
        self.root.title("Robotic Arm Controller")
        self.root.geometry("480x420")
        self.ser = None

        # --- Port selection ---
        top = tk.Frame(root, pady=8)
        top.pack(fill="x", padx=16)
        tk.Label(top, text="COM Port:").pack(side="left")
        self.port_var = tk.StringVar()
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_menu = tk.OptionMenu(top, self.port_var, *ports or ["No ports"])
        self.port_menu.pack(side="left", padx=6)
        self.port_var.set(ports[0] if ports else "")
        self.connect_btn = tk.Button(top, text="Connect", command=self.connect, bg="#4CAF50", fg="white")
        self.connect_btn.pack(side="left", padx=6)
        self.status = tk.Label(top, text="Disconnected", fg="red")
        self.status.pack(side="left", padx=8)

        # --- Servo sliders ---
        labels = ["Servo 1 — Base", "Servo 2 — Shoulder", "Servo 3 — Elbow", "Servo 4 — Gripper"]
        self.sliders = []
        for i, name in enumerate(labels):
            frame = tk.Frame(root, pady=4)
            frame.pack(fill="x", padx=16)
            tk.Label(frame, text=name, width=20, anchor="w").pack(side="left")
            sl = tk.Scale(frame, from_=0, to=180, orient="horizontal",
                          length=260, command=lambda v, n=i+1: self.send(n, int(v)))
            sl.set(90)
            sl.pack(side="left")
            tk.Label(frame, text="°").pack(side="left")
            self.sliders.append(sl)

        # --- Preset buttons ---
        btn_frame = tk.Frame(root, pady=12)
        btn_frame.pack()
        tk.Button(btn_frame, text="Home (all 90°)", command=self.home, width=16).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Pick up", command=self.pickup, width=16).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Release", command=self.release, width=16).pack(side="left", padx=6)

        # --- Log ---
        self.log = tk.Text(root, height=5, state="disabled", bg="#f5f5f5", font=("Courier", 9))
        self.log.pack(fill="x", padx=16, pady=4)

    def connect(self):
        # Try selected port first, then auto-scan all available ports
        ports_to_try = [self.port_var.get()]
        all_ports = [p.device for p in serial.tools.list_ports.comports()]
        ports_to_try += [p for p in all_ports if p != self.port_var.get()]

        for port in ports_to_try:
            try:
                self.ser = serial.Serial(port, 9600, timeout=1)
                time.sleep(2)
                self.status.config(text=f"Connected: {port}", fg="green")
                self.log_msg(f"Connected to {port}")
                return
            except serial.SerialException as e:
                self.log_msg(f"Tried {port}: {e}")
                continue

        self.status.config(text="Failed — no port found", fg="red")
        self.log_msg("Could not connect to any port. Check USB and Device Manager.")

    def send(self, servo_num, angle):
        if self.ser and self.ser.is_open:
            cmd = f"S{servo_num}:{angle}\n"
            self.ser.write(cmd.encode())
            self.log_msg(f"Sent: {cmd.strip()}")

    def home(self):
        for i in range(1, 5):
            self.send(i, 90)
            self.sliders[i-1].set(90)

    def pickup(self):
        moves = [(1, 90), (2, 45), (3, 120), (4, 30)]
        for s, a in moves:
            self.send(s, a)
            self.sliders[s-1].set(a)
            time.sleep(0.3)

    def release(self):
        self.send(4, 150)
        self.sliders[3].set(150)

    def log_msg(self, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

root = tk.Tk()
ArmController(root)
root.mainloop()