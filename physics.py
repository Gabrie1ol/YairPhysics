import tkinter as tk

# קבועים
c = 3e8  # מהירות האור במטר לשנייה

class PhotonRocketSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("סימולציית חללית פוטונית")

        # הגדלת גודל המסך
        self.canvas_width = 2000  # רוחב גדול יותר
        self.canvas_height = 600  # גובה גדול יותר
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        self.info = tk.Label(root, text="", font=("Arial", 12))
        self.info.pack(pady=5)

        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        # שדות קלט
        tk.Label(control_frame, text="מסה (ק\"ג):").grid(row=0, column=0)
        self.mass_entry = tk.Entry(control_frame)
        self.mass_entry.insert(0, "1000")
        self.mass_entry.grid(row=0, column=1)

        tk.Label(control_frame, text="שטח קליטה (מ\"ר):").grid(row=1, column=0)
        self.area_entry = tk.Entry(control_frame)
        self.area_entry.insert(0, "10")
        self.area_entry.grid(row=1, column=1)

        tk.Label(control_frame, text="עוצמת אור (W/m²):").grid(row=2, column=0)
        self.intensity_entry = tk.Entry(control_frame)
        self.intensity_entry.insert(0, "1e8")
        self.intensity_entry.grid(row=2, column=1)

        tk.Label(control_frame, text="משך (שניות):").grid(row=3, column=0)
        self.duration_entry = tk.Entry(control_frame)
        self.duration_entry.insert(0, "20")
        self.duration_entry.grid(row=3, column=1)

        tk.Button(control_frame, text="🚀 התחל סימולציה", command=self.start_simulation).grid(row=4, column=0, columnspan=2, pady=5)

        self.dt = 0.1
        self.simulating = False

        # יחס מטרים לפיקסל
        self.scale = 1e3  # 1000 מטר = פיקסל

    def start_simulation(self):
        try:
            self.mass = float(self.mass_entry.get())
            self.area = float(self.area_entry.get())
            self.intensity = float(self.intensity_entry.get())
            self.duration = float(self.duration_entry.get())
        except ValueError:
            self.info.config(text="יש להזין ערכים תקינים")
            return

        self.t = 0
        self.velocity = 0
        self.position = 0
        self.simulating = True

        self.canvas.delete("all")
        self.trail = []

        self.rocket_y = 300  # עדכון המיקום כדי להתאים למסך החדש
        self.draw_rocket(10)

        self.update_simulation()

    def draw_rocket(self, x):
        y = self.rocket_y

        if hasattr(self, 'rocket_parts'):
            for part in self.rocket_parts:
                self.canvas.delete(part)

        # ציור "חללית שטסה ימינה" (חרטום לימין)
        body = self.canvas.create_rectangle(x - 15, y - 5, x + 15, y + 5, fill="white", outline="")
        top_wing = self.canvas.create_polygon(x - 5, y - 5, x - 15, y - 15, x - 10, y - 5, fill="gray")
        bottom_wing = self.canvas.create_polygon(x - 5, y + 5, x - 15, y + 15, x - 10, y + 5, fill="gray")
        nose = self.canvas.create_polygon(x + 15, y - 5, x + 15, y + 5, x + 25, y, fill="red")

        self.rocket_parts = [body, top_wing, bottom_wing, nose]

    def update_simulation(self):
        if self.simulating and self.t <= self.duration:
            acceleration = (self.intensity * self.area) / (self.mass * c)

            self.velocity += acceleration * self.dt
            self.position += self.velocity * self.dt
            self.t += self.dt

            x = 10 + self.position * self.scale

            self.draw_rocket(x)

            self.trail.append((x - 15, self.rocket_y))
            for tx, ty in self.trail[-20:]:
                self.canvas.create_oval(tx - 1, ty - 1, tx + 1, ty + 1, fill="lightgray", outline="lightgray")

            self.info.config(
                text=f"זמן: {self.t:.1f} שניות | מהירות: {self.velocity:.3f} m/s"
            )

            self.root.after(int(self.dt * 1000), self.update_simulation)
        else:
            self.simulating = False
            self.info.config(text=self.info.cget("text") + "\n✔️ סימולציה הסתיימה!")

# הפעלת התוכנית
root = tk.Tk()
app = PhotonRocketSimulation(root)
root.mainloop()

