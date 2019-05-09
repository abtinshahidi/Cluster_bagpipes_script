################################################################################
############################ I/O config ########################################
################################################################################

main_dir = "/home/abtin/playground/dev/files_cluster/bagpipe_cluster/"

# catalogs = ["goodss", "goodsn", "cosmos", "uds", "egs"]

# Which catalog:
catalog = "cosmos"


# where is the list of filters
# Filters' directory
filters_address = main_dir + "data/filters/" + catalog + "/"
# Catalogs_dir
catalog_file_address = main_dir + "/data/CANDELS_ordered.hdf5"


# Doing extra calculations! need further inquiry! DOES NOT INTERFERE WITH THE DEFAULT OUTPUT
# Output directory
import os
output_dir = main_dir + "/FULL_CAT_RUN/"

if os.path.isdir(output_dir) == False:
    try:
        os.mkdir(output_dir)
    except:
        print("Couldn't make output directory!")
        raise ValueError
