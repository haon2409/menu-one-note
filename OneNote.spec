# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['menu_one_note.py'],
    pathex=[],
    binaries=[],
    datas=[('one_note_have_text_icon.png', '.'), ('one_note_no_text_icon.png', '.'), ('note.txt', '.'), ('lined_background.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OneNote',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['one_note_have_text_icon.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OneNote',
)
app = BUNDLE(
    coll,
    name='OneNote.app',
    icon='one_note_have_text_icon.png',
    bundle_identifier='com.yourcompany.onenote',
)
