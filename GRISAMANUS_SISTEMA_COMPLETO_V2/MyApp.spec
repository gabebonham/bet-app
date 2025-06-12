# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('C:\\Users\\v4lus\\Documents\\projs\\python\\eliseu\\GRISAMANUS_SISTEMA_COMPLETO_V2\\venv2\\Lib\\site-packages\\sktime\\utils\\_estimator_html_repr.css', 'sktime/utils/'), ('app/generated', 'app/generated')]
binaries = []
hiddenimports = ['app.view.app_view', 'app.view.graphs.graph', 'app.view.graphs.visualizer', 'app.services.service', 'app.services.file_util', 'app.ml.implementacao_drisamanus_corrigida', 'app.ml.prediction_processing', 'app.ml.betting_config']
tmp_ret = collect_all('app.view')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('app.services')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('app.ml')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['app\\view\\app_view.py'],
    pathex=['C:\\Users\\v4lus\\Documents\\projs\\python\\eliseu\\GRISAMANUS_SISTEMA_COMPLETO_V2'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='MyApp',
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
    name='MyApp',
)
