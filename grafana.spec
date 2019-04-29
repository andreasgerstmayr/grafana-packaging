%global grafana_arches %{lua: go_arches = {}
  for arch in rpm.expand("%{go_arches}"):gmatch("%S+") do
    go_arches[arch] = 1
  end
  for arch in rpm.expand("%{nodejs_arches}"):gmatch("%S+") do
    if go_arches[arch] then
      print(arch .. " ")
  end
end}

Name:             grafana
Version:          6.1.4
Release:          1%{?dist}
Summary:          Metrics dashboard and graph editor
License:          ASL 2.0
URL:              https://grafana.org

# Source0 contains the tagged upstream sources
Source0:          https://github.com/grafana/grafana/archive/v%{version}/%{name}-%{version}.tar.gz

# Source1 contains the front-end javascript modules bundled into a webpack
Source1:          grafana_webpack-%{version}.tar.gz

# Source2 is the script to create the above webpack from grafana sources
Source2:          make_webpack.sh

# Patches for upstream (except Patch5)
Patch0:           000-go-test-fixes.patch
Patch1:           001-man-pages.patch
Patch2:           002-update-golang-oauth2-vendor-sources.patch
Patch3:           003-file-mode-updates.patch
Patch4:           004-grafana.ini-for-Linux-distros.patch
Patch5:           005-remove-jaeger-tracing.patch
Patch6:           006-native-RPM-spec-and-webpack-build-script.patch

# Intersection of go_arches and nodejs_arches
ExclusiveArch:    %{grafana_arches}

%global           GRAFANA_USER %{name}
%global           GRAFANA_GROUP %{name}
%global           GRAFANA_HOME %{_datadir}/%{name}

# grafana-server service daemon uses systemd
%{?systemd_requires}
Requires(pre):    shadow-utils

BuildRequires:    systemd, golang, compiler(go-compiler)

