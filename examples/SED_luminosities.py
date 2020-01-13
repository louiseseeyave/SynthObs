

import numpy as np

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import SynthObs
from SynthObs.SED import models

import FLARE
import FLARE.filters

import matplotlib.pyplot as plt


"This is an more efficient way of calculating the broadband luminosities of galaxies. It produces the same answer as generate_SED within ~0.05 dex"


model = models.define_model('BPASSv2.2.1.binary/ModSalpeter_300') # DEFINE SED GRID -
model.dust = {'slope': -1.0} # define dust curve


# --- read in test data

test = SynthObs.test_data() # --- read in some test data


# --- create rest-frame luminosities

filters = ['FAKE.TH.'+f for f in ['FUV','NUV','V']] # --- define the filters. FAKE.FAKE are just top-hat filters using for extracting rest-frame quantities.

F = FLARE.filters.add_filters(filters, new_lam = model.lam)

model.create_Lnu_grid(F) # --- create new L grid for each filter. In units of erg/s/Hz



# --- Pure stellar
test.tauVs = np.zeros(test.Masses.shape)
Lnu = models.generate_Lnu(model, test.Masses, test.Ages, test.Metallicities, test.tauVs, F, fesc = 1.0) # --- calculate rest-frame Luminosity. In units of erg/s/Hz
for f in F['filters']:
    print(f, Lnu[f])

# --- Just BC
test.tauVs = np.zeros(test.Masses.shape)
Lnu = models.generate_Lnu(model, test.Masses, test.Ages, test.Metallicities, F, test.tauVs, fesc = 0.0) # --- calculate rest-frame Luminosity. In units of erg/s/Hz
for f in F['filters']:
    print(f, Lnu[f])


# --- TOTAL
A = 5.2
test.tauVs = (10**A) * test.MetSurfaceDensities # --- calculate V-band (550nm) optical depth for each star particle
Lnu = models.generate_Lnu(model, test.Masses, test.Ages, test.Metallicities, test.tauVs, F, fesc = 0.0) # --- calculate rest-frame Luminosity. In units of erg/s/Hz

for f in F['filters']:
    print(f, Lnu[f])
