#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Abtin Shahidi"
__copyright__ = "Copyright 2019, Finding physical properties using Bagpipes"
__credits__ = ["Abtin Shahidi"]
# __license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Abtin Shahidi"
__email__ = "abtin.shahidi@email.ucr.edu"
__status__ = "Production"


# importing bagpipes
import bagpipes as pipes


# Importing needed functions
from modules.path_definitons import catalog
from modules.needed_functions import (
                                      list_of_arrays_ID,
                                      list_of_redshifts,
                                      fit_instructions,
                                      load_catalog,
                                      _filt_list,
                                      count_available_cpu,
                                      )


def main(i):
    print("Core {} has been stated".format(i))
    IDs = list_of_arrays_ID[i]
    redshifts = list_of_redshifts[i]
    fit_cat = pipes.fit_catalogue(IDs, fit_instructions, load_catalog,
                                  spectrum_exists = False, redshifts = redshifts
                                  , cat_filt_list = _filt_list,
                                  run = catalog)

    fit_cat.fit(verbose=False)




if __name__ == '__main__':
    # importing multiprocessing
    import multiprocessing as mp
    print("The number of CPUs: ", count_available_cpu)
    pool = mp.Pool(processes=count_available_cpu)
    results = pool.map(main, range(count_available_cpu))