# golang build deps. These allow us to unbundle vendor golang source.
BuildRequires: golang(github.com/aws/aws-sdk-go)
BuildRequires: golang(github.com/benbjohnson/clock)
BuildRequires: golang(github.com/beorn7/perks/quantile)
BuildRequires: golang(github.com/bmizerany/assert)
BuildRequires: golang(github.com/bradfitz/gomemcache/memcache)
BuildRequires: golang(github.com/BurntSushi/toml)
BuildRequires: golang(github.com/codahale/hdrhistogram)
BuildRequires: golang(github.com/codegangsta/cli)
BuildRequires: golang(github.com/davecgh/go-spew/spew)
BuildRequires: golang(github.com/denisenkom/go-mssqldb)
BuildRequires: golang(github.com/facebookgo/inject)
BuildRequires: golang(github.com/facebookgo/structtag)
BuildRequires: golang(github.com/fatih/color)
BuildRequires: golang(github.com/go-ini/ini)
BuildRequires: golang(google.golang.org/appengine)
BuildRequires: golang(golang.org/x/sys/unix)
BuildRequires: golang(github.com/go-macaron/binding)
BuildRequires: golang(github.com/go-macaron/gzip)
BuildRequires: golang(github.com/go-macaron/inject)
BuildRequires: golang(github.com/go-macaron/session)
BuildRequires: golang(google.golang.org/genproto/googleapis/rpc/status)
BuildRequires: golang(github.com/gopherjs/gopherjs/js)
BuildRequires: golang(github.com/gorilla/websocket)
BuildRequires: golang(github.com/gosimple/slug)
BuildRequires: golang(github.com/go-sql-driver/mysql)
BuildRequires: golang(github.com/go-stack/stack)
BuildRequires: golang(github.com/go-xorm/builder)
BuildRequires: golang(github.com/go-xorm/core)
BuildRequires: golang(github.com/go-xorm/xorm)
BuildRequires: golang(google.golang.org/grpc)
BuildRequires: golang(github.com/hashicorp/go-hclog)
# need grpc_broker in go-plugin >= 1.0.0-1
BuildRequires: golang(github.com/hashicorp/go-plugin)
BuildRequires: golang(github.com/hashicorp/go-version)
BuildRequires: golang(github.com/hashicorp/yamux)
BuildRequires: golang(github.com/inconshreveable/log15)
BuildRequires: golang(github.com/jmespath/go-jmespath)
BuildRequires: golang(github.com/jtolds/gls)
BuildRequires: golang(github.com/klauspost/compress/flate)
BuildRequires: golang(github.com/klauspost/compress/gzip)
BuildRequires: golang(github.com/klauspost/compress/snappy)
BuildRequires: golang(github.com/klauspost/cpuid)
BuildRequires: golang(github.com/klauspost/crc32)
BuildRequires: golang(github.com/kr/pretty)
BuildRequires: golang(github.com/kr/text)
BuildRequires: golang(github.com/lib/pq)
BuildRequires: golang(github.com/mattn/go-colorable)
BuildRequires: golang(github.com/mattn/go-isatty)
BuildRequires: golang(github.com/mattn/go-sqlite3)
BuildRequires: golang(github.com/matttproud/golang_protobuf_extensions/pbutil)
BuildRequires: golang(github.com/mitchellh/go-testing-interface)
BuildRequires: golang(github.com/oklog/run)
BuildRequires: golang(github.com/opentracing/opentracing-go)
BuildRequires: golang(github.com/patrickmn/go-cache)
BuildRequires: golang(github.com/pkg/errors)
BuildRequires: golang(github.com/prometheus/client_golang/api)
BuildRequires: golang(github.com/prometheus/client_golang/api/prometheus/v1)
BuildRequires: golang(github.com/prometheus/client_model/go)
BuildRequires: golang-github-prometheus-common-devel
BuildRequires: golang(github.com/prometheus/common/expfmt)
BuildRequires: golang(github.com/prometheus/common/model)
BuildRequires: golang(github.com/prometheus/common/expfmt)
BuildRequires: golang(github.com/prometheus/procfs)
BuildRequires: golang(github.com/prometheus/procfs/internal/util)
BuildRequires: golang(github.com/prometheus/procfs)
BuildRequires: golang(github.com/prometheus/procfs/internal/util)
BuildRequires: golang(github.com/prometheus/procfs/nfs)
BuildRequires: golang(github.com/prometheus/procfs/xfs)
BuildRequires: golang(github.com/rainycape/unidecode)
BuildRequires: golang(github.com/sergi/go-diff/diffmatchpatch)
BuildRequires: golang(github.com/smartystreets/assertions)
BuildRequires: golang(github.com/smartystreets/goconvey/convey)
BuildRequires: golang(github.com/smartystreets/goconvey/convey/gotest)
BuildRequires: golang(github.com/smartystreets/goconvey/convey/reporting)
BuildRequires: golang(github.com/teris-io/shortid)
BuildRequires: golang(github.com/Unknwon/com)
BuildRequires: golang(github.com/VividCortex/mysqlerr)
BuildRequires: golang(github.com/yudai/gojsondiff)
BuildRequires: golang(github.com/yudai/golcs)
BuildRequires: golang(golang.org/x/crypto/pbkdf2)
BuildRequires: golang(golang.org/x/crypto/ed25519)
BuildRequires: golang(golang.org/x/crypto/md4)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/net/context/ctxhttp)
BuildRequires: golang(golang.org/x/net/http2)
BuildRequires: golang(golang.org/x/net/http2/hpack)
BuildRequires: golang(golang.org/x/net/http/httpguts)
BuildRequires: golang(golang.org/x/net/idna)
BuildRequires: golang(golang.org/x/net/internal/timeseries)
BuildRequires: golang(golang.org/x/net/trace)
BuildRequires: golang(golang.org/x/text/collate)
BuildRequires: golang(golang.org/x/text/collate/build)
BuildRequires: golang(golang.org/x/text/internal/colltab)
BuildRequires: golang(golang.org/x/text/internal/gen)
BuildRequires: golang(golang.org/x/text/internal/tag)
BuildRequires: golang(golang.org/x/text/internal/triegen)
BuildRequires: golang(golang.org/x/text/internal/ucd)
BuildRequires: golang(golang.org/x/oauth2)
BuildRequires: golang(golang.org/x/oauth2/google)
BuildRequires: golang(golang.org/x/oauth2/internal)
BuildRequires: golang(golang.org/x/oauth2/jws)
BuildRequires: golang(golang.org/x/oauth2/jwt)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/golang/protobuf/ptypes)
BuildRequires: golang(github.com/golang/protobuf/ptypes)
BuildRequires: golang(github.com/golang/protobuf/ptypes/duration)
BuildRequires: golang(github.com/golang/protobuf/ptypes/any)
BuildRequires: golang(github.com/golang/protobuf/ptypes/timestamp)
BuildRequires: golang(cloud.google.com/go/compute/metadata)
BuildRequires: golang(gopkg.in/alexcesaro/quotedprintable.v3)
BuildRequires: golang(gopkg.in/asn1-ber.v1)
BuildRequires: golang(github.com/go-bufio/bufio)
BuildRequires: golang(github.com/go-ini/ini)
BuildRequires: golang(github.com/go-macaron/macaron)
BuildRequires: golang(github.com/go-redis/redis)
BuildRequires: golang(gopkg.in/square/go-jose.v2)
BuildRequires: golang(gopkg.in/square/go-jose.v2/cipher)
BuildRequires: golang(gopkg.in/square/go-jose.v2/json)
BuildRequires: golang(github.com/go-yaml/yaml)
BuildRequires: golang(golang.org/x/sync/errgroup)
BuildRequires: golang(gopkg.in/ldap.v3)
BuildRequires: golang(gopkg.in/mail.v2)

