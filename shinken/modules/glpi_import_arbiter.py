#!/usr/bin/python
#Copyright (C) 2009 Gabes Jean, naparuba@gmail.com
#
#This file is part of Shinken.
#
#Shinken is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Shinken is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Shinken.  If not, see <http://www.gnu.org/licenses/>.


#This Class is a plugin for the Shinken Arbiter. It connect to
#a GLPI with webservice (xmlrpc, SOAP is garbage) and take all
#hosts. Simple way from now


import xmlrpclib


#This text is print at the import
print "I am simple GLPI importer for Arbiter"


properties = {
    'type' : 'glpi_import',
    'external' : False,
    }


#called by the plugin manager to get a broker
def get_instance(plugin):
    print "Get a Simple GLPI importer arbiter for plugin %s" % plugin.get_name()
    uri = plugin.uri
    login_name = plugin.login_name
    login_password = plugin.login_password
    instance = Glpi_importer_arbiter(plugin.get_name(), uri, login_name, login_password)
    return instance



#Just get hostname from a GLPI webservices
class Glpi_importer_arbiter:
    def __init__(self, name, server, uri, login_name, login_password):
        self.name = name
        self.uri = uri
        self.login_name = login_name
        self.login_password = login_password
        

    #Called by Arbiter to say 'let's prepare yourself guy'
    def init(self):
        print "I open the GLPI connexion to %s" % self.uri
        self.con = xmlrpclib.ServerProxy(uri)
        print "Connexion opened"
        print "Authentification in progress"
        arg = {'login_name' : self.login_name , 'login_password' : self.login_password}
        res = proxy.glpi.doLogin(arg)
        self.session = res['session']
        print "My session number", self.session



    def get_name(self):
        return self.name


    #Ok, main function that will load hosts from GLPI
    def get_objects(self):
        r = {'hosts' : []}
        arg = {'session' : self.session}
        all_hosts = proxy.glpi.listComputers(arg)
        print "Get all hosts", all_hosts
        for host in all_hosts:
            print "\n\n"
            print "Host info in GLPI", host
            arg = {'session' : self.session, 'computer' : host['id']}
            host_info = proxy.glpi.getComputer(arg)
            print "Host info", host_info
            h = {'host_name' : host_info['name'],
                 'alias' : host_info['name'],
                 'address' : host_info['name'],
                 #TODO : get a true field
                 'use' : 'generic-host'
                 }
            r['hosts'].append(h)
        print "Returning to Arbiter the hosts:", r
        return r
