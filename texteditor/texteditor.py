import wx
import wx.lib.dialogs
import wx.stc as stc
import os

# Font face data depending on OS
if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 8,
             }
elif wx.Platform == '__WXMAC__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Monaco',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 12,
              'size2': 10,
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }

# Application Framework
class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		# variables for file i/o
		self.dirname = ''
		self.filename = ''
		self.lineNumbersEnabled = True
		self.leftMarginWidth = 25

		# Initialize the application Frame and create the Styled Text Control
		wx.Frame.__init__(self, parent, title=title, size=(800, 600))
		self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

		# Bind Ctrl + '=' and Ctrl + '-' to zooming in and out or making the text bigger/smaller
		self.control.CmdKeyAssign(ord('='), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN) # Ctrl + = to zoom in
		self.control.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT) # Ctrl + - to zoom out

		# Set some properties of the text control
		self.control.SetViewWhiteSpace(False)

		# Set margins
		self.control.SetMargins(5,0) # 5px margin on left inside of text control
		self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER) # line numbers column
		self.control.SetMarginWidth(1, self.leftMarginWidth) # width of line numbers column

		# Create the status bar at the bottom
		self.CreateStatusBar()
		self.UpdateLineCol(self) # show the line #, row # in status bar
		self.StatusBar.SetBackgroundColour((220,220,220))

		# Setting up the file menu
		filemenu = wx.Menu()
		menuNew = filemenu.Append(wx.ID_NEW, "&New", " Create a new document (Ctrl+N)")
		menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", " Open an existing document (Ctrl+O)")
		menuSave = filemenu.Append(wx.ID_SAVE, "&Save", " Save the current document (Ctrl+S)")
		menuSaveAs = filemenu.Append(wx.ID_SAVEAS, "Save &As", " Save a new document (Alt+S)")
		filemenu.AppendSeparator()
		menuClose = filemenu.Append(wx.ID_EXIT, "&Close", " Close the application (Ctrl+W)")

		# Setting up the Edit menu
		editmenu = wx.Menu()
		menuUndo = editmenu.Append(wx.ID_UNDO, "&Undo", " Undo last action (Ctrl+Z)")
		menuRedo = editmenu.Append(wx.ID_REDO, "&Redo", " Redo last action (Ctrl+Y)")
		editmenu.AppendSeparator()
		menuSelectAll = editmenu.Append(wx.ID_SELECTALL, "&Select All", " Select the entire document (Ctrl+A)")
		menuCopy = editmenu.Append(wx.ID_COPY, "&Copy", " Copy selected text (Ctrl+C)")
		menuCut = editmenu.Append(wx.ID_CUT, "C&ut", " Cut selected text (Ctrl+X)")
		menuPaste = editmenu.Append(wx.ID_PASTE, "&Paste", " Pasted text from the clipboard (Ctrl+V)")

		# Setting up the Preferences menu
		prefmenu = wx.Menu()
		menuLineNumbers = prefmenu.Append(wx.ID_ANY, "Toggle &Line Numbers", " Show/Hide the line numbers column")

		# Setting up the help menu
		helpmenu = wx.Menu()
		menuHowTo = helpmenu.Append(wx.ID_ANY, "&How To...", " Get help using the text editor (F1)")
		helpmenu.AppendSeparator()
		menuAbout = helpmenu.Append(wx.ID_ABOUT, "&About", " Read about the text editor and it's making (F2)")

		# Creating the menubar
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu, "&File")
		menuBar.Append(editmenu, "&Edit")
		menuBar.Append(prefmenu, "&Preferences")
		menuBar.Append(helpmenu, "&Help")
		self.SetMenuBar(menuBar)

		# File events
		self.Bind(wx.EVT_MENU, self.OnNew, menuNew)
		self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
		self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
		self.Bind(wx.EVT_MENU, self.OnSaveAs, menuSaveAs)
		self.Bind(wx.EVT_MENU, self.OnClose, menuClose)

		# Edit events
		self.Bind(wx.EVT_MENU, self.OnUndo, menuUndo)
		self.Bind(wx.EVT_MENU, self.OnRedo, menuRedo)
		self.Bind(wx.EVT_MENU, self.OnSelectAll, menuSelectAll)
		self.Bind(wx.EVT_MENU, self.OnCopy, menuCopy)
		self.Bind(wx.EVT_MENU, self.OnCut, menuCut)
		self.Bind(wx.EVT_MENU, self.OnPaste, menuPaste)

		# Preference events
		self.Bind(wx.EVT_MENU, self.OnToggleLineNumbers, menuLineNumbers)

		# Help events
		self.Bind(wx.EVT_MENU, self.OnHowTo, menuHowTo)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

		# Key bindings
		self.control.Bind(wx.EVT_CHAR, self.OnCharEvent)
		self.control.Bind(wx.EVT_KEY_UP, self.UpdateLineCol)
		self.control.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

		# go ahead and display the application
		self.Show()


	# New document menu action
	def OnNew(self, e):
		# Empty the instance variable for current filename, and the main text box's content
		self.filename = ""
		self.control.SetValue("")

	# Open existing document menu action
	def OnOpen(self, e):
		# First try opening the existing file; if it fails, the file doesn't exist most likely
		try:
			dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.FD_OPEN)
			if (dlg.ShowModal() == wx.ID_OK):
				self.filename = dlg.GetFilename()
				self.dirname = dlg.GetDirectory()
				f = open(os.path.join(self.dirname, self.filename), 'r')
				self.control.SetValue(f.read())
				f.close()
			dlg.Destroy()
		except:
			dlg = wx.MessageDialog(self, " Couldn't open file", "Error 009", wx.ICON_ERROR)
			dlg.ShowModal()
			dlg.Destroy()

	# Save the document menu action
	def OnSave(self, e):
		# First try just saving the existing file, but if that file doesn't
		# exist it will fail, and the except will launch the Save As.
		try:
			f = open(os.path.join(self.dirname, self.filename), 'w')
			f.write(self.control.GetValue())
			f.close()
		except:
			try:
				# If regular save fails, try the Save As method.
				dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
				if (dlg.ShowModal() == wx.ID_OK):
					self.filename = dlg.GetFilename()
					self.dirname = dlg.GetDirectory()
					f = open(os.path.join(self.dirname, self.filename), 'w')
					f.write(self.control.GetValue())
					f.close()
				dlg.Destroy()
			except:
				pass

	# Save a new document menu action
	def OnSaveAs(self, e):
		try:
			dlg = wx.FileDialog(self, "Save file as", self.dirname, self.filename, "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
			if (dlg.ShowModal() == wx.ID_OK):
				self.filename = dlg.GetFilename()
				self.dirname = dlg.GetDirectory()
				f = open(os.path.join(self.dirname, self.filename), 'w')
				f.write(self.control.GetValue())
				f.close()
			dlg.Destroy()
		except:
			pass

	# Terminate the program menu action
	def OnClose(self, e):
		self.Close(True)

	# Undo event menu action
	def OnUndo(self, e):
		self.control.Undo()

	# Redo event menu action
	def OnRedo(self, e):
		self.control.Redo()

	# Select All text menu action
	def OnSelectAll(self, e):
		self.control.SelectAll()

	# Copy selected text menu action
	def OnCopy(self, e):
		self.control.Copy()

	# Cut selected text menu action
	def OnCut(self, e):
		self.control.Cut()

	# Paste text from clipboard menu action
	def OnPaste(self, e):
		self.control.Paste()

	# Toggle Line numbers menu action
	def OnToggleLineNumbers(self, e):
		if (self.lineNumbersEnabled):
			self.control.SetMarginWidth(1,0)
			self.lineNumbersEnabled = False
		else:
			self.control.SetMarginWidth(1, self.leftMarginWidth)
			self.lineNumbersEnabled = True

	# Show How To menu action
	def OnHowTo(self, e):
		# Simple display the How To from HowTo.txt in a modal window
		f = open("HowTo.txt", "r")
		msg = f.read()
		f.close()
		dlg = wx.lib.dialogs.ScrolledMessageDialog(self, msg, "How To:", size=(400, 500))
		dlg.ShowModal()
		dlg.Destroy()

	# Show About menu action
	def OnAbout(self, e):
		# Simple display a modal window telling about the application
		dlg = wx.MessageDialog(self, "An elegant, yet simple, text editor made with Python and wxPython.\nCreated by Aman Pandit\n25/03/2021\nVersion 1.0.0\nInspired by Zachary King\n", "About My Text Editor", wx.OK)
		dlg.ShowModal()
		dlg.Destroy()

	# Update the Line/Col in status bar
	def UpdateLineCol(self, e):
		line = self.control.GetCurrentLine() + 1
		col = self.control.GetColumn(self.control.GetCurrentPos())
		stat = "Line %s, Column %s" % (line, col)
		self.StatusBar.SetStatusText(stat, 0)

	# Left mouse up
	def OnLeftUp(self, e):
		# This way if you click on another position in the text box
		# it will update the line/col number in the status bar (like it should)
		self.UpdateLineCol(self)
		e.Skip()

	# Char event
	def OnCharEvent(self, e):
		# These are keyboard shortcuts.
		# Some of these are very unstable and
		# may only work on Windows currently.
		keycode = e.GetKeyCode()
		controlDown = e.CmdDown()
		altDown = e.AltDown()
		shiftDown = e.ShiftDown()
		#print(keycode) # helps with testing
		if (keycode == 14): # Ctrl + N
			self.OnNew(self)
		elif (keycode == 15): # Ctrl + O
			self.OnOpen(self)
		elif (keycode == 19): # Ctrl + S
			self.OnSave(self)
		elif (altDown and (keycode == 115)): # Alt + S
			self.OnSaveAs(self)
		elif (keycode == 23): # Ctrl + W
			self.OnClose(self)
		elif (keycode == 1): # Ctrl + A
			self.OnSelectAll(self)
		elif (keycode == 340): # F1
			self.OnHowTo(self)
		elif (keycode == 341): # F2
			self.OnAbout(self)
		else:
			e.Skip()


app = wx.App(False)
frame = MainWindow(None, "Text Editor")
app.MainLoop()
