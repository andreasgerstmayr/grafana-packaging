# grafana
The grafana package

## Setup instructions
* clone the upstream sources: `git clone https://github.com/grafana/grafana && cd grafana`
* checkout the desired version (tag): `git checkout vX.Y.Z`
* run: `go mod vendor && git add -f vendor && git commit -m vendor` (this step is required because some patches modify vendor sources)
* apply existing patches: `git am ../*.patch` and resolve any errors
* create new patches from the modified git commits: `git format-patch -N --no-stat --no-signature <commit-hash-of-vendor-commit>`

## Upgrade instructions
* follow the Setup instructions above with the new upstream version
* update `Version`, `Release`, `%changelog` and tarball NVRs in the specfile
* create bundles and manifest: `make clean all`
* update specfile with contents of the `.manifest` file
* update the manpages patch in `0002-add-manpages.patch` and other patches if required
* run local build: `rpkg local`
* run rpm linter: `rpkg lint -r grafana.rpmlintrc`
* run a scratch build: `fedpkg scratch-build --srpm`
* upload new source tarballs: `fedpkg new-sources *.tar.gz *.tar.xz`
* commit new `sources` file

## Patches
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
