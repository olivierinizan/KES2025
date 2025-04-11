# K-CAP-2023
Experiments for K-CAP paper 2023.

# Python dependencies
- itertools
- numpy
- matplotlib.pyplot 
- rdflib

# Commande line
$ python BookV2.py | ActorV2.py | CityV2.py | MountainV2.py | UniversityV2.py | RestaurantV2.py


# Outputs
- Outputs looks like:

    .Genuine Identities  
    [14, 5, 147, 363]  
    Weak Identities  
    [61, 4, 342, 3852]  
    Genuine Differences  
    [0, 0, 0, 1]  
    Weak Differences  
    [5, 323, 0, 0]  
    Undecidability Type 1 Genuine  
    [1464, 183, 4521, 110]  
    Undecidability Type 1 Weak  
    [323, 4215, 7]  
    Undecidability Type 2 Genuine  
    [21, 1969]  
    Undecidability Type 2 Weak  
    [9]  
    Undecidability Type 1 & 2 Genuine  
    [1587]  
    Undecidability Type 1 & 2 Weak  
    [490]  

- The sum of Genuine Identities and Differences 
are reported in the Table 3 of the paper.

- The numbers of the Figure 4 are extracted from:
    - Genuine Incomp: Undecidability Type 1 Genuine
    - Genuine Conflicts: Undecidability Type 2 Genuine
    - GI x GC: Undecidability Type 1 & 2 Genuine

# Lattice of Identities
- The data of the Figure 3 of the paper can be obtained with:
$ python BookPatternIde.py
   
