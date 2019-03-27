# -*- mode: python -*-

block_cipher = None


a = Analysis(['microblog.py'],
             pathex=['/Users/ryan/Class Projects/@ Stream - General IT/4 - Dynamic Website Construction/Projects/2018S2 - In Class/DynamicWeb'],
             binaries=[],
             datas=[('app/templates', 'templates'), ('app/static', 'static')],
             hiddenimports=['alembic','altgraph','click','ecdsa','esptool','Flask','Flask-Login','Flask-Migrate','Flask-SQLAlchemy','Flask-WTF','future','itsdangerous','Jinja2','macholib','Mako','MarkupSafe','pefile','pur','pyaes','PyInstaller','pyserial','python-dateutil','python-editor','six','SQLAlchemy','Werkzeug','WTForms'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))
    return extra_datas


a.datas += extra_datas("app/static")
a.datas += extra_datas("app/templates")
a.datas += extra_datas("app")



pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='microblog',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='microblog.app',
             icon=None,
             bundle_identifier=None)




