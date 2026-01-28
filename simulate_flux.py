"""
Holographic Projection Framework (HPF) - Flux Saturation Simulation
Author: [Your Name/Handle]
License: MIT


Description:
This script simulates the flow of information packets across a 1D discrete lattice
approaching a horizon proxy. It demonstrates the "Shadow Floor" effect where
finite bandwidth at the horizon forces a non-zero reflection (jitter) of 
incident information flux.


Theoretical Basis:
- Axiom I: Finite Resolution (Lattice limit)
- Axiom II: Reversible Updates (Bijective dynamics)
- Axiom III: Saturation (Bandwidth caps)


Usage:
    python simulate_flux.py
"""


import random
import time


def run_hpf_simulation_v2():
    print("--- HPF Simulation: Horizon Saturation Protocol ---")
    print("Initializing Discrete Lattice...")
    
    # --- SIMULATION PARAMETERS ---
    # STEPS: How long we run the universe.
    STEPS = 500             
    
    # LATTICE_SIZE: Radial distance to the Black Hole.
    LATTICE_SIZE = 15       
    
    # SATURATION_LIMIT: (Axiom III) Max bits per voxel. 
    # Lower = Higher "Pressure" to demonstrate the effect.
    SATURATION_LIMIT = 2    
    
    # INPUT_RATE: Accretion rate from the universe.
    INPUT_RATE = 0.9        
    
    # SINK_RATE: The processing speed of the Singularity.
    # If SINK_RATE < INPUT_RATE, a backlog (Shadow) forms.
    SINK_RATE = 0.5         
    
    # The Lattice: A 1D array representing space.
    lattice = [0] * LATTICE_SIZE
    
    # Metrics Storage
    history_flux = []


    print(f"[-] Saturation Limit: {SATURATION_LIMIT} bits/voxel")
    print(f"[-] Input Flux: {INPUT_RATE}")
    print(f"[-] Horizon Sink Rate: {SINK_RATE}")
    print("[-] Starting Reversible Update Cycles...\n")


    # --- MAIN LOOP ---
    for step in range(STEPS):
        
        # metric: Count how many packets are rejected this turn
        current_bounces = 0
        
        # 1. INJECTION (Boundary Condition)
        # Attempt to add new info to the outer edge of the system
        if random.random() < INPUT_RATE:
            if lattice[0] < SATURATION_LIMIT:
                lattice[0] += 1
            else:
                # Boundary is full; immediate rejection
                current_bounces += 1


        # 2. PROPAGATION & SATURATION (Right-to-Left Update)
        # We iterate backwards to move particles toward the sink (index -1)
        for i in range(LATTICE_SIZE - 1, -1, -1):
            if lattice[i] > 0:
                
                # CASE A: THE HORIZON (The Sink)
                if i == LATTICE_SIZE - 1:
                    # The Horizon has finite bandwidth (SINK_RATE).
                    # It cannot delete information instantly.
                    if random.random() < SINK_RATE:
                        lattice[i] -= 1 # Absorbed into singularity
                    else:
                        # Horizon is busy! Packet stalls/reflects.
                        current_bounces += 1 
                
                # CASE B: INTERIOR SPACE
                else:
                    # Try to move to the next voxel (i+1)
                    # CHECK AXIOM III: Is the destination saturated?
                    if lattice[i+1] < SATURATION_LIMIT:
                        lattice[i] -= 1
                        lattice[i+1] += 1
                    else:
                        # TRAFFIC JAM (Bijective Rejection)
                        # The packet cannot move forward, so it stays.
                        # This contributes to the resistive pressure (Shadow Floor).
                        current_bounces += 1


        # 3. DATA LOGGING
        # We record the flux after a warmup period to ignore initial transient states
        if step > 50:
            history_flux.append(current_bounces)


    # --- VISUALIZATION & ANALYSIS ---
    print("[Visualization: Outward Flux / Shadow Intensity]")
    print("Each bar represents reflected information density at time T.")
    
    avg_flux = sum(history_flux)/len(history_flux)
    print(f"\n>> Average Shadow Floor Intensity: {avg_flux:.2f}")


    # Render ASCII Plot of the last 20 steps
    start_index = max(0, len(history_flux) - 20)
    for i in range(start_index, len(history_flux)):
        val = int(history_flux[i])
        # Scaling for visual clarity if numbers are high
        bar_len = val 
        bar = "█" * bar_len
        print(f"T={i+50}: {bar} ({val})")


    # Final Verification Logic
    print("-" * 30)
    if avg_flux > 0:
        print("RESULT: SATURATION CONFIRMED.")
        print("The horizon exhibits a non-zero reflective floor.")
    else:
        print("RESULT: CLASSICAL ABSORPTION.")
        print("No saturation observed (increase input or decrease sink rate).")


if __name__ == "__main__":
    run_hpf_simulation_v2()