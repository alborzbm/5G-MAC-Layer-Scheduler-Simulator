import numpy as np
import config

class SimulationMetrics:
    def __init__(self, n_users):
        self.n_users = n_users
        self.total_data_served_mbits = np.zeros(n_users)
        self.packet_delays = []
        self.total_packets_generated = 0
        self.total_packets_dropped = 0
    
    def log_transmission(self, user_id, data_mbits, served_packets_info):
        self.total_data_served_mbits[user_id] += data_mbits
        for packet, delay in served_packets_info:
            self.packet_delays.append(delay)
    
    def log_arrivals(self, num_new_packets):
        self.total_packets_generated += num_new_packets
        
    def log_drops(self, dropped_packets):
        self.total_packets_dropped += len(dropped_packets)

    def jains_fairness_index(self):
        if np.sum(self.total_data_served_mbits) == 0:
            return 0.0
        
        sum_T = np.sum(self.total_data_served_mbits)
        sum_T_squared = np.sum(self.total_data_served_mbits**2)
        N = self.n_users
        
        return (sum_T**2) / (N * sum_T_squared)
    
    def get_final_results(self, sim_duration_ms):
        total_throughput_mbps = (np.sum(self.total_data_served_mbits) * 1000.0) / sim_duration_ms
        
        if self.total_packets_generated == 0:
            packet_drop_rate = 0.0
        else:
            packet_drop_rate = self.total_packets_dropped / self.total_packets_generated
        
        if not self.packet_delays:
            avg_packet_delay_ms = 0.0
        else:
            avg_packet_delay_ms = np.mean(self.packet_delays) * config.TTI_MS
            
        results = {
            "total_throughput_mbps": total_throughput_mbps,
            "jains_fairness": self.jains_fairness_index(),
            "avg_packet_delay_ms": avg_packet_delay_ms,
            "packet_drop_rate": packet_drop_rate,
            "per_user_throughput": self.total_data_served_mbits,
            "all_packet_delays_tti": self.packet_delays
        }
        return results