# Declare all nodejs modules bundled in the webpack - this is for security
# purposes so if nodejs-foo ever needs an update, affected packages can be
# easily identified. This is generated from package-lock.json once the webpack
# has been built with make_webpack.sh.
Provides: bundled(nodejs-abbrev) = 1.1.1
Provides: bundled(nodejs-ansi-regex) = 2.1.1
Provides: bundled(nodejs-ansi-styles) = 2.2.1
Provides: bundled(nodejs-argparse) = 1.0.10
Provides: bundled(nodejs-array-find-index) = 1.0.2
Provides: bundled(nodejs-async) = 1.5.2
Provides: bundled(nodejs-balanced-match) = 1.0.0
Provides: bundled(nodejs-brace-expansion) = 1.1.11
Provides: bundled(nodejs-builtin-modules) = 1.1.1
Provides: bundled(nodejs-camelcase) = 2.1.1
Provides: bundled(nodejs-camelcase-keys) = 2.1.0
Provides: bundled(nodejs-chalk) = 1.1.3
Provides: bundled(nodejs-coffee-script) = 1.10.0
Provides: bundled(nodejs-colors) = 1.1.2
Provides: bundled(nodejs-concat-map) = 0.0.1
Provides: bundled(nodejs-currently-unhandled) = 0.4.1
Provides: bundled(nodejs-dateformat) = 1.0.12
Provides: bundled(nodejs-decamelize) = 1.2.0
Provides: bundled(nodejs-error-ex) = 1.3.2
Provides: bundled(nodejs-escape-string-regexp) = 1.0.5
Provides: bundled(nodejs-esprima) = 2.7.3
Provides: bundled(nodejs-eventemitter2) = 0.4.14
Provides: bundled(nodejs-exit) = 0.1.2
Provides: bundled(nodejs-find-up) = 1.1.2
Provides: bundled(nodejs-findup-sync) = 0.3.0
Provides: bundled(nodejs-fs.realpath) = 1.0.0
Provides: bundled(nodejs-get-stdin) = 4.0.1
Provides: bundled(nodejs-getobject) = 0.1.0
Provides: bundled(nodejs-glob) = 7.0.6
Provides: bundled(nodejs-graceful-fs) = 4.1.15
Provides: bundled(nodejs-grunt) = 1.0.1
Provides: bundled(nodejs-grunt-cli) = 1.2.0
Provides: bundled(nodejs-grunt-known-options) = 1.1.1
Provides: bundled(nodejs-grunt-legacy-log) = 1.0.2
Provides: bundled(nodejs-lodash) = 4.17.11
Provides: bundled(nodejs-grunt-legacy-log-utils) = 1.0.0
Provides: bundled(nodejs-grunt-legacy-util) = 1.0.0
Provides: bundled(nodejs-has-ansi) = 2.0.0
Provides: bundled(nodejs-hooker) = 0.2.3
Provides: bundled(nodejs-hosted-git-info) = 2.7.1
Provides: bundled(nodejs-iconv-lite) = 0.4.24
Provides: bundled(nodejs-indent-string) = 2.1.0
Provides: bundled(nodejs-inflight) = 1.0.6
Provides: bundled(nodejs-inherits) = 2.0.3
Provides: bundled(nodejs-is-arrayish) = 0.2.1
Provides: bundled(nodejs-is-builtin-module) = 1.0.0
Provides: bundled(nodejs-is-finite) = 1.0.2
Provides: bundled(nodejs-is-utf8) = 0.2.1
Provides: bundled(nodejs-isexe) = 2.0.0
Provides: bundled(nodejs-js-yaml) = 3.5.5
Provides: bundled(nodejs-load-json-file) = 1.1.0
Provides: bundled(nodejs-loud-rejection) = 1.6.0
Provides: bundled(nodejs-map-obj) = 1.0.1
Provides: bundled(nodejs-meow) = 3.7.0
Provides: bundled(nodejs-minimatch) = 3.0.4
Provides: bundled(nodejs-minimist) = 1.2.0
Provides: bundled(nodejs-nopt) = 3.0.6
Provides: bundled(nodejs-normalize-package-data) = 2.4.2
Provides: bundled(nodejs-number-is-nan) = 1.0.1
Provides: bundled(nodejs-object-assign) = 4.1.1
Provides: bundled(nodejs-once) = 1.4.0
Provides: bundled(nodejs-parse-json) = 2.2.0
Provides: bundled(nodejs-path-exists) = 2.1.0
Provides: bundled(nodejs-path-is-absolute) = 1.0.1
Provides: bundled(nodejs-path-type) = 1.1.0
Provides: bundled(nodejs-pify) = 2.3.0
Provides: bundled(nodejs-pinkie) = 2.0.4
Provides: bundled(nodejs-pinkie-promise) = 2.0.1
Provides: bundled(nodejs-read-pkg) = 1.1.0
Provides: bundled(nodejs-read-pkg-up) = 1.0.1
Provides: bundled(nodejs-redent) = 1.0.0
Provides: bundled(nodejs-repeating) = 2.0.1
Provides: bundled(nodejs-resolve) = 1.1.7
Provides: bundled(nodejs-rimraf) = 2.2.8
Provides: bundled(nodejs-safer-buffer) = 2.1.2
Provides: bundled(nodejs-semver) = 5.6.0
Provides: bundled(nodejs-signal-exit) = 3.0.2
Provides: bundled(nodejs-spdx-correct) = 3.1.0
Provides: bundled(nodejs-spdx-exceptions) = 2.2.0
Provides: bundled(nodejs-spdx-expression-parse) = 3.0.0
Provides: bundled(nodejs-spdx-license-ids) = 3.0.3
Provides: bundled(nodejs-sprintf-js) = 1.0.3
Provides: bundled(nodejs-strip-ansi) = 3.0.1
Provides: bundled(nodejs-strip-bom) = 2.0.0
Provides: bundled(nodejs-strip-indent) = 1.0.1
Provides: bundled(nodejs-supports-color) = 2.0.0
Provides: bundled(nodejs-trim-newlines) = 1.0.0
Provides: bundled(nodejs-underscore.string) = 3.2.3
Provides: bundled(nodejs-validate-npm-package-license) = 3.0.4
Provides: bundled(nodejs-which) = 1.2.14
Provides: bundled(nodejs-wrappy) = 1.0.2
Provides: bundled(nodejs-yarn) = 1.13.0


