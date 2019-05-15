from yapsy.PluginManager import PluginManager

# Build the manager
simplePluginManager = PluginManager()
# Tell it the default place(s) where to find plugins
simplePluginManager.setPluginPlaces(["modules"])
# Load all plugins
simplePluginManager.collectPlugins()

plugins = simplePluginManager.getAllPlugins()
print(plugins)