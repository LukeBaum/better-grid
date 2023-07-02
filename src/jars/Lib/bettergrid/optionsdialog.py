from ij.gui import GenericDialog, Overlay, Line
from javax.swing import JDialog, JLabel, JButton, JCheckBox, JRadioButton, ButtonGroup, JSpinner, SpinnerNumberModel, JColorChooser
from java.awt import Color
from javax.swing.event import ChangeListener
from java.awt.event import ItemListener, ItemEvent
import math
from bettergrid.settings import Settings

class OptionsDialog(JDialog):

        squaredString = u'\u00B2'

	def __init__(self, imp):
	
		# Only continue if there is an active image.
		self.imp = imp
	
		# Get the main Fiji window	
		gd = GenericDialog("Better Grid Options")
		fijiWindow = gd.getOwner()
		gd.dispose()
		
		# Initialize the dialog		
		JDialog.__init__(self, fijiWindow, "Better Grid...", True)
		self.setDefaultCloseOperation(JDialog.HIDE_ON_CLOSE)
		self.setLayout(None)
		self.setResizable(False)
		self.setSize(305, 325)
		self.setLocationRelativeTo(None)
		
		# Boolean describing whether the user cancelled (Closed) or continued (pressed OK)
		self.userCanceled = True
		
		# The overlay we're making.
		self.overlay = Overlay()
		self.imp.setOverlay(self.overlay)
		
		# Initialize some values.
		
		cal = self.imp.getCalibration()
		self.unit = cal.getUnit()
		if self.unit.endswith("s") == False:
			self.unit = self.unit + "s"
		self.pixelWidth = cal.pixelWidth
		self.pixelHeight = cal.pixelHeight
		
		# The components on the dialog.
		
		SpinnerHandler = SpinnerListener()
		SpinnerHandler.setParentDialog(self)
		RadioHandler = RadioListener()
		RadioHandler.setParentDialog(self)
		
		self.okButton = JButton("OK", actionPerformed = self.eventOkClicked)
		self.cancelButton = JButton("Cancel", actionPerformed = self.eventCancelClicked)
		
		self.unitLabel = JLabel("Grid Unit:")
		
		unitButtonGroup = ButtonGroup()
		
		self.unitPixelsRadioButton = JRadioButton("pixels" + OptionsDialog.squaredString, False)
		self.unitOtherRadioButton = JRadioButton("N/A", False)
			
		unitButtonGroup.add(self.unitPixelsRadioButton)
		unitButtonGroup.add(self.unitOtherRadioButton)

		self.options = Settings(True)
		
		self.cellAreaLabel = JLabel("Cell Area (pixels" + OptionsDialog.squaredString + "):")
		self.cellAreaSpinner = JSpinner(SpinnerNumberModel(self.options.cellArea, 3, 1000000, 1))
		
		self.gridXOffsetLabel = JLabel("Grid X Offset (pixels):")
		self.gridXOffsetSpinner = JSpinner(SpinnerNumberModel(self.options.offsetX, 0, 1000000, 1))
		
		self.gridYOffsetLabel = JLabel("Grid Y Offset (pixels):")
		self.gridYOffsetSpinner = JSpinner(SpinnerNumberModel(self.options.offsetY, 0, 1000000, 1))
		
		for spinner in [self.cellAreaSpinner, self.gridXOffsetSpinner, self.gridYOffsetSpinner]:
			editor = spinner.getEditor()
			textbox = editor.getComponent(0)
			formatter = textbox.getFormatter()
			formatter.setCommitsOnValidEdit(True)
			spinner.addChangeListener(SpinnerHandler)
		
		self.lineBoldCheckbox = JCheckBox("Bold gridlines", self.options.boldGridlines)
		self.lineBoldCheckbox.addChangeListener(SpinnerHandler)
		
		self.lineColorChooser = JColorChooser(self.options.lineColor)
		
		self.lineColorChooserButton = JButton("Change gridline color...", actionPerformed = self.eventColorChooserButtonClicked)
		
		if self.unit is None:
			self.unitPixelsRadioButton.setSelected(True)
			self.unitOtherRadioButton.setVisible(False)
		elif self.unit == "pixels":
			self.unitPixelsRadioButton.setSelected(True)
			self.unitOtherRadioButton.setVisible(False)
		else:
			self.cellAreaLabel.setText("Cell Area (" + self.unit + OptionsDialog.squaredString + "):")
			self.unitOtherRadioButton.setSelected(True)
			self.unitOtherRadioButton.setText(self.unit + OptionsDialog.squaredString)
			self.unitOtherRadioButton.addItemListener(RadioHandler)
			self.gridXOffsetLabel.setText("Grid X Offset (" + self.unit + "):")
			self.gridYOffsetLabel.setText("Grid Y Offset (" + self.unit + "):")
		
		self.add(self.unitLabel)
		self.unitLabel.setBounds(20, 20, 75, 25)
		
		self.add(self.unitPixelsRadioButton)
		self.unitPixelsRadioButton.setBounds(150, 20, 60, 25)
		
		self.add(self.unitOtherRadioButton)
		self.unitOtherRadioButton.setBounds(212, 20, 70, 25)
		
		self.add(self.cellAreaLabel)
		self.cellAreaLabel.setBounds(20, 50, 150, 25)
		
		self.add(self.cellAreaSpinner)
		self.cellAreaSpinner.setBounds(180, 50, 100, 25)
		
		self.add(self.gridXOffsetLabel)
		self.gridXOffsetLabel.setBounds(20, 80, 150, 25)
		
		self.add(self.gridXOffsetSpinner)
		self.gridXOffsetSpinner.setBounds(180, 80, 100, 25)
		
		self.add(self.gridYOffsetLabel)
		self.gridYOffsetLabel.setBounds(20, 110, 150, 25)
		
		self.add(self.gridYOffsetSpinner)
		self.gridYOffsetSpinner.setBounds(180, 110, 100, 25)
		
		self.add(self.lineBoldCheckbox)
		self.lineBoldCheckbox.setBounds(20, 170, 100, 25)
		
		self.add(self.lineColorChooserButton)
		self.lineColorChooserButton.setBackground(self.options.lineColor)
		self.lineColorChooserButton.setBounds(120, 170, 160, 25)
		
		self.add(self.okButton)
		self.okButton.setBounds(110, 245, 80, 25)
		
		self.add(self.cancelButton)
		self.cancelButton.setBounds(200, 245, 80, 25)
		
		self.drawGrid()
		
		
	def eventOkClicked(self, event):
		self.userCanceled = False
		self.options.save()
		self.setVisible(False)
		
	def eventCancelClicked(self, event):
		self.setVisible(False)
		
	def eventColorChooserButtonClicked(self, event):
		selectedColor = JColorChooser.showDialog(self, "Choose Gridline Color", self.lineColorChooserButton.getBackground())
		if selectedColor is not None:
			self.lineColorChooserButton.setBackground(selectedColor)
			self.options.red = selectedColor.getRed()
			self.options.green = selectedColor.getGreen()
			self.options.blue = selectedColor.getBlue()
			self.options.alpha = selectedColor.getAlpha()
			self.drawGrid()
			
	def lineBoldCheckboxCheckedChanged(self, event):
		self.drawGrid()
			
	def drawGrid(self):
		self.options.cellArea = self.cellAreaSpinner.getValue()
		cellLength = float(math.sqrt(self.options.cellArea))
		self.options.offsetX = self.gridXOffsetSpinner.getValue()
		xOffset = int(self.options.offsetX)
		self.options.offsetY = self.gridYOffsetSpinner.getValue()
		yOffset = int(self.options.offsetY)
		self.lineWidth = 1
		self.options.boldGridlines = self.lineBoldCheckbox.isSelected()
		if self.options.boldGridlines == True:
			self.lineWidth = 3
		self.options.lineColor = self.lineColorChooserButton.getBackground()
		width = self.imp.getWidth()
		height = self.imp.getHeight()
		
		self.overlay.clear()
		
		if self.unitOtherRadioButton.isSelected() == True:
                        self.options.gridUnit = self.unit
			cellLength = cellLength / self.pixelWidth
			xOffset = int(round(float(xOffset) / self.pixelHeight, 0))
			yOffset = int(round(float(yOffset) / self.pixelWidth, 0))

		cellLength = int(round(cellLength, 0))
		
		while xOffset > cellLength:
			xOffset = xOffset - cellLength
		
		for x in range(xOffset, width, cellLength):
			self.drawLine(x, 0, x, height - 1)
			
		while yOffset > cellLength:
			yOffset = yOffset - cellLength	
		
		for y in range(yOffset, height, cellLength):
			self.drawLine(0, y, width - 1, y)
			
		self.imp.setOverlay(self.overlay)
	
	def drawLine(self, x1, y1, x2, y2):
		lroi = Line(x1, y1, x2, y2)
		lroi.setStrokeColor(self.options.lineColor)
		lroi.setStrokeWidth(self.lineWidth)
		self.overlay.add(lroi)		
		
