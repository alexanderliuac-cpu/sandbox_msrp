import datetime

class CarAppraisal:
    def __init__(self, make, model, year, trim, msrp, current_mileage):
        self.make = make
        self.model = model
        self.year = year
        self.trim = trim
        self.msrp = msrp
        self.mileage = current_mileage
        
        # MARKET REALITY FACTORS (The "Hidden" variables)
        # Standard cars depreciate ~15-20% year one.
        # Luxury EVs (like RZ450e) are currently hitting ~30-40% due to Tesla price cuts/inventory.
        self.market_depreciation_rates = {
            "Standard": 0.15,
            "Luxury_Gas": 0.20,
            "Luxury_EV": 0.38,  # The "Real" number for RZ/Mirai right now
            "Toyota_Hybrid": 0.10 # Holds value well
        }

    def calculate_value(self, category="Luxury_EV"):
        # 1. Age Calculation
        current_year = datetime.datetime.now().year
        # Add 1 year if it's a "last year" model to account for immediate drive-off drop
        age = max(1, current_year - self.year) 
        
        # 2. Base Depreciation (The "Market" Hit)
        depreciation_rate = self.market_depreciation_rates.get(category, 0.20)
        # Compounding depreciation formula: Value = MSRP * ((1 - rate) ^ age)
        base_residual_value = self.msrp * ((1 - depreciation_rate) ** age)
        
        # 3. Mileage Penalty
        # Standard lease allowance is usually 10k-12k miles/year.
        # Excess mileage is usually penalized at $0.25/mile.
        standard_miles = 10000 * age
        excess_miles = max(0, self.mileage - standard_miles)
        mileage_penalty = excess_miles * 0.25
        
        # 4. "Real" Trade-In Value (Wholesale)
        # Dealers typically pay 10-15% UNDER the retail residual to make profit.
        dealer_margin = 0.12
        trade_in_value = (base_residual_value - mileage_penalty) * (1 - dealer_margin)
        
        return int(trade_in_value)

# --- USER INPUT AREA ---

# Your Specific Car Logic
my_car = CarAppraisal(
    make="Lexus",
    model="RZ 450e",
    year=2023,
    trim="Luxury",
    msrp=64000,          # Approx original MSRP for Luxury trim
    current_mileage=12500
)

# Run the Scenarios
print(f"--- Appraisal for {my_car.year} {my_car.make} {my_car.model} ---")

# Scenario A: The "Fantasy" Book Value (Standard Depreciation)
fantasy_value = my_car.calculate_value(category="Standard")
print(f"Fantasy Book Value (Standard Market): ${fantasy_value}")

# Scenario B: The "Real" Market (EV Crash)
real_value = my_car.calculate_value(category="Luxury_EV")
print(f"Realistic Trade-In Floor (EV Market): ${real_value}")

# Logic Check against your Carvana Offer
print(f"\nvs Your Carvana Offer: $29,600")
diff = real_value - 29600
if diff < 0:
    print(f"Carvana is OVERPAYING by ${abs(diff)}")
else:
    print(f"Carvana is UNDERPAYING by ${diff}")
