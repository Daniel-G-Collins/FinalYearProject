import numpy as np

def calc_dict(search_domains):
    
    # intialize search domains
    #search_domains = ["Sphere", "Rosenbrock", "Ackley", "Griewank", "Rastrigin", "Schaffer2D","Griewank10D"]
    #for i in range(1, 26):
    #    search_domains.append("f"+str(i))

    search_domains = tuple(search_domains)
    global domain_dict
    domain_dict = {key: None for key in search_domains}
    global a, b, c
    #set function values for each domain	
    domain_dict["Sphere"] = lambda x, y: x**2 + y**2
    domain_dict["Rosenbrock"] = lambda x, y: (1 - x)**2 + 100 * (y - x**2)**2
    domain_dict["Ackley"] = lambda x, y: -20 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2))) - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + np.e + 20
    domain_dict["Griewank"] = lambda x, y: (x**2 + y**2) / 4000 - np.cos(x) * np.cos(y / np.sqrt(2)) + 1
    domain_dict["Rastrigin"] = lambda x, y: 20 + x**2 + y**2 - 10 * np.cos(2 * np.pi * x) - 10 * np.cos(2 * np.pi * y)
    domain_dict["Schaffer2D"] = lambda x, y: 0.5 + (np.sin(x**2 - y**2)**2 - 0.5) / (1 + 0.001 * (x**2 + y**2))**2

    domain_dict["Shifted Sphere"] = lambda x, y, a=1, b=1: (x - a)**2 + (y - b)**2  # Sphere, shifted by a and b
    
    domain_dict["Shifted Schwefel"] = lambda x, y: abs(x-1) + abs(y-1)  #Schwefel shifted
    domain_dict["Shifted and Rotated Elliptic"] = lambda x, y, z=[1, 2], R=np.eye(2): np.sum(np.dot(R, np.array([x, y]) - z)**2)    # Shifted Rotated Elliptic
    domain_dict["Schwefel shifted with Noise"] = lambda x, y: abs(x-1) + abs(y-1) + (np.random.randn() *0.2) # Schwefel shifted with noise 
    #El-Attar-Vidyasagar-Dutta Function                        100             49              1
    domain_dict["El-Attar-Vidyasagar-Dutta"] = lambda x, y: (x**2 + y - 10)**2 + (x + y**2 - 7)**2 + (x**2 + y**3 - 1)**2    
    #Weierstrass
    a, b, k_max = 0.5, 3, 20
    domain_dict["Weierstrass"] = lambda x, y: sum(
        a**k * np.cos(2 * np.pi * b**k * (x + 0.5)) + 
        a**k * np.cos(2 * np.pi * b**k * (y + 0.5)) 
        for k in range(k_max + 1)
    ) - 2 * sum(a**k * np.cos(2 * np.pi * b**k * 0.5) for k in range(k_max + 1))
    #Shifted Rotated Griewank (without bounds)
    domain_dict["Shifted Rotated Griewank"] = lambda x, y: ((x**2) + (y**2)) / 4000 - np.cos((x-4)*np.cos(np.pi/4)-(y-4)*np.sin(np.pi/4)) * np.cos(((x-4)*np.sin(np.pi/4)+(y-4)*np.cos(np.pi/4)) / np.sqrt(2)) + 1    
    #Shifted Rotated Ackley ----- optimum on bounds already?
    domain_dict["Shifted Rotated Ackley"] = lambda x, y: -20 * np.exp(-0.2 * np.sqrt(0.5 * (((x+1)*np.cos(np.pi/4)-(y+1)*np.sin(np.pi/4))**2 + ((y+1)*np.cos(np.pi/4)+(x+1)*np.sin(np.pi/4))**2))) - np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + np.e + 15
    #Shifted Rastrigin (also down 20)
    domain_dict["Shifted Rastrigin"] = lambda x, y: (x+1)**2 + (y+1)**2 - 10 * np.cos(2 * np.pi * (x+1)) - 10 * np.cos(2 * np.pi * (y+1))
    #Shifted Rotated Rastrigin (also down 20)
    domain_dict["Shifted Rotated Rastrigin"] = lambda x, y: ((x+1)*np.cos(np.pi/4) - (y+1)*np.sin(np.pi/4))**2 + ((y+1)*np.cos(np.pi/4)+ (x+1)*np.sin(np.pi/4))**2 - 10 * np.cos(2 * np.pi * (x+1)) - 10 * np.cos(2 * np.pi * (y+1))
    #Weirstrass shifted and rotated
    domain_dict["Weirstrass shifted and Rotated"] = lambda x, y, N=10: sum(.5**n * (np.cos(3**n * np.pi * ((x+1)*np.cos(np.pi/4)-(y+1)*np.sin(np.pi/4))) + np.cos(3**n * np.pi * ((y+1)*np.cos(np.pi/4)+(x+1)*np.sin(np.pi/4)))) for n in range(N))  
    #Schwefel
    domain_dict["Schwefel"] = lambda x, y: abs(x) + abs(y) 
    #Griewank plus Rosenbrock, amplified and dampened
    domain_dict["Griewank plus Rosenbrock, Amplified and Dampened"] = lambda x, y:  (((x)**2 + (y)**2) / 4000 - np.cos(x-4) * np.cos((y-4) / np.sqrt(2)) + 1)*10+ ((1 - (x-4))**2 + 100 * ((y-4) - (x-4)**2)**2)/20000
    #(((x)**2 + (y)**2) / 4000 - np.cos(x-4) * np.cos((y-4) / np.sqrt(2)) + 1)*2
    #Ridge Function
    domain_dict["Ridge"] = lambda x, y: x + 2*(y**2)**0.5
    #Modified Shekel-25 function
    domain_dict["Shekel-25"] = lambda x, y: (1 / 500 + np.sum(1 / (np.arange(1, 26) + np.sum((np.array([x, y])[:, np.newaxis] - np.array([
        [-32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32],
        [-32, -32, -32, -32, -32, -16, -16, -16, -16, -16, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 32, 32, 32, 32, 32]
    ]))**6, axis=0)))) ** -1
    #Shubert-3 function
    domain_dict["Shubert-3"] = lambda x, y: sum(
        sum(j * np.sin((j + 1) * xi + j) for j in range(1, 5)) for xi in [x, y]
    )

    #Trid Function
    domain_dict["Trid"] = lambda x, y: (x - 1)**2 + (y - 1)**2 - (x * y)
    #Egg Crate Function
    domain_dict["Egg Crate"] = lambda x, y: x**2 + y**2 + 25 * (np.sin(x)**2 + np.sin(y)**2)
    #Himmelblau's Function
    domain_dict["Himmelblau"] = lambda x, y: (x**2 + y - 11)**2 + (x + y**2 - 7)**2
    #Holder Table Function
    domain_dict["Holder Table Function"] = lambda x, y: -np.abs(np.sin(x) * np.cos(y) * np.exp(np.abs(1 - (np.sqrt(x**2 + y**2) / np.pi))))
    #Keane Function
    domain_dict["Keane Function"] = lambda x, y: -(np.sin(x - y)**2 * np.sin(x + y)**2 / np.sqrt(x**2 + y**2))
    #Bird function
    domain_dict["Bird Function"] = lambda x, y: np.sin(x) * np.exp((1 - np.cos(y))**2) + np.cos(y) * np.exp((1 - np.sin(x))**2) + (x - y)**2
    #Xin-She Yang N.4 Function
    domain_dict["Xin-She Yang N.4"] = lambda x, y: (np.sum(np.sin([x, y])**2) - np.exp(-np.sum(np.array([x, y])**2))) * np.exp(-np.sum(np.sin(np.sqrt(np.abs([x, y])))**2)) 
    #Cross-in-Tray Function
    domain_dict["Cross-in-Tray"] = lambda x,y: -0.0001 *(np.abs(np.sin(x)*np.sin(y)*np.exp(np.abs(100-(np.sqrt(x**2 + y**2)/np.pi))))+1)**0.1
    #Schwefel 2.21 Function
    domain_dict["Schwefel 2.21"] = lambda x, y: np.max(np.abs([x, y]))
    #print(f"{domain_dict["f23"](0,0)}")
    #print(f"{domain_dict["Griewank"](0,0)}")
    return domain_dict