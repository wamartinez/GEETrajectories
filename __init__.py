# -*- coding: utf-8 -*-
"""
/***************************************************************************
                                 A QGIS plugin
 Get coordinates
                             -------------------
        begin                : 2021-06-24
        copyright            : (C) 2021 by William Martinez
        email                : willimarti2008@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """LoadGEETrajectories class from file GEETrajectories.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .GEETrajectories import GEETrajectories
    return GEETrajectories(iface)
