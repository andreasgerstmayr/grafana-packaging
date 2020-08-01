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
Version:          7.1.1
Release:          2%{?dist}
Summary:          Metrics dashboard and graph editor
License:          ASL 2.0
URL:              https://grafana.org

# Source0 contains the tagged upstream sources
Source0:          https://github.com/grafana/grafana/archive/v%{version}/%{name}-%{version}.tar.gz

# Source1 contains the bundled Go dependencies
Source1:          grafana-vendor-%{version}.tar.gz

# Source2 contains the front-end javascript modules bundled into a webpack
Source2:          grafana-webpack-%{version}.tar.gz

# Source3 contains Grafana configuration defaults for distributions
Source3:          distro-defaults.ini

# Source4 contains the Makefile to create a Go vendor tarball and a webpack from grafana sources
Source4:          Makefile

# Source5 contains the script to generate the list of bundled nodejs packages
Source5:          create_webpack_manifest.py

# Patches
Patch1:           001-wrappers-grafana-cli.patch
Patch2:           002-manpages.patch

# Required for Go >= 1.15
# https://github.com/golang/go/commit/201cb046b745f8bb00e3d382290190c74ba7b7e1
# https://github.com/golang/go/issues/32479
Patch3:           003-golang1.15.patch

# Required for s390x
# the golden files include memory dumps from a x86 machine
# integers are stored as little endian on x86, but as big endian on s390x
# therefore loading this memory dump fails on s390x
Patch4:           004-remove-goldenfiles-test.patch

# Intersection of go_arches and nodejs_arches
ExclusiveArch:    %{grafana_arches}

# omit golang debugsource, see BZ995136 and related
%global           dwz_low_mem_die_limit 0
%global           _debugsource_template %{nil}

%global           GRAFANA_USER %{name}
%global           GRAFANA_GROUP %{name}
%global           GRAFANA_HOME %{_datadir}/%{name}

# grafana-server service daemon uses systemd
%{?systemd_requires}
Requires(pre):    shadow-utils

BuildRequires:    git, systemd, golang, go-srpm-macros, go-rpm-macros

Obsoletes:        grafana-cloudwatch < 7.1.1-1
Obsoletes:        grafana-elasticsearch < 7.1.1-1
Obsoletes:        grafana-azure-monitor < 7.1.1-1
Obsoletes:        grafana-graphite < 7.1.1-1
Obsoletes:        grafana-influxdb < 7.1.1-1
Obsoletes:        grafana-loki < 7.1.1-1
Obsoletes:        grafana-mssql < 7.1.1-1
Obsoletes:        grafana-mysql < 7.1.1-1
Obsoletes:        grafana-opentsdb < 7.1.1-1
Obsoletes:        grafana-postgres < 7.1.1-1
Obsoletes:        grafana-prometheus < 7.1.1-1
Obsoletes:        grafana-stackdriver < 7.1.1-1

%if 0%{?fedora} || 0%{?rhel} > 7
Recommends: grafana-pcp >= 3.0.0
%endif

