import numpy as np
import config

class ChannelModel:
    def __init__(self, n_users):
        self.n_users = n_users
        self.n_rbs = config.N_RBS
        
        # Power per RB in dBm
        self.power_per_rb_dbm = config.BASE_TX_POWER_DBM - 10 * np.log10(config.N_RBS)
        
        # Pre-calculate pathloss (PL) and shadowing for each user
        shadowing_db = np.random.normal(0, config.SHADOWING_STD_DEV_DB, n_users)
        self.user_pathloss_db = config.MEAN_PATHLOSS_DB + shadowing_db
        
        # Pre-generate fast fading samples (Rayleigh)
        # Power values, hence exponential distribution (amplitude is Rayleigh)
        self.fading_samples = np.random.exponential(
            scale=1.0, 
            size=(n_users, config.FAST_FADING_SAMPLES)
        )
        self.fading_index = np.zeros(n_users, dtype=int)

    def get_achievable_rates(self, tti_index):
        # Calculate received power in dBm
        rx_power_dbm = self.power_per_rb_dbm - self.user_pathloss_db
        
        # Get fast fading for this TTI
        fading_db = 10 * np.log10(self.fading_samples[
            range(self.n_users), self.fading_index
        ])
        
        # Update indices for next TTI
        self.fading_index = (self.fading_index + 1) % config.FAST_FADING_SAMPLES
        
        # Calculate SINR in linear scale
        signal_power_linear = 10**((rx_power_dbm + fading_db) / 10)
        noise_power_linear = 10**(config.TOTAL_NOISE_POWER_DBM / 10)
        sinr_linear = signal_power_linear / noise_power_linear
        
        # Calculate achievable rate using Shannon capacity (per RB)
        # R = B * log2(1 + SINR)
        rate_per_rb_bps = config.BANDWIDTH_PER_RB_HZ * np.log2(1 + sinr_linear)
        
        # Total rate if all RBs are allocated to this user
        total_rate_bps = rate_per_rb_bps * self.n_rbs
        
        # Convert to Mbits per TTI
        rate_mbps_per_tti = (total_rate_bps * (config.TTI_MS / 1000.0)) / 1_000_000
        
        return rate_mbps_per_tti