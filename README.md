# grafana
The grafana package

## Upgrade instructions
(replace X.Y.Z with the new Grafana version)

* update `Version` and `%changelog` in the specfile
* create bundles and manifests: `VER=X.Y.Z make`
* update specfile with contents of `grafana-vendor-X.Y.Z.tar.gz.manifest` and `grafana-webpack-X.Y.Z.tar.gz.manifest`
* check if the default configuration has changed: `diff grafana-X.Y.Z/conf/defaults.ini distro-defaults.ini` and update `distro-defaults.ini` if necessary
* run local build: `rpkg local`
* run rpm linter: `rpkg lint`
* run local builds with different OS versions: `./run_container_build.sh version`
* run a scratch build: `fedpkg scratch-build --srpm`
* upload new source tarballs: `fedpkg new-sources grafana-X.Y.Z.tar.gz grafana-vendor-X.Y.Z.tar.gz grafana-webpack-X.Y.Z.tar.gz`