# vendored golang build dependencies
# Note: generated by the Makefile (see README.md)
Provides: bundled(golang(github.com/BurntSushi/toml)) = 0.3.1
Provides: bundled(golang(github.com/VividCortex/mysqlerr)) = 0.0.0-20170204212430.6c6b55f8796f
Provides: bundled(golang(github.com/aws/aws-sdk-go)) = 1.29.20
Provides: bundled(golang(github.com/benbjohnson/clock)) = 0.0.0-20161215174838.7dc76406b6d3
Provides: bundled(golang(github.com/bradfitz/gomemcache)) = 0.0.0-20190329173943.551aad21a668
Provides: bundled(golang(github.com/crewjam/saml)) = 0.0.0-20191031171751.c42136edf9b1
Provides: bundled(golang(github.com/davecgh/go-spew)) = 1.1.1
Provides: bundled(golang(github.com/denisenkom/go-mssqldb)) = 0.0.0-20190707035753.2be1aa521ff4
Provides: bundled(golang(github.com/facebookgo/inject)) = 0.0.0-20180706035515.f23751cae28b
Provides: bundled(golang(github.com/fatih/color)) = 1.7.0
Provides: bundled(golang(github.com/go-macaron/binding)) = 0.0.0-20190806013118.0b4f37bab25b
Provides: bundled(golang(github.com/go-macaron/gzip)) = 0.0.0-20160222043647.cad1c6580a07
Provides: bundled(golang(github.com/go-macaron/session)) = 0.0.0-20190805070824.1a3cdc6f5659
Provides: bundled(golang(github.com/go-sql-driver/mysql)) = 1.5.0
Provides: bundled(golang(github.com/go-stack/stack)) = 1.8.0
Provides: bundled(golang(github.com/gobwas/glob)) = 0.2.3
Provides: bundled(golang(github.com/golang/protobuf)) = 1.4.0
Provides: bundled(golang(github.com/google/go-cmp)) = 0.4.0
Provides: bundled(golang(github.com/gorilla/websocket)) = 1.4.1
Provides: bundled(golang(github.com/gosimple/slug)) = 1.4.2
Provides: bundled(golang(github.com/grafana/grafana-plugin-model)) = 0.0.0-20190930120109.1fc953a61fb4
Provides: bundled(golang(github.com/grafana/grafana-plugin-sdk-go)) = 0.75.0
Provides: bundled(golang(github.com/hashicorp/go-hclog)) = 0.0.0-20180709165350.ff2cf002a8dd
Provides: bundled(golang(github.com/hashicorp/go-plugin)) = 1.2.2
Provides: bundled(golang(github.com/hashicorp/go-version)) = 1.1.0
Provides: bundled(golang(github.com/inconshreveable/log15)) = 0.0.0-20180818164646.67afb5ed74ec
Provides: bundled(golang(github.com/influxdata/influxdb-client-go)) = 1.3.0
Provides: bundled(golang(github.com/jmespath/go-jmespath)) = 0.0.0-20180206201540.c2b33e8439af
Provides: bundled(golang(github.com/jung-kurt/gofpdf)) = 1.10.1
Provides: bundled(golang(github.com/lib/pq)) = 1.2.0
Provides: bundled(golang(github.com/linkedin/goavro/v2)) = 2.9.7
Provides: bundled(golang(github.com/mattn/go-isatty)) = 0.0.12
Provides: bundled(golang(github.com/mattn/go-sqlite3)) = 1.11.0
Provides: bundled(golang(github.com/opentracing/opentracing-go)) = 1.1.0
Provides: bundled(golang(github.com/patrickmn/go-cache)) = 2.1.0+incompatible
Provides: bundled(golang(github.com/pkg/errors)) = 0.9.1
Provides: bundled(golang(github.com/prometheus/client_golang)) = 1.3.0
Provides: bundled(golang(github.com/prometheus/client_model)) = 0.1.0
Provides: bundled(golang(github.com/prometheus/common)) = 0.7.0
Provides: bundled(golang(github.com/robfig/cron)) = 0.0.0-20180505203441.b41be1df6967
Provides: bundled(golang(github.com/robfig/cron/v3)) = 3.0.0
Provides: bundled(golang(github.com/smartystreets/goconvey)) = 0.0.0-20190731233626.505e41936337
Provides: bundled(golang(github.com/stretchr/testify)) = 1.5.1
Provides: bundled(golang(github.com/teris-io/shortid)) = 0.0.0-20171029131806.771a37caa5cf
Provides: bundled(golang(github.com/timberio/go-datemath)) = 0.1.1-0.20200323150745.74ddef604fff
Provides: bundled(golang(github.com/ua-parser/uap-go)) = 0.0.0-20190826212731.daf92ba38329
Provides: bundled(golang(github.com/uber/jaeger-client-go)) = 2.24.0+incompatible
Provides: bundled(golang(github.com/unknwon/com)) = 1.0.1
Provides: bundled(golang(github.com/urfave/cli/v2)) = 2.1.1
Provides: bundled(golang(github.com/xorcare/pointer)) = 1.1.0
Provides: bundled(golang(github.com/yudai/gojsondiff)) = 1.0.0
Provides: bundled(golang(golang.org/x/crypto)) = 0.0.0-20200406173513.056763e48d71
Provides: bundled(golang(golang.org/x/net)) = 0.0.0-20200501053045.e0ff5e5a1de5
Provides: bundled(golang(golang.org/x/oauth2)) = 0.0.0-20200107190931.bf48bf16ab8d
Provides: bundled(golang(golang.org/x/sync)) = 0.0.0-20200317015054.43a5402ce75a
Provides: bundled(golang(golang.org/x/xerrors)) = 0.0.0-20191204190536.9bdfabe68543
Provides: bundled(golang(google.golang.org/grpc)) = 1.29.1
Provides: bundled(golang(gopkg.in/ini.v1)) = 1.46.0
Provides: bundled(golang(gopkg.in/ldap.v3)) = 3.0.2
Provides: bundled(golang(gopkg.in/macaron.v1)) = 1.3.9
Provides: bundled(golang(gopkg.in/mail.v2)) = 2.3.1
Provides: bundled(golang(gopkg.in/redis.v5)) = 5.2.9
Provides: bundled(golang(gopkg.in/square/go-jose.v2)) = 2.4.1
Provides: bundled(golang(gopkg.in/yaml.v2)) = 2.2.8
Provides: bundled(golang(xorm.io/core)) = 0.7.3
Provides: bundled(golang(xorm.io/xorm)) = 0.8.1

