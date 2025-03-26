from swarm import swarm
import searchDomain
from bounds import Bounds
import sys
import pandas as pd


def evaluate(domains, domainDict):
    #allResults = []
    types = "Standard" , "StandardWithDampeningFactor"
    for type in types:
        # Prepare a list to collect results from all functions
        allResults = []
        
        for searchDomain in domains:
            # Prepare results dictionary for this specific function
            results = {
                "Function": searchDomain,
                "PSO Final Mean": None,
                "PSO Final Std": None,
                "PSO PB Mean": None,
                "PSO PB Std": None,
                "Ring Final Mean": None,
                "Ring Final Std": None,
                "Ring PB Mean": None,
                "Ring PB Std": None,
                "VN Final Mean": None,
                "VN Final Std": None,
                "VN PB Mean": None,
                "VN PB Std": None
            }
            
            # Setup and run PSO
            numIterations = 100
            bounds = Bounds()
            
            s = swarm(domainDict[searchDomain], searchDomain, numParticles=400, numIterations=numIterations, pType=type)
            
            # Run iterations
            for _ in range(numIterations):
                s.updateSwarm()
            
            # Get results
            final_mean, final_std, pb_mean, pb_std,ring_final_mean, ring_final_std, ring_pb_mean, ring_pb_std,VN_final_mean, VN_final_std, VN_pb_mean, VN_pb_std = s.getResults()
            
            # Populate results
            results["PSO Final Mean"] = final_mean
            results["PSO Final Std"] = final_std
            results["PSO PB Mean"] = pb_mean
            results["PSO PB Std"] = pb_std
            results["Ring Final Mean"] = ring_final_mean
            results["Ring Final Std"] = ring_final_std
            results["Ring PB Mean"] = ring_pb_mean
            results["Ring PB Std"] = ring_pb_std
            results["VN Final Mean"] = VN_final_mean
            results["VN Final Std"] = VN_final_std
            results["VN PB Mean"] = VN_pb_mean
            results["VN PB Std"] = VN_pb_std
            
            # Append to overall results
            allResults.append(results)

        df = pd.DataFrame(allResults)
        filename = f"{type}Results.csv"  # File name based on particle type
        df.to_csv(filename, index=False)
        print(f"Results saved to {filename} for \"{type}\" particles")
    print("Open the files in Excel")

    

domains = sys.argv[1:]
#pType = sys.argv[1]
#print(f"Domains: {domains}")
domainDict = searchDomain.calc_dict(domains)
bounds = Bounds()
evaluate(domains,domainDict)
