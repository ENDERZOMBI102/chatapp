# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['src\\guiclient\\main.py'],
             pathex=['C:\\Users\\Flavia\\PycharmProjects\\chatapp'],
             binaries=[],
             datas=[],
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
          name='GUIClient',
          debug=False,
          bootloader_ignore_signals=False,
          strip=True,
          upx=True,
          upx_exclude=[],
          windowed=True,
          runtime_tmpdir=None,
          console=True )
