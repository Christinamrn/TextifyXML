# TextifyXML

![image](/logo/TextifyXML_png.png)

### Presentation

I created this little app following a discussion with a friend who was struggling to find a way to convert his XML files exported from [TACTEO](https://tacteo.huma-num.fr/) while keeping only the text, not the XML tags. Online, it was impossible to find a website or an application that could reach his expectations. Some of them still included the tags, others needed to copy and paste texts but no upload and/or download features. That's the reason why I decided to a create a solution by myself. A simple one using _python_ and _Tkinter_. My friend doesn't know anything about coding so I used __PyInstaller__ to have TextifyXML directly as an application. It works with all OS.

I made a first version which was just a button to select a file then it created a text file copying the same filename. It was great but a bit limited for someone who needed to convert __plenty__ of files into __one single__ text file.

[Update : v1.1 - 17/02/26] I did a new version also supported by __macOS__ with __Intel__ processors. I had to use _PyQt6_ instead of _tkinter_. The new file is named `TextifyXML-qt.py` and has similar functions. Upcoming features will only be develop for PyQt6 version.

### About this version
This version includes :
- Add one or multiples XML files
- XML files are displayed in a list
- Remove a file
- Have duplicate XML files
- Move a file up or down in the list
- Drag and drop to change the order of a file in the list
- Alphabetical order option (or reversed)
- Preview for each file (XML and TXT)
- Add a personalised output filename
- Save the output file

[Update : v1.2 - 22/02/26]
- Add multiple files with drag and drop
- Multiple selection
- Suppr as a keyboard shortcut
- Preview before saving for the output file
- Add/Remove horizontal line as a separator between files translated in the output file

### Convert your XML files with TextifyXML
The following command lines are for the PyQt6 version. To use the tk version, replace `TextifyXML-qt.py` by  `TextifyXML-tk.py`.

#### Command line
To run TextifyXML directly from the source using Python.
```bash
python TextifyXML-qt.py
```

#### PyInstaller
To run TextifyXML as a standalone application, build it using the appropriate command for your operating system. The executable will be available in the `/dist` directory.
##### Windows (.exe)
```bash
python -m PyInstaller --onefile --windowed --icon ".\logo\TextifyXML_ico.ico" --add-data ".\logo\TextifyXML_png.png;logo" --name "TextifyXML" TextifyXML-qt.py
```

##### macOS (.app)
```bash
python -m PyInstaller --onefile --windowed --icon "./logo/TextifyXML_icns.icns" --add-data "./logo/TextifyXML_png.png:logo" --name "TextifyXML" TextifyXML-qt.py
```
