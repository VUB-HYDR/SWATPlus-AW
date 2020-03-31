'''
date        : 31/03/2020
description : this module coordinates the gis part of model setup

author      : Celray James CHAWANDA
contact     : celray.chawanda@outlook.com
licence     : MIT 2020
'''

import os.path
import shutil
import sys

import warnings

# skip deprecation warnings when importing PyQt5
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from qgis.core import *
    from qgis.utils import iface
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *

# QgsApplication.setPrefixPath('C:/Program Files/QGIS 3.10/apps/qgis', True)
qgs = QgsApplication([], True)
qgs.initQgis()

# Prepare processing framework 
sys.path.append('{QGIS_Dir}/apps/qgis-ltr/python/plugins'.format(
    QGIS_Dir = os.environ['QGIS_Dir'])) # Folder where Processing is located
from processing.core.Processing import Processing
Processing.initialize()

import processing

sys.path.append(os.path.join(os.environ["swatplus_wf_dir"], "packages"))
sys.path.insert(0, sys.argv[1])

from helper_functions import list_files

import atexit
import qswatplus
import namelist

from qswatplus.QSWATPlus import QSWATPlus
from qswatplus.delineation import Delineation
from qswatplus.hrus import HRUs
from qswatplus.QSWATUtils import QSWATUtils
from qswatplus.parameters import Parameters
from glob import glob

atexit.register(QgsApplication.exitQgis)


class DummyInterface(object):
    """Dummy iface to give access to layers."""

    def __getattr__(self, *args, **kwargs):
        """Dummy function."""
        def dummy(*args, **kwargs):
            return self
        return dummy

    def __iter__(self):
        """Dummy function."""
        return self

    def __next__(self):
        """Dummy function."""
        raise StopIteration

    def layers(self):
        """Simulate iface.legendInterface().layers()."""
        return list(QgsProject.instance().mapLayers().values())


if namelist.Model_2_namelist:
    sys.exit(0)

iface = DummyInterface()


# def run_qswat_plus():
plugin = QSWATPlus(iface)
dlg = plugin._odlg  # useful shorthand for later

base_dir = sys.argv[1]
projDir = "{base}/{model_name}".format(base=base_dir,
                                       model_name=namelist.Project_Name)

if not os.path.exists(projDir):
    QSWATUtils.error('Project directory {0} not found'.format(projDir), True)
    sys.exit(1)

# clean up before new files
Watershed_shapes = list_files(QSWATUtils.join(
    projDir, r'Watershed\Shapes'), "shp")
delete_shapes = []

for Watershed_shape in Watershed_shapes:
    if os.path.basename(Watershed_shape).startswith("reservoirs"):
        delete_shapes.append(Watershed_shape)
    if os.path.basename(Watershed_shape).startswith("rivs"):
        delete_shapes.append(Watershed_shape)
    if os.path.basename(Watershed_shape).startswith("subs"):
        delete_shapes.append(Watershed_shape)
    if Watershed_shape.endswith("channel.shp"):
        delete_shapes.append(Watershed_shape)
    if Watershed_shape.endswith("stream.shp"):
        delete_shapes.append(Watershed_shape)
    if Watershed_shape.endswith("subbasins.shp"):
        delete_shapes.append(Watershed_shape)
    if os.path.basename(Watershed_shape).startswith("hrus"):
        delete_shapes.append(Watershed_shape)
    if Watershed_shape.endswith("wshed.shp"):
        delete_shapes.append(Watershed_shape)
    if os.path.basename(Watershed_shape).startswith("lsus"):
        delete_shapes.append(Watershed_shape)

for delete_shape in delete_shapes:
    QSWATUtils.removeFiles(delete_shape)


shutil.rmtree(QSWATUtils.join(projDir, r'Watershed\Text'), ignore_errors=True)

projName = os.path.split(projDir)[1]
projFile = "{dir}/{nm}.qgs".format(dir=projDir, nm=projName)
shutil.rmtree(QSWATUtils.join(projDir, 'Scenarios'), ignore_errors=True)

proj = QgsProject.instance()

proj.read(projFile)
proj.read(projFile)

plugin.setupProject(proj, True)


if not (os.path.exists(plugin._gv.textDir) and os.path.exists(plugin._gv.landuseDir)):
    QSWATUtils.error('Directories not created', True)
    sys.exit(1)

if not dlg.delinButton.isEnabled():
    QSWATUtils.error('Delineate button not enabled', True)
    sys.exit(1)

delin = Delineation(plugin._gv, plugin._demIsProcessed)
delin.init()

QSWATUtils.information(
    '\n\n\t - DEM: {0}'.format(os.path.split(plugin._gv.demFile)[1]), True)

delin.addHillshade(plugin._gv.demFile, None, None, None)
QSWATUtils.information(
    '\t - Inlets/outlets file: {0}'.format(os.path.split(plugin._gv.outletFile)[1]), True)
delin.runTauDEM2()
delin.finishDelineation()
if not dlg.hrusButton.isEnabled():
    QSWATUtils.error('\t ! HRUs button not enabled', True)
    sys.exit(1)

# ensure that HRUs runs 'from files' and not from 'saved from previous run'
plugin._gv.db.clearTable('BASINSDATA')
hrus = HRUs(plugin._gv, dlg.reportsBox)
hrus.init()
hrus.readFiles()
if not os.path.exists(QSWATUtils.join(plugin._gv.textDir, Parameters._TOPOREPORT)):
    QSWATUtils.error('\t ! Elevation report not created', True)
    sys.exit(1)


if not os.path.exists(QSWATUtils.join(plugin._gv.textDir, Parameters._BASINREPORT)):
    QSWATUtils.error('\t ! Landuse and soil report not created', True)
    sys.exit(1)


hrus.calcHRUs()
if not os.path.exists(QSWATUtils.join(plugin._gv.textDir, Parameters._HRUSREPORT)):
    QSWATUtils.error('\t ! HRUs report not created', True)
    sys.exit(1)


if not os.path.exists(QSWATUtils.join(projDir, r'Watershed\Shapes\rivs1.shp')):
    QSWATUtils.error('\t ! Streams shapefile not created', True)
    sys.exit(1)


if not os.path.exists(QSWATUtils.join(projDir, r'Watershed\Shapes\subs1.shp')):
    QSWATUtils.error('\t ! Subbasins shapefile not created', True)
    sys.exit(1)


if os.path.isdir("{base}/__pycache__".format(base=sys.argv[1])):
    shutil.rmtree("{base}/__pycache__".format(base=sys.argv[1]))

print("")