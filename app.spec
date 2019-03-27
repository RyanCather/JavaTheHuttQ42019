# -*- mode: python -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['/Users/ryan/Class Projects/@ Stream - General IT/4 - Dynamic Website Construction/Projects/2018S2 - In Class/DynamicWeb'],
             binaries=[],
             datas=[('templates', 'templates'), ('static', 'static')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
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
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='app.app',
             icon=None,
             bundle_identifier=None)