%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.


%prep
%setup -q -T -D -b 0
%setup -q -T -D -b 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# Set up build subdirs and links
mkdir -p %{_builddir}/src/github.com/grafana
ln -sf %{_builddir}/%{name}-%{version} \
    %{_builddir}/src/github.com/grafana/grafana

# remove some (apparent) development files, for rpmlint
rm -f %{_builddir}/src/github.com/grafana/grafana/public/sass/.sass-lint.yml
rm -f %{_builddir}/src/github.com/grafana/grafana/public/test/.jshintrc

# Unbundle all grafana vendor sources, as per BuildRequires above.
# An exception is grafana-plugin-model, which is part of grafana.
cp --parents -a vendor/github.com/grafana %{_builddir}
rm -r vendor # remove all vendor sources
mv %{_builddir}/vendor vendor # put back what we're keeping


%build
# Build the server-side binaries: grafana-server and grafana-cli
export GOPATH=%{_builddir}:%{gopath}
%gobuild -o grafana-cli ./pkg/cmd/grafana-cli
%gobuild -o grafana-server ./pkg/cmd/grafana-server


%install
# binaries
install -d %{buildroot}%{_sbindir}
install -p -m 755 %{name}-server %{name}-cli %{buildroot}%{_sbindir}

# other shared files, public html, webpack
install -d %{buildroot}%{_datadir}/%{name}
cp -a conf public %{buildroot}%{_datadir}/%{name}

