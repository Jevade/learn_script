from setuptools import setup  
import sys  
if sys.platform == 'darwin':  
    setup(  
          app = ["showBin2.py"],  
          setup_requires=["py2app"],  
    )  