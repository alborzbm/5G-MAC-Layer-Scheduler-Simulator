import numpy as np
from collections import deque, namedtuple
import config

# A simple Packet data structure
Packet = namedtuple('Packet', ['id', 'size_bits', 'arrival_tti', 'deadline_tti'])
packet_counter = 0

class UserQueue:
    def __init__(self, user_id):
        self.user_id = user_id
        self.buffer = deque()
    
    def add_packet(self, packet):
        self.buffer.append(packet)
    
    def is_empty(self):
        return len(self.buffer) == 0
    
    def peek(self):
        return self.buffer[0] if not self.is_empty() else None
        
    def check_deadlines(self, current_tti):
        dropped_packets = []
        while not self.is_empty() and self.buffer[0].deadline_tti < current_tti:
            dropped_packets.append(self.buffer.popleft())
        return dropped_packets

    def service_data(self, data_capacity_mbits, current_tti):
        data_served_bits = 0
        packets_served = []
        
        data_capacity_bits = data_capacity_mbits * 1_000_000
        
        while not self.is_empty() and data_served_bits < data_capacity_bits:
            packet = self.buffer.popleft()
            data_served_bits += packet.size_bits
            
            delay = current_tti - packet.arrival_tti
            packets_served.append((packet, delay))
            
        return packets_served, data_served_bits / 1_000_000 # Return Mbits

class TrafficGenerator:
    def __init__(self, n_users):
        self.n_users = n_users
        
        # Probability of a packet arrival per user per TTI
        self.arrival_prob = config.PACKET_ARRIVAL_RATE_PPS * (config.TTI_MS / 1000.0)
        self.deadline_ttis = config.PACKET_DEADLINE_MS / config.TTI_MS

    def generate_arrivals(self, queues, current_tti):
        global packet_counter
        
        # Use Poisson process for arrivals
        num_arrivals_per_user = np.random.poisson(self.arrival_prob, self.n_users)
        
        # This function was fixed (Logic Error)
        total_new_packets = 0 
        
        for user_id in range(self.n_users):
            for _ in range(num_arrivals_per_user[user_id]):
                new_packet = Packet(
                    id=packet_counter,
                    size_bits=config.PACKET_SIZE_BITS,
                    arrival_tti=current_tti,
                    deadline_tti=current_tti + self.deadline_ttis
                )
                queues[user_id].add_packet(new_packet)
                packet_counter += 1
                total_new_packets += 1 
        
        return total_new_packets