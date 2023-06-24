from java.awt import Color
from java.lang.System import getProperty
from os.path import exists
from os import mkdir

class Settings():

    def __init__(self, attemptLoad=False):
        self.gridUnit = "pixels"
        self.cellArea = 50
        self.offsetX = 0
        self.offsetY = 0
        self.boldGridlines = False
        self.lineColor = Color.CYAN

        self.red = 0
        self.green = 0
        self.blue = 0
        self.alpha = 255

        self.isWindows = False
        if getProperty('os.name').lower().startswith('win'):
            self.isWindows = True

        self.findFilePath()

        if attemptLoad:
            self.load()

    def findFilePath(self):
        homePath = str(getProperty('user.home'))
        self.filePath = homePath + '/.Better Grid/settings.ini'
        self.fileDirectory = homePath + '/.Better Grid'
        if self.isWindows:
            self.filePath = homePath + '\\AppData\\Roaming\\Better Grid\\settings.ini'
            self.fileDirectory = homePath + '\\AppData\\Roaming\\Better Grid'

    def load(self):
        
        readablePath = self.filePath.replace('\\', '/')

        if exists(readablePath) == False:
            print "Settings file does not exist for Better Grid preferences, using base defaults."
            return False

        lines = None
        try:
            with open(readablePath, 'r') as settingsFile:
                lines = settingsFile.readlines()
        except:
            print "Could not load preferences from settings file for Better Grid."
            return False

        if len(lines) < 1:
            print "No preferences were inside the Better Grid settings file."
            return False
        
        for line in lines:

            line = line.replace('\n', '').lower()

            if line.startswith('grid_unit = '):
                x = line[12:]
                if len(x) > 0:
                    self.gridUnit = x
                    
            elif line.startswith('cell_area = '):
                x = line[12:]
                if x.isnumeric():
                    self.cellArea = self.__validateArea(int(x))
                        
            elif line.startswith('offset_x = '):
                x = line[11:]
                if x.isnumeric():
                    self.offsetX = self.__validateOffset(int(x))
                        
            elif line.startswith('offset_y = '):
                x = line[11:]
                if x.isnumeric():
                    self.offsetY = self.__validateOffset(int(x))
                        
            elif line.startswith('bold_gridlines = '):
                x = line[17:]
                if x == 'true':
                    self.boldGridlines = True
                elif x == 'false':
                    self.boldGridlines = False
                    
            elif line.startswith('color_red = '):
                x = line[12:]
                if x.isnumeric():
                    self.red = self.__validateColor(int(x))
                
            elif line.startswith('color_green = '):
                x = line[14:]
                if x.isnumeric():
                    self.green = self.__validateColor(int(x))
                    
            elif line.startswith('color_blue = '):
                x = line[13:]
                if x.isnumeric():
                    self.blue = self.__validateColor(int(x))
                
            elif line.startswith('color_alpha = '):
                x = line[14:]
                if x.isnumeric():
                    self.alpha = self.__validateColor(int(x))

        self.lineColor = Color(self.red, self.green, self.blue, self.alpha)

    def __validateArea(self, area):
        return self.__adjustNumberToRange(3, 1000000, area)

    def __validateOffset(self, offset):
        return self.__adjustNumberToRange(0, 1000000, offset)

    def __validateColor(self, colorCode):
        return self.__adjustNumberToRange(0, 255, colorCode)

    def __adjustNumberToRange(self, minimum, maximum, number):
        if number < minimum:
            number = minimum
        elif number > maximum:
            number = maximum
        return number

    def toIniString(self):
        settings = 'grid_unit = ' + self.gridUnit + '\n'
        settings += 'cell_area = ' + str(self.cellArea) + '\n'
        settings += 'offset_x = ' + str(self.offsetX) + '\n'
        settings += 'offset_y = ' + str(self.offsetY) + '\n'
        settings += 'bold_gridlines = ' + str(self.boldGridlines).lower() + '\n'
        settings += 'color_red = ' + str(self.red) + '\n'
        settings += 'color_green = ' + str(self.green) + '\n'
        settings += 'color_blue = ' + str(self.blue) + '\n'
        settings += 'color_alpha = ' + str(self.alpha)        
        return settings

    def save(self):
        
        saveDirectory = self.fileDirectory.replace('\\', '/')
        saveFile = self.filePath.replace('\\', '/')

        try:
            if exists(saveDirectory) == False:
                mkdir(saveDirectory)
        except:
            print "Could not create directory to save Better Grid preferences."
            return False

        settings = self.toIniString()

        try:
            with open(saveFile, 'w') as writer:
                writer.write(settings)
        except:
            print "Could not write to settings file to save Better Grid preferences."
