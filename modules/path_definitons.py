################################################################################
############################ I/O config ########################################
################################################################################

main_dir = "/home/abtin/playground/dev/files_cluster/bagpipe_cluster/"


# where is the list of filters
# Filters' directory
filters_goodsn = main_dir + "data/filters/goodsn/"
# Catalogs_dir
catalog_file_address = main_dir + "/data/CANDELS_ordered.hdf5"
# Output directory
import os
output_dir = main_dir + "/FULL_CAT_RUN/"

if os.path.isdir(output_dir) == False:
    try:
        os.mkdir(output_dir)
    except:
        print("Couldn't make output directory!")
        raise ValueError
