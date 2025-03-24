from swarm import swarm
import searchDomain
from bounds import Bounds
import sys
import pandas as pd


def evaluate(domains, domainDict):
    #allResults = []
    types = "Standard" , "StandardWithDampeningFactor"
    for type in types:
        allResults = []
        for searchDomain in domains:
            results = {
                "Function": [],
                "PSO Mean": [],
                "PSO Std": [],
                "Global Mean": [],
                "Global Std": [],
                "Ring Mean": [],
                "Ring Std": [],
                "VN Mean": [],
                "VN Std": []
            }

            results["Function"].append(searchDomain)
            numIterations = 100
            s = swarm(domainDict[searchDomain], searchDomain, numParticles=400, numIterations=numIterations, pType=type)
            for _ in range(numIterations):
                s.updateSwarm()
            
            mean, std, globalMean, globalStd, ringMean, ringStd, VNMean, VNStd = s.getResults()
            if searchDomain == "Weierstrass" and type == "Standard":
                print(f"global mean in evaluate(): {ringMean}")
            
            results["PSO Mean"].append(mean)
            results["PSO Std"].append(std)
            results["Global Mean"].append(globalMean)
            results["Global Std"].append(globalStd)
            results["Ring Mean"].append(ringMean)
            if searchDomain == "Weierstrass" and type == "Standard":
                print(f"ring mean in evaluate(): {results['Ring Mean']}")
            results["Ring Std"].append(ringStd)
            results["VN Mean"].append(VNMean)
            results["VN Std"].append(VNStd)


            allResults.append(results)

        df = pd.concat([pd.DataFrame(result) for result in allResults], ignore_index=True)
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
