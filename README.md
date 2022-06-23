# grafana
The grafana package

## Upgrade instructions
* update `Version`, `Release`, `%changelog` and tarball NVRs in the specfile
* create bundles and manifest: `make clean all`
* update specfile with contents of the `.manifest` file
* check if the default configuration has changed: `diff grafana-X.Y.Z/conf/defaults.ini distro-defaults.ini` and update `distro-defaults.ini` if necessary
* update the manpages patch in `002-manpages.patch` and other patches if required
* run local build: `rpkg local`
* run rpm linter: `rpkg lint -r grafana.rpmlintrc`
* run a scratch build: `fedpkg scratch-build --srpm`
* upload new source tarballs: `fedpkg new-sources *.tar.gz *.tar.xz`
* commit new `sources` file

## Patches
`git format-patch -N --no-stat --no-signature <commit>`
* create the patch
* declare and apply (`%prep`) the patch in the specfile
* if the patch affects Go or Node.js dependencies, or the webpack
  * add the patch to `PATCHES_PRE_VENDOR` or `PATCHES_PRE_WEBPACK` in the Makefile
  * create new tarballs
  * update the specfile with new tarball name and contents of the `.manifest` file

### General guidelines
* aim to apply all patches in the specfile
* avoid rebuilding the tarballs

Patches fall in several categories:
  * modify dependency versions
  * modify both sources and vendored dependencies (e.g. CVEs)
  * modify the Node.js source (i.e. affect the webpack)
  * some patches are conditional (e.g. FIPS)

Patches cannot be applied twice.
It is not possible to unconditionally apply all patches in the Makefile, and great care must be taken to include the required patches at the correct stage of the build.

## Reproducible Bundles
Run `./create_bundles_in_container.sh` to generate a reproducible vendor and webpack bundle.
Alternatively, install the same software as in the container, create a bind mount from `/tmp/grafana-build` to the directory of this repository, and run `make`.
The bind mount is required because Webpack stores absolute paths in the JS source maps, and also resolves symlinks (i.e. symlinking `/tmp/grafana-build` doesn't work).

## Verification
* compare the list of files with the upstream RPM at https://grafana.com/grafana/download
