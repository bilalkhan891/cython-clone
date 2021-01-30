#!python
#cython: language_level=3

import os
import shutil


targetDirName = "myProj"
currentWorkingDir = os.getcwd()
buildDirName = targetDirName + "_build"
buildDirPath = ''
path_separator = '/'
if os.name == 'nt':
    path_separator = '\\'

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
            print("After 2nd create build")
        elif dlPrevDir == 'N':
            print("Stopped.")
        else:
            print("Enter valid input.")
            createBuild()
    else:
        print("Copying target directory to build directory")
        print("Target: " + currentWorkingDir + path_separator + targetDirName)
        print("Build: " + currentWorkingDir + path_separator + buildDirName)
        buildDirPath = shutil.copytree(src=currentWorkingDir + path_separator + targetDirName,
                                       dst=currentWorkingDir + path_separator + buildDirName)
        createSetupFile(buildDirPath)
        removePyFiles(buildDirPath)


def createSetupFile(absolutBuildDirPath):
    f = open(os.path.join(currentWorkingDir, "setup.py"), "a+")
    print("setup file")
    print("""\
from Cython.Build import cythonize
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os

setup(
    cmdclass = {'build_ext': build_ext},
    name = "mysqleasy",
    ext_modules = cythonize('**/*.py'),
)""")
    f.write("""
from Cython.Build import cythonize
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os

setup(
    cmdclass = {'build_ext': build_ext},
    name = "mysqleasy",
    ext_modules = cythonize('**/*.py'),
)""")
    f.close()
    os.system(f"python setup.py build_ext --inplace")
    os.remove(f"{currentWorkingDir}" + path_separator + "setup.py")


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

print("Creating build ...")
createBuild()

if os.path.exists("build.c"):
    os.remove("build.c")
if os.path.exists("setup.c"):
    os.remove("setup.c")

print("Creating package directory ...")
print(currentWorkingDir+ path_separator + "package")
# creating package directory
packageDirPath = shutil.copytree(src=currentWorkingDir,
                                       dst=currentWorkingDir + path_separator + "package")
print("Removing  directory ... " +packageDirPath + path_separator + buildDirName)
# remove files and folders from package
shutil.rmtree(packageDirPath + path_separator + buildDirName)
print("Removing  directory ... " +packageDirPath + path_separator + targetDirName)
shutil.rmtree(packageDirPath + path_separator + targetDirName)
print("Removing  file ... " +packageDirPath + path_separator + "build.py")
os.remove(packageDirPath + path_separator + "build.py")

# Delete build folder from root
print("Removing directory ... " +currentWorkingDir + path_separator + buildDirName)
shutil.rmtree(currentWorkingDir + path_separator + buildDirName)
print("Removing directory ... " +currentWorkingDir + path_separator + "build")
shutil.rmtree(currentWorkingDir + path_separator + "build")

print("Removing pyd files ...")
removePydFromRoot()

