################################################################################
############################ libraries #########################################
################################################################################

# Importing the needed libraries
import numpy as np
import bagpipes as pipes
import deepdish as dd
import os



from .general_functions import (
                               available_cpu_count,
                               devide_arrays,
                               redshift_selection,
                               )
from .path_definitons import (
                               filters_address,
                               catalog_file_address,
                               output_dir,
                               )

import numpy as np

# Reading filter's list from our file

_filt_list_ = np.loadtxt(filters_ + "filters_list.txt", dtype="str")

_filt_list = [ filters_ + i for i in _filt_list_]



# Which catalog: 
catalog = "cosmos"


if catalog == "egs":
    _filt_list = _filt_list[:23]


# Loading the Catalog
photometry_catalogs = dd.io.load(catalog_file_address)


# CPU count
count_available_cpu = available_cpu_count()
IDs = photometry_catalogs[catalog]["00_ID"]
redshifts = photometry_catalogs[catalog]["z_Best"]

IDs, redshifts = redshift_selection(IDs, redshifts, [3, 4.5])

list_of_arrays_ID = devide_arrays(IDs, count_available_cpu)
list_of_redshifts = devide_arrays(redshifts, count_available_cpu)


# # Dealing with log files: generic
# log_file = "/data/abtin/bagpipes_run/FULL_CAT_RUN/goodsn/.log_errors"
# # Creating log file if it does not exist
# if os.path.exists(log_file) is not True:
#     open(log_file, "a").close()



################################################################################
############################ Fitting instruction ###############################
################################################################################
# Defining the fitting instructions for the bagpipes : look at documentation here:
# https://bagpipes.readthedocs.io/en/latest/index.html


# Assuming exponentially declining SFH and defining the dynamic range of their
# parameters.
exp = {}
exp["age"] = (0.01, 13.)
exp["tau"] = (0.005, 10.)
exp["massformed"] = (1., 15.)
exp["metallicity"] = (0., 2.5)

# Assuming Calzetti dust extinction law
dust = {}
dust["type"] = "Calzetti"
dust["Av"] = (0., 2.)

fit_instructions = {}
# fit_instructions["redshift"] = (0.01, 10)
fit_instructions["exponential"] = exp
fit_instructions["dust"] = dust


################################################################################
############################ Function to load catalogs ###########################
################################################################################
# this is required for the bagpipes- take ID and find photometry, and errors

def load_catalog(ID):
    import numpy as np
    import re
    # This is for reading the catalog from a dictionary of CANDELS photometry
    list_of_keys = list(photometry_catalogs[catalog].keys())
    list_of_keys.sort()

    # Doing  some string manipulation
    if catalog=="goodsn":
        rrr = re.compile(".*FLUX")
        new_list = list(filter(rrr.match, list_of_keys))
        # Bands and their corresponding errors
        bands_list = list(new_list[:18])
        bands_err_list = list(new_list[18:])
    
    elif catalog=="cosmos":
        # Doing  some string manipulation
        rrr = re.compile(".*FLUX")
        new_list = list(filter(rrr.match, list_of_keys))
        # Bands and their corresponding errors
        bands_list = list(new_list[::2])
        bands_err_list = list(new_list[1::2])


    elif catalog=="uds":
        # Doing  some string manipulation
        rrr = re.compile(".*Flux")
        new_list = list(filter(rrr.match, list_of_keys))
        # Bands and their corresponding errors
        bands_list = list(new_list[::2])
        bands_err_list = list(new_list[1::2])    

    elif catalog=="egs":
        # Doing  some string manipulation
        rrr = re.compile(".*FLUX")
        new_list = list(filter(rrr.match, list_of_keys))
        # Bands and their corresponding errors
        bands_list = list(new_list[::2])[:23]
        bands_err_list = list(new_list[1::2])[:23]
        
    # Finding the row to read
    row = int(float(ID))-1
    fluxes = []
    fluxerrs = []

    # going through all of the bands for each ID and assign photometry and it's
    # errors to it
    for band, band_err in zip(bands_list, bands_err_list):
        fluxes.append(photometry_catalogs[catalog][band][int(row)])
        fluxerrs.append(photometry_catalogs[catalog][band_err][int(row)])

    # Putting the photometry and it's errors in a 2D numpy array. Format wanted
    #  by the bagpipes
    photometry = np.c_[np.array(fluxes), np.array(fluxerrs)]

    # blow up the errors associated with any missing fluxes.
    for i in range(len(photometry)):
        if (photometry[i, 0] <= 0.) or (photometry[i, 1] <= 0):
#             print(photometry[i])
            photometry[i,:] = [0., 9.9*10**99.]

    # Enforce a maximum SNR of 20, or 10 in the IRAC channels.
    for i in range(len(photometry)):
        if i < 10:
            max_snr = 20.

        else:
            max_snr = 10.

        if photometry[i, 0]/photometry[i, 1] > max_snr:
            photometry[i, 1] = photometry[i, 0]/max_snr

    return photometry #, info



# Procedures to save more complicated results into a separate file
def getting_posterior(_fit_):
    import bagpipes as pipes
    import deepdish as dd

    # output_dir = "/home/abtin/playground/test_files/"
    try:
        _fit_.posterior.get_basic_quantities()
        _fit_.posterior.get_advanced_quantities()
        result = _fit_.posterior.samples
    except:
        pass

    try:
        del result["sfh"]
    except KeyError:
        del result["spectrum_full"]
    except KeyError:
        del result["tform"]
    except KeyError:
        del result["tquench"]
    except KeyError:
        pass
    _name_ = _fit_.galaxy.ID+"_ADV.h5"

    try:
        dd.io.save(output_dir+_name_, result)
    except:
        with open(log_file, "a") as log:
            log.write(_name_+"\n")
            log.close()