# Declare all nodejs modules bundled in the webpack - this is for security
# purposes so if nodejs-foo ever needs an update, affected packages can be
# easily identified.
# Note: generated with the Makefile (see README.md)
Provides: bundled(nodejs-@grafana/slate-react) = 0.22.9-grafana
Provides: bundled(nodejs-@reduxjs/toolkit) = 1.3.4
Provides: bundled(nodejs-@torkelo/react-select) = 3.0.8
Provides: bundled(nodejs-@types/antlr4) = 4.7.1
Provides: bundled(nodejs-@types/braintree__sanitize-url) = 4.0.0
Provides: bundled(nodejs-@types/common-tags) = 1.8.0
Provides: bundled(nodejs-@types/jsurl) = 1.2.28
Provides: bundled(nodejs-@types/md5) = 2.1.33
Provides: bundled(nodejs-@types/react-loadable) = 5.5.2
Provides: bundled(nodejs-@types/react-virtualized-auto-sizer) = 1.0.0
Provides: bundled(nodejs-@welldone-software/why-did-you-render) = 4.0.6
Provides: bundled(nodejs-abortcontroller-polyfill) = 1.4.0
Provides: bundled(nodejs-angular) = 1.6.9
Provides: bundled(nodejs-angular-bindonce) = 0.3.1
Provides: bundled(nodejs-angular-native-dragdrop) = 1.2.2
Provides: bundled(nodejs-angular-route) = 1.6.6
Provides: bundled(nodejs-angular-sanitize) = 1.6.6
Provides: bundled(nodejs-antlr4) = 4.8.0
Provides: bundled(nodejs-baron) = 3.0.3
Provides: bundled(nodejs-brace) = 0.11.1
Provides: bundled(nodejs-calculate-size) = 1.1.1
Provides: bundled(nodejs-classnames) = 2.2.6
Provides: bundled(nodejs-clipboard) = 2.0.4
Provides: bundled(nodejs-common-tags) = 1.8.0
Provides: bundled(nodejs-core-js) = 1.2.7
Provides: bundled(nodejs-d3) = 5.15.0
Provides: bundled(nodejs-d3-scale-chromatic) = 1.5.0
Provides: bundled(nodejs-dangerously-set-html-content) = 1.0.6
Provides: bundled(nodejs-emotion) = 10.0.27
Provides: bundled(nodejs-eventemitter3) = 3.1.2
Provides: bundled(nodejs-fast-text-encoding) = 1.0.0
Provides: bundled(nodejs-file-saver) = 2.0.2
Provides: bundled(nodejs-hoist-non-react-statics) = 2.5.5
Provides: bundled(nodejs-immutable) = 3.8.2
Provides: bundled(nodejs-is-hotkey) = 0.1.4
Provides: bundled(nodejs-jquery) = 3.4.1
Provides: bundled(nodejs-jsurl) = 0.1.5
Provides: bundled(nodejs-lodash) = 3.10.1
Provides: bundled(nodejs-lru-cache) = 4.1.5
Provides: bundled(nodejs-marked) = 0.3.19
Provides: bundled(nodejs-md5) = 2.2.1
Provides: bundled(nodejs-memoize-one) = 4.1.0
Provides: bundled(nodejs-moment) = 2.24.0
Provides: bundled(nodejs-moment-timezone) = 0.5.28
Provides: bundled(nodejs-mousetrap) = 1.6.5
Provides: bundled(nodejs-mousetrap-global-bind) = 1.1.0
Provides: bundled(nodejs-nodemon) = 2.0.2
Provides: bundled(nodejs-papaparse) = 4.6.3
Provides: bundled(nodejs-prismjs) = 1.17.1
Provides: bundled(nodejs-prop-types) = 15.7.2
Provides: bundled(nodejs-rc-cascader) = 1.0.1
Provides: bundled(nodejs-re-resizable) = 6.2.0
Provides: bundled(nodejs-react) = 16.10.2
Provides: bundled(nodejs-react-dom) = 16.10.2
Provides: bundled(nodejs-react-grid-layout) = 0.17.1
Provides: bundled(nodejs-react-highlight-words) = 0.16.0
Provides: bundled(nodejs-react-loadable) = 5.5.0
Provides: bundled(nodejs-react-popper) = 1.3.3
Provides: bundled(nodejs-react-redux) = 7.2.0
Provides: bundled(nodejs-react-sizeme) = 2.6.8
Provides: bundled(nodejs-react-split-pane) = 0.1.89
Provides: bundled(nodejs-react-transition-group) = 2.9.0
Provides: bundled(nodejs-react-use) = 13.27.0
Provides: bundled(nodejs-react-virtualized-auto-sizer) = 1.0.2
Provides: bundled(nodejs-react-window) = 1.8.5
Provides: bundled(nodejs-redux) = 3.7.2
Provides: bundled(nodejs-redux-logger) = 3.0.6
Provides: bundled(nodejs-redux-thunk) = 2.3.0
Provides: bundled(nodejs-regenerator-runtime) = 0.11.1
Provides: bundled(nodejs-reselect) = 4.0.0
Provides: bundled(nodejs-rst2html) = 1.0.4
Provides: bundled(nodejs-rxjs) = 6.5.5
Provides: bundled(nodejs-search-query-parser) = 1.5.4
Provides: bundled(nodejs-slate) = 0.47.8
Provides: bundled(nodejs-slate-plain-serializer) = 0.7.10
Provides: bundled(nodejs-tether) = 1.4.7
Provides: bundled(nodejs-tether-drop) = 1.5.0
Provides: bundled(nodejs-tinycolor2) = 1.4.1
Provides: bundled(nodejs-tti-polyfill) = 0.2.2
Provides: bundled(nodejs-whatwg-fetch) = 3.0.0