# man pages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 docs/man/man1/* %{buildroot}%{_mandir}/man1

# config dirs
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/sysconfig

# config defaults
install -p -m 644 conf/distro-defaults.ini \
    %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
install -p -m 644 conf/distro-defaults.ini \
    %{buildroot}%{_datadir}/%{name}/conf/defaults.ini
install -p -m 644 conf/ldap.toml %{buildroot}%{_sysconfdir}/%{name}/ldap.toml
install -p -m 644 packaging/rpm/sysconfig/grafana-server \
    %{buildroot}%{_sysconfdir}/sysconfig/grafana-server

# config database directory and plugins
install -d %{buildroot}%{_sharedstatedir}/%{name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{name}/plugins

# log directory
install -d %{buildroot}%{_localstatedir}/log/%{name}

# systemd service files
install -d %{buildroot}%{_unitdir} # only needed for manual rpmbuilds
install -p -m 644 packaging/rpm/systemd/grafana-server.service \
    %{buildroot}%{_unitdir}

# daemon run pid file config for using tmpfs
install -d %{buildroot}%{_tmpfilesdir}
echo "d %{_rundir}/%{name} 0755 %{GRAFANA_USER} %{GRAFANA_GROUP} -" \
    > %{buildroot}%{_tmpfilesdir}/%{name}.conf

%pre
getent group %{GRAFANA_GROUP} >/dev/null || groupadd -r %{GRAFANA_GROUP}
getent passwd %{GRAFANA_USER} >/dev/null || \
    useradd -r -g %{GRAFANA_GROUP} -d %{GRAFANA_HOME} -s /sbin/nologin \
    -c "%{GRAFANA_USER} user account" %{GRAFANA_USER}
exit 0

%preun
%systemd_preun grafana-server.service

%post
%systemd_post grafana-server.service

%postun
%systemd_postun_with_restart grafana-server.service


%check
cd %{_builddir}/src/github.com/grafana/grafana
export GOPATH=%{_builddir}:%{gopath}
# this test fails for some reason
rm -f pkg/services/provisioning/dashboards/file_reader_linux_test.go
# should be using %%gochecks here, but it doesn't work
go test ./pkg/...


%files
# binaries
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}-cli

# config files
%dir %{_sysconfdir}/%{name}
%config(noreplace) %attr(644, root, %{GRAFANA_GROUP}) %{_sysconfdir}/%{name}/grafana.ini
%config(noreplace) %attr(644, root, %{GRAFANA_GROUP}) %{_sysconfdir}/%{name}/ldap.toml
%config(noreplace) %{_sysconfdir}/sysconfig/grafana-server

# Grafana configuration to dynamically create /run/grafana/grafana.pid on tmpfs
%{_tmpfilesdir}/%{name}.conf

# config database directory and plugins (actual db files are created by grafana-server)
%attr(-, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}
%attr(-, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}/plugins

