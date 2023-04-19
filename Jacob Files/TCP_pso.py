# CS 420/CS 527 Lab 4: Particle Swarm Optimization 
# Catherine Schuman
# March 2023

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
from csv import writer


# TO DO:
# TCP Tahoe = Slow Start + AIMD + Fast Retransmit
# Slow start: Lasts until the congestion reaches up to the slow start threshold
    # ex: double window size until reach threshold, then increase tau at set increment
    # If there is a "Miss", reset congestion window size to o riginal value of 1 or something
    # the threshold is updated to congestion window / 2 and the process restarts

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
    def __init__(self, num_particles, inertia, phi_1, phi_2, ww, wh, max_vel, tau, above_thresh, below_thresh, type):
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

        self.type = type

        self.increment_social_below_thresh = below_thresh
        self.increment_social_above_thresh = above_thresh
        self.default_phi_2 = phi_2
        self.threshold = 3 # default value
        
        for i in range(num_particles):
            p = []
            p.append(np.random.random()*ww-ww/2)
            p.append(np.random.random()*wh-wh/2)
            particle = Particle(p)

            if self.type == "Q":
                particle.best_val = self.Q(p)
            else:
                particle.best_val = self.B(p)  

            if (self.global_best_val == None or self.global_best_val > particle.best_val):
                self.global_best_val = particle.best_val
                self.global_best[:] = p[:]
            self.particles.append(particle)
            
    
    def Q(self, position):
        x = position[0]
        y = position[1]
        # Rosenbrock (banana) function
        val=(1-x)**2+100*(y-x**2)**2

        return val
    
    def B(self, position):
        x = position[0]
        y = position[1]
        # Booth function
        val = 100*(y-x**2)**2 + (1-x)**2
        return val
    
    def update(self):
        for i in range(self.num_particles):
            p = self.particles[i]
            p.update(self)
        if (self.improvement):
            self.steps_since_improvement = 0

            #reset phi_2 to original value
            self.phi_2 = self.default_phi_2
            print(f"phi_2 reset to: {self.phi_2}")

            #reduce threshold to window/2 or something, maybe not because this is supposed to represent
            #network reliability, but just because a max is found doesn't mean that there will be consistently more, 
            #only indicative of an unreliable/congested network
        else:
            self.steps_since_improvement += 1

        self.improvement = False

        #is tau necessary? We are finding the ideal number of steps to pass before increasing
        # we are also increasing the amount that the social is increasing by, so probably necessary
        #steps_since_improvement
        if (self.steps_since_improvement > self.tau):
            # multiply social by factor of increment_social_below_thresh
            
            if (self.phi_2 <= self.threshold): 
                if self.phi_2 >= 2: 
                    self.phi_2 = self.phi_2 * self.increment_social_below_thresh
                else:
                    self.phi_2 = 2
            print(f"phi_2 increased to: {self.phi_2}")

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
parser.add_argument("--tau", default=3, type=int, help="Tau")
parser.add_argument("--social_above_thresh", default=1, type=int, help="Increment Social Above Threshold")
parser.add_argument("--social_below_thresh", default=1.05, type=float, help="Increment Social Below Threshold")
parser.add_argument("--destination", default="", type=str, help="destination file prefix")
    
args = parser.parse_args()
# Print all of the command line arguments
Q_Row_Entry = []
B_Row_Entry = []

d = vars(args)
for k in d.keys():

    #print(k + str(":") + str(d[k]))
    if (k != "destination" and k != "tau" and k != "social_above_thresh" and k != "social_below_thresh"):
        Q_Row_Entry.append(d[k])
        B_Row_Entry.append(d[k])

# Create PSO for both functions
psoQ = PSO(args.num_particles, args.inertia, args.cognition, args.social, 100, 100, 2, args.tau, args.social_above_thresh, args.social_below_thresh, "Q")
psoB = PSO(args.num_particles, args.inertia, args.cognition, args.social, 100, 100, 2, args.tau, args.social_above_thresh, args.social_below_thresh, "B")

def global_best(pso, type):
    for i in range(1000):
        pso.update()
        x,y = pso.scatter_plot()
        error_x = np.sum([(pso.particles[k].position[0]-pso.global_best[0])**2 for k in range(args.num_particles)])
        error_y = np.sum([(pso.particles[k].position[1]-pso.global_best[1])**2 for k in range(args.num_particles)])
        error_x = np.sqrt((1.0/(2*args.num_particles))*error_x)
        error_y = np.sqrt((1.0/(2*args.num_particles))*error_y)
        if (error_x < 0.00001 and error_y < 0.00001):
            break

    #print("epoch_stop:", i)
    #print("solution_found:", pso.global_best)
    #print("fitness:", pso.global_best_val)

    if type == "Q":
        Q_Row_Entry.append(i)
        Q_Row_Entry.append(pso.global_best)
        Q_Row_Entry.append(pso.global_best_val)
    else:
        B_Row_Entry.append(i)
        B_Row_Entry.append(pso.global_best)
        B_Row_Entry.append(pso.global_best_val)

global_best(psoQ,"Q")
global_best(psoB,"B")

rowcount = 0
row_labels = ["particles","inertia","cognition","social","epoch_stop","solution_found","fitness"]


#Booth
try: 
    with open(f'{args.destination}_Booth.csv', 'x', newline='') as output_file:
        writer_object = writer(output_file)
        writer_object.writerow(row_labels)
        output_file.close()       
except:
    pass
with open(f'{args.destination}_Booth.csv','a+', newline='') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow(B_Row_Entry)
    f_object.close()

#Rosenbrock
try: 
    with open(f'{args.destination}_Rosenbrock.csv', 'x', newline='') as output_file:
        writer_object = writer(output_file)
        writer_object.writerow(row_labels)
        output_file.close()        
except:
    pass
with open(f'{args.destination}_Rosenbrock.csv','a+', newline='') as f_object:
    writer_object = writer(f_object)
    writer_object.writerow(Q_Row_Entry)
    f_object.close()
