from swarm import swarm
import searchDomain
from bounds import Bounds
import sys
import pandas as pd


def evaluate(domains, domainDict):
    #allResults = []
    types = "Standard" , "StandardWithDampeningFactor"
    topologies = "Global", "Ring", "VN"
    for type in types:
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
                    
                    s = swarm(domainDict[searchDomain], searchDomain, topology, numParticles=100, numIterations=numIterations, pType=type)
                    
                    #run simulation
                    for _ in range(numIterations):
                        s.updateSwarm(topology)
                    
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
        filename = f"{type}Results.csv"
        df.to_csv(filename, index=False)
        print(f"Results saved to {filename} for \"{type}\" particles")
    print("Open the files in Excel")

    

domains = sys.argv[1:]
#pType = sys.argv[1]
#print(f"Domains: {domains}")
domainDict = searchDomain.calc_dict(domains)
bounds = Bounds()
evaluate(domains,domainDict)