# shared directory and all files therein
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/public
%dir %{_datadir}/%{name}/conf
%attr(-, root, %{GRAFANA_GROUP}) %{_datadir}/%{name}/conf/*

# systemd service file
%{_unitdir}/grafana-server.service

# log directory - grafana.log is created by grafana-server, and it does it's own log rotation
%attr(0755, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_localstatedir}/log/%{name}

# man pages for grafana binaries
%{_mandir}/man1/%{name}-server.1*
%{_mandir}/man1/%{name}-cli.1*

# other docs and license
%license LICENSE
%doc CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md NOTICE.md
%doc PLUGIN_DEV.md README.md ROADMAP.md UPGRADING_DEPENDENCIES.md


%changelog
* Wed Apr 24 2019 Mark Goodwin <mgoodwin@redhat.com> 6.1.4-1
- update to latest upstream stable release 6.1.4, see CHANGELOG
- use gobuild and gochecks macros, eliminate arch symlinks
- re-enable grafana-debugsource package
- fix GRAFANA_GROUP typo
- fix more modes for brp-mangle-shebangs
- vendor source unbundling now done in prep after patches
- remove all rhel and fedora conditional guff

* Tue Apr 16 2019 Mark Goodwin <mgoodwin@redhat.com> 6.1.3-1
- update to latest upstream stable release 6.1.3, see CHANGELOG
- unbundle all vendor sources, replace with BuildRequires, see
  the long list of blocker BZs linked to BZ#1670656
- BuildRequires go-plugin >= v1.0.0 for grpc_broker (thanks eclipseo)
- tweak make_webpack to no longer use grunt, switch to prod build
- add ExclusiveArch lua script (thanks quantum.analyst)
- move db directory and plugins to /var/lib/grafana
- split out into 6 patches, ready for upstream PRs
- add check to run go tests for gating checks

* Thu Apr 04 2019 Mark Goodwin <mgoodwin@redhat.com> 6.1.0-1
- update to latest upstream stable release 6.1.0, see CHANGELOG

* Thu Mar 21 2019 Mark Goodwin <mgoodwin@redhat.com> 6.0.2-1
- bump to latest upstream stable release 6.0.2-1
- unbundle almost all remaining vendor code, see linked blockers in BZ#1670656

* Fri Mar 15 2019 Mark Goodwin <mgoodwin@redhat.com> 6.0.1-3
- bump to latest upstream stable release 6.0.1-1

* Thu Mar 14 2019 Mark Goodwin <mgoodwin@redhat.com> 6.0.1-2
- unbundle and add BuildRequires for golang-github-rainycape-unidecode-devel

* Thu Mar 07 2019 Mark Goodwin <mgoodwin@redhat.com> 6.0.1-1
- update to v6.0.1 upstream sources, tweak distro config, re-do patch
- simplify make_webpack.sh script (Elliott Sales de Andrade)
- vendor/github.com/go-ldap is now gone, so don't unbundle it

* Thu Mar 07 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-11
- tweak after latest feedback, bump to 5.4.3-11 (BZ 1670656)
- build debuginfo package again
- unbundle BuildRequires for golang-github-hashicorp-version-devel
- remove some unneeded development files
- remove macros from changelog and other rpmlint tweaks

* Fri Feb 22 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-10
- tweak spec for available and unavailable (bundled) golang packages

* Wed Feb 20 2019 Xavier Bachelot <xavier@bachelot.org> 5.4.3-9
- Remove extraneous slash (cosmetic)
- Create directories just before moving stuff in them
- Truncate long lines
- Group all golang stuff
- Simplify BuildRequires/bundled Provides
- Sort BuildRequires/bundled Provides
- Fix bundled go packages Provides

* Fri Feb 15 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-8
- add BuildRequires (and unbundle) vendor sources available in Fedora
- declare Provides for remaining (bundled) vendor go sources
- do not attempt to unbundle anything on RHEL < 7 or Fedora < 28

* Thu Feb 07 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-7
- further refinement for spec doc section from Xavier Bachelot
- disable debug_package to avoid empty debugsourcefiles.list

* Wed Feb 06 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-6
- further refinement following review by Xavier Bachelot

* Tue Feb 05 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-5
- further refinement following review by Xavier Bachelot

* Fri Feb 01 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-4
- further spec updates after packaging review
- reworked post-install scriplets

* Thu Jan 31 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-3
- tweak FHS patch, update spec after packaging review

* Wed Jan 30 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.3-2
- add patch to be standard FHS compliant, remove phantomjs
- update to v5.4.3 upstream community sources

* Wed Jan 09 2019 Mark Goodwin <mgoodwin@redhat.com> 5.4.2-1
- update to v5.4.2 upstream community sources

* Thu Oct 18 2018 Mark Goodwin <mgoodwin@redhat.com> 5.3.1-1
- update to v5.3.1 upstream community sources

* Tue Oct 02 2018 Mark Goodwin <mgoodwin@redhat.com> 5.2.5-1
- native RPM spec build with current tagged v5.2.5 sources
