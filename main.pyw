from GUI_actions import application

if __name__ == '__main__':
    application()

# pip install PyInstaller

# В окно терминала:
# pyinstaller --onefile --icon=icon.ico main.py
# onefile если вам нужен только .exe
# Вместо icon.ico путь к вашей заранее выбранной иконке!

# Чтобы не запускалась командная строка вместе с программой
# нужно создать файл с расширением pyw (типа main.pyw)
# и указать в строке компиляции его, типа
# pyinstaller --onefile --icon=icon.ico main.pyw

# для упаковки программы в exe
# pyinstaller --onefile --icon=image/iconSearchInFile.ico Main/main.pyw

# для упаковки в exe
# python -m nuitka --onefile --standalone --plugin-enable=pyqt5 --windows-disable-console --windows-icon-from-ico=image/iconSearchInFile.ico Main/main.pyw
