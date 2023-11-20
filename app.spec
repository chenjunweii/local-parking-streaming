# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Project/local-parking-streaming/app.py'],
    pathex=[],
    binaries=[('C:/Project/local-parking-streaming/build/lib.win-amd64-cpython-311/wd.cp311-win_amd64.pyd', '.'), ('C:/Project/local-parking-streaming/build/lib.win-amd64-cpython-311/config.cp311-win_amd64.pyd', '.'), ('C:/Project/local-parking-streaming/build/lib.win-amd64-cpython-311/service.cp311-win_amd64.pyd', '.')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Project\\local-parking-streaming\\assets\\streaming.ico'],
)
