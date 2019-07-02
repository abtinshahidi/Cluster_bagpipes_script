# -*- coding: utf-8 -*-

# importing the deepdish to load the full catalog
import deepdish as dd
import multiprocessing as mp

# import the address to filters and catalog and fittings instructions
from .definitions import (
                               filters_address,
                               catalog_file_address,
                               fit_dict,
                         )
# import the functions to count the CPUs on the machine, a function  to  devide
# the galaxies into the groups to send to differnt processes, and the selection
# based on the redshifts and their stellar mass. (from final redshift catalog)
from .general_functions import available_cpu_count, devide_arrays, selection
from .fitting import fit_galaxies


# Loading the Catalog
photometry_catalogs = dd.io.load(catalog_file_address)

# CPU count
count_available_cpu = available_cpu_count()


def find_loading(catalog):
    """
        The function to define the load function for different catalogs to pass
      to the fits function.
    """
    def load_catalog(ID):
        import numpy as np
        import re
        # This is for reading the catalog from a dictionary
        # of CANDELS photometry
        list_of_keys = list(photometry_catalogs[catalog].keys())
        list_of_keys.sort()

        # Doing  some string manipulation
        if catalog=="goodsn":
            rrr = re.compile(".*FLUX")
            new_list = list(filter(rrr.match, list_of_keys))
            # Bands and their corresponding errors
            bands_list = list(new_list[:18])
            bands_err_list = list(new_list[18:])

        # Doing  some string manipulation
        elif catalog=="goodss":
            rrr = re.compile(".*FLUX")
            new_list = list(filter(rrr.match, list_of_keys))
            # Bands and their corresponding errors
            bands_list = list(new_list[::2])[:-4]
            bands_err_list = list(new_list[1::2])[:-3]

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

        # going through all of the bands for each ID and assign photometry and
        # it's errors to it
        for band, band_err in zip(bands_list, bands_err_list):
            fluxes.append(photometry_catalogs[catalog][band][int(row)])
            fluxerrs.append(photometry_catalogs[catalog][band_err][int(row)])

        # Putting the photometry and it's errors in a 2D numpy array. Format
        # wanted by the bagpipes
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
    return load_catalog

def find_filters(catalog):
    """
    Find the filters for the respective catalog
    """
    filters_address_ = filters_address + catalog + "/"
    with open(filters_address_ + "filters_list.txt", "r") as f:
        di = f.readlines()
    _filt_list_ = [d[:-1] for d in di]
    _filt_list = [ filters_address_ + i for i in _filt_list_]
    if catalog == "egs":
        _filt_list = _filt_list[:23]
    return _filt_list

# function to make the intial configuration
def full_catalogs(catalogs):
    full_cat = {}
    for catalog in catalogs:
        IDs_ = photometry_catalogs[catalog]["00_ID"]
        redshifts_ = photometry_catalogs[catalog]["z_Best"]
        mass_ = photometry_catalogs[catalog]["log(Mass)_med"]

        IDs, redshifts, mass = selection(IDs_,
                                         redshifts_,
                                         mass_,
                                         [3, 4.5],
                                         [10.0, 15])

        list_of_arrays_ID = devide_arrays(IDs, count_available_cpu)
        list_of_redshifts = devide_arrays(redshifts, count_available_cpu)
        list_of_mass = devide_arrays(mass, count_available_cpu)

        find_l = find_loading(catalog)
        find_filt = find_filters(catalog)

        full_cat[catalog] = {"IDs" : list_of_arrays_ID,
                             "redshifts" : list_of_redshifts,}
    return full_cat

def main(i, catalog, full_catal):
    """
    This is the function that take the core number catalog
    and initial configurations

    """
    print("Core {} has been started".format(i))

    list_of_arrays_ID = full_catal[catalog]["IDs"]
    list_of_redshifts = full_catal[catalog]["redshifts"]

    IDs = list_of_arrays_ID[i]
    redshifts = list_of_redshifts[i]

    fit_cat = fit_galaxies(IDs=IDs,
                           redshifts=redshifts,
                           fit_inst_dict= fit_dict,
                           catalog=catalog,
                           load_data = find_loading(catalog),
                           spectrum_exists=False,
                           filt_list=find_filters(catalog))


def fit_catalogs(catalogs):
    """
    This is the function that takes the catalogs list and goes through each
    catalog and break them into n processes which n is the number of cores
    on the machine.

    There is a sleep of 1s between each process to avoid any confusion.
    """
    from time import sleep
    full_cat = full_catalogs(catalogs)
    for catalog in catalogs:
        print("The number of CPUs: ", count_available_cpu)
        # create a list to store the proccesses
        jobs = []
        # Going through different cores
        for i in range(count_available_cpu):
            # Making a proccess for fitting the SEDs
            p = mp.Process(target=main, args=(i, catalog, full_cat))
            jobs.append(p)
            # Start the process
            p.start()
            sleep(1)
        # Wait untill all of the processes are finished
        for process in jobs:
            process.join()

        print(catalog.upper() + "'s SED fitting is finished!'")
