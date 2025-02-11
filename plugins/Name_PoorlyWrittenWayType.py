#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Etienne Chové <chove@crans.org> 2009                       ##
## Copyrights Frédéric Rodrigo 2014-2015                                 ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from modules.OsmoseTranslation import T_
from plugins.Plugin import Plugin
import re


class P_Name_PoorlyWrittenWayType(Plugin):

    def generator(self, p):
        (p1, p2) = p.split("|")
        r = u"^(("
        start = 0
        if self.toponymie:
            r += p1[0]  # keep first leter in uppercase
            start = 1
        for c in p1[start:]:
            r += "[{0}{1}]".format(c.lower(), c.upper())
        r += r")(\.|"
        for c in p2:
            r += r"[{0}{1}]".format(c.lower(), c.upper())
        r += r")?) .*$"
        return re.compile(r)

    def init(self, logger, toponymie = False):
        Plugin.init(self, logger)
        self.toponymie = toponymie
        self.errors[702] = self.def_class(item = 5020, level = 2, tags = ['name', 'fix:chair'],
            title = T_('Badly written way name'),
            detail = T_(
'''An abbreviation is present (eg Rd instead of Road) or first letter of name is lower case.'''),
            fix = T_(
'''Write the name with all letters without an abbreviation and first letter in upper case.'''))

    def way(self, data, tags, nds):
        if u"name" not in tags or u"highway" not in tags:
            return
        name = tags["name"]
        for test in self.ReTests:
            if not name.startswith("{0} ".format(test[0][1])):
                r = test[1].match(name)
                if r:
                    return {"class": 702, "subclass": test[0][0], "fix": {"name": name.replace(r.group(1), test[0][1])}}

    def relation(self, data, tags, members):
        return self.way(data, tags, None)
