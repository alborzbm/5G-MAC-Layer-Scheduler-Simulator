import numpy as np
import config

class SchedulerBase:
    def __init__(self, n_users):
        self.n_users = n_users
        self.name = "SchedulerBase"
    
    def select_user(self, current_rates, user_queues):
        # Base method, should be overridden
        raise NotImplementedError
    
    def update_state(self, scheduled_user, data_sent_mbits):
        # Used by schedulers that need state (like PF)
        pass

class RoundRobin(SchedulerBase):
    def __init__(self, n_users):
        super().__init__(n_users)
        self.name = "RoundRobin"
        self.next_user = 0
    
    def select_user(self, current_rates, user_queues):
        start_user = self.next_user
        for i in range(self.n_users):
            user_to_check = (start_user + i) % self.n_users
            if not user_queues[user_to_check].is_empty():
                self.next_user = (user_to_check + 1) % self.n_users
                return user_to_check
        
        # No user has data
        self.next_user = (start_user + 1) % self.n_users
        return None

class MaxRate(SchedulerBase):
    def __init__(self, n_users):
        super().__init__(n_users)
        self.name = "MaxRate"

    def select_user(self, current_rates, user_queues):
        best_rate = -1
        best_user = None
        
        for i in range(self.n_users):
            if not user_queues[i].is_empty() and current_rates[i] > best_rate:
                best_rate = current_rates[i]
                best_user = i
                
        return best_user

class ProportionalFair(SchedulerBase):
    def __init__(self, n_users):
        super().__init__(n_users)
        self.name = "ProportionalFair"
        self.avg_throughput = np.ones(n_users) # Initialize to 1 to avoid div by zero
        self.alpha = config.PF_ALPHA
    
    def select_user(self, current_rates, user_queues):
        best_metric = -1
        best_user = None
        
        pf_metrics = current_rates / self.avg_throughput
        
        for i in range(self.n_users):
            if not user_queues[i].is_empty() and pf_metrics[i] > best_metric:
                best_metric = pf_metrics[i]
                best_user = i
        
        return best_user

    def update_state(self, scheduled_user, data_sent_mbits):
        # Update all users (decay)
        self.avg_throughput *= (1 - self.alpha)
        
        # Update the scheduled user (growth)
        if scheduled_user is not None:
            self.avg_throughput[scheduled_user] += self.alpha * data_sent_mbits

class EarliestDeadlineFirst(SchedulerBase):
    def __init__(self, n_users):
        super().__init__(n_users)
        self.name = "EarliestDeadlineFirst"

    def select_user(self, current_rates, user_queues):
        best_user = None
        earliest_deadline = float('inf')
        
        for i in range(self.n_users):
            packet = user_queues[i].peek()
            if packet and packet.deadline_tti < earliest_deadline:
                earliest_deadline = packet.deadline_tti
                best_user = i
        
        return best_user