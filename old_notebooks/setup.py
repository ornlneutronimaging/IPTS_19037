from setuptools import setup, find_packages
import os
import sys

if 'help' in sys.argv[:]:
    print("MANUAL:")
    print("=======")
    print("To build interfaces")
    print("> python setup.py pyuic")
    sys.exit(0)

if 'pyuic' in sys.argv[:]:
    indir = 'designer'
    outdir = '__code'
    files = os.listdir(indir)
    files = [os.path.join('designer', item) for item in files]
    files = [item for item in files if item.endswith('.ui')]

    done = 0
    for inname in files:
        outname = inname.replace('.ui', '.py')
        outname = outname.replace(indir, outdir)
        if os.path.exists(outname):
            if os.stat(inname).st_mtime < os.stat(outname).st_mtime:
                continue
        print("Converting '%s' to '%s'" % (inname, outname))
        command = "pyuic4 %s -o %s"  % (inname, outname)
        os.system(command)
        done += 1
    if not done:
        print("Did not convert any '.ui' files")
    sys.exit(0)

