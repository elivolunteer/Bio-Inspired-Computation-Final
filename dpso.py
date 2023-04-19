# CS 420/CS 527 Lab 4: Particle Swarm Optimization 
# Catherine Schuman
# March 2023

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

class Particle:
    def __init__(self, position):
        self.position = np.array(position)
        self.v = np.array([0,0])
        self.best_position = self.position.copy()
        
    def update(self, pso):
        self.v = pso.inertia*self.v+pso.phi_1*np.random.random(2)*(np.subtract(self.best_position,self.position))+pso.phi_2*np.random.random(2)*np.subtract(pso.global_best,self.position)
            
        if (self.v[0]**2+self.v[1]**2 > pso.max_vel**2):
            self.v = (pso.max_vel/np.sqrt(self.v[0]**2+self.v[1]**2))*self.v
        
        self.position = np.add(self.position, self.v)
            
        val = pso.Q(self.position)
        if (val < self.best_val):
            self.best_val = val
            self.best_position = self.position.copy()
        
        if (val < pso.global_best_val):
            pso.global_best_val = val
            pso.global_best = self.position.copy()
            pso.improvement = True

        
class PSO:
    def __init__(self, num_particles, inertia, phi_1, phi_2, ww, wh, max_vel, tau):
        self.num_particles = num_particles
        self.inertia = inertia
        self.phi_1 = phi_1
        self.phi_2 = phi_2
        self.ww = ww
        self.wh = wh
        self.max_vel = max_vel
        self.tau = tau
        self.steps_since_improvement = 0
        self.improvement = False
        self.global_best = np.array([0,0])
        self.global_best_val = None
        self.particles = []
        
        for i in range(num_particles):
            p = []
            p.append(np.random.random()*ww-ww/2)
            p.append(np.random.random()*wh-wh/2)
            particle = Particle(p)
            particle.best_val = self.Q(p)
            if (self.global_best_val == None or self.global_best_val > particle.best_val):
                self.global_best_val = particle.best_val
                self.global_best[:] = p[:]
            self.particles.append(particle)
            
    
    def Q(self, position):
        x = position[0]
        y = position[1]
        # Rosenbrock (banana) function
        val=(1-x)**2+100*(y-x**2)**2
        # Booth Fucntion
        #val = (x+2*y-7)**2+(2*x+y-5)**2
        # Drop Wave Function
        #val = -((1+np.cos(12*np.sqrt(x**2+y**2)))/(0.5*(x**2+y**2)+2))
        # Levy Function
        #val = np.sin(3*np.pi*x)**2+(x-1)**2*(1+np.sin(3*np.pi*y)**2)+(y-1)**2*(1+np.sin(2*np.pi*y)**2)
        # Rastrigin Function
        #val = 20+np.power(x,2)-10*np.cos(2*np.pi*x)+np.power(y,2)-10*np.cos(2*np.pi*y)
        # Shubert Function
        # val = 0
        # for i in range(1,6):
        #     val += i*np.cos((i+1)*x+i)+i*np.cos((i+1)*y+i)
        # Zakharov Function
        #val = np.power(x,2)+np.power(y,2)-0.5*(np.cos(2*np.pi*x)+np.cos(2*np.pi*y))+0.5
        # Three Hump Camel Function
        #val = 2*x**2-1.05*x**4+np.power(x,6)/6+x*y+y**2
        # Beale Function
        #val = (1.5-x+x*y)**2+(2.25-x+x*y**2)**2+(2.625-x+x*y**3)**2
        # Goldstein-Price Function
        #val = (1+(x+y+1)**2*(19-14*x+3*x**2-14*y+6*x*y+3*y**2))*(30+(2*x-3*y)**2*(18-32*x+12*x**2+48*y-36*x*y+27*y**2))

        return val
    
    def update(self):
        for i in range(self.num_particles):
            p = self.particles[i]
            p.update(self)
        if (self.improvement):
            self.steps_since_improvement = 0
        else:
            self.steps_since_improvement += 1
        self.improvement = False

        if (self.steps_since_improvement > self.tau):
            self.phi_1 -= 0.1
            self.steps_since_improvement = 0
            
    def scatter_plot(self):
        x = []
        y = []
        for i in range(self.num_particles):
            x.append(self.particles[i].position[0])
            y.append(self.particles[i].position[1])
        return x,y

parser = argparse.ArgumentParser(description="CS 420/CS 527 Lab 4: PSO")
parser.add_argument("--num_particles", default=40, type=int, help="Number of particles")
parser.add_argument("--inertia", default=0.5, type=float, help="Inertia")
parser.add_argument("--cognition", default=1, type=float, help="Cognition parameter")
parser.add_argument("--social", default=1, type=float, help="Social parameter")
parser.add_argument("--tau", default=10, type=int, help="Tau")
    
args = parser.parse_args()
# Print all of the command line arguments
d = vars(args)
for k in d.keys():
    print(k + str(":") + str(d[k]))

# Create PSO
pso = PSO(args.num_particles, args.inertia, args.cognition, args.social, 100, 100, 2, args.tau)

for i in range(200):
    print("epoch:", i)
    pso.update()
    x,y = pso.scatter_plot()
    error_x = np.sum([(pso.particles[k].position[0]-pso.global_best[0])**2 for k in range(args.num_particles)])
    error_y = np.sum([(pso.particles[k].position[1]-pso.global_best[1])**2 for k in range(args.num_particles)])
    error_x = np.sqrt((1.0/(2*args.num_particles))*error_x)
    error_y = np.sqrt((1.0/(2*args.num_particles))*error_y)
    # if (pso.global_best_val < 1e-10):
    #     break
    # if (error_x < 0.00001 and error_y < 0.00001):
    #     break

print("epoch_stop:", i)
print("solution_found:", pso.global_best)
print("fitness:", pso.global_best_val)
