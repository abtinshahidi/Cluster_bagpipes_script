################################################################################
############################ I/O config ########################################
################################################################################

#################### GOOGLE computing instances ########################
main_dir = "/home/abtinshahidi/Cluster_bagpipes_script/"
results_dir = "/home/abtinshahidi/data/SED_fitting_results/"
# catalogs = ["goodss", "goodsn", "cosmos", "uds", "egs"]

# where is the list of filters
# Filters' directory
filters_address = main_dir + "data1/CANDELS/data/filters/"

# Catalogs_dir
catalog_file_address = main_dir + "data1/CANDELS/data/CANDELS_ordered.hdf5"


######################## Vienna ############################
main_dir = "/home/abtin/playground/random_stuff/dev/files_cluster/"
results_dir = "/home/abtin/playground/SED_fitting_results/"
# catalogs = ["goodss", "goodsn", "cosmos", "uds", "egs"]


# where is the list of filters
# Filters' directory
filters_address = main_dir + "data/filters/"

# Catalogs_dir
catalog_file_address = main_dir + "data/CANDELS_ordered.hdf5"

####################################################################
##################### MODELS for SED fitting #######################
####################################################################
#==========================================#
# Same dust model accross different models #
#==========================================#
# Calzetti dust model #
#=====================#
dust = {}                           # Dust component
dust["type"] = "Calzetti"           # Define the shape of the attenuation curve
dust["Av"] = (0., 2.)               # Vary Av between 0 and 2 magnitudes


#======================================#
# Same nebular emmision accross models #
#======================================#
# Nebular emission model #
#========================#
nebular = {}
nebular["logU"] = -3.


# -------------------- STAR FORMATION HISTORY -------------------------
#===========#
# tau model #
#===========#
exp = {}                    # Tau-model star-formation history component
exp["age"] = (0.1, 1.5)     # Vary age between 100 Myr and 1.5 Gyr. In practice
                            # the code automatically limits this to the age of
                            # the Universe at the observed redshift.

exp["tau"] = (0.05, 10.)     # Vary tau between 50 Myr and 10 Gyr


exp["massformed"] = (1., 15.)        # vary log_10(M*/M_solar) between 1 and 15
exp["metallicity"] = (0., 2.5)       # vary Z between 0 and 2.5 Z_oldsolar

#--------------------------#
# Without nebular emission #
#--------------------------#
# The fit instructions dictionary
fit_instructions_tau = {}
fit_instructions_tau["exponential"] = exp
fit_instructions_tau["dust"] = dust

#-----------------------#
# With nebular emission #
#-----------------------#
fit_instructions_tau_neb["exponential"] = exp
fit_instructions_tau_neb["dust"] = dust
fit_instructions_tau_neb["nebular"] = nebular



#==========================#
# Constant (Top-Hat) model #
#==========================#
constant = {}              # tophat function between some limits
constant["age_max"] = (0.5, 2)   # Time since the constant switched on in Gyr
constant["age_min"] = (0.5, 2)   # Time since the constant switched off in Gyr

constant["massformed"] = (1., 15.)
constant["metallicity"] = (0., 2.5)


#--------------------------#
# Without nebular emission #
#--------------------------#
# The fit instructions dictionary
fit_instructions_const = {}
fit_instructions_const["constant"] = constant
fit_instructions_const["dust"] = dust

#-----------------------#
# With nebular emission #
#-----------------------#
# The fit instructions dictionary
fit_instructions_const_neb = {}
fit_instructions_const_neb["constant"] = constant
fit_instructions_const_neb["dust"] = dust
fit_instructions_const_neb["nebular"] = nebular



#==========================#
# Constant (Top-Hat) model #
#==========================#
# The fit instructions dictionary
constant = {}              # tophat function between some limits
constant["age_max"] = (0.5, 2)   # Time since the constant switched on in Gyr
constant["age_min"] = (0.5, 2)   # Time since the constant switched off in Gyr

constant["massformed"] = (1., 15.)
constant["metallicity"] = (0., 2.5)


#--------------------------#
# Without nebular emission #
#--------------------------#
# The fit instructions dictionary
fit_instructions_const = {}
fit_instructions_const["constant"] = constant
fit_instructions_const["dust"] = dust

#-----------------------#
# With nebular emission #
#-----------------------#
# The fit instructions dictionary
fit_instructions_const_neb = {}
fit_instructions_const_neb["constant"] = constant
fit_instructions_const_neb["dust"] = dust
fit_instructions_const_neb["nebular"] = nebular


#========================#
# Double power law model #
#========================#
dblplaw = {}
 # Vary the time of peak star-formation between
# the Big Bang at 0 Gyr and 15 Gyr later. In
# practice the code automatically stops this
# exceeding the age of the universe at the
# observed redshift.
dblplaw["tau"] = (0., 15.)

# Vary the falling power law slope from 0.01 to 1000.
dblplaw["alpha"] = (0.01, 1000.)
# Vary the rising power law slope from 0.01 to 1000.
dblplaw["beta"] = (0.01, 1000.)
# Impose a prior which is uniform in log_10 of the
# parameter betweenthe limits which have been set
# above as in Carnall et al. (2017).
dblplaw["alpha_prior"] = "log_10"
dblplaw["beta_prior"] = "log_10"

dblplaw["massformed"] = (1., 15.)
dblplaw["metallicity"] = (0., 2.5)

#--------------------------#
# Without nebular emission #
#--------------------------#
# The fit instructions dictionary
fit_instructions_dbplaw = {}                # The fit instructions dictionary
fit_instructions_dbplaw["dblplaw"] = dblplaw
fit_instructions_dbplaw["dust"] = dust


#-----------------------#
# With nebular emission #
#-----------------------#
# The fit instructions dictionary
fit_instructions_dbplaw_neb = {}              # The fit instructions dictionary
fit_instructions_dbplaw_neb["dblplaw"] = dblplaw
fit_instructions_dbplaw_neb["dust"] = dust
fit_instructions_dbplaw_neb["nebular"] = nebular

fit_dict = {
            # tau model
            "tau_sfh" : fit_instructions_tau,
            "tau_sfh_neb" : fit_instructions_tau_neb,
            # Constant model
            "const_sfh" : fit_instructions_const,
            "const_sfh_neb" : fit_instructions_const_neb,
            # Double power law model
            "dbplaw_sfh" : fit_instructions_dbplaw,
            "dbplaw_sfh_neb" : fit_instructions_dbplaw_neb,
}
