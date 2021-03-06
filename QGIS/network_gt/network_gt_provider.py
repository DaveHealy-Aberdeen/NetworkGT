# -*- coding: utf-8 -*-

"""
/***************************************************************************
 NetworkGT
                                 A QGIS plugin
 The NetworkGT (Network Geometry and Typology) Toolbox is a set of tools designed for the geometric and topological analysis of fracture networks.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-08-22
        copyright            : (C) 2019 by Bjorn Nyberg
        email                : bjorn.nyberg@uib.no
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Bjorn Nyberg'
__date__ = '2019-08-22'
__copyright__ = '(C) 2019 by Bjorn Nyberg'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os
from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .Branches_Nodes import BranchesNodes
from .Simple_Grid import ContourGrid
from .Simple_Line_Grid import LineGrid
from .Topology_Parameters import TopologyParameters
from .Line_Frequency import LineFrequency
from .Distribution_Analysis import DistributionAnalysis
from .Sets import Sets
from .rose_diagrams import RoseDiagrams
from .TB import TBlocks
from .BI import IBlocks
from .Clusters import Clusters
from .Repair import RepairTool
from .Histogram import Histogram

class NetworkGTProvider(QgsProcessingProvider):

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)

    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass

    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm(TopologyParameters())
        self.addAlgorithm(BranchesNodes())
        self.addAlgorithm(DistributionAnalysis())
        self.addAlgorithm(LineFrequency())
        self.addAlgorithm(TopologyParameters())
        self.addAlgorithm(LineGrid())
        self.addAlgorithm(ContourGrid())
        self.addAlgorithm(Sets())
        self.addAlgorithm(RoseDiagrams())
        self.addAlgorithm(TBlocks())
        self.addAlgorithm(IBlocks())
        self.addAlgorithm(Clusters())
        self.addAlgorithm(RepairTool())
        self.addAlgorithm(Histogram())
   
    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'NetworkGT'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('NetworkGT')

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        iconPath = os.path.join( os.path.dirname(__file__), 'icon.jpg')
        return QIcon(iconPath)

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