%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.


%prep
%setup -q -T -D -b 0
rm -r plugins-bundled # compiled bundled plugins are in grafana-webpack
%setup -q -T -D -b 1
%setup -q -T -D -b 2

%patch1 -p1
%patch2 -p1
%if 0%{?fedora} >= 33
%patch3 -p1
%endif
%ifarch s390x
%patch4 -p1
%endif

# Set up build subdirs and links
mkdir -p %{_builddir}/src/github.com/grafana
ln -sf %{_builddir}/%{name}-%{version} \
    %{_builddir}/src/github.com/grafana/grafana


%build
# Build the server-side binaries
cd %{_builddir}/src/github.com/grafana/grafana
export GOPATH=%{_builddir}

# see grafana-X.X.X/build.go
export LDFLAGS="-X main.version=%{version} -X main.buildstamp=${SOURCE_DATE_EPOCH}"
for cmd in grafana-cli grafana-server; do
    %gobuild -o %{_builddir}/bin/${cmd} ./pkg/cmd/${cmd}
done

%install

# dirs, shared files, public html, webpack
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_libexecdir}/%{name}
cp -a conf public plugins-bundled %{buildroot}%{_datadir}/%{name}

# wrappers
install -p -m 755 packaging/wrappers/grafana-cli %{buildroot}%{_sbindir}/%{name}-cli

