import sys
import subprocess
import os

def cmdcall(cmdlist, hostname=""):
    if hostname == "":
        cmd = cmdlist
    else:
        cmd = ['ssh', hostname] + cmdlist
    print cmd
    subprocess.call(cmd)

def main():
    if len(sys.argv) < 3:
        print "usage:", sys.argv[0], "host-name", "package1", "package2"
        exit(1)
    hostname = sys.argv[1]
    packagelist = sys.argv[2:]

    print "Hostname:", hostname
    print "Package list:", packagelist
   
    wd = os.getcwd()

    if not os.path.exists(os.path.join(wd, "tmpdir")):
        os.mkdir(os.path.join(wd, "tmpdir"))
    os.chdir(os.path.join(wd, "tmpdir"))

    cmdcall("pwd")
    cmdcall(["python", os.path.join(wd, "grabpackages.py"), 
             "-o", os.path.join(wd, "download_script")] +
             packagelist,
            hostname=hostname)
    cmdcall(["sh", os.path.join(wd, "download_script")])
    cmdcall("sudo cp *.deb /var/cache/apt/archives".split(),
            hostname=hostname)
    cmdcall("sudo apt-get install".split() + packagelist,
            hostname=hostname)
if __name__ == "__main__":
    main()
