# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app\\view\\app_view.py'],
    pathex=[],
    binaries=[],
    datas=[('app\\view\\graphs\\graph.py', 'app\\view\\graphs'), ('app\\view\\graphs\\visualizer.py', 'app\\view\\graphs'), ('app\\services\\service.py', 'app\\services'), ('app\\services\\file_util.py', 'app\\services'), ('app\\ml\\implementacao_drisamanus_corrigida.py', 'app\\ml'), ('app\\ml\\betting_config.py', 'app\\ml')],
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
    name='app_view',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app_view',
)
