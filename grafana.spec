%global grafana_arches %{lua: go_arches = {}
  for arch in rpm.expand("%{go_arches}"):gmatch("%S+") do
    go_arches[arch] = 1
  end
  for arch in rpm.expand("%{nodejs_arches}"):gmatch("%S+") do
    if go_arches[arch] then
      print(arch .. " ")
  end
end}

# Unbundle Grafana vendor sources and instead use BuildRequires
# on platforms that have enough golang devel support.
%if 0%{?rhel} == 0
%global           unbundle_vendor_sources 1
%endif

Name:             grafana
Version:          6.7.3
%global commit    a04ef6c
Release:          1%{?dist}
Summary:          Metrics dashboard and graph editor
License:          ASL 2.0
URL:              https://grafana.org

# Source0 contains the tagged upstream sources
Source0:          https://github.com/grafana/grafana/archive/v%{version}/%{name}-%{version}.tar.gz

# Source1 contains the front-end javascript modules bundled into a webpack
Source1:          grafana_webpack-%{version}.tar.gz

# Source2 is the script to create the above webpack from grafana sources
Source2:          make_grafana_webpack.sh

# Source3 contains Grafana configuration defaults for distributions
Source3:          distro-defaults.ini

# Patches
Patch1:           001-login-oauth-use-oauth2-exchange.patch
Patch2:           002-remove-jaeger-tracing.patch
Patch3:           003-manpages.patch
Patch4:           004-wrappers-grafana-cli.patch
Patch5:           005-pkg-main-fix-import-paths.patch
Patch6:           006-pkg-setting-ini-default-section.patch
Patch7:           007-pkg-prometheus-client-query-range.patch
Patch8:           008-pkg-services-notifications-codes-Unknwon.patch
Patch9:           009-pkg-fix-xorm-import.patch

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

BuildRequires:    git, systemd, golang, go-srpm-macros go-rpm-macros

Recommends: grafana-cloudwatch = %{version}-%{release}
Recommends: grafana-elasticsearch = %{version}-%{release}
Recommends: grafana-azure-monitor = %{version}-%{release}
Recommends: grafana-graphite = %{version}-%{release}
Recommends: grafana-influxdb = %{version}-%{release}
Recommends: grafana-loki = %{version}-%{release}
Recommends: grafana-mssql = %{version}-%{release}
Recommends: grafana-mysql = %{version}-%{release}
Recommends: grafana-opentsdb = %{version}-%{release}
Recommends: grafana-postgres = %{version}-%{release}
Recommends: grafana-prometheus = %{version}-%{release}
Recommends: grafana-stackdriver = %{version}-%{release}
Recommends: grafana-pcp >= 2

