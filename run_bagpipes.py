#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This is a module for runnning the SED-fitting on all of the CANDELS sources

    This includes the following fields:

        1. GOODS-South
        2. GOODS-North
        3. EGS
        4. UDS
        5. COSMOS


    The initial configuration is in ./sources/definitions.py
"""




__author__ = "Abtin Shahidi"
__copyright__ = "Finding physical properties of galaxies using Bagpipes"
__credits__ = ["Abtin Shahidi"]
__email__ = "abtin.shahidi-at-email.ucr.edu"

# Import the function to devide
from modules.fit_catalogs import fit_catalogs


catalogs = ["goodss", "goodsn", "cosmos", "uds", "egs"]

if __name__ == '__main__':
    # Fit the catalogs
    fit_catalogs(catalogs)
