from yapsy.PluginManager import PluginManager

print("Iniciado")

# Build the manager
simplePluginManager = PluginManager()
# Tell it the default place(s) where to find plugins
simplePluginManager.setPluginPlaces(["modules"])
# Load all plugins
simplePluginManager.collectPlugins()

plugins = simplePluginManager.getAllPlugins()
tests_by_port = {}
pluginsByPort()

def pluginsByPort():
    global plugins
    global tests_by_port

    tests = {}

    for i in plugins:
        tests = i.get_test_list()

        for t in tests:
            p = t.get_port()
            if p in tests:
                tests[p].append(t)

    tests_by_port = tests

def reloadPlugins():
    global plugins
    simplePluginManager = PluginManager()
    simplePluginManager.setPluginPlaces(["modules"])
    plugins = simplePluginManager.getAllPlugins()
    print(plugins)
    pluginsByPort()

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

def checkIfPluginExists(pluginName):
    for plugin in plugins:
        if plugin.name == pluginName:
            return True
    return False

def getPluginIfExists(pluginName):
    for plugin in plugins:
        if plugin.name == pluginName:
            return plugin
    return None