%if 0%{?unbundle_vendor_sources}
# golang build deps. These allow us to unbundle vendor golang source.
# Note: generated with the list_go_buildrequires.sh script (see README.md)
BuildRequires: golang(github.com/apache/arrow/go/arrow)
BuildRequires: golang(github.com/apache/arrow/go/arrow/array)
BuildRequires: golang(github.com/apache/arrow/go/arrow/ipc)
BuildRequires: golang(github.com/apache/arrow/go/arrow/memory)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/awsutil)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/credentials)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/credentials/ec2rolecreds)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/credentials/endpointcreds)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/defaults)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/ec2metadata)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/request)
BuildRequires: golang(github.com/aws/aws-sdk-go/aws/session)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/cloudwatch)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/ec2)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/ec2/ec2iface)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/resourcegroupstaggingapi)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/resourcegroupstaggingapi/resourcegroupstaggingapiiface)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/s3/s3manager)
BuildRequires: golang(github.com/aws/aws-sdk-go/service/sts)
BuildRequires: golang(github.com/benbjohnson/clock)
BuildRequires: golang(github.com/bradfitz/gomemcache/memcache)
BuildRequires: golang(github.com/BurntSushi/toml)
BuildRequires: golang(github.com/cheekybits/genny/generic)
BuildRequires: golang(github.com/crewjam/saml)
BuildRequires: golang(github.com/davecgh/go-spew/spew)
BuildRequires: golang(github.com/denisenkom/go-mssqldb)
BuildRequires: golang(github.com/facebookgo/inject)
BuildRequires: golang(github.com/fatih/color)
BuildRequires: golang(github.com/gobwas/glob)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/go-macaron/binding)
BuildRequires: golang(github.com/go-macaron/gzip)
BuildRequires: golang(github.com/go-macaron/session)
BuildRequires: golang(github.com/google/go-cmp/cmp)
BuildRequires: golang(github.com/google/go-cmp/cmp/cmpopts)
BuildRequires: golang(github.com/gorilla/websocket)
BuildRequires: golang(github.com/gosimple/slug)
BuildRequires: golang(github.com/go-sql-driver/mysql)
BuildRequires: golang(github.com/go-stack/stack)
BuildRequires: golang(github.com/go-xorm/core)
BuildRequires: golang(github.com/hashicorp/go-hclog)
BuildRequires: golang(github.com/hashicorp/go-plugin)
BuildRequires: golang(github.com/hashicorp/go-version)
BuildRequires: golang(github.com/inconshreveable/log15)
BuildRequires: golang(github.com/jmespath/go-jmespath)
BuildRequires: golang(github.com/jung-kurt/gofpdf)
BuildRequires: golang(github.com/lib/pq)
BuildRequires: golang(github.com/linkedin/goavro)
BuildRequires: golang(github.com/mattetti/filebuffer)
BuildRequires: golang(github.com/mattn/go-isatty)
BuildRequires: golang(github.com/mattn/go-sqlite3)
BuildRequires: golang(github.com/opentracing/opentracing-go)
BuildRequires: golang(github.com/opentracing/opentracing-go/ext)
BuildRequires: golang(github.com/opentracing/opentracing-go/log)
BuildRequires: golang(github.com/patrickmn/go-cache)
BuildRequires: golang(github.com/pkg/errors)
BuildRequires: golang(github.com/prometheus/client_golang/api)
BuildRequires: golang(github.com/prometheus/client_golang/api/prometheus/v1)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus/promhttp)
BuildRequires: golang(github.com/prometheus/client_model/go)
BuildRequires: golang(github.com/prometheus/common/expfmt)
BuildRequires: golang(github.com/prometheus/common/model)
BuildRequires: golang(github.com/robfig/cron)
BuildRequires: golang(github.com/smartystreets/goconvey/convey)
BuildRequires: golang(github.com/stretchr/testify/require)
BuildRequires: golang(github.com/teris-io/shortid)
BuildRequires: golang(github.com/ua-parser/uap-go/uaparser)
BuildRequires: golang(github.com/uber/jaeger-client-go/config)
BuildRequires: golang(github.com/uber/jaeger-client-go/zipkin)
BuildRequires: golang(github.com/Unknwon/com)
BuildRequires: golang(github.com/urfave/cli/v2)
BuildRequires: golang(github.com/VividCortex/mysqlerr)
BuildRequires: golang(github.com/yudai/gojsondiff)
BuildRequires: golang(github.com/yudai/gojsondiff/formatter)
BuildRequires: golang(golang.org/x/crypto/pbkdf2)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/net/context/ctxhttp)
BuildRequires: golang(golang.org/x/oauth2)
BuildRequires: golang(golang.org/x/oauth2/google)
BuildRequires: golang(golang.org/x/oauth2/jwt)
BuildRequires: golang(golang.org/x/sync/errgroup)
BuildRequires: golang(golang.org/x/xerrors)
BuildRequires: golang(google.golang.org/grpc)
BuildRequires: golang(google.golang.org/grpc/codes)
BuildRequires: golang(google.golang.org/grpc/metadata)
BuildRequires: golang(google.golang.org/grpc/status)
BuildRequires: golang(gopkg.in/ini.v1)
BuildRequires: golang(gopkg.in/ldap.v3)
BuildRequires: golang(gopkg.in/macaron.v1)
BuildRequires: golang(gopkg.in/mail.v2)
BuildRequires: golang(gopkg.in/redis.v5)
BuildRequires: golang(gopkg.in/robfig/cron.v3)
BuildRequires: golang(gopkg.in/square/go-jose.v2)
BuildRequires: golang(gopkg.in/square/go-jose.v2/jwt)
BuildRequires: golang(gopkg.in/yaml.v2)
BuildRequires: golang(xorm.io/xorm)
%endif

