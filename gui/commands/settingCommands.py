from gui.commands.switch import Switch
class settingCommands():
    def __init__(self):
        self.browseSwitch = Switch(True)
        self.deleteSwitch = Switch(True)
        self.downloadSwitch = Switch(True)
        self.executeSwitch = Switch(True)
        self.injectSwitch = Switch(True)
        self.renameSwitch = Switch(True)
        self.sysinfoSwitch = Switch(False)
        self.hideSwitch = Switch(False)
        self.startupSwitch = Switch(False)