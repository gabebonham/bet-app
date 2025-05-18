# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['view\\app_view.py'],
    pathex=['app'],
    binaries=[],
    datas=[('app/generated', 'generated')],
    hiddenimports=['view.app_view', 'view.graphs.graph', 'view.graphs.visualizer', 'services.service', 'services.file_util', 'ml.gris', 'ml.betting_config'],
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
    a.binaries,
    a.datas,
    [],
    name='app_view',
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
)