# Declare all nodejs modules bundled in the webpack - this is for security
# purposes so if nodejs-foo ever needs an update, affected packages can be
# easily identified.
# Note: generated with the list_bundled_nodejs_packages.sh script (see README.md)
Provides: bundled(nodejs-@braintree/sanitize-url) = 4.0.0
Provides: bundled(nodejs-@grafana/slate-react) = 0.22.9-grafana
Provides: bundled(nodejs-@reduxjs/toolkit) = 1.2.1
Provides: bundled(nodejs-@torkelo/react-select) = 3.0.8
Provides: bundled(nodejs-@types/md5) = 2.1.33
Provides: bundled(nodejs-@types/react-loadable) = 5.5.2
Provides: bundled(nodejs-@types/react-virtualized-auto-sizer) = 1.0.0
Provides: bundled(nodejs-@types/uuid) = 3.4.7
Provides: bundled(nodejs-abortcontroller-polyfill) = 1.4.0
Provides: bundled(nodejs-angular) = 1.6.9
Provides: bundled(nodejs-angular-bindonce) = 0.3.1
Provides: bundled(nodejs-angular-native-dragdrop) = 1.2.2
Provides: bundled(nodejs-angular-route) = 1.6.6
Provides: bundled(nodejs-angular-sanitize) = 1.6.6
Provides: bundled(nodejs-baron) = 3.0.3
Provides: bundled(nodejs-brace) = 0.10.0
Provides: bundled(nodejs-calculate-size) = 1.1.1
Provides: bundled(nodejs-classnames) = 2.2.6
Provides: bundled(nodejs-clipboard) = 2.0.4
Provides: bundled(nodejs-core-js) = 1.2.7
Provides: bundled(nodejs-d3) = 5.15.0
Provides: bundled(nodejs-d3-scale-chromatic) = 1.5.0
Provides: bundled(nodejs-emotion) = 10.0.27
Provides: bundled(nodejs-eventemitter3) = 2.0.3
Provides: bundled(nodejs-fast-text-encoding) = 1.0.0
Provides: bundled(nodejs-file-saver) = 1.3.8
Provides: bundled(nodejs-hoist-non-react-statics) = 3.3.0
Provides: bundled(nodejs-immutable) = 3.8.2
Provides: bundled(nodejs-is-hotkey) = 0.1.4
Provides: bundled(nodejs-jquery) = 3.4.1
Provides: bundled(nodejs-lodash) = 3.10.1
Provides: bundled(nodejs-lru-cache) = 4.1.5
Provides: bundled(nodejs-marked) = 0.3.19
Provides: bundled(nodejs-md5) = 2.2.1
Provides: bundled(nodejs-memoize-one) = 4.1.0
Provides: bundled(nodejs-moment) = 2.24.0
Provides: bundled(nodejs-mousetrap) = 1.6.3
Provides: bundled(nodejs-mousetrap-global-bind) = 1.1.0
Provides: bundled(nodejs-nodemon) = 1.18.10
Provides: bundled(nodejs-papaparse) = 4.6.3
Provides: bundled(nodejs-prismjs) = 1.16.0
Provides: bundled(nodejs-prop-types) = 15.7.2
Provides: bundled(nodejs-rc-cascader) = 0.17.5
Provides: bundled(nodejs-re-resizable) = 6.2.0
Provides: bundled(nodejs-react) = 16.10.2
Provides: bundled(nodejs-react-dom) = 16.10.2
Provides: bundled(nodejs-react-grid-layout) = 0.17.1
Provides: bundled(nodejs-react-highlight-words) = 0.11.0
Provides: bundled(nodejs-react-loadable) = 5.5.0
Provides: bundled(nodejs-react-popper) = 1.3.3
Provides: bundled(nodejs-react-redux) = 7.1.1
Provides: bundled(nodejs-react-sizeme) = 2.5.2
Provides: bundled(nodejs-react-split-pane) = 0.1.89
Provides: bundled(nodejs-react-transition-group) = 2.6.1
Provides: bundled(nodejs-react-use) = 12.8.0
Provides: bundled(nodejs-react-virtualized-auto-sizer) = 1.0.2
Provides: bundled(nodejs-react-window) = 1.7.1
Provides: bundled(nodejs-redux) = 3.7.2
Provides: bundled(nodejs-redux-logger) = 3.0.6
Provides: bundled(nodejs-redux-thunk) = 2.3.0
Provides: bundled(nodejs-regenerator-runtime) = 0.11.1
Provides: bundled(nodejs-reselect) = 4.0.0
Provides: bundled(nodejs-rst2html) = 1.0.4
Provides: bundled(nodejs-rxjs) = 5.5.12
Provides: bundled(nodejs-search-query-parser) = 1.5.2
Provides: bundled(nodejs-slate) = 0.47.8
Provides: bundled(nodejs-slate-plain-serializer) = 0.7.10
Provides: bundled(nodejs-tether) = 1.4.5
Provides: bundled(nodejs-tether-drop) = 1.5.0
Provides: bundled(nodejs-tinycolor2) = 1.4.1
Provides: bundled(nodejs-tti-polyfill) = 0.2.2
Provides: bundled(nodejs-uuid) = 3.3.3
Provides: bundled(nodejs-whatwg-fetch) = 3.0.0
Provides: bundled(nodejs-xss) = 1.0.3