# binaries
install -p -m 755 %{_builddir}/bin/%{name}-server %{buildroot}%{_sbindir}
install -p -m 755 %{_builddir}/bin/%{name}-cli %{buildroot}%{_libexecdir}/%{name}

# man pages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 docs/man/man1/* %{buildroot}%{_mandir}/man1

# config dirs
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/dashboards
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/datasources
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/notifiers
install -d %{buildroot}%{_sysconfdir}/%{name}/provisioning/plugins
install -d %{buildroot}%{_sysconfdir}/sysconfig

# config defaults
install -p -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
install -p -m 640 conf/ldap.toml %{buildroot}%{_sysconfdir}/%{name}/ldap.toml
install -p -m 644 %{SOURCE3} %{buildroot}%{_datadir}/%{name}/conf/defaults.ini
install -p -m 644 packaging/rpm/sysconfig/grafana-server \
    %{buildroot}%{_sysconfdir}/sysconfig/grafana-server

# config database directory and plugins
install -d -m 750 %{buildroot}%{_sharedstatedir}/%{name}
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
# create grafana.db with secure permissions on new installations
# otherwise grafana-server is creating grafana.db on first start
# with world-readable permissions, which may leak encrypted datasource
# passwords to all users (if the secret_key in grafana.ini was not changed)

# https://bugzilla.redhat.com/show_bug.cgi?id=1805472
if [ "$1" = 1 ] && [ ! -f %{_sharedstatedir}/%{name}/grafana.db ]; then
    touch %{_sharedstatedir}/%{name}/grafana.db
fi

# apply secure permissions to grafana.db if it exists
# (may not exist on upgrades, because users can choose between sqlite/mysql/postgres)
if [ -f %{_sharedstatedir}/%{name}/grafana.db ]; then
    chown %{GRAFANA_USER}:%{GRAFANA_GROUP} %{_sharedstatedir}/%{name}/grafana.db
    chmod 640 %{_sharedstatedir}/%{name}/grafana.db
fi

# required for upgrades
chmod 640 %{_sysconfdir}/%{name}/grafana.ini
chmod 640 %{_sysconfdir}/%{name}/ldap.toml

%postun
%systemd_postun_with_restart grafana-server.service


%check
cd %{_builddir}/src/github.com/grafana/grafana
export GOPATH=%{_builddir}
# remove tests currently failing - these two are due to a symlink
# BUILD/src/github.com/grafana/grafana -> BUILD/grafana-6.6.1
rm -f pkg/services/provisioning/dashboards/file_reader_linux_test.go
rm -f pkg/services/provisioning/dashboards/file_reader_test.go
%gotest ./pkg/...


%files
# binaries and wrappers
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}-cli
%{_libexecdir}/%{name}

# config files
%dir %{_sysconfdir}/%{name}
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/dashboards
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/datasources
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/notifiers
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/plugins
%config(noreplace) %attr(0640, root, %{GRAFANA_GROUP}) %{_sysconfdir}/%{name}/grafana.ini
%config(noreplace) %attr(0640, root, %{GRAFANA_GROUP}) %{_sysconfdir}/%{name}/ldap.toml
%config(noreplace) %{_sysconfdir}/sysconfig/grafana-server

