# -*- coding: utf-8 -*-

__author__ = "Abtin Shahidi"
__copyright__ = "Copyright 2019, General useful fumctions"
__credits__ = ["Abtin Shahidi"]
# __license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Abtin Shahidi"
__email__ = "abtin.shahidi@email.ucr.edu"
__status__ = "Development"

def selection(ID, redshift, mass,
              redshift_range=[3, 4.5],
              mass_range=[10, 14.5]):
    import numpy as np
    assert (len(ID) == len(redshift)) * (len(ID) == len(mass))
    final_ID = []
    final_z = []
    final_m = []

    for idi, z, m in zip(ID, redshift, mass):
        if z>redshift_range[0] and z<redshift_range[1]:
            if m>mass_range[0] and m<mass_range[1]:
                final_ID.append(idi)
                final_z.append(z)
                final_m.append(m)
    return np.array(final_ID), np.array(final_z), np.array(final_m)




def devide_arrays(_array_, number_of_devision):
    try:
        assert isinstance(number_of_devision, int), "Expected integer \
                                                     for number of divisions"
        remainder = len(_array_)%number_of_devision
    except:
        raise ValueError

    lenght_of_each = len(_array_)//number_of_devision
    out = []
    for i in range(number_of_devision):
        if i < number_of_devision-1:
            out.append(_array_[i*lenght_of_each:(i+1)*lenght_of_each])
        else:
            out.append(_array_[i*lenght_of_each:(i+1)*lenght_of_each+remainder])

    ## Testing block not neccessary ##
    count = sum([len(x) for x in out])
    assert count == len(_array_)

    return out


def available_cpu_count():
    """
    Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program
    """

    # Needed libraries
    import os
    import re
    import subprocess


    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                      open('/proc/self/status').read())
        if m:
            res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # https://github.com/giampaolo/psutil
    try:
        import psutil
        return psutil.cpu_count()   # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass

    # POSIX
    try:
        res = int(os.sysconf('SC_NPROCESSORS_ONLN'))

        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ['NUMBER_OF_PROCESSORS'])

        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime
        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],
                                  stdout=subprocess.PIPE)
        scStdout = sysctl.communicate()[0]
        res = int(scStdout)

        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open('/proc/cpuinfo').read().count('processor\t:')

        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudoDevices = os.listdir('/devices/pseudo/')
        res = 0
        for pd in pseudoDevices:
            if re.match(r'^cpuid@[0-9]+$', pd):
                res += 1

        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open('/var/run/dmesg.boot').read()
        except IOError:
            dmesgProcess = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
            dmesg = dmesgProcess.communicate()[0]

        res = 0
        while '\ncpu' + str(res) + ':' in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    raise Exception('Can not determine number of CPUs on this system')
