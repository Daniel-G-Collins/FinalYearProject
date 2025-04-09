from swarm import swarm
import searchDomain
from bounds import Bounds
import sys
import pandas as pd
import numpy as np  # For mean and std calculations

def evaluate(domains, domainDict):
    types = "Standard", "Constricted"
    topologies = "Global", "Ring", "VN"
    num_trials = 50  # Number of runs per topology
    
    for p_type in types:
        allResults = []
        for searchDomain in domains:
            results = {
                "Function": searchDomain,
                "Global Final Mean": None,
                "Global Final Std": None,
                "Global PB Mean": None,
                "Global PB Std": None,
                "Ring Final Mean": None,
                "Ring Final Std": None,
                "Ring PB Mean": None,
                "Ring PB Std": None,
                "VN Final Mean": None,
                "VN Final Std": None,
                "VN PB Mean": None,
                "VN PB Std": None
            }
            
            for topology in topologies:
                # Arrays to store results across trials
                final_means = []
                final_stds = []
                pb_means = []
                pb_stds = []
                
                # Run 50 trials for this topology
                for _ in range(num_trials):
                    # Setup swarm
                    s = swarm(
                        domainDict[searchDomain], 
                        searchDomain, 
                        topology, 
                        numParticles=49, 
                        numIterations=100, 
                        pType=p_type
                    )
                    
                    # Run simulation
                    for _ in range(100):  # numIterations = 100
                        s.updateSwarm(topology)
                    
                    # Get results for this trial
                    final_mean, final_std, pb_mean, pb_std = s.getResults(topology)
                    
                    # Store results for averaging later
                    final_means.append(final_mean)
                    final_stds.append(final_std)
                    pb_means.append(pb_mean)
                    pb_stds.append(pb_std)
                
                # Compute mean and std across all trials
                results[f"{topology} Final Mean"] = np.mean(final_means)
                results[f"{topology} Final Std"] = np.std(final_means)
                results[f"{topology} PB Mean"] = np.mean(pb_means)
                results[f"{topology} PB Std"] = np.std(pb_means)
                print(f"Results done for {topology}")
            
            # Append results for this function
            allResults.append(results)
        
        # Save to CSV
        df = pd.DataFrame(allResults)
        filename = f"{p_type}ReportResults.csv"
        df.to_csv(filename, index=False)
        print(f"Results saved to {filename} for \"{p_type}\" particles")
    
    print("Open the files in Excel")

if __name__ == "__main__":
    domains = sys.argv[1:]
    domainDict = searchDomain.calc_dict(domains)
    bounds = Bounds()
    evaluate(domains, domainDict)