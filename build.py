#!python
#cython: language_level=3

import os
import shutil


targetDirName = "myProj"
currentWorkingDir = os.getcwd()
buildDirName = targetDirName + "_build"
buildDirPath = ''


def createBuild():
    if os.path.exists(buildDirName) or os.path.exists("package"):

        dlPrevDir = input("Previous files already exists. Want to remove them? Y/N: ")
        if dlPrevDir == 'Y':
            if os.path.exists("package"):
                shutil.rmtree("package")
            if os.path.exists(buildDirName):
                shutil.rmtree(buildDirName)
            # deleting Pyd files

            print("Deleted old directory.")
            createBuild()
        elif dlPrevDir == 'N':
            print("Stopped.")
        else:
            print("Enter valid input.")
            createBuild()
    else:
        buildDirPath = shutil.copytree(src=currentWorkingDir + "/" + targetDirName,
                                       dst=currentWorkingDir + "/" + buildDirName)
        createSetupFile(buildDirPath)
        removePyFiles(buildDirPath)


def createSetupFile(absolutBuildDirPath):
    f = open(os.path.join(currentWorkingDir, "setup.py"), "a+")
    f.write("""\
from Cython.Build import cythonize
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os

setup(
    cmdclass={'build_ext': build_ext},
    name="remotepy", 
    ext_modules=cythonize(\
    \"""" + absolutBuildDirPath + """\" + '**/*.py'),)""")
    f.close()
    os.system(f"python setup.py build_ext --inplace")
    os.remove(f"{currentWorkingDir}/setup.py")


def removePyFiles(buildDirPath):

    for root, dir, files in os.walk(buildDirPath):

        print(f"_____ {dir} _____")
        for file in files:
            if file.endswith(".py") or file.endswith("setup.c"):
                os.remove(os.path.join(root, file))


# deleting pyd files from root
def removePydFromRoot():
    for root, dir, files in os.walk(os.getcwd()):
        if root == os.getcwd():
            for file in files:
                if file.endswith(".pyd") and dir != "package":
                    os.remove(os.path.join(root, file))


createBuild()

# creating package directory
packageDirPath = shutil.copytree(src=currentWorkingDir,
                                       dst=currentWorkingDir + "/package")

# remove files and folders from package
shutil.rmtree(packageDirPath + "/" + buildDirName)
shutil.rmtree(packageDirPath + "/" + targetDirName)
os.remove(packageDirPath + "/build.py")

# Delete build folder from root
shutil.rmtree(currentWorkingDir + "/" + buildDirName)
shutil.rmtree(currentWorkingDir + "/build")

removePydFromRoot()