%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.


%package cloudwatch
Requires: %{name} = %{version}-%{release}
Summary: Grafana cloudwatch datasource

%description cloudwatch
The Grafana cloudwatch datasource.

%package elasticsearch
Requires: %{name} = %{version}-%{release}
Summary: Grafana elasticsearch datasource

%description elasticsearch
The Grafana elasticsearch datasource.

%package azure-monitor
Requires: %{name} = %{version}-%{release}
Summary: Grafana azure-monitor datasource

%description azure-monitor
The Grafana azure-monitor datasource.

%package graphite
Requires: %{name} = %{version}-%{release}
Summary: Grafana graphite datasource

%description graphite
The Grafana graphite datasource.

%package influxdb
Requires: %{name} = %{version}-%{release}
Summary: Grafana influxdb datasource

%description influxdb
The Grafana influxdb datasource.

%package loki
Requires: %{name} = %{version}-%{release}
Summary: Grafana loki datasource

%description loki
The Grafana loki datasource.

%package mssql
Requires: %{name} = %{version}-%{release}
Summary: Grafana mssql datasource

%description mssql
The Grafana mssql datasource.

%package mysql
Requires: %{name} = %{version}-%{release}
Summary: Grafana mysql datasource

%description mysql
The Grafana mysql datasource.

%package opentsdb
Requires: %{name} = %{version}-%{release}
Summary: Grafana opentsdb datasource

%description opentsdb
The Grafana opentsdb datasource.

%package postgres
Requires: %{name} = %{version}-%{release}
Summary: Grafana postgres datasource

%description postgres
The Grafana postgres datasource.

%package prometheus
Requires: %{name} = %{version}-%{release}
Summary: Grafana prometheus datasource

%description prometheus
The Grafana prometheus datasource.

%package stackdriver
Requires: %{name} = %{version}-%{release}
Summary: Grafana stackdriver datasource

