# -*- mode: python -*-

block_cipher = None

a = Analysis(['Service.py'],
             pathex=['C:\\Users\\Ramzi\\Documents\\Ramzi\\Dev\\py\\Projects\\RAT SQL\\SourceCode\\Build'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Service',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=False,
		  # icon='icon.ico'
          )
