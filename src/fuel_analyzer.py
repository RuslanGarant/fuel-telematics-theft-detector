import time

class FuelTheftDetector:
    def __init__(self, theft_threshold=15.0, window_size=3):
        self.THEFT_THRESHOLD = theft_threshold  # Liters dropped to trigger theft alert
        self.WINDOW_SIZE = window_size
        self.fuel_history = []

    def moving_average_filter(self, new_reading):
        """Filters fuel sloshing noise caused by vehicle movement"""
        self.fuel_history.append(new_reading)
        if len(self.fuel_history) > self.WINDOW_SIZE:
            self.fuel_history.pop(0)
        return sum(self.fuel_history) / len(self.fuel_history)

    def analyze_fuel_stream(self, data_stream):
        print("[SYSTEM] Starting Fuel Telematics Analytics Engine...")
        previous_filtered_level = None

        for record in data_stream:
            timestamp = record["timestamp"]
            raw_level = record["fuel_level"]
            ignition_on = record["ignition"]

            # Smooth out the sensor noise (sloshing)
            filtered_level = self.moving_average_filter(raw_level)
            
            if previous_filtered_level is not None:
                fuel_drop = previous_filtered_level - filtered_level
                
                # If ignition is OFF and fuel level drops rapidly, trigger theft alarm
                if not ignition_on and fuel_drop >= self.THEFT_THRESHOLD:
                    print(f"[CRITICAL ALERT | {timestamp}] Sudden fuel drop of {fuel_drop:.1f}L detected while ignition is OFF! Possible FUEL THEFT in progress.")
                    print(f"  Raw Sensor Input: {raw_level}L | Filtered State: {filtered_level:.1f}L")
                elif fuel_drop >= self.THEFT_THRESHOLD:
                    print(f"[FLEET NOTICE | {timestamp}] High fuel consumption detected ({fuel_drop:.1f}L drop). Vehicle is driving under heavy load.")

            previous_filtered_level = filtered_level
            time.sleep(0.1)

if __name__ == "__main__":
    # Simulated IoT Telematics Stream from Fuel Level Sensor (FLS) via CAN-bus / GPS Tracker
    simulated_telematics_data = [
        {"timestamp": "01:00:00", "fuel_level": 300.5, "ignition": True},
        {"timestamp": "01:00:10", "fuel_level": 298.2, "ignition": True},  # Minor sloshing / consumption
        {"timestamp": "01:00:20", "fuel_level": 302.1, "ignition": True},  # Sloshing upward on a hill
        {"timestamp": "01:01:00", "fuel_level": 295.0, "ignition": False}, # Vehicle stops, engine OFF
        {"timestamp": "01:01:10", "fuel_level": 295.1, "ignition": False}, # Stable stop
        {"timestamp": "01:01:20", "fuel_level": 260.0, "ignition": False}, # Suddent drop! (Fuel Theft Event)
        {"timestamp": "01:01:30", "fuel_level": 230.0, "ignition": False}, # Theft continues
    ]

    detector = FuelTheftDetector(theft_threshold=10.0, window_size=3)
    detector.analyze_fuel_stream(simulated_telematics_data)
