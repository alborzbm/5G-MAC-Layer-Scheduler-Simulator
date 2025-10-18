import matplotlib.pyplot as plt
import numpy as np
import os
import config

def save_plot(fig, filename):
    save_dir = config.PLOT_SAVE_DIR
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    fig.savefig(os.path.join(save_dir, filename), bbox_inches='tight')
    print(f"  Plot saved to {os.path.join(save_dir, filename)}")

def plot_throughput_fairness(all_results):
    fig, ax = plt.subplots(figsize=(10, 7))
    
    labels = []
    throughputs = []
    fairness_indices = []
    
    for name, res in all_results.items():
        labels.append(name)
        throughputs.append(res['total_throughput_mbps'])
        fairness_indices.append(res['jains_fairness'])
        
    ax.scatter(throughputs, fairness_indices, s=200, alpha=0.7)
    
    for i, label in enumerate(labels):
        ax.annotate(label, (throughputs[i] + 0.5, fairness_indices[i]), fontsize=12)
        
    ax.set_title('Performance Trade-off: Throughput vs. Fairness', fontsize=16)
    ax.set_xlabel('Total System Throughput (Mbps)', fontsize=14)
    ax.set_ylabel("Jain's Fairness Index", fontsize=14)
    ax.set_ylim(0, 1.05)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    save_plot(fig, 'throughput_vs_fairness.png')
    plt.close(fig)

def plot_throughput_pdr(all_results):
    fig, ax = plt.subplots(figsize=(10, 7))
    
    labels = []
    throughputs = []
    pdrs = []
    
    for name, res in all_results.items():
        labels.append(name)
        throughputs.append(res['total_throughput_mbps'])
        pdrs.append(res['packet_drop_rate'] * 100) # As percentage
        
    ax.scatter(throughputs, pdrs, s=200, alpha=0.7, c='red')
    
    for i, label in enumerate(labels):
        ax.annotate(label, (throughputs[i] + 0.5, pdrs[i]), fontsize=12)
        
    ax.set_title('Performance Trade-off: Throughput vs. Reliability', fontsize=16)
    ax.set_xlabel('Total System Throughput (Mbps)', fontsize=14)
    ax.set_ylabel("Packet Drop Rate (%)", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    save_plot(fig, 'throughput_vs_pdr.png')
    plt.close(fig)

def plot_user_throughput_distribution(all_results):
    sched_names = list(all_results.keys())
    n_scheds = len(sched_names)
    n_users = config.N_USERS
    
    fig, axes = plt.subplots(n_scheds, 1, figsize=(12, n_scheds * 4), sharex=True)
    if n_scheds == 1: axes = [axes] # Make it iterable
    
    for ax, name in zip(axes, sched_names):
        user_data = all_results[name]['per_user_throughput']
        user_indices = np.arange(n_users)
        ax.bar(user_indices, user_data)
        ax.set_title(f'Per-User Throughput Distribution: {name}', fontsize=14)
        ax.set_ylabel('Total Data (Mbits)')
        ax.set_xticks(user_indices)
        ax.set_xticklabels([f'U{i}' for i in user_indices])
    
    axes[-1].set_xlabel('User ID')
    fig.tight_layout()
    save_plot(fig, 'user_throughput_distribution.png')
    plt.close(fig)

def plot_delay_cdf(all_results):
    fig, ax = plt.subplots(figsize=(10, 7))
    
    for name, res in all_results.items():
        delays = res['all_packet_delays_tti']
        if not delays:
            continue
            
        delays_ms = np.array(delays) * config.TTI_MS
        sorted_delays = np.sort(delays_ms)
        cdf = np.arange(1, len(sorted_delays) + 1) / len(sorted_delays)
        
        ax.plot(sorted_delays, cdf, label=name, linewidth=2)
    
    ax.set_title('CDF of Packet Delay', fontsize=16)
    ax.set_xlabel('Packet Delay (ms)', fontsize=14)
    ax.set_ylabel('Cumulative Probability (CDF)', fontsize=14)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(fontsize=12)
    
    save_plot(fig, 'delay_cdf.png')
    plt.close(fig)