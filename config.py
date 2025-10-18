import numpy as np

# --- Simulation Parameters ---
SIMULATION_TIME_MS = 2000  # Total simulation time in milliseconds
TTI_MS = 1.0               # Duration of one time slot (TTI) in milliseconds
N_USERS = 20               # Number of users
N_RBS = 50                 # Number of Resource Blocks (RBs) available

# --- Channel Model Parameters ---
CHANNEL_BANDWIDTH_MHZ = 20
RB_BANDWIDTH_KHZ = 180
BANDWIDTH_PER_RB_HZ = RB_BANDWIDTH_KHZ * 1000
NOISE_POWER_DBM = -174 # Thermal noise in dBm/Hz
NOISE_FIGURE_DB = 5
TOTAL_NOISE_POWER_DBM = NOISE_POWER_DBM + 10 * np.log10(BANDWIDTH_PER_RB_HZ) + NOISE_FIGURE_DB
BASE_TX_POWER_DBM = 46 # gNodeB total transmit power

# Simulate different user distances by assigning different average pathloss
MEAN_PATHLOSS_DB = np.random.uniform(low=70, high=120, size=N_USERS)
SHADOWING_STD_DEV_DB = 8
FAST_FADING_SAMPLES = 10000 # Pre-generate fading samples

# --- Traffic Model Parameters ---
# Poisson arrival process
PACKET_ARRIVAL_RATE_PPS = 500  # Avg packets per second per user
PACKET_SIZE_BITS = 1024 * 8   # Size of one packet in bits
PACKET_DEADLINE_MS = 50       # Packet lifetime in milliseconds

# --- Scheduler Parameters ---
PF_ALPHA = 0.05 # Smoothing factor for Proportional Fair

# --- Plotting Parameters ---
PLOT_SAVE_DIR = "plots"