%description stackdriver
The Grafana stackdriver datasource.


%prep
%setup -q -T -D -b 0
%setup -q -T -D -b 1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

# Set up build subdirs and links
mkdir -p %{_builddir}/src/github.com/grafana
ln -sf %{_builddir}/%{name}-%{version} \
    %{_builddir}/src/github.com/grafana/grafana

# remove some (apparent) development files, for rpmlint
rm -f public/sass/.sass-lint.yml public/test/.jshintrc

%if 0%{?unbundle_vendor_sources}
# Unbundle all grafana vendor sources, as per BuildRequires above.
# Note there are some exceptions.
cp --parents -a \
    vendor/github.com/grafana/grafana-plugin-model \
    vendor/github.com/grafana/grafana-plugin-sdk-go \
    %{_builddir}
rm -r vendor # remove all vendor sources
mv %{_builddir}/vendor vendor # put back what we're keeping
%endif

%build
# Build the server-side binaries
cd %{_builddir}/src/github.com/grafana/grafana
%global archbindir bin/`go env GOOS`-`go env GOARCH`
echo _builddir=%{_builddir} archbindir=%{archbindir} gopath=%{gopath}
[ ! -d %{archbindir} ] && mkdir -p %{archbindir}

# non-modular build
export GOPATH=%{_builddir}:%{gopath}
export GO111MODULE=off; rm -f go.mod

# see grafana-X.X.X/build.go
export LDFLAGS="-X main.version=%{version} -X main.commit=%{commit} -X main.buildstamp=${SOURCE_DATE_EPOCH} -X main.buildBranch=master"
for cmd in grafana-cli grafana-server; do
    %gobuild -o %{archbindir}/${cmd} ./pkg/cmd/${cmd}
done

%install
# Fix up arch bin directories
[ ! -d bin/x86_64 ] && ln -sf linux-amd64 bin/x86_64
[ ! -d bin/i386 ] && ln -sf linux-386 bin/i386
[ ! -d bin/ppc64le ] && ln -sf linux-ppc64le bin/ppc64le
[ ! -d bin/s390x ] && ln -sf linux-s390x bin/s390x
[ ! -d bin/arm ] && ln -sf linux-arm bin/arm
[ ! -d bin/arm64 ] && ln -sf linux-arm64 bin/aarch64
[ ! -d bin/aarch64 ] && ln -sf linux-aarch64 bin/aarch64

# dirs, shared files, public html, webpack
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/%{name}
install -d %{buildroot}%{_libexecdir}/%{name}
cp -a conf public %{buildroot}%{_datadir}/%{name}

# wrappers
install -p -m 755 packaging/wrappers/grafana-cli %{buildroot}%{_sbindir}/%{name}-cli

# binaries
install -p -m 755 %{archbindir}/%{name}-server %{buildroot}%{_sbindir}
install -p -m 755 %{archbindir}/%{name}-cli %{buildroot}%{_libexecdir}/%{name}

# man pages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 docs/man/man1/* %{buildroot}%{_mandir}/man1

# config dirs
install -d %{buildroot}%{_sysconfdir}/%{name}
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

%postun
%systemd_postun_with_restart grafana-server.service


%check
cd %{_builddir}/src/github.com/grafana/grafana
export GOPATH=%{_builddir}:%{gopath}
# remove tests currently failing - these two are due to a symlink
# BUILD/src/github.com/grafana/grafana -> BUILD/grafana-6.6.1
rm -f pkg/services/provisioning/dashboards/file_reader_linux_test.go
rm -f pkg/services/provisioning/dashboards/file_reader_test.go
export GO111MODULE=off
%gotest ./pkg/...


%files
# binaries and wrappers
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}-cli
%{_libexecdir}/%{name}

# config files
%dir %{_sysconfdir}/%{name}
%config(noreplace) %attr(640, root, %{GRAFANA_GROUP}) %{_sysconfdir}/%{name}/grafana.ini
%config(noreplace) %attr(640, root, %{GRAFANA_GROUP}) %{_sysconfdir}/%{name}/ldap.toml
%config(noreplace) %{_sysconfdir}/sysconfig/grafana-server

# Grafana configuration to dynamically create /run/grafana/grafana.pid on tmpfs
%{_tmpfilesdir}/%{name}.conf

# config database directory and plugins
%attr(750, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}
%attr(-, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}/plugins

# shared directory and all files therein, except some datasources
%{_datadir}/%{name}

# built-in datasources that are sub-packaged
%global dsdir %{_datadir}/%{name}/public/app/plugins/datasource
%exclude %{dsdir}/cloudwatch 
%exclude %{dsdir}/elasticsearch 
%exclude %{dsdir}/graphite
%exclude %{dsdir}/grafana-azure-monitor-datasource
%exclude %{dsdir}/influxdb
%exclude %{dsdir}/loki
%exclude %{dsdir}/mssql
%exclude %{dsdir}/mysql
%exclude %{dsdir}/opentsdb
%exclude %{dsdir}/postgres
%exclude %{dsdir}/prometheus
%exclude %{dsdir}/stackdriver

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

#
# datasources split out into subpackages
#
%files cloudwatch
%{_datadir}/%{name}/public/app/plugins/datasource/cloudwatch
%doc %{_datadir}/%{name}/public/app/plugins/datasource/cloudwatch/README.md

%files elasticsearch
%{_datadir}/%{name}/public/app/plugins/datasource/elasticsearch
%doc %{_datadir}/%{name}/public/app/plugins/datasource/elasticsearch/README.md

%files azure-monitor
%{_datadir}/%{name}/public/app/plugins/datasource/grafana-azure-monitor-datasource

%files graphite
%{_datadir}/%{name}/public/app/plugins/datasource/graphite
%doc %{_datadir}/%{name}/public/app/plugins/datasource/graphite/README.md

%files influxdb
%{_datadir}/%{name}/public/app/plugins/datasource/influxdb
%doc %{_datadir}/%{name}/public/app/plugins/datasource/influxdb/README.md

%files loki
%{_datadir}/%{name}/public/app/plugins/datasource/loki
%doc %{_datadir}/%{name}/public/app/plugins/datasource/loki/README.md

%files mssql
%{_datadir}/%{name}/public/app/plugins/datasource/mssql
%doc %{_datadir}/%{name}/public/app/plugins/datasource/mssql/README.md

%files mysql
%{_datadir}/%{name}/public/app/plugins/datasource/mysql
%doc %{_datadir}/%{name}/public/app/plugins/datasource/mysql/README.md

%files opentsdb
%{_datadir}/%{name}/public/app/plugins/datasource/opentsdb
%doc %{_datadir}/%{name}/public/app/plugins/datasource/opentsdb/README.md

%files postgres
%{_datadir}/%{name}/public/app/plugins/datasource/postgres
%doc %{_datadir}/%{name}/public/app/plugins/datasource/postgres/README.md

%files prometheus
%{_datadir}/%{name}/public/app/plugins/datasource/prometheus
%doc %{_datadir}/%{name}/public/app/plugins/datasource/prometheus/README.md

%files stackdriver
%{_datadir}/%{name}/public/app/plugins/datasource/stackdriver
%doc %{_datadir}/%{name}/public/app/plugins/datasource/stackdriver/README.md


%changelog
* Thu Apr 23 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 6.7.3-1
- update to 6.7.3 tagged upstream community sources, see CHANGELOG
- set grafana version in Grafana UI and grafana-cli --version
- declare README.md as documentation of datasource plugins
- create grafana.db on first installation (fixes RH BZ #1805472)
- change permissions of /var/lib/grafana to 750
- change permissions of /var/lib/grafana/grafana.db to 640 and
  user/group grafana:grafana
- change permissions of grafana.ini and ldap.toml to 640
  (contains secret_key/bind_password)

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
