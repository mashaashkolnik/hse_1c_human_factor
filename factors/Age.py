import pyro
import pyro.distributions as distrs

pyro.set_rng_seed(100)

random_noise = distrs.Normal(0.0, 0.15)  # mean = 0.0, sigma = 0.15

class FactorAge:
    def __init__(self, age: int):
        self.age = age
    
    def get_accel(self)->float:
        accel = 0.0
        if 17 <= self.age < 21:
            accel = distrs.Laplace(0.25, 0.15)().item()  # mean = 0.25, sigma = 0.15
        elif 21 <= self.age < 26:
            accel = distrs.Normal(0.15, 0.15)().item()  # mean = 0.15, sigma = 0.15
        elif 26 <= self.age < 45:
            accel = distrs.Normal(0.0, 0.4)().item()  # mean = 0, sigma = 0.4
        elif 45 <= self.age < 65:
            accel = random_noise().item()
        else:
            condition = { 0: "Normal", 1: "Fast" }[distrs.Bernoulli(0.3)().item()]  # success_prob = 0.3
            if condition == "Normal":
                accel = random_noise().item()
            else:
                accel = distrs.Uniform(0.2, 0.35)().item()  # lower_bound = 0.2, upper_bound = 0.35
        
        return accel

    def get_decel(self)->float:
        decel = 0.0
        if 17 <= self.age < 55:
            decel = random_noise().item()
        else:
            decel = distrs.Uniform(-0.3, 0.2)().item()  # lower_bound = -0.3, upper_bound = 0.2
        
        return decel

    def get_sigma(self)->float:
        sigma = 0.0
        if 17 <= self.age < 45:
            sigma = random_noise().item()
        elif 45 <= self.age < 55:
            sigma = distrs.Normal(0.1, 0.05)().item()  # mean = 0.1, sigma = 0.05
        else:
            sigma = distrs.Chi2(2)().item() / 10  # k = 2 -> mean = 0.1 , sigma = 0.2
    
        return sigma
        
    def get_minGap(self)->float:
        minGap = 0.0
        if 17 <= self.age < 30:
            minGap = random_noise().item()
        elif 30 <= self.age < 60:
            minGap = distrs.Uniform(-0.2, 0.2)().item()  # lower_bound = -0.2, upper_bound = 0.2
        else:
            condition = { 0: "Normal", 1: "Fast"}[distrs.Bernoulli(0.4)().item()]  # success_prob = 0.4
            if condition == "Normal":
                minGap = distrs.Uniform(0.0, 0.15)().item()  # lower_bound = 0.0, upper_bound = 0.15
            else:
                minGap = distrs.Normal(-0.1, 0.05)().item()  # mean = -0.1, sigma = 0.05
    
        return minGap

    def get_actionStepLength(self)->float:
        actionStepLength = 0.0
        if 17 <= self.age < 45:
            actionStepLength = distrs.Uniform(-0.1, 0.1)().item()  # lower_bound = -0.1, upper_bound = 0.1
        else:
            actionStepLength = distrs.Chi2(2)().item() / 16 - 0.025  # k = 2 -> mean = 0.125, sigma = 0.125
    
        return actionStepLength

    def get_jmCrossingGap(self)->float:
        jmCrossingGap = 0.0
        if 17 <= self.age < 30:
            jmCrossingGap = distrs.Normal(-0.12, 0.1)().item()  # mean = -0.12, sigma = 0.1
        else:
            jmCrossingGap = random_noise().item()
        
        return jmCrossingGap
    
    def get_collisionMinGapFactor(self)->float:
        collisionMinGapFactor = 0.0
        if self.age < 33:
            collisionMinGapFactor = distrs.Uniform(0.3, 0.7)().item()  # lower_bound = 0.3, upper_bound = 0.7
        elif 33 <= self.age < 55:
            collisionMinGapFactor = distrs.Normal(0.5, 0.1)().item()  # mean = 0.5, sigma = 0.1
        else:
            collisionMinGapFactor = distrs.Normal(0.7, 0.15)().item()  # mean = 0.7, sigma = 0.15
        
        return collisionMinGapFactor
    
    def get_minGapLat(self)->float:
        minGapLat = 0.0
        if self.age < 30:
            minGapLat = distrs.Laplace(-0.2, 0.05)().item()  # mean = -0.2, sigma = 0.05
        elif 30 <= self.age < 50:
            minGapLat = distrs.Normal(0.0, 0.5)().item()  # mean = 0.0, sigma = 0.5
        else:
            minGapLat = distrs.Uniform(-0.2, 0.2)().item()  # lower_bound = -0.2, upper_bound = 0.2
        
        return minGapLat 
    
    def get_maxSpeedLat(self)->float:
        maxSpeedLat = 0.0
        if self.age < 23:
            maxSpeedLat = distrs.Normal(0.2, 0.12)().item()  # mean = 0.2, sigma = 0.12
        elif 23 <= self.age < 45:
            maxSpeedLat = distrs.Normal(0.08, 0.15)().item()  # mean = 0.08, sigma = 0.15
        else:
            maxSpeedLat = distrs.Uniform(-0.1, 0.1)().item()  # lower_bound = -0.1, upper_bound = 0.1
            
        return maxSpeedLat
    
    def get_jmIgnoreFoeProb(self)->float:
        jmIgnoreFoeProb = 0.0
        if self.age < 23:
            jmIgnoreFoeProb = distrs.Uniform(-0.3, 0.3)().item()  # lower_bound = -0.5, upper_bound = 0.5
        elif 23 <= self.age < 40:
            jmIgnoreFoeProb = distrs.Laplace(0.12, 0.12)().item()  # mean = 0.1, sigma = 0.1
        else:
            jmIgnoreFoeProb = distrs.Normal(0.1, 0.06)().item()  # mean = 0.11, sigma = 0.03

        return jmIgnoreFoeProb
    
    def get_jmIgnoreFoeSpeed(self)->float:
        raise NotImplementedError
    
    def get_impatience(self)->float:
        impatience = 0.0
        if self.age < 22:
            impatience = distrs.Normal(0.3, 0.05)().item()  # mean = 0.3, sigma = 0.05
        elif 22 <= self.age < 40:
            impatience = distrs.Exponential(4)().item()  # mean = 0.25, sigma = 0.0625
        else:
            impatience = distrs.Normal(0.1, 0.1)().item()  # mean = 0.1, sigma = 0.1
        
        return impatience
