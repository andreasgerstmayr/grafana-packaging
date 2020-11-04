# grafana
The grafana package

## Upgrade instructions
(replace X.Y.Z with the new Grafana version)

* update `Version` and `%changelog` in the specfile
* create bundles and manifests: `VER=X.Y.Z make clean all`
* update specfile with contents of the `*.manifest` files
* check if the default configuration has changed: `diff grafana-X.Y.Z/conf/defaults.ini distro-defaults.ini` and update `distro-defaults.ini` if necessary
* run local build: `rpkg local`
* run rpm linter: `rpkg lint -r grafana.rpmlintrc`
* run local builds with different OS versions: `./run_container_build.sh fedora-version`
* run a scratch build: `fedpkg scratch-build --srpm`
* upload new source tarballs: `fedpkg new-sources grafana-X.Y.Z.tar.gz grafana-vendor-X.Y.Z.tar.gz`

## Backporting
* create the patch
* declare and apply (`%prep`) the patch in the specfile
* if the patch affects Go or Node.js dependencies, or the webpack
  * create new tarballs and rename them to `grafana-...-X.Y.Z-R.tar.gz`
  * update the specfile

Note: the Makefile automatically applies all patches before creating the tarballs
