import numpy as np
import pandas as pd
import random
import os

particles = 10
inertia = 0.1
cognition = 0.1
social = 0.1
social_increment_below_thresh = 2


#increment particles
#while particles <= 100:
#    for i in range(20):
#        os.system(f"python pso.py --iteration {i} --num_particles {particles}")
#    particles = particles + 10

#increment inertia
#while inertia <= 1:
#    for i in range(20):
#        os.system(f"python pso.py --iteration {i} --inertia {inertia}")
#    inertia = round(inertia + 0.1,1)

#increment cognition
#while cognition <= 4:
#    for i in range(20):
#        os.system(f"python pso.py --iteration {i} --cognition {cognition}")
#    cognition = round(cognition + 0.1,1)

#increment social
#while social <= 4:
#    for i in range(20):
#        os.system(f"python pso.py --iteration {i} --social {social}")
#    social = round(social + 0.1,1)


for i in range(20):
    os.system(f"python Bio-Inspired-Computation-Final/TCP_pso.py")