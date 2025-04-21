
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Toplevel, Label, PhotoImage
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import random
import os

class AstronomyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌌 Astronomy Data Visualizer")
        self.root.geometry("1000x720")
        self.data = []
        self.processed_data = []

        self.setup_style()
        self.setup_ui()

    def setup_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10), padding=4)
        style.configure("TEntry", padding=4)

    def setup_ui(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10)

        ttk.Button(top_frame, text="📡 Fetch Data", command=self.fetch_data).grid(row=0, column=0, padx=10)
        ttk.Button(top_frame, text="🧮 Process Data", command=self.process_data).grid(row=0, column=1, padx=10)
        ttk.Button(top_frame, text="📊 Visualize", command=self.visualize_data).grid(row=0, column=2, padx=10)

        search_frame = ttk.LabelFrame(self.root, text="🔍 Search Exoplanets")
        search_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(search_frame, text="Planet Name:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_planet).pack(side=tk.LEFT)

        self.output_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 10), height=10)
        self.output_box.pack(padx=10, pady=10, fill="both", expand=True)

        self.figure = plt.Figure(figsize=(7.5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.chart_frame = ttk.LabelFrame(self.root, text="🪐 Orbital Period vs Radius")
        self.chart_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.chart = FigureCanvasTkAgg(self.figure, self.chart_frame)
        self.chart.get_tk_widget().pack(fill="both", expand=True)

    def fetch_data(self):
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
        query = {
            "query": "SELECT pl_name, pl_orbper, pl_rade, disc_year FROM ps",
            "format": "json"
        }
        try:
            response = requests.get(url, params=query)
            self.data = response.json() if response.status_code == 200 else []
            self.output_box.insert(tk.END, f"✅ Fetched {len(self.data)} records.\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def process_data(self):
        self.processed_data = [
            p for p in self.data if p.get("pl_orbper") and p.get("pl_rade")
        ]
        self.output_box.insert(tk.END, f"✅ Processed {len(self.processed_data)} records.\n")

    def visualize_data(self):
        if not self.processed_data:
            messagebox.showwarning("Warning", "No data to visualize. Please process first.")
            return

        self.ax.clear()
        self.ax.set_xscale("log")
        self.ax.set_yscale("log")
        x = [p["pl_orbper"] for p in self.processed_data]
        y = [p["pl_rade"] for p in self.processed_data]
        sizes = [random.uniform(10, 30) for _ in self.processed_data]
        self.scatter = self.ax.scatter(x, y, alpha=0.5, s=sizes)
        self.ax.set_title("Orbital Period vs Radius")
        self.ax.set_xlabel("Orbital Period (days)")
        self.ax.set_ylabel("Radius (Earth radii)")
        self.chart.draw()

        def animate(frame):
            new_sizes = [random.uniform(10, 30) for _ in self.processed_data]
            self.scatter.set_sizes(new_sizes)
            return self.scatter,

        self.ani = FuncAnimation(self.figure, animate, interval=1000, blit=False)
        self.output_box.insert(tk.END, "✅ Chart with animation updated.\n")

    def search_planet(self):
        keyword = self.search_entry.get().strip().lower()
        if not keyword:
            return
        matches = [p for p in self.processed_data if keyword in p["pl_name"].lower()]
        self.output_box.insert(tk.END, f"🔎 Found {len(matches)} match(es):\n")
        for p in matches[:10]:
            info = f'{p["pl_name"]} | Radius: {p["pl_rade"]} | Period: {p["pl_orbper"]}'
            self.output_box.insert(tk.END, info + "\n")
            self.output_box.window_create(tk.END, window=ttk.Button(self.root, text="ℹ️", command=lambda p=p: self.show_popup(p)))
            self.output_box.insert(tk.END, "\n")

    def show_popup(self, planet):
        radius = planet.get("pl_rade", 0)
        if radius < 1.5:
            image_file = "earth_like.png"
        elif 1.5 <= radius <= 3:
            image_file = "super_earth.png"
        else:
            image_file = "gas_giant.png"

        popup = Toplevel(self.root)
        popup.title(f"Planet Info: {planet.get('pl_name', 'N/A')}")
        popup.geometry("300x400")

        info_text = (
            f"Name: {planet.get('pl_name', 'N/A')}\n"
            f"Radius: {radius} Earth radii\n"
            f"Orbital Period: {planet.get('pl_orbper', 'N/A')} days\n"
            f"Discovery Year: {planet.get('disc_year', 'N/A')}"
        )

        label = Label(popup, text=info_text, font=("Segoe UI", 10), justify="left")
        label.pack(pady=10)

        if os.path.exists(image_file):
            img = PhotoImage(file=image_file)
            img_label = Label(popup, image=img)
            img_label.image = img
            img_label.pack(pady=10)
        else:
            Label(popup, text="🔍 Image not found").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = AstronomyApp(root)
    root.mainloop()

