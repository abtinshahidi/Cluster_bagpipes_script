#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Abtin Shahidi"
__copyright__ = "Copyright 2019, Finding physical properties of galaxies using Bagpipes"
__credits__ = ["Abtin Shahidi"]
# __license__ = "GPL"
__version__ = "0.2.0"
__maintainer__ = "Abtin Shahidi"
__email__ = "abtin.shahidi@email.ucr.edu"
__status__ = "Development"

# Import the function to devide
from .modules.fit_catalogs import fit_catalogs


catalogs = ["goodss", "goodsn", "cosmos", "uds", "egs"]


if __name__ == '__main__':
    # Fit the catalogs 
    fit_catalogs(catalogs)