# Grafana configuration to dynamically create /run/grafana/grafana.pid on tmpfs
%{_tmpfilesdir}/%{name}.conf

# config database directory and plugins
%attr(0750, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}
%attr(-, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}/plugins

# shared directory and all files therein
%{_datadir}/%{name}
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
%doc CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md GOVERNANCE.md ISSUE_TRIAGE.md MAINTAINERS.md NOTICE.md
%doc PLUGIN_DEV.md README.md ROADMAP.md SECURITY.md SUPPORT.md UPGRADING_DEPENDENCIES.md WORKFLOW.md


%changelog
* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 30 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 7.1.1-1
- update to 7.1.1 tagged upstream community sources, see CHANGELOG
- merge all datasources into main grafana package
- bundle golang dependencies

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 05 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 6.7.4-1
- update to 6.7.4 tagged upstream community sources, see CHANGELOG
- security fix for CVE-2020-13379

* Tue Apr 28 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 6.7.3-1
- update to 6.7.3 tagged upstream community sources, see CHANGELOG
- add scripts to list Go dependencies and bundled npmjs dependencies
- set Grafana version in Grafana UI and grafana-cli --version
- declare README.md as documentation of datasource plugins
- create grafana.db on first installation (fixes RH BZ #1805472)
- change permissions of /var/lib/grafana to 750 (CVE-2020-12458)
- change permissions of /var/lib/grafana/grafana.db to 640 and
  user/group grafana:grafana (CVE-2020-12458)
- change permissions of grafana.ini and ldap.toml to 640 (CVE-2020-12459)

* Wed Feb 26 2020 Mark Goodwin <mgoodwin@redhat.com> 6.6.2-1
- added patch0 to set the version string correctly
- removed patch 004-xerrors.patch, it's now upstream
- added several patches for golang vendored vrs build dep differences
- added patch to move grafana-cli binary to libexec dir
- update to 6.6.2 tagged upstream community sources, see CHANGELOG

* Wed Nov 20 2019 Mark Goodwin <mgoodwin@redhat.com> 6.3.6-1
- add weak depenency on grafana-pcp
- add patch to mute shellcheck SC1090 for grafana-cli
- update to 6.3.6 upstream community sources, see CHANGELOG

* Thu Sep 05 2019 Mark Goodwin <mgoodwin@redhat.com> 6.3.5-1
- drop uaparser patch now it's upstream
- add xerrors patch, see https://github.com/golang/go/issues/32246
- use vendor sources on rawhide until modules are fully supported
- update to latest upstream community sources, see CHANGELOG

* Fri Aug 30 2019 Mark Goodwin <mgoodwin@redhat.com> 6.3.4-1
- include fix for CVE-2019-15043
- add patch for uaparser on 32bit systems
- update to latest upstream community sources, see CHANGELOG

* Wed Jul 31 2019 Mark Goodwin <mgoodwin@redhat.com> 6.2.5-1
- update to latest upstream community sources, see CHANGELOG

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 07 2019 Mark Goodwin <mgoodwin@redhat.com> 6.2.2-1
- split out some datasource plugins to sub-packages
- update to latest upstream community sources, see CHANGELOG

* Wed Jun 05 2019 Mark Goodwin <mgoodwin@redhat.com> 6.2.1-1
- update to latest upstream community sources, see CHANGELOG

* Fri May 24 2019 Mark Goodwin <mgoodwin@redhat.com> 6.2.0-1
- update to latest upstream community sources
- drop a couple of patches

* Wed May 08 2019 Mark Goodwin <mgoodwin@redhat.com> 6.1.6-2
- add conditional unbundle_vendor_sources macro

* Tue Apr 30 2019 Mark Goodwin <mgoodwin@redhat.com> 6.1.6-1
- update to latest upstream stable release 6.1.6, see CHANGELOG
- includes jQuery 3.4.0 security update

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
