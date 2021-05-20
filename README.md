# grafana
The grafana package

## Upgrade instructions
(replace X.Y.Z with the new Grafana version)

* update `Version`, `Release` and `%changelog` in the specfile
* create bundles and manifest: `VER=X.Y.Z make clean all`
* update specfile with contents of the `.manifest` file
* check if the default configuration has changed: `diff grafana-X.Y.Z/conf/defaults.ini distro-defaults.ini` and update `distro-defaults.ini` if necessary
* update the manpages patch in `002-manpages.patch` and other patches if required
* run local build: `rpkg local`
* run rpm linter: `rpkg lint -r grafana.rpmlintrc`
* run local builds with different OS versions: `./run_container_build.sh fedora-version`
* run a scratch build: `fedpkg scratch-build --srpm`
* upload new source tarballs: `fedpkg new-sources *.tar.gz *.tar.xz`

## Backporting
* create the patch
* declare and apply (`%prep`) the patch in the specfile
* if the patch affects Go or Node.js dependencies, or the webpack
  * create new tarballs and rename them to `grafana-...-X.Y.Z-R.tar.gz`
  * update the specfile with new tarball path and contents of the `.manifest` file

Note: the Makefile automatically applies all patches before creating the tarballs

## Verification
* compare the list of files with the upstream RPM at https://grafana.com/grafana/download
