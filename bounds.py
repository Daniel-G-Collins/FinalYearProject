import numpy as np

class Bounds:
    def __init__(self):
        self.bounds_dict = {
            "Sphere": (-5.12, 5.12, -5.12, 5.12),
            "Rosenbrock": (-2.048, 2.048, -2.048, 2.048),
            "Ackley": (-32, 32, -32, 32),
            "Griewank": (-600, 600, -600, 600),
            "Rastrigin": (-5.12, 5.12, -5.12, 5.12),
            "Schaffer2D": (-100, 100, -100, 100),
            "Shifted Sphere": (-5.12, 5.12, -5.12, 5.12),
            "Shifted Schwefel": (-np.pi, np.pi, -np.pi, np.pi),
            "Shifted and Rotated Elliptic": (-100, 100, -100, 100),
            "Schwefel shifted with Noise": (-np.pi, np.pi, -np.pi, np.pi),
            "El-Attar-Vidyasagar-Dutta": (-10, 10, -10, 10), ## Check bounds
            "Weierstrass": (-1, 1, -1, 1),
            "Shifted Rotated Griewank": (-600, 600, -600, 600),
            "Shifted Rotated Ackley": (-32.768, 32.768, -32.768, 32.768),
            "Shifted Rastrigin": (-5.12, 5.12, -5.12, 5.12),
            "Shifted Rotated Rastrigin": (-5.12, 5.12, -5.12, 5.12),
            "Weirstrass shifted and Rotated": (-0.5, 0.5, -0.5, 0.5),
            "Schwefel": (-np.pi, np.pi, -np.pi, np.pi),
            "Griewank plus Rosenbrock, Amplified and Dampened": (-5, 5, -5, 5),
            "Ridge": (-10, 10, -10, 10),
            "Shekel-25": (-10, 10, -10, 10),
            "Shubert-3": (-10, 10, -10, 10),
            "Trid": (-10, 10, -10, 10),
            "Egg Crate": (-5, 5, -5, 5),
            "Himmelblau": (-5, 5, -5, 5),
            "Holder Table Function": (-10, 10, -10, 10),
            "Keane Function": (-10, 10, -10, 10),
            "Bird Function": (-10, 10, -10, 10),
            "Xin-She Yang N.4": (-2 * np.pi, 2 * np.pi, -2 * np.pi, 2 * np.pi),
            "Cross-in-Tray": (-10, 10, -10, 10),
            "Schwefel 2.21": (-100, 100, -100, 100)
        }

    def getBounds(self, functionName):
        return self.bounds_dict.get(functionName)
