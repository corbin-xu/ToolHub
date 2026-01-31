# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['gui_app.py'],
    pathex=[],
    binaries=[],
    datas=[('templates', 'templates'), ('config.json', '.')],
    hiddenimports=['openpyxl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'PIL', 'matplotlib', 'scipy'],
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
    name='ToolHub',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='ToolHub.app',
    icon=None,
    bundle_identifier='com.corbin-xu.toolhub',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleDevelopmentRegion': 'en',
        'CFBundleLocalizations': ['en', 'zh_CN', 'zh_TW'],
    },
)
