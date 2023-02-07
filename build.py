from PyInstaller import __main__ as m

m.run([
    'main.py',
    '--name=file_organizer',
    '--icon=favicon.ico',
    '--onefile'
])
