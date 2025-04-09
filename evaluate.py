from swarm import Swarm
import searchDomain
from bounds import Bounds
import sys
import pandas as pd


def evaluate(domains, domainDict):
    #allResults = []
    topologies = "Global", "Ring", "VN"

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
            #Setup
                numIterations = 100
            #bounds = Bounds()
                bounds = Bounds()
                functionBounds = bounds.getBounds(searchDomain)
                    
                s = Swarm(domainDict[searchDomain], functionBounds, 2, 
                            num_particles=100, max_iter=numIterations, topology=topology)
                
                #run simulation
                for _ in range(numIterations):
                    s.updateSwarm()
                
                #get results
                final_mean, final_std, pb_mean, pb_std = s.getResults(topology)
                
                #add results
                results[f"{topology} Final Mean"] = final_mean
                results[f"{topology} Final Std"] = final_std
                results[f"{topology} PB Mean"] = pb_mean
                results[f"{topology} PB Std"] = pb_std
                
            #append results
            allResults.append(results)

    #csv file based on particle type
    df = pd.DataFrame(allResults)
    filename = f"dms-pso-Results.csv"
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
    print("Open the files in Excel")


domains = sys.argv[1:]
#pType = sys.argv[1]
#print(f"Domains: {domains}")
domainDict = searchDomain.calc_dict(domains)
bounds = Bounds()
evaluate(domains,domainDict)
