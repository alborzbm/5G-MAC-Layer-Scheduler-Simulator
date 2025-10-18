import numpy as np
import config
from traffic import UserQueue, TrafficGenerator
from channel import ChannelModel
from metrics import SimulationMetrics

class Simulator:
    def __init__(self, scheduler_class):
        self.n_users = config.N_USERS
        self.total_ttis = int(config.SIMULATION_TIME_MS / config.TTI_MS)
        
        self.scheduler = scheduler_class(self.n_users)
        self.channel = ChannelModel(self.n_users)
        self.traffic_gen = TrafficGenerator(self.n_users)
        self.user_queues = [UserQueue(i) for i in range(self.n_users)]
        self.metrics = SimulationMetrics(self.n_users)
    
    def run(self):
        print(f"  Running simulation for: {self.scheduler.name}...")
        
        for tti in range(self.total_ttis):
            
            # This block was fixed (Logic Error)
            # 1. Generate new packet arrivals
            new_packets_count = self.traffic_gen.generate_arrivals(self.user_queues, tti)
            self.metrics.log_arrivals(new_packets_count)
            
            # 2. Check for dropped packets (deadlines)
            for q in self.user_queues:
                dropped = q.check_deadlines(tti)
                self.metrics.log_drops(dropped)
            
            # 3. Get channel conditions
            current_rates_mbits = self.channel.get_achievable_rates(tti)
            
            # 4. Run scheduler
            user_id = self.scheduler.select_user(current_rates_mbits, self.user_queues)
            
            data_sent_mbits = 0.0
            
            # 5. Service the selected user
            if user_id is not None:
                data_capacity = current_rates_mbits[user_id]
                served_packets_info, data_sent_mbits = self.user_queues[user_id].service_data(
                    data_capacity, tti
                )
                
                self.metrics.log_transmission(user_id, data_sent_mbits, served_packets_info)

            # 6. Update scheduler state (e.g., for PF)
            self.scheduler.update_state(user_id, data_sent_mbits)
            
        return self.metrics.get_final_results(config.SIMULATION_TIME_MS)