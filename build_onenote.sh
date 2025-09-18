pyinstaller --noconfirm --onedir --windowed \
  --icon=one_note_icon.icns \
  --add-data "one_note_have_text_icon.png:." \
  --add-data "one_note_no_text_icon.png:." \
  --add-data "note.txt:." \
  --add-data "lined_background.png:." \
  --name OneNote \
  --osx-bundle-identifier com.yourcompany.onenote \
  menu_one_note.py
