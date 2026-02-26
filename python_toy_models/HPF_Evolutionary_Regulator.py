"""
HPF Module: Evolutionary Regulator
================================================================================
File:   HPF_Evolutionary_Regulator.py
Author: Eric Keaton Porter
Date:   2026
Context: Unified Holographic Emergence Theory (UHET)

## Purpose
To test the hypothesis that "Measurement" (Renormalization) is an emergent 
survival strategy, not a fundamental axiom.

## Experiment
1. Environment: High Entropic Flux (Sf=100.0).
2. Agents: Simple mathematical kernels with mutable 'Genome' for signal processing.
   - Gene[0] (Center_Bias): How much of the local mean to subtract?
   - Gene[1] (Scale_Damp):  How strongly to divide by local variance?
3. Selection Pressure: "Geometric Stability"
   - Death Condition A: Signal Collapse (Variance -> 0)
   - Death Condition B: Saturation (Values hit +/- Infinity or NaN)
   
## Prediction
If the hypothesis holds, the population will converge on:
   - Center_Bias -> 1.0 (Full Mean Subtraction)
   - Scale_Damp  -> 1.0 (Full Standard Deviation Division)
   
   i.e., The agents will "invent" LayerNorm to survive.
"""

import random
import statistics
import math
import copy

# --- CONFIGURATION ---
POPULATION_SIZE = 100
GENERATIONS = 50
FLUX_MAGNITUDE = 100.0  # The "Heat Death" scenario from Phase II
INPUT_DIM = 20

class KernelAgent:
    def __init__(self, id_tag, genome=None):
        self.id = id_tag
        if genome:
            self.genome = genome
        else:
            # Random initialization
            # gene[0]: Centering Factor (0.0 = don't shift, 1.0 = subtract mean)
            # gene[1]: Scaling Factor (0.0 = static gain, 1.0 = divide by std_dev)
            self.genome = [random.uniform(-0.5, 1.5), random.uniform(-0.5, 1.5)]
        
        self.fitness = 0.0

    def process(self, signal_vector):
        """
        Apply the agent's 'Physics' to the input signal.
        Formula: Out = (In - (Mean * Gene0)) / ( (StdDev * Gene1) + epsilon )
        """
        try:
            local_mean = statistics.mean(signal_vector)
            local_stdev = statistics.pstdev(signal_vector)
            
            # The Agent's unique transformation logic
            bias_term = local_mean * self.genome[0]
            scale_term = (local_stdev * self.genome[1])
            
            # Protection against divide-by-zero for the simulation's sake,
            # though in physics this would just be a singularity (Death).
            if abs(scale_term) < 1e-9: 
                scale_term = 1.0 # Default to unity gain if gene is effectively zero

            output = []
            for x in signal_vector:
                # Apply the transformation
                val = (x - bias_term) / abs(scale_term)
                output.append(val)
            
            return output

        except Exception:
            return [0.0] * len(signal_vector)

def evaluate_fitness(agent):
    """
    Fitness = Stability.
    Can the agent keep the signal 'alive' (measurable) without exploding?
    Target: Output signal should have variance ~1.0 (Unit Normal).
    """
    # Generate random High-Entropy Input (The "Chaos")
    # Mean is drifting, Variance is huge (Sf=100)
    drift = random.uniform(-500, 500)
    input_signal = [random.gauss(drift, FLUX_MAGNITUDE) for _ in range(INPUT_DIM)]
    
    output = agent.process(input_signal)
    
    try:
        out_mean = statistics.mean(output)
        out_std = statistics.pstdev(output)
        
        # CRITERIA 1: Centering (Avoid Saturation Bias)
        # We want the mean to stay near 0.
        score_center = 1.0 / (1.0 + abs(out_mean))
        
        # CRITERIA 2: Scaling (Avoid Collapse or Explosion)
        # We want std_dev to be close to 1.0 (The "Sweet Spot" of existence)
        # If std < 0.1, signal is dead. If std > 10, signal saturates.
        score_scale = 1.0 / (1.0 + abs(out_std - 1.0))
        
        # Combined Fitness
        return score_center * score_scale

    except:
        return 0.0

def mutate(genome):
    """Apply random mutations to the 'physics' constants."""
    mutation_rate = 0.1
    new_genome = copy.deepcopy(genome)
    
    # Mutate Centering
    if random.random() < 0.3:
        new_genome[0] += random.gauss(0, mutation_rate)
        
    # Mutate Scaling
    if random.random() < 0.3:
        new_genome[1] += random.gauss(0, mutation_rate)
        
    return new_genome

def run_evolution():
    print(f"--- HPF EVOLUTIONARY REGULATOR ---")
    print(f"Goal: Survive Flux Sf={FLUX_MAGNITUDE}")
    print(f"Hypothesis: Agents will invent 'Renormalization' (Genome -> [1.0, 1.0])")
    print("-" * 60)
    
    population = [KernelAgent(i) for i in range(POPULATION_SIZE)]
    
    for gen in range(GENERATIONS):
        # 1. Evaluate
        scores = []
        for agent in population:
            agent.fitness = evaluate_fitness(agent)
            scores.append(agent.fitness)
        
        # Statistics for this generation
        avg_score = statistics.mean(scores)
        best_agent = max(population, key=lambda a: a.fitness)
        
        # Visual logging every 10 gens
        if gen % 10 == 0 or gen == GENERATIONS - 1:
            g_center = best_agent.genome[0]
            g_scale = best_agent.genome[1]
            print(f"Gen {gen:<3} | Best Fitness: {best_agent.fitness:.4f} | "
                  f"Strategy: SubMean*{g_center:.2f}, DivStd*{g_scale:.2f}")

        # 2. Selection (Survival of the Fittest)
        # Keep top 20%
        sorted_pop = sorted(population, key=lambda a: a.fitness, reverse=True)
        survivors = sorted_pop[:int(POPULATION_SIZE * 0.2)]
        
        # 3. Reproduction
        new_pop = []
        while len(new_pop) < POPULATION_SIZE:
            parent = random.choice(survivors)
            child_genome = mutate(parent.genome)
            new_pop.append(KernelAgent(len(new_pop), child_genome))
            
        population = new_pop

    print("-" * 60)
    print("RESULT ANALYSIS:")
    
    final_best = max(population, key=lambda a: a.fitness)
    c_gene = final_best.genome[0]
    s_gene = final_best.genome[1]
    
    print(f"Final Converged Strategy:")
    print(f"  > Mean Subtraction Factor: {c_gene:.4f} (Expected ~1.0)")
    print(f"  > Variance Division Factor: {s_gene:.4f} (Expected ~1.0)")
    
    if 0.9 < c_gene < 1.1 and 0.9 < s_gene < 1.1:
        print("\n>> CONCLUSION: VERIFIED.")
        print("   The population independently discovered Renormalization")
        print("   as the optimal survival strategy against high entropy.")
        print("   'Measurement' is an emergent property of stability.")
    else:
        print("\n>> CONCLUSION: INCONCLUSIVE / DIVERGENT.")

if __name__ == "__main__":
    run_evolution()
