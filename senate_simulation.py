import numpy as np

def run_senate_simulation(incumbent_protection_rate, n_simulations=10000):
    # Core baseline seats that are not up for reelection in 2026
    senate_dem_base = 35
    senate_gop_base = 31

    # Active seats up for election with defending incumbents (Total: 32)
    dem_incumbents = 13
    gop_incumbents = 19

    # Highly contested open seats with no active incumbent (Iowa, Ohio, Texas)
    open_seats = 3
    p_open_gop = 0.5  # Equal baseline probability for open battlegrounds

    np.random.seed(42)  # Fixed seed for simulation consistency
    gop_wins_total = 0

    for _ in range(n_simulations):
        # Simulate Democratic incumbent performance
        # If a Democrat fails to defend a seat, it flips to the GOP
        dem_retained = np.random.binomial(dem_incumbents, incumbent_protection_rate)
        gop_flipped = dem_incumbents - dem_retained

        # Simulate Republican incumbent performance
        # If a Republican fails to defend a seat, it flips to the Democrats
        gop_retained = np.random.binomial(gop_incumbents, incumbent_protection_rate)

        # Simulate the outcome of the 3 wide-open battleground seats
        gop_open_wins = np.random.binomial(open_seats, p_open_gop)

        # Sum total expected seats for the Republican Party (GOP)
        total_gop_seats = senate_gop_base + gop_retained + gop_flipped + gop_open_wins

        # GOP needs a strict majority of 51+ seats to maintain control of the Senate
        if total_gop_seats >= 51:
            gop_wins_total += 1

    return (gop_wins_total / n_simulations) * 100

# Defining scenario rates and their corresponding subjective probability weights
scenarios = {
    80: {"rate": 0.80, "weight": 0.25},  # Favorable Democratic wave / Polling error scenario
    85: {"rate": 0.85, "weight": 0.55},  # Realistic consensus / Standard polling dynamic
    90: {"rate": 0.90, "weight": 0.20}   # Historical baseline performance for incumbents
}

print("=== 2026 US SENATE PROBABILISTIC SIMULATION RESULTS ===")
weighted_gop_control_prob = 0.0

for name, data in scenarios.items():
    sim_prob = run_senate_simulation(data["rate"])
    weighted_contribution = sim_prob * data["weight"]
    weighted_gop_control_prob += weighted_contribution
    print(f"Scenario: {name}% Incumbent Protection Rate")
    print(f" -> Raw Probability of GOP Senate Control: {sim_prob:.2f}%")
    print(f" -> Assigned Weight: {data['weight']*100:.0f}% (Contribution: {weighted_contribution:.2f}%)\n")

print("-" * 55)
print(f"FINAL WEIGHTED PROBABILITY OF GOP RETAINING SENATE CONTROL: {weighted_gop_control_prob:.2f}%")
print("-" * 55)
