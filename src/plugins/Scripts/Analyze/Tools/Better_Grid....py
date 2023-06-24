from ij import IJ
from bettergrid.optionsdialog import OptionsDialog			

if __name__ == "__main__" or __name__ == "__builtin__":

	imp = None

	try:
		imp = IJ.getImage()
	except:
		print "No open images"
		
	if imp is not None:

		dialog = OptionsDialog(imp)
		dialog.setVisible(True)
		
		if dialog.userCanceled:
			dialog.overlay.clear()
			dialog.imp.setOverlay(None)
			dialog.overlay = None
			
		dialog.dispose()
