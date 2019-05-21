from yapsy.PluginManager import PluginManager

# Build the manager
simplePluginManager = PluginManager()
# Tell it the default place(s) where to find plugins
simplePluginManager.setPluginPlaces(["modules"])
# Load all plugins
simplePluginManager.collectPlugins()

plugins = simplePluginManager.getAllPlugins()

def GetPluginsNames():
    PluginNames=[]
    for plugin in plugins:
        PluginNames.append(plugin.name)
    return PluginNames

def GetPluginDescription(pluginName):
    for plugin in plugins:
        if plugin.name == pluginName:
            return plugin.description
    return "ERROR"