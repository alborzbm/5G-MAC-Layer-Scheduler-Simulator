import numpy as np
import config
import plotting
from simulation import Simulator
from schedulers import RoundRobin, MaxRate, ProportionalFair, EarliestDeadlineFirst

def run_all_simulations():
    
    # List of scheduler classes to test
    scheduler_classes_to_run = [
        RoundRobin,
        MaxRate,
        ProportionalFair,
        EarliestDeadlineFirst
    ]
    
    all_results = {}
    
    print("--- Starting 5G MAC Scheduler Simulation ---")
    print(f"Config: {config.N_USERS} Users, {config.SIMULATION_TIME_MS} ms Simulation Time")
    
    for sched_class in scheduler_classes_to_run:
        # We need a fresh seed for each run to ensure fair comparison
        # (i.e., all schedulers face the same channel and traffic)
        np.random.seed(42)
        
        sim = Simulator(sched_class)
        results = sim.run()
        all_results[sim.scheduler.name] = results
        print(f"  Finished: {sim.scheduler.name}")
        print(f"    -> Throughput: {results['total_throughput_mbps']:.2f} Mbps")
        print(f"    -> Fairness:   {results['jains_fairness']:.4f}")
        print(f"    -> Avg Delay:  {results['avg_packet_delay_ms']:.2f} ms")
        print(f"    -> Drop Rate:  {results['packet_drop_rate'] * 100:.2f} %")

    print("\n--- All Simulations Complete ---")
    
    return all_results

def generate_plots(all_results):
    print("\n--- Generating Plots ---")
    plotting.plot_throughput_fairness(all_results)
    plotting.plot_throughput_pdr(all_results)
    plotting.plot_user_throughput_distribution(all_results)
    plotting.plot_delay_cdf(all_results)
    print("--- All Plots Generated ---")

if __name__ == "__main__":
    final_results = run_all_simulations()
    generate_plots(final_results)