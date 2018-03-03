RPM Packaging for Clearwater IMS
================================

The [Clearwater IMS](https://www.projectclearwater.org/) is officially packaged for Ubuntu 14.04.
Here we are re-packaging it for RHEL, CentOS, and other RPM-based Linux distributions. We support
the x86_64 platform only.


How To
------

First run `fetch-sources` to download the sources and archive them in the `SOURCES` directory.

To build, you must use [CentOS](https://www.centos.org/) to build the RPMs. There are three ways to
satisfy this requirement:

1. Install CentOS yourself.
2. Use our included [Vagrant](https://www.vagrantup.com/) configuration to quickly bring up a CentOS
   virtual machine. Just change to the `vagrant` directory and run `vagrant up`, and then `vagrant ssh` to
   login. The build scripts are in the `build` directory within the virtual machine. Note that you
   will need the VirtualBox Guest Additions. Install them automatically via a plugin:
   `vagrant plugin install vagrant-vbguest`.
3. On any Linux, use [mock](https://github.com/rpm-software-management/mock) to emulate CentOS in a
   chroot environment. For this, use `build-via-mock` instead of `build`.

From within CentOS, run `build`, and go make yourself a cup of tea, because it's going to take a
while. Unfortunately, the Clearwater build scripts were not designed to run with concurrency
(`make --jobs` will not work), so you will not benefit from having a multi-core machine.

When finished (phew!) your RPMs will be available under `RPMS/x86_64`.

You can also build individual spec files by providing the name as an argument, for example:
`build clearwater-ellis`.

Also useful may be the `quick-build` script, which skips the `%prepare` and `%build` sections in the spec
file.
