# -*- coding: utf-8 -*-

"""
This is a modules for fit different models to galaxies.
You can access to this with:
                             fitting.fit_various_models
                             fitting.fit_galaxies
"""


import bagpipes as pipes
import numpy as np
import deepdish as dd
from copy import deepcopy
import os


from .definitions import fit_dict, results_dir
res = deepcopy(results_dir)




def create_obs_galaxies(IDs, **kwargs):
    """
    Create a list of galaxy object from the observation
    Iterate through IDs and will pass the kwargs to the
    bagpipes.galaxy

    INPUT
    ======
                IDs (an array of IDs) : A list of  IDs
                kwargs : arguments to be passed to the
                        bagpipes.galaxy

    OUTPUT
    ======
                a list of galaxy object from Bagpipes
    """
    gal_list = []
    for idx in IDs:
        galaxy = pipes.galaxy(ID = idx, **kwargs)
        gal_list.append(galaxy)
    return gal_list

def fit_various_models(galaxy, redshift, fit_instructions_dict, catalog):
    """
    This is the  function  to  fit  different models to the
    galaxy object. It will create the following directories:

      results_dir/
                 catalog/
                         results/

    And for every run (model) a different directory will be
    made to store the results.

    FUNCTION:
    =========
              It will save a .h5 file with all the SED fitting results
              information for every galaxy and they are as follows:
               (for more info look at Bagpipes)

            fit.posterior.get_basic_quantities()
            fit.posterior.get_advanced_quantities()
            results = fit.results
            added_results = fit.posterior.samples

            results["samples"] = added_results
            results["samples"]["ages"] = fit.posterior.sfh.ages
            results["filters_list"] = galaxy.filt_list
            results["model_components"] = fit.fitted_model.model_components



    INPUT
    ======
            galaxy (Galaxy obj) : galaxy obj from bagpipes
            redshift (float): redshift of the Galaxy
            fit_instructions_dict (dict): A dictionary of --->
                                          {run (model) : fit_instructions}
            catalog (string) : catalog string like GOODSS, GOODSN, UDS, ...

    OUTPUT
    ======
            None
    """
    # Create the main results directory if not exists
    if not os.path.isdir(res):
        os.mkdir(res)

    results_dir = res + catalog + "/"

    if not os.path.isdir(results_dir):
        os.mkdir(results_dir)

    if not os.path.isdir(results_dir + "results"):
        os.mkdir(results_dir + "results")

    # Create the error log file if not exists
    log_error = results_dir + "results/.no_fitting"
    if not os.path.exists(log_error):
        with open(log_error, "w+") as f:
            f.close()

    # Create directories for every models if not exists
    for run in fit_instructions_dict:
        if not os.path.isdir(results_dir + "results/" + run):
            os.mkdir(results_dir + "results/" + run)
#         print(run)

    for run, fit_info in fit_instructions_dict.items():
        run = run + "_" + catalog
        try:
            fit_info["redshift"] = redshift
            fit = pipes.fit(galaxy=galaxy,
                            fit_instructions=fit_info,
                            run =run)
            fit.fit(verbose=False)

            fit.posterior.get_basic_quantities()
            fit.posterior.get_advanced_quantities()
            results = fit.results
            added_results = fit.posterior.samples

            results["samples"] = added_results
            results["samples"]["ages"] = fit.posterior.sfh.ages
            results["filters_list"] = galaxy.filt_list
            results["model_components"] = fit.fitted_model.model_components
            # Saving the results of the SED fitting with all of the main
            # physical quantities.
            path_to_save = results_dir + "results/" + run \
                           + "/" + galaxy.ID + ".h5"
            if not os.path.exists(path_to_save):
                dd.io.save(path_to_save, results)
        except:
            with open(log_error, "a") as f:
                f.write("No fitting for " + run + "  " + fit.galaxy.ID)

    return None


def fit_galaxies(IDs, redshifts, catalog, fit_inst_dict, **kwargs):
    """
    This is the function to fit different models to the given list of
    IDs and redshifts.
    """
    gal_list = create_obs_galaxies(IDs, **kwargs)
    for galaxy, redshift in zip(gal_list, redshifts):
        _ = fit_various_models(galaxy, redshift, fit_inst_dict, catalog)
    return None
