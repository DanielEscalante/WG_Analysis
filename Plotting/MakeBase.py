#!/usr/bin/env python
import ROOT
from itertools import product
ROOT.PyConfig.IgnoreCommandLineOptions = True
#import numpy as np
from math import pi
import os
import selection_defs as defs
from SampleManager import SampleManager

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--baseDirMuG',      default=None,           dest='baseDirMuG',         required=False, help='Path to muon base directory')
parser.add_argument('--baseDirElG',      default=None,           dest='baseDirElG',         required=False, help='Path to electron base directory')
parser.add_argument('--baseDirMuMu',      default=None,          dest='baseDirMuMu',        required=False, help='Path to muon base directory')
parser.add_argument('--baseDirElEl',      default=None,          dest='baseDirElEl',        required=False, help='Path to electron base directory')
parser.add_argument('--outputDir',       default=None,           dest='outputDir',          required=False, help='Output directory to write histograms')
parser.add_argument('--data',            default=False,          dest='data',               required=False, help='Use data or MC')
parser.add_argument('--batch',           default=False,          dest='batch',  action="store_true",            required=False, help='Supress X11 output')
parser.add_argument('--year',            default=2016,           dest='year',   type=int,   required=False, help='Set run year')

options = parser.parse_args()

_TREENAME = 'UMDNTuple/EventTree'
_FILENAME = 'tree.root'
datestr   = "2019_12_12"

if options.year == 2016:
    _XSFILE   = 'cross_sections/photon16.py'
    _LUMI     = 35900
    _SAMPCONF = 'Modules/Resonance2016.py'
    etastr    = ""
    #etastr    = "&& !(ph_eta[0]<0 && ph_phi[0]<16*pi/18 && ph_phi[0]>13*pi/18)"
    lumiratio = 1.
    #lumiratio = 1./(1-3./72)
elif options.year == 2017:
    _SAMPCONF = 'Modules/Resonance2017.py'
    _XSFILE   = 'cross_sections/photon17.py'
    _LUMI     = 41000
    #etastr    = "&& !(ph_eta[0]>0 && ph_phi[0]>15*pi/18)"
    #lumiratio = 1./(1-3./72.)
elif options.year == 2018:
    _SAMPCONF = 'Modules/Resonance2018.py'
    _XSFILE   = 'cross_sections/photon18.py'
    _LUMI     = 59740
    #etastr    = "&& !(ph_phi[0]<5*pi/18 && ph_phi[0]>3*pi/18)"
    #lumiratio = 1./(1-1./18)
    datestr   = "2020_01_30"


if options.batch:
    ROOT.gROOT.SetBatch(True)
if options.outputDir is None :
    options.outputDir = "Plots/" + __file__.rstrip(".py")
if options.outputDir is not None :
    if not os.path.isdir( options.outputDir ) :
        os.makedirs( options.outputDir )


ROOT.gStyle.SetOptStat(0)
#ROOT.gStyle.SetOptFit(1)

# if no option is given, here are the default directories to read
if options.baseDirMuG is None: options.baseDirMuG = "/data2/users/kakw/Resonances%i/LepGamma_mug_%s/"%(options.year,datestr)
if options.baseDirElG is None: options.baseDirElG = "/data2/users/kakw/Resonances%i/LepGamma_elg_%s/"%(options.year,datestr)
#options.baseDirElG = "/data/users/friccita/WGammaNtuple/LepGamma_elg_2019_04_11/"

baseel = 'ph_n==1 && el_n==1 && el_pt30_n==1 && mu_n==0'
basemu = 'ph_n==1 && mu_n==1 && mu_pt30_n==1 && el_n==0'

passpix = '&& ph_hasPixSeed[0]==0'  #Pixel seed
failpix = '&& ph_hasPixSeed[0]==1'
passcsev = '&& ph_passEleVeto[0]==1' #CSEV
failcsev = '&& ph_passEleVeto[0]==0'

phptgt = "&&ph_pt[0]>%i"
phptlt = "&&ph_pt[0]<%i"
elptgt = "&&el_pt[0]>%i"
elptlt = "&&el_pt[0]<%i"
muptgt = "&&mu_pt[0]>%i"
muptlt = "&&mu_pt[0]<%i"
metgt = "&&met_pt[0]>%i"
metlt = "&&met_pt[0]<%i"

phpt50 = "&&ph_pt[0]>50"
phpt80 = "&&ph_pt[0]>80"
elpt40 = "&&el_pt[0]>40"
metlt25 = '&&met_pt<25'
metgt25 = '&&met_pt>25'
metlt40 = '&&met_pt<40'
metgt40 = '&&met_pt>40'

ph_eb =  ' && ph_IsEB[0]'
el_eb =  ' &&abs(el_eta[0])<2.1'

invZ = '&& abs(m_lep_ph-91)>15'
massZ = '&& abs(m_lep_ph-91)<15'
flatphi = "ph_phi[0]+3.1416*(1+2*(ph_eta[0]>0))"

weight="PUWeight*NLOWeight"
pie = 3.1416

## read MuG samples
sampManMuG= SampleManager( options.baseDirMuG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio,
                            readHists=False , weightHistName = "weighthist")

## read ElG samples
sampManElG= SampleManager( options.baseDirElG, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio ,
                            readHists=False , weightHistName = "weighthist")

## read MuMu samples
sampManMuMu= SampleManager( options.baseDirMuMu, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio,
                            readHists=False , weightHistName = "weighthist")

## read ElEl samples
sampManElEl= SampleManager( options.baseDirElEl, _TREENAME, filename=_FILENAME, xsFile=_XSFILE, lumi=_LUMI*lumiratio ,
                            readHists=False , weightHistName = "weighthist")
