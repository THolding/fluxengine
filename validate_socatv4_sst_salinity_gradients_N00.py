#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:55:38 2018

Runs the flux engine for using SOCATv4 pco2 data for 2010.
Compares output to a known reference output for verification.

@author: verwirrt
"""

from ofluxghg_run import run_fluxengine;
from fluxengine_src.tools.ofluxghg_flux_budgets import run_flux_budgets;
from fluxengine_src.tools.compare_net_budgets import calc_net_budget_percentages
from argparse import Namespace;
from os import getcwd, path;

#Runs the validation proceedure for socat using sst salinity gradients and Nightinggale 2000 k parameterisation.
def run_socat_sst_salinity_gradients_N00_validation(verbose=True):
    #Run flux engine
    if verbose:
        print "Running FluxEngine for year 2010...";
    configFilePath = "configs/socatv4_sst_salinity_gradients-N00.conf";
    runStatus = run_fluxengine(configFilePath, [2010], range(0,12), processLayersOff=True, verbose=False);
    
    
    #run net budgets
    if verbose:
        print "\n\nNow calculating flux budgets...";
    fluxBudgetsArgs = Namespace(LooseIce=False, cidataset='OIC1', cwdataset='OSFC', dir=path.join(getcwd(),
                                'output/validate_socatv4_sst_salinity_N00/'), fluxdataset='OF', gridarea=0,
                                gridareadataset='area', gridareafile='no_file', icePercent=False, icedataset='P1',
                                kwdataset='OK3', landdataset='land_proportion', landfile=path.join(getcwd(), 'data/onedeg_land.nc'),
                                maskdatasets=[], maskfile=path.join(getcwd(), 'data/World_Seas-IHO-mask.nc'),
                                outroot=path.join(getcwd(), 'output/validate_socatv4_sst_salinity_N00/'), places=10, ref=None,
                                regions=[], verbosity=0, window=None);
    run_flux_budgets(fluxBudgetsArgs);
    
    
    #compare similarity flux budgets output between new and ref runs
    if verbose:
        print "\n\nComparing output to reference data...";
    newPath = "output/validate_socatv4_sst_salinity_N00/_global.txt";
    refPath = "data/validation_data/validation_reference_output/socatv4_sst_salinity_N00_reference/SST_Salinity_gradients-N00_global.txt";
    diffs = calc_net_budget_percentages(newPath, refPath, verbose=False);
    
    numFailed = 0;
    for key in diffs:
        if diffs[key] > 101.0 or diffs[key] < 99.0:
            if verbose:
                print key, "percentage difference from reference:", diffs[key];
            numFailed += 1;
    
    if numFailed == 0:
        if verbose:
            print "\nValidation successful! All values are within threshold limits:";
            validationSuccessful = True;
        for key in diffs:
            if verbose:
                print "\t"+key+": "+str(diffs[key])+"%";
    else:
        if verbose:
            print "\nValidation failed because %d values were outside threshold limits." % numFailed;
            validationSuccessful = True;
    
    return {"run status":runStatus, "number of net budgets exceeding threshold":numFailed,
            "validation successful?":validationSuccessful, "percentage difference from reference (dictionary)":diffs};
    
if __name__ == "__main__":
    run_socat_sst_salinity_gradients_N00_validation(verbose=True);

