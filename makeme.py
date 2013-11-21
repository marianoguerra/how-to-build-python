from __future__ import print_function
import os
import platform

# sudo apt-get install apt-rdepends
# sudo apt-rdepends python3.3 | grep ^lib

UBUNTU_DEFAULT_DEPS = {
    "libs": {
        "bz2": ["libbz2-1.0", "libbz2-dev"],
        "bdb": ["libdb5.1", "libdb5.1-dev"],
        "ffi": ["libffi6", "libffi-dev"],
        "lzma": ["liblzma5", "liblzma-dev"],
        "ncurses": ["libncursesw5", "libncursesw5-dev"],
        "tinfo": ["libtinfo5", "libtinfo-dev"],
        "ssl": ["libssl1.0.0", "libssl-dev"],
        "pcre": ["libpcre3", "libpcre3-dev"],
        "readline": ["libreadline6", "libreadline6-dev"],
        "sqlite": ["libsqlite3-0", "libsqlite3-dev"],
        "expat": ["libexpat1", "libexpat1-dev"]
    },
    "install-command": "sudo apt-get install -y %s",
    "build": ["build-essential wget"]
}

DEPENDENCIES = {
    "Linux": {
        "Ubuntu": {
            "12.04": UBUNTU_DEFAULT_DEPS,
            "12.10": UBUNTU_DEFAULT_DEPS,
            "13.04": UBUNTU_DEFAULT_DEPS,
            "13.10": UBUNTU_DEFAULT_DEPS
        }
    }
}

PY_MINOR_MAX = {
    "3.3": 3,
    "3.2": 5,
    "3.1": 5,
    "3.0": 1,
    "2.7": 6,
    "2.6": 9,
    "2.5": 6,
    "2.4": 6,
    "2.3": 7,
    "2.2": 3,
    "2.1": 3,
    "2.0": 1,
    "1.6": 1,
    "1.5": 2
}

PY_ALL_MINOR = {}
PY_MINOR_LATEST = {}

for key, minor_max in PY_MINOR_MAX.items():
    PY_ALL_MINOR[key] = []
    PY_MINOR_LATEST[key] = "%s.%d" % (key, minor_max)
    for i in range(minor_max + 1):
        PY_ALL_MINOR[key].append("%s.%d" % (key, i))

PY_MAJOR_LATEST = {
    "1": "1.6.1",
    "2": "2.7.6",
    "3": "3.3.3",
}

PY_LATEST = {}
PY_LATEST.update(PY_MINOR_LATEST)
PY_LATEST.update(PY_MAJOR_LATEST)

def build_info(system, dist, version):
    return DEPENDENCIES.get(system, {}).get(dist, {}).get(version, None)

def get_source_filename(version):
    return "Python-%s.tgz" % version

def get_source_dirname(version):
    return "Python-%s" % version

def get_source_url(version):
    return "http://www.python.org/ftp/python/%s/%s" % (version,
            get_source_filename(version))

def print_instructions(py_version, prefix):
    system = platform.system()
    dist = platform.dist()
    dist_name = dist[0]
    dist_version = dist[1]
    deps = build_info(system, dist[0], dist[1])

    if deps is None:
        print("Unknown dependencies for %s %s %s" % (system, dist_name,
                dist_version))
    else:
        libs = deps["libs"]
        build_deps = deps["build"]
        command = deps["install-command"]
        all_packages = []
        for lib_name, lib_packages in libs.items():
            all_packages.extend(lib_packages)

        print("# instructions to compile python %s" % py_version)
        print("set -e")
        print("START_DIR=$(pwd)")
        print("# install build dependencies")
        print(command % " ".join(build_deps))
        print()
        print("# install lib build deps")
        print(command % " ".join(all_packages))
        print()
        print("# fetch")
        print("wget %s" % get_source_url(py_version))
        print("# extract")
        print("tar -xzf %s" % get_source_filename(py_version))
        print("# build")
        print("cd %s" % get_source_dirname(py_version))
        print("mkdir -p %s" % prefix)
        print("./configure --prefix=%s/%s && make && make install" % (prefix,
            py_version))
        print("cd $START_DIR")

if __name__ == "__main__":
    for key, py_version in PY_MINOR_LATEST.items():
        if key in {"2.4", "2.5", "2.6", "2.7", "3.0.", "3.1", "3.2", "3.3"}:
            print_instructions(py_version, "~/.pbt/vms")
