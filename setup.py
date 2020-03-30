# -*- coding: cp936 -*-

from cx_Freeze import setup, Executable as cxExecutable
import platform

if platform.system() == 'Windows':
    # base must be set on Windows to either console or gui app
    # testpubsub is currently a console application
    base = 'Win32GUI'
    # base = 'Console'
else:
    base = None

opts = {'compressed': True,
        'create_shared_zip': False,
        }

WIN_Target = cxExecutable(
    script='MyQesGen.py',
    base=base,
    targetName=u'LoveMath.exe',
    compress=True,
    appendScriptToLibrary=False,
    appendScriptToExe=False,
    excludes={'doctest',
              'optparse', 'pickle', 'numpy', 'pydoc', 'pygame'
              },
    icon='heart.ico'
)

setup(
    name=u'�����������',
    description=u"�Զ���������������",
    version=u'1.35',
    author=u'Quinn',

    options={'build_exe': opts},
    executables=[WIN_Target]
)
