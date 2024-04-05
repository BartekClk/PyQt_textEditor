from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QColorDialog

class CustomFont:
    def __init__(self, custom) -> None:
        self.textEditor = custom.textEdit

    def getColor(self):
        colorDialog = QColorDialog()
        color = colorDialog.getColor()

        if color.isValid():
            return color
        else:
            return None

    def checkIfBold(self):
        cursor = self.textEditor.textCursor()
        if cursor.hasSelection() and not cursor.atBlockStart() and cursor.position() == cursor.selectionStart():
            cursor.setPosition(cursor.selectionEnd())
        is_bold = cursor.charFormat().fontWeight() == QFont.Weight.Bold
        self.isBold = is_bold

    def checkIfItalic(self):
        cursor = self.textEditor.textCursor()
        if cursor.hasSelection() and not cursor.atBlockStart() and cursor.position() == cursor.selectionStart():
            cursor.setPosition(cursor.selectionEnd())
        is_italic = cursor.charFormat().fontItalic()
        self.isItalic = is_italic

    def checkIfUnderline(self):
        cursor = self.textEditor.textCursor()
        if cursor.hasSelection() and not cursor.atBlockStart() and cursor.position() == cursor.selectionStart():
            cursor.setPosition(cursor.selectionEnd())
        is_underline = cursor.charFormat().fontUnderline()
        self.isUnderline = is_underline

    def setBoldText(self):
        cursor = self.textEditor.textCursor()

        if cursor.hasSelection() and not cursor.atBlockStart() and cursor.position() == cursor.selectionStart():
            cursor.setPosition(cursor.selectionEnd())

        is_bold = cursor.charFormat().fontWeight() == QFont.Weight.Bold
        self.isBold = is_bold

        new_weight = QFont.Weight.Normal if is_bold else QFont.Weight.Bold

        self.textEditor.setFontWeight(new_weight)

    def setItalicText(self):
        cursor = self.textEditor.textCursor()

        if cursor.hasSelection() and not cursor.atBlockStart() and cursor.position() == cursor.selectionStart():
            cursor.setPosition(cursor.selectionEnd())

        is_italic = cursor.charFormat().fontItalic()
        self.isItalic = is_italic

        new_italic = not is_italic
        self.textEditor.setFontItalic(new_italic)

    def setUnderlineText(self):
        cursor = self.textEditor.textCursor()

        if cursor.hasSelection() and not cursor.atBlockStart() and cursor.position() == cursor.selectionStart():
            cursor.setPosition(cursor.selectionEnd())

        is_underline = cursor.charFormat().fontUnderline()
        self.isUnderline = is_underline

        new_underline = not is_underline
        self.textEditor.setFontUnderline(new_underline)