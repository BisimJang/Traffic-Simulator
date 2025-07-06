Traffic Simulation Application

Overview
This project is a SUMO-based traffic simulation with real-time visualization using Tkinter and Dash. It includes:
- Traffic flow and signal visualization
- Congestion heatmaps
- Real-time traffic optimization using Reinforcement Learning
- A user-friendly GUI to control the simulation

Installation
1. Install Dependencies
Ensure you have Python 3.8+ installed. Then, install the required packages:
```bash
pip install -r requirements.txt
```

2. Install SUMO
SUMO (Simulation of Urban Mobility) is required. Download and install it from:
[https://sumo.dlr.de/docs/Downloads.html](https://sumo.dlr.de/docs/Downloads.html)

After installation, set the SUMO_HOME environment variable:
```bash
setx SUMO_HOME "C:\path\to\sumo"
```

3. Running the Simulation
To start the application, run:
```bash
python GUI.py
```
This will launch the GUI where you can control the simulation, summarize results, and open the dashboard.

---

Standalone Executable (.exe)
A prebuilt executable (`TrafficSim.exe`) is available for Windows users, eliminating the need for Python installation.

Running the .exe
Simply double-click `TrafficSim.exe` in the `dist/` folder.

If Windows flags the `.exe` as a potential virus, this is a false positive due to PyInstaller's packaging. To run it:
1. Click More Info on the Windows Defender warning.
2. Click Run Anyway.

Alternatively, you can rebuild the `.exe` yourself:
```bash
pyinstaller --onefile --windowed --name TrafficSim GUI.py
```

If `pyinstaller` is not recognized, install it using:
```bash
pip install pyinstaller
```

---

Project Structure
```
TrafficSim/
│── GUI.py              # Main GUI for controlling the simulation
│── simulation.py       # Runs SUMO simulation
│── summarize.py        # Processes traffic data
│── dashboard.py        # Web-based visualization using Dash
│── traffic_data.csv    # Stores logged traffic data
│── requirements.txt    # Python dependencies
│── README.md           # This file
│── dist/               # Folder containing the executable
```

---

Troubleshooting
- SUMO not found? Ensure `SUMO_HOME` is correctly set.
- .exe flagged as a virus? Add an exclusion in Windows Defender.
- PyInstaller issues? Try reinstalling:
  ```bash
  pip install --upgrade pyinstaller
  ```
- GUI not updating? Check logs for errors and restart the application.

---