class SpinnerListener(ChangeListener):
	
	def __init__(self):
		self.parent = None
	
	def setParentDialog(self, dialog):
		self.parent = dialog
	
	def stateChanged(self, event):
		if self.parent is not None:
			self.parent.drawGrid()
			
class RadioListener(ItemListener):
	
	def __init__(self):
		self.parent = None	
		
	def setParentDialog(self, dialog):
		self.parent = dialog
				
	def itemStateChanged(self, e):
		if self.parent is not None:
			if e.getStateChange() == ItemEvent.SELECTED:
				self.parent.cellAreaLabel.setText("Cell Area (" + self.parent.unit + OptionsDialog.squaredString + "):")
				self.parent.gridXOffsetLabel.setText("Grid X Offset (" + self.parent.unit + "):")
                                self.parent.gridYOffsetLabel.setText("Grid Y Offset (" + self.parent.unit + "):")
			elif e.getStateChange() == ItemEvent.DESELECTED:
				self.parent.cellAreaLabel.setText("Cell Area (pixels" + OptionsDialog.squaredString + "):")
				self.parent.gridXOffsetLabel.setText("Grid X Offset (pixels):")
                                self.parent.gridYOffsetLabel.setText("Grid Y Offset (pixels):")
			self.parent.drawGrid()
