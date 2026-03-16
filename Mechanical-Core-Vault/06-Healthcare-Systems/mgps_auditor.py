import csv
from datetime import datetime

class MGPSAuditor:
    """
    Hospital Medical Gas Pipeline System (MGPS) - Operational Auditor
    Designed by: Syed Hilaluddin Madany
    Logic: HTM 02-01 / JCI Standards (1+1 Redundancy)
    """

    def __init__(self, hospital_name, capacity_liters=11000):
        # Engineering Constants
        self.hospital_name = hospital_name
        self.capacity = capacity_liters
        self.expansion_ratio = 860  # LOX Liquid to Gas Ratio
        self.readings = []

    def add_reading(self, date_str, tank1_pct, tank2_pct, duty_tank="Tank 1"):
        """
        Ingests daily DOT panel readings.
        duty_tank: The tank currently connected to the hospital line.
        """
        self.readings.append({
            "date": date_str,
            "t1": float(tank1_pct),
            "t2": float(tank2_pct),
            "duty": duty_tank
        })

    def process_audit(self, filename="MGPS_Audit_Report.csv"):
        """
        Applies 80/40/20 Safety Logic and calculates Volumetric Consumption.
        """
        # Sort readings by date
        self.readings.sort(key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"))
        
        headers = ["Date", "Duty Tank", "T1 %", "T2 %", "Daily Cons (L)", "Gas Yield (m3)", "Alarm Status"]
        rows = []
        total_liquid_consumed = 0

        for i in range(len(self.readings)):
            curr = self.readings[i]
            daily_l = 0
            
            # 1. Differential Logic: Compare current day to previous day
            if i > 0:
                prev = self.readings[i-1]
                # Combined system drop logic to handle 1+1 tank switching
                pct_drop = (prev['t1'] + prev['t2']) - (curr['t1'] + curr['t2'])
                if pct_drop > 0:
                    daily_l = (pct_drop / 100) * self.capacity
            
            # 2. Safety Threshold Logic (40/20 Rule)
            active_level = curr['t1'] if curr['duty'] == "Tank 1" else curr['t2']
            if active_level <= 20:
                status = "🚨 CRITICAL REFILL"
            elif active_level <= 40:
                status = "⚠️ LOW ALARM"
            elif active_level > 80:
                status = "ℹ️ ABOVE SOF"
            else:
                status = "✅ NORMAL"

            gas_m3 = (daily_l * self.expansion_ratio) / 1000
            total_liquid_consumed += daily_l
            
            rows.append([
                curr['date'], curr['duty'], curr['t1'], curr['t2'],
                round(daily_l, 2), round(gas_m3, 2), status
            ])

        # 3. Professional CSV Export
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"AUDIT REPORT: {self.hospital_name}"])
            writer.writerow([f"Capacity: {self.capacity}L | Expansion: 1:{self.expansion_ratio}"])
            writer.writerow([])
            writer.writerow(headers)
            writer.writerows(rows)
            writer.writerow([])
            writer.writerow(["SUMMARY", "", "", "TOTAL:", round(total_liquid_consumed, 2), round((total_liquid_consumed * 860)/1000, 2)])

        print(f"✅ Audit Complete. Report saved to: {filename}")

# --- EXECUTION (Example for Github Demo) ---
if __name__ == "__main__":
    # Simulate a 1+1 Duty/Standby Operation
    auditor = MGPSAuditor("International Medical Center", 11000)
    
    auditor.add_reading("2026-03-01", 80.0, 80.0, "Tank 1")
    auditor.add_reading("2026-03-02", 78.5, 80.0, "Tank 1")
    auditor.add_reading("2026-03-15", 40.0, 80.0, "Tank 1") # Hits 40% Low Alarm
    auditor.add_reading("2026-03-16", 40.0, 78.2, "Tank 2") # Switch to Standby Logic
    
    auditor.process_audit()
