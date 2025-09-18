OneNote - A Simple Menu Bar Note-Taking App for macOS
Overview
OneNote is a lightweight macOS application that resides in the menu bar, allowing users to quickly take and save notes to a note.txt file. The app features a dynamic status bar icon that updates based on whether notes are present and supports basic text editing with undo/redo functionality.
Features

Menu Bar Access: Open a note-taking window from the status bar.
Dynamic Icon: Shows one_note_have_text_icon.png when notes exist, otherwise one_note_no_text_icon.png.
Plain Text Editing: Simple text input with customizable font size (16) and line spacing (5).
Auto-Save: Saves notes to note.txt after a 0.5-second delay.
Edit Menu: Includes Copy, Cut, Paste, Select All, Undo, and Redo with standard macOS shortcuts (e.g., Cmd+Z, Cmd+Shift+Z).
Persistent Notes: Notes are saved to note.txt in the app directory.

Requirements

macOS
Python 3.x
PyObjC (pip install pyobjc)
PyInstaller (pip install pyinstaller)

Installation

Clone the repository:git clone https://github.com/haon2409/menu-one-note.git
cd menu-one-note


Install dependencies:pip install pyobjc pyinstaller


Build the app:chmod +x build_onenote.sh
./build_onenote.sh


Find the built app (OneNote.app) in the dist folder.

File Structure

menu_one_note.py: Core application logic.
OneNote.spec: PyInstaller configuration for building the app.
build_onenote.sh: Script to automate the build process.
Info.plist: macOS app bundle configuration.
note.txt: Stores user notes.
one_note_have_text_icon.png: Icon for non-empty notes.
one_note_no_text_icon.png: Icon for empty notes.
lined_background.png: Unused background image (optional).
one_note_icon.icns: App icon for the macOS bundle.

Usage

Open dist/OneNote.app or build the app using the script.
Click the menu bar icon to open the note-taking window.
Type notes; they auto-save to note.txt after a 0.5-second delay.
Use Edit menu or shortcuts (e.g., Cmd+C for Copy, Cmd+Z for Undo).
Click the menu bar icon again to close the popover.

Notes

Notes are saved to /Users/haonguyen/Projects/menu/menu_one_note/note.txt. Update the path in menu_one_note.py if needed.
The LineView class for lined backgrounds is commented out but can be enabled.
The app runs as a menu bar app and persists after closing the window.

Troubleshooting

Icons not showing: Ensure one_note_have_text_icon.png, one_note_no_text_icon.png, and one_note_icon.icns are in the project directory.
Build failures: Confirm PyObjC and PyInstaller are installed.
File path issues: Adjust paths in menu_one_note.py to match your system.

License
MIT License. See LICENSE for details.