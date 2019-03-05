

import numpy as np

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import SynthObs
from SynthObs.SED import models

import FLARE
import FLARE.filters

import matplotlib.pyplot as plt




model = models.define_model('BPASSv2.2.1.binary/ModSalpeter_300') # DEFINE SED GRID - 
model.dust = {'A': 5.2, 'slope': -1.0} # DEFINE DUST MODEL - these are the calibrated z=8 values for the dust model




# --- read in test data

test = SynthObs.test_data() # --- read in some test data




# --- create observed frame fluxes

z = 8.

F = FLARE.filters.add_filters(FLARE.filters.NIRCam_W, new_lam = model.lam * (1. + z)) 

cosmo = FLARE.default_cosmo()

model.create_Fnu_grid(F, z, cosmo) # --- create new Fnu grid for each filter. In units of nJy/M_sol

Fnu = models.generate_Fnu(model, test.Masses, test.Ages, test.Metallicities, test.MetSurfaceDensities, F) # --- calculate rest-frame flux of each object in nJy

for f in F['filters']:
    print(f, Fnu[f]) 


















