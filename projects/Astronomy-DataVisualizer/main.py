import requests
import matplotlib.pyplot as plt

def fetch_exoplanet_data():
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
    query = {
        "query": "SELECT pl_name, pl_orbper, pl_rade, disc_year FROM ps",
        "format": "json"
    }
    response = requests.get(url, params=query)
    return response.json() if response.status_code == 200 else []

def process_data(data):
    return [planet for planet in data if planet.get("pl_orbper") and planet.get("pl_rade")]

def plot_orbital_period_vs_radius(data):
    x = [planet["pl_orbper"] for planet in data]
    y = [planet["pl_rade"] for planet in data]
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, alpha=0.5)
    plt.title("Orbital Period vs Radius")
    plt.xlabel("Orbital Period (days)")
    plt.ylabel("Radius (Earth radii)")
    plt.grid(True)
    plt.savefig("orbital_plot.png")  # ✅ Save as image
    print("Plot saved as orbital_plot.png")

def search_planets(data, keyword):
    return [planet for planet in data if keyword.lower() in planet["pl_name"].lower()]

def main():
    data = []
    cleaned_data = []

    while True:
        print("\n--- Astronomy Data Visualizer ---")
        print("1. Fetch Data")
        print("2. Process Data")
        print("3. Visualize Orbital Period vs Radius")
        print("4. Search Planet by Name")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Fetching data...")
            data = fetch_exoplanet_data()
            print(f"Fetched {len(data)} records.")
        elif choice == "2":
            if not data:
                print("Please fetch data first.")
            else:
                cleaned_data = process_data(data)
                print(f"Processed {len(cleaned_data)} records.")
        elif choice == "3":
            if not cleaned_data:
                print("Please process data first.")
            else:
                plot_orbital_period_vs_radius(cleaned_data)
        elif choice == "4":
            if not cleaned_data:
                print("Please process data first.")
            else:
                keyword = input("Enter planet name keyword: ")
                results = search_planets(cleaned_data, keyword)
                if results:
                    for r in results:
                        print(f"{r['pl_name']} | Radius: {r['pl_rade']} Earth | Orbital Period: {r['pl_orbper']} days")
                else:
                    print("No matching planets found.")
        elif choice == "5":
            print("Exiting. Bye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
