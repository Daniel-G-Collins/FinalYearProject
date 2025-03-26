import sys
import searchDomain
import os
import pandas as pd
import numpy as np
from bounds import Bounds
from swarm import Swarm

def evaluate(domains, domainDict):
    all_results = []
    
    for searchDomain in domains:
        #results dictionary
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
        
        #Setup and run PSO
        numIterations = 100
        bounds = Bounds()
        functionBounds = bounds.getBounds(searchDomain)
        s = Swarm(domainDict[searchDomain], functionBounds, 2, num_particles=400, max_iter=numIterations)
        
        # Run iterations
        for _ in range(numIterations):
            s.updateSwarm()
        
        #results
        final_mean, final_std, pb_mean, pb_std,ring_final_mean, ring_final_std, ring_pb_mean, ring_pb_std,VN_final_mean, VN_final_std, VN_pb_mean, VN_pb_std = s.getResults()
        
        #populate dictioonary
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

        all_results.append(results)

    filename = os.path.join(f'dms_repro_evaluation.csv')

    df = pd.DataFrame(all_results)
    df.to_csv(filename, index=False)
    
    print(f"Results written to {filename}")

domains = sys.argv[1:]
#pType = sys.argv[1]
#print(f"Domains: {domains}")
domainDict = searchDomain.calc_dict(domains)
bounds = Bounds()
evaluate(domains,domainDict)