# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

py_files = ['Start.py',

            'menu\\UserOption.py',
            'menu\\XmindUploadCase.py',
            'menu\\LoadCommonTest.py',

            'login\\Login.py',
            'log\\LogSql.py',

            'gui\\LoginPage.py',
            'gui\\MenuPage.py',
            'gui\\UserinfoPage.py',
            'gui\\testcase\\XmindUpdatePage.py',
            'gui\\testcase\\TestTaskPage.py',
            'gui\\LogPage.py',
            'gui\\StatisticsPage.py',
            'gui\\ChangePasswordPage.py',

            'data\\CaselibUpdataSql.py',
            'data\\BugAmountSql.py',
            'data\\TestTaskSql.py',
            'data\\CaseSql.py',
            'data\\InsertCaseSql.py',
            'data\\TestTaskSql.py',
            'data\\SqlConnect.py',
            'data\\ChangePsSql.py',

            'picture\\VersionInformation.py',
]

add_files = [
    ('picture\\xmind.ico','picture'),
    ('picture\\yingcang.png','picture'),
    ('picture\\zhanshi.png','picture'),
    ('picture\\moban.xmind','picture'),
]

a = Analysis(py_files,
             pathex=['D:\\pyproject\\GeekTest'],
             binaries=[],
             datas=add_files,
             hiddenimports=['tkcalendar',
                            'babel.numbers'],
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
          name='GeekTest',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='D:\\pyproject\\GeekTest\\picture\\xmind.ico')
