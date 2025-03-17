print('Ibrahim Fahad')
from graphh import GraphHopper
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import folium

api_key = "6f63a9db-97f4-47e0-8359-1ebb19487363"

#CO2 Emissions (kg/km) researched from government websites
EMISSION_FACTORS = {
    "gasoline_car": 0.21,
    "ev_car": 0.05,
    "transit": 0.08,
    "bicycling": 0.00,
    "walking": 0.00, 
    "train": 0.05
}

mapper = GraphHopper("<API_KEY>") #I am not putting the API key here for security reasons.


def calc_emissions():
    try:
        origin = mapper.address_to_latlong(origin_address.get())
        destination = mapper.address_to_latlong(destination_address.get())
        print(f"API Response for {origin_address.get()}: {origin}")
        print(f"API Response for {destination_address.get()}: {destination}")
        
        distance_km = mapper.distance([origin, destination], unit='km')
        
            
        
        print(origin)
        print(destination)
        
        
        mode = transport_mode.get()
        #calculate CO2 Emissions
        emission_factor = EMISSION_FACTORS.get(mode, 0.21)
        emissions = round(distance_km * emission_factor, 2)
        
        if (mode == "gasoline_car" or mode == "ev_car") and distance_km < 10:
            messagebox.showinfo("Tip", 'Since this is under 10 km, you can walk or bike, or take public transportation.')
        elif (mode == "gasoline_car" or mode == "ev_car") and distance_km < 50:
            messagebox.showinfo("Tip", 'Since this is under 50 km, you should take public transportation.')
        
        #display results
        result_text = f"Distance: {round(distance_km, 2)} km\n"
        result_text += f"CO2 Emissions: {emissions} kg\n"
        
        messagebox.showinfo("Results", result_text)
        
    except ValueError:
        messagebox.showerror("Error", "Please Enter Valid Coordinates!")
        

#create a main window

root = ttk.Window(themename="darkly")
title = ttk.Label(root, text="GreenRide - Eco Friendly Commute Planner")
title.pack()

#take user input

label_origin_address = ttk.Label(root, text="Enter Origin Address: ")
label_origin_address.pack()

origin_address = ttk.Entry(root)
origin_address.pack()

label_destination_address = ttk.Label(root, text="Enter Destination Address: ")
label_destination_address.pack()

destination_address = ttk.Entry(root)
destination_address.pack()

transport_mode = ttk.StringVar(value="driving")
mode_label = ttk.Label(root, text="Enter Transport Mode: ")
mode_label.pack()

modes = ["gasoline_car", "ev_car", "transit", "bicycling", "walking", "train"]
for m in modes:
    mode_radio = ttk.Radiobutton(root, text=m.replace("_", " ").capitalize(), variable=transport_mode, value=m)
    mode_radio.pack()
    
calc_button = ttk.Button(root, text="Calculate Distance and CO2 Emissions", command=calc_emissions)
calc_button.pack()

root.mainloop()
