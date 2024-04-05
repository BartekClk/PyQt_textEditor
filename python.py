from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow, QColorDialog
from PyQt6.QtGui import QPixmap, QFont, QTextCharFormat, QIntValidator
from PyQt6 import uic
from PyQt6.QtCore import Qt
import sys
import json
from customfont import CustomFont

class File_dialog(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("untitled.ui", self)
        self.ui = uic.loadUi("untitled.ui", self)

        self.fonts = CustomFont(self)

        self.initEditMenu()

        self.textEdit = self.ui.textEdit

        self.changeFontSize()

        self.fontSelect.currentFontChanged.connect(self.changeFont)

        self.show()

    def importIcons(self):
        with open(self.jsonPath_icons, 'r') as file:
            json_data = json.load(file)
        return(json_data)
    
    def setIcon(self, element, iconPath, iconScale=0.8, alignVertically=True, keepAspectRatio=True):
        labelSize = element.size()

        svg_data = iconPath

        pixmap = QPixmap()
        pixmap.loadFromData(svg_data.encode())
        if keepAspectRatio:
            pixmap = pixmap.scaled(int(labelSize.width()*iconScale), int(labelSize.height()*iconScale), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        else:
            pixmap = pixmap.scaled(labelSize.width(), labelSize.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pixmapHeight = pixmap.height()

        element.setPixmap(pixmap)
        element.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if alignVertically:
            verticalOffset = int((labelSize.height() - pixmapHeight) / 2)+1
            element.setContentsMargins(0, verticalOffset, 0, 0)
        pass

    def initEditMenu(self):
        self.minimumFontSize = 4
        self.maximumFontSize = 500

        self.jsonPath_icons = "icons.json"
        self.jsonIcons = self.importIcons()

        self.isBold = False
        self.isItalic = False
        self.isUnderline = False

        self.undo = self.ui.undo
        self.redo = self.ui.redo
        self.fontSelect = self.ui.font
        self.fontSize = self.ui.fontSize
        self.minusSize = self.ui.minusSize
        self.plusSize = self.ui.plusSize
        self.bold = self.ui.bold
        self.italic = self.ui.italic
        self.underline = self.ui.underline
        self.textColor = self.ui.textColor
        self.bgColor = self.ui.selectColor
        self.alignJustify = self.ui.alignJustify
        self.alignLeft = self.ui.alignLeft
        self.alignCenter = self.ui.alignCenter
        self.alignRight = self.ui.alignRight

        self.actionSave = self.ui.actionSave
        self.actionSave_as = self.ui.actionSave_as
        self.actionOpen = self.ui.actionOpen

        font = QFont()
        font.setPointSize(12)
        self.textEdit.document().setDefaultFont(font)
        
        self.spacers = [self.ui.spacer_1, self.ui.spacer_2, self.ui.spacer_3, self.ui.spacer_4, self.ui.spacer_6]
        for spacer in self.spacers:
            self.setIcon(spacer, self.jsonIcons["verticalLine"], iconScale=0.8, alignVertically=True, keepAspectRatio=True)

        self.setIcon(self.undo, self.jsonIcons["undoArrow"])
        self.setIcon(self.redo, self.jsonIcons["redoArrow"])
        self.setIcon(self.minusSize, self.jsonIcons["minusSize"])
        self.setIcon(self.plusSize, self.jsonIcons["plusSize"])
        self.setIcon(self.bold, self.jsonIcons["bold"])
        self.setIcon(self.italic, self.jsonIcons["italic"])
        self.setIcon(self.underline, self.jsonIcons["underline"])
        self.setIcon(self.textColor, self.jsonIcons["textColor"])
        self.setIcon(self.bgColor, self.jsonIcons["backgroundColor"])
        self.setIcon(self.alignJustify, self.jsonIcons["alignJustify"])
        self.setIcon(self.alignLeft, self.jsonIcons["alignLeft"])
        self.setIcon(self.alignCenter, self.jsonIcons["alignCenter"])
        self.setIcon(self.alignRight, self.jsonIcons["alignRight"])

        onlyInt = QIntValidator()
        onlyInt.setRange(self.minimumFontSize, self.maximumFontSize)
        self.fontSize.setValidator(onlyInt)
        self.fontSize.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.textEdit.setFocus()
        self.textEdit.selectionChanged.connect(self.onSelectionChange)

        self.undo.clicked.connect(self.onUndo)
        self.redo.clicked.connect(self.onRedo)

        self.minusSize.clicked.connect(self.onMinusSize)
        self.plusSize.clicked.connect(self.onPlusSize)

        self.fontSize.editingFinished.connect(self.changeFontSize)

        self.bold.clicked.connect(self.toggleBold)
        self.italic.clicked.connect(self.toggleItalic)
        self.underline.clicked.connect(self.toggleUnderline)

        self.textColor.clicked.connect(self.setColor)
        self.bgColor.clicked.connect(self.setBgColor)

        self.alignJustify.clicked.connect(lambda: self.setTextAlignment(Qt.AlignmentFlag.AlignJustify))
        self.alignLeft.clicked.connect(lambda: self.setTextAlignment(Qt.AlignmentFlag.AlignLeft))
        self.alignCenter.clicked.connect(lambda: self.setTextAlignment(Qt.AlignmentFlag.AlignCenter))
        self.alignRight.clicked.connect(lambda: self.setTextAlignment(Qt.AlignmentFlag.AlignRight))

        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.saveAs)
        self.actionOpen.triggered.connect(self.openFile)

        

    def onSelectionChange(self):
        self.fontSizeOnSelectionChange()
        self.checkIfBold()
        self.checkIfItalic()
        self.checkIfUnderline()

    def onUndo(self):
        self.textEdit.undo()
        self.fontSizeOnSelectionChange()
        pass

    def onRedo(self):
        self.textEdit.redo()
        self.fontSizeOnSelectionChange()
        pass

    def changeFont(self):
        font = self.fontSelect.currentFont()
        cursor = self.textEdit.textCursor()
        selected_text = cursor.selectedText()

        if len(selected_text) > 0:
            char_format = QTextCharFormat()
            char_format.setFont(font)
            cursor.mergeCharFormat(char_format)
        else:
            self.textEdit.setCurrentFont(font)

    def onMinusSize(self):
        size = self.fontSize.text()
        size = int(size)
        if size > self.minimumFontSize:
            size -= 1
        self.fontSize.setText(str(size))
        self.changeFontSize()

    def onPlusSize(self):
        size = self.fontSize.text()
        size = int(size)
        if size < self.maximumFontSize:
            size += 1
        self.fontSize.setText(str(size))
        self.changeFontSize()

    def changeFontSize(self):
        font_size_text = self.fontSize.text()
        try:
            font_size = float(font_size_text)
        except ValueError:
            return

        cursor = self.textEdit.textCursor()
        selected_text = cursor.selectedText()

        if len(selected_text) > 0:
            char_format = QTextCharFormat()
            char_format.setFontPointSize(font_size)
            cursor.mergeCharFormat(char_format)
        else:
            self.textEdit.setFontPointSize(font_size)
    
    def fontSizeOnSelectionChange(self):
        cursor = self.textEdit.textCursor()
        char_format = cursor.charFormat()
        font_size = int(char_format.fontPointSize())
        self.fontSize.setText(str(font_size))

    def checkIfBold(self):
        self.fonts.checkIfBold()
        self.isBold = self.fonts.isBold
        if self.isBold:
            self.bold.setStyleSheet("QLabel { background-color : gray;}")
        else:
            self.bold.setStyleSheet("")

    def checkIfItalic(self):
        self.fonts.checkIfItalic()
        self.isItalic = self.fonts.isItalic
        if self.isItalic:
            self.italic.setStyleSheet("QLabel { background-color : gray;}")
        else:
            self.italic.setStyleSheet("")

    def checkIfUnderline(self):
        self.fonts.checkIfUnderline()
        self.isUnderline = self.fonts.isUnderline
        if self.isUnderline:
            self.underline.setStyleSheet("QLabel { background-color : gray;}")
        else:
            self.underline.setStyleSheet("")

    def toggleBold(self):
        self.fonts.setBoldText()
        self.checkIfBold()
    
    def toggleItalic(self):
        self.fonts.setItalicText()
        self.checkIfItalic()

    def toggleUnderline(self):
        self.fonts.setUnderlineText()
        self.checkIfUnderline()

    def getColor(self):
        colorDialog = QColorDialog()
        color = colorDialog.getColor()

        if color.isValid():
            return color
        else:
            return None
    
    def setColor(self):
        color = self.getColor()
        cursor = self.textEdit.textCursor()

        if color is not None:
            self.textColor = color
            char_format = cursor.charFormat()
            char_format.setForeground(color)
            cursor.setCharFormat(char_format)

    def setBgColor(self):
        color = self.getColor()
        cursor = self.textEdit.textCursor()

        if color is not None:
            self.bgColor = color
            char_format = cursor.charFormat()
            char_format.setBackground(color)
            cursor.setCharFormat(char_format)

    def setTextAlignment(self, alignment):
        document = self.textEdit.document()
        option = document.defaultTextOption()
        option.setAlignment(alignment)
        document.setDefaultTextOption(option)

    def insertUnorderedList(self):
        cursor = self.textEdit.textCursor()
        cursor.insertHtml("<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>")

    def save(self):
        if not hasattr(self, 'current_file'):
            self.saveAs()
            return

        with open(self.current_file, 'w') as f:
            text = self.textEdit.toPlainText()
            f.write(text)

    def saveAs(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);")
        if file_path:
            self.current_file = file_path
            self.save()

    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if file_path:
            self.current_file = file_path
            with open(file_path, 'r') as f:
                content = f.read()
                self.textEdit.setText(content)

app=QApplication(sys.argv)
file_dialog=File_dialog()
sys.exit(app.exec())