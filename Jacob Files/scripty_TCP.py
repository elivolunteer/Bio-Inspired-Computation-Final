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


for i in range(75):
    #os.system(f"python /Users/jacobduell/Library/CloudStorage/OneDrive-Personal/UT/'CS Documents'/420/Labs/'Final Project'/Bio-Inspired-Computation-Final/TCP_pso.py --destination TCP_")
    os.system(f"python TCP_pso.py --destination TCP_")

for i in range(75):
    #os.system(f"python /Users/jacobduell/Library/CloudStorage/OneDrive-Personal/UT/'CS Documents'/420/Labs/'Final Project'/Bio-Inspired-Computation-Final/'Jacob Files'/pso.py")
    os.system(f"python lowPhi2.py")

for i in range(75):
    #os.system(f"python /Users/jacobduell/Library/CloudStorage/OneDrive-Personal/UT/'CS Documents'/420/Labs/'Final Project'/Bio-Inspired-Computation-Final/'Jacob Files'/pso.py")
    os.system(f"python highPhi2.py")

for i in range(75):
    #os.system(f"python /Users/jacobduell/Library/CloudStorage/OneDrive-Personal/UT/'CS Documents'/420/Labs/'Final Project'/Bio-Inspired-Computation-Final/'Jacob Files'/pso.py")
    os.system(f"python superhighPhi2.py")