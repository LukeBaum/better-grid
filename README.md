# Better Grid
A more useful grid than the one bundled with ImageJ when you need an accurate preview of a grid with offsets

## Purpose

Better Grid is an ImageJ (Fiji) extension to be used in place of the standard Grid command bundled with ImageJ. (As of the time of this writing, the built-in Grid command is accessed from the Analyze Menu: Analyze -> Tools -> Grid...)

Specifically, Better Grid shows you a true preview of what the grid overlay will look like. This is much different than the functionality of the built-in Grid command where the preview is often incorrect or outdated and the placement of the overlay moves after clicking "OK". With Better Grid, the grid overlay remains where you see it in the preview after you click "OK".

## Features Compared to Built in Grid

Below is a complete feature comparison to help you determine when to use the built-in grid and when to use Better Grid.

- Differences
  - Offsets
    - Grid: You can center the grid on the image or position the grid with a random offset from the edges of the image, without a reliable preview of where the grid will actually wind up
    - Better Grid: You can position the grid with or without an offset you specify, either by pixel or image unit (microns, etc.) with a real-time preview
  - Grid type
    - Grid: Choose from six different types
    - Better Grid: Only a solid-line grid is available (equivalent to "Lines" in built-in Grid)
  - Area
    - Grid: The user must specify the area per "point" using the image unit (microns^2, etc.)
    - Better Grid: The user can specify the area per cell in either image units or pixels
  - Line Color:
    - Grid: Choose from one of nine basic colors
    - Better Grid: Choose almost any color imaginable through use of a color picker
- Same
  - The ability to use bold gridlines
  - Options persist between runs

## Installation

### Update Site Installation

If you want to use Better Grid in a production manner (you want to use it and don't intend to make your own changes), the preferred installation method is to add an update site to ImageJ.

To do this, under the Help menu, choose "Update...", then click the "Manage update sites" button.

Click the "Add update site" button. In the new row that is added to the list, fill out only the first two fields. In the name column, put "Better Grid". In the URL column, put "http://bettergrid.trimd.com/".

Make sure the checkbox for the site is checked, and click the "Close" button. You should now see the files to be installed. Proceed, and restart ImageJ.

### Manual Installation

If you want to make your own changes or manually install the plugin for any reason, start by cloning a local copy of this repository or downloading a copy of it.

Once you do, enter the "src" subfolder. Inside, you'll see two more subfolders: "jars" and "plugins".

You essentially want to copy these two folders into your Fiji folder. You should simply be able to copy and paste the folders and the operating system will "merge" the new ones with the existing file structure.

Optional: once you do this, you can go to the /jars/Lib subfolder inside your Fiji folder. You should see a subfolder here called "bettergrid". If you wish, you can place that folder in a .zip file (bettergrid.zip) and rename it to bettergrid.jar, then delete the bettergrid folder. When Fiji is launched, it will find the script files inside the "bettergrid" folder, whether it is directly in the /jars/Lib subfolder, or inside a .jar file like /jars/Lib/bettergrid.jar. (Putting things inside a .jar file like this does not make sense when you are making edits. This is more for simplifying deployment.)

## Additional Information

- Better Grid is written in Jython.
- Better Grid keeps your preferences in a settings file.
  - On Windows, the location is <user's home folder>\AppData\Roaming\Better Grid\settings.ini
  - On Linux/Unix/macOS, the location is <user's home folder>/.Better Grid/settings.ini
  - You can move this file between computers to preserve your preferences.
- Given that Better Grid uses its own settings file, it may not be surprising that Better Grid does not use Fiji's built-in script parameters.
  - The reasons for this are
    - It is extremely difficult (if not impossible) to provide a real-time grid preview as settings are adjusted when using the automatically generated dialog from script parameters
    - Parameters with like names overwrite each other between scripts and plugins, which could lead to bizarre interactions
    - The automatically generated dialog from script parameters is rather ugly
  - While forgoing the use of built-in script parameters provides the above benefits, this also means that Better Grid cannot be used in headless mode.
