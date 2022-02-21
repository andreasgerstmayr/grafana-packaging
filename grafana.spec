# Specify if the frontend will be compiled as part of the build or
# is attached as a webpack tarball (in case of an unsuitable nodejs version on the build system)
%define compile_frontend 0

%if 0%{?rhel}
%define enable_fips_mode 1
%else
%define enable_fips_mode 0
%endif

%global grafana_arches %{lua: go_arches = {}
  for arch in rpm.expand("%{go_arches}"):gmatch("%S+") do
    go_arches[arch] = 1
  end
  for arch in rpm.expand("%{nodejs_arches}"):gmatch("%S+") do
    if go_arches[arch] then
      print(arch .. " ")
  end
end}

%global gomodulesmode GO111MODULE=auto

Name:             grafana
Version:          8.4.1
Release:          1%{?dist}
Summary:          Metrics dashboard and graph editor
License:          AGPLv3
URL:              https://grafana.org

# Source0 contains the tagged upstream sources
Source0:          https://github.com/grafana/grafana/archive/v%{version}/%{name}-%{version}.tar.gz

# Source1 contains the bundled Go and Node.js dependencies
# Note: In case there were no changes to this tarball, the NVR of this tarball
# lags behind the NVR of this package.
Source1:          grafana-vendor-%{version}-1.tar.xz

%if %{compile_frontend} == 0
# Source2 contains the precompiled frontend
# Note: In case there were no changes to this tarball, the NVR of this tarball
# lags behind the NVR of this package.
Source2:          grafana-webpack-%{version}-1.tar.gz
%endif

# Source3 contains the Makefile to create the required bundles
Source3:          Makefile

# Source4 contains the script to build the frontend
Source4:          build_frontend.sh

# Source5 contains the script to generate the list of bundled nodejs packages
Source5:          list_bundled_nodejs_packages.py

# Patches
Patch1:           001-wrappers-grafana-cli.patch
Patch2:           002-manpages.patch
Patch3:           003-default-configuration.patch

# Required for s390x
# the golden files include memory dumps from a x86 machine
# integers are stored as little endian on x86, but as big endian on s390x
# therefore loading this memory dump fails on s390x
Patch4:           004-skip-x86-goldenfiles-tests.patch

Patch5:           005-remove-unused-backend-dependencies.patch

Patch8:           008-remove-unused-frontend-crypto.patch

# The Makefile removes a few files with crypto implementations
# from the vendor tarball, which are not used in Grafana.
# This patch removes all references to the deleted files.
Patch9:           009-patch-removed-backend-crypto.patch

# This patch modifies the x/crypto/pbkdf2 function to use OpenSSL
# if FIPS mode is enabled.
Patch10:          010-fips.patch

# https://github.com/grafana/grafana/pull/42334
Patch11:          011-use-hmac-sha-256-for-password-reset-tokens.patch

# gonum.org/v1/gonum supports go1.18 since commit cccd8af5f6bd1539dd688c88102cb37e9117f96a
# https://github.com/gonum/gonum/pull/1729
Patch12:          012-support-go1.18.patch

# disable husky git hook
Patch13:          013-disable-husky.patch

# skip test which tries to install a plugin from the grafana.com marketplace
# and requires internet connectivity
Patch14:          014-skip-marketplace-plugin-install-test.patch

# Intersection of go_arches and nodejs_arches
ExclusiveArch:    %{grafana_arches}
ExcludeArch:      i686

BuildRequires:    systemd
BuildRequires:    golang >= 1.17
BuildRequires:    go-srpm-macros
%if 0%{?fedora} >= 31
BuildRequires:    go-rpm-macros
%endif

%if %{compile_frontend}
BuildRequires:    nodejs >= 1:16
BuildRequires:    yarnpkg
%endif

%if %{enable_fips_mode}
BuildRequires:    openssl-devel
%endif

%global           GRAFANA_USER %{name}
%global           GRAFANA_GROUP %{name}
%global           GRAFANA_HOME %{_datadir}/%{name}

# grafana-server service daemon uses systemd
%{?systemd_requires}
Requires(pre):    shadow-utils

%if 0%{?fedora} || 0%{?rhel} > 7
Recommends: grafana-pcp
%endif

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
Provides:         grafana-cloudwatch = 7.1.1-1
Provides:         grafana-elasticsearch = 7.1.1-1
Provides:         grafana-azure-monitor = 7.1.1-1
Provides:         grafana-graphite = 7.1.1-1
Provides:         grafana-influxdb = 7.1.1-1
Provides:         grafana-loki = 7.1.1-1
Provides:         grafana-mssql = 7.1.1-1
Provides:         grafana-mysql = 7.1.1-1
Provides:         grafana-opentsdb = 7.1.1-1
Provides:         grafana-postgres = 7.1.1-1
Provides:         grafana-prometheus = 7.1.1-1
Provides:         grafana-stackdriver = 7.1.1-1

# vendored golang and node.js build dependencies
# this is for security purposes, if nodejs-foo ever needs an update,
# affected packages can be easily identified.
# Note: generated by the Makefile (see README.md)
Provides: bundled(golang(cloud.google.com/go/storage)) = 1.14.0
Provides: bundled(golang(cuelang.org/go)) = 0.4.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go)) = 57.1.0+incompatible
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/azcore)) = 0.19.0
Provides: bundled(golang(github.com/Azure/azure-sdk-for-go/sdk/azidentity)) = 0.10.0
Provides: bundled(golang(github.com/Azure/go-autorest/autorest)) = 0.11.20
Provides: bundled(golang(github.com/BurntSushi/toml)) = 0.3.1
Provides: bundled(golang(github.com/Masterminds/semver)) = 1.5.0
Provides: bundled(golang(github.com/VividCortex/mysqlerr)) = 0.0.0-20170204212430.6c6b55f8796f
Provides: bundled(golang(github.com/aws/aws-sdk-go)) = 1.40.37
Provides: bundled(golang(github.com/beevik/etree)) = 1.1.0
Provides: bundled(golang(github.com/benbjohnson/clock)) = 1.1.0
Provides: bundled(golang(github.com/bradfitz/gomemcache)) = 0.0.0-20190913173617.a41fca850d0b
Provides: bundled(golang(github.com/centrifugal/centrifuge)) = 0.19.0
Provides: bundled(golang(github.com/cortexproject/cortex)) = 1.10.1-0.20211014125347.85c378182d0d
Provides: bundled(golang(github.com/davecgh/go-spew)) = 1.1.1
Provides: bundled(golang(github.com/denisenkom/go-mssqldb)) = 0.10.0
Provides: bundled(golang(github.com/dop251/goja)) = 0.0.0-20210804101310.32956a348b49
Provides: bundled(golang(github.com/fatih/color)) = 1.10.0
Provides: bundled(golang(github.com/gchaincl/sqlhooks)) = 1.3.0
Provides: bundled(golang(github.com/getsentry/sentry-go)) = 0.10.0
Provides: bundled(golang(github.com/go-openapi/strfmt)) = 0.20.2
Provides: bundled(golang(github.com/go-redis/redis/v8)) = 8.11.4
Provides: bundled(golang(github.com/go-sourcemap/sourcemap)) = 2.1.3+incompatible
Provides: bundled(golang(github.com/go-sql-driver/mysql)) = 1.6.0
Provides: bundled(golang(github.com/go-stack/stack)) = 1.8.0
Provides: bundled(golang(github.com/gobwas/glob)) = 0.2.3
Provides: bundled(golang(github.com/gofrs/uuid)) = 4.0.0+incompatible
Provides: bundled(golang(github.com/gogo/protobuf)) = 1.3.2
Provides: bundled(golang(github.com/golang/mock)) = 1.6.0
Provides: bundled(golang(github.com/golang/snappy)) = 0.0.4
Provides: bundled(golang(github.com/google/go-cmp)) = 0.5.7
Provides: bundled(golang(github.com/google/uuid)) = 1.3.0
Provides: bundled(golang(github.com/google/wire)) = 0.5.0
Provides: bundled(golang(github.com/gorilla/websocket)) = 1.4.2
Provides: bundled(golang(github.com/gosimple/slug)) = 1.9.0
Provides: bundled(golang(github.com/grafana/cuetsy)) = 0.0.0-20211119211437.8c25464cc9bf
Provides: bundled(golang(github.com/grafana/grafana-aws-sdk)) = 0.10.0
Provides: bundled(golang(github.com/grafana/grafana-plugin-sdk-go)) = 0.126.0
Provides: bundled(golang(github.com/grafana/loki)) = 1.6.2-0.20211015002020.7832783b1caa
Provides: bundled(golang(github.com/grpc-ecosystem/go-grpc-middleware)) = 1.3.0
Provides: bundled(golang(github.com/hashicorp/go-hclog)) = 0.16.1
Provides: bundled(golang(github.com/hashicorp/go-plugin)) = 1.4.3
Provides: bundled(golang(github.com/hashicorp/go-version)) = 1.3.0
Provides: bundled(golang(github.com/influxdata/influxdb-client-go/v2)) = 2.6.0
Provides: bundled(golang(github.com/influxdata/line-protocol)) = 0.0.0-20210311194329.9aa0e372d097
Provides: bundled(golang(github.com/jmespath/go-jmespath)) = 0.4.0
Provides: bundled(golang(github.com/json-iterator/go)) = 1.1.12
Provides: bundled(golang(github.com/laher/mergefs)) = 0.1.1
Provides: bundled(golang(github.com/lib/pq)) = 1.10.0
Provides: bundled(golang(github.com/linkedin/goavro/v2)) = 2.10.0
Provides: bundled(golang(github.com/m3db/prometheus_remote_client_golang)) = 0.4.4
Provides: bundled(golang(github.com/magefile/mage)) = 1.12.1
Provides: bundled(golang(github.com/mattn/go-isatty)) = 0.0.12
Provides: bundled(golang(github.com/mattn/go-sqlite3)) = 1.14.7
Provides: bundled(golang(github.com/matttproud/golang_protobuf_extensions)) = 1.0.2-0.20181231171920.c182affec369
Provides: bundled(golang(github.com/mwitkow/go-conntrack)) = 0.0.0-20190716064945.2f068394615f
Provides: bundled(golang(github.com/ohler55/ojg)) = 1.12.9
Provides: bundled(golang(github.com/opentracing/opentracing-go)) = 1.2.0
Provides: bundled(golang(github.com/patrickmn/go-cache)) = 2.1.0+incompatible
Provides: bundled(golang(github.com/pkg/errors)) = 0.9.1
Provides: bundled(golang(github.com/prometheus/alertmanager)) = 0.23.1-0.20211116083607.e2a10119aaf7
Provides: bundled(golang(github.com/prometheus/client_golang)) = 1.12.1
Provides: bundled(golang(github.com/prometheus/client_model)) = 0.2.0
Provides: bundled(golang(github.com/prometheus/common)) = 0.32.1
Provides: bundled(golang(github.com/prometheus/prometheus)) = 1.8.2-0.20211011171444.354d8d2ecfac
Provides: bundled(golang(github.com/robfig/cron)) = 0.0.0-20180505203441.b41be1df6967
Provides: bundled(golang(github.com/robfig/cron/v3)) = 3.0.1
Provides: bundled(golang(github.com/russellhaering/goxmldsig)) = 1.1.1
Provides: bundled(golang(github.com/stretchr/testify)) = 1.7.0
Provides: bundled(golang(github.com/teris-io/shortid)) = 0.0.0-20171029131806.771a37caa5cf
Provides: bundled(golang(github.com/ua-parser/uap-go)) = 0.0.0-20211112212520.00c877edfe0f
Provides: bundled(golang(github.com/uber/jaeger-client-go)) = 2.29.1+incompatible
Provides: bundled(golang(github.com/unknwon/com)) = 1.0.1
Provides: bundled(golang(github.com/urfave/cli/v2)) = 2.3.0
Provides: bundled(golang(github.com/vectordotdev/go-datemath)) = 0.1.1-0.20220110192739.f9ce83ec349f
Provides: bundled(golang(github.com/weaveworks/common)) = 0.0.0-20210913144402.035033b78a78
Provides: bundled(golang(github.com/xorcare/pointer)) = 1.1.0
Provides: bundled(golang(github.com/yudai/gojsondiff)) = 1.0.0
Provides: bundled(golang(go.opentelemetry.io/collector)) = 0.31.0
Provides: bundled(golang(go.opentelemetry.io/collector/model)) = 0.31.0
Provides: bundled(golang(go.opentelemetry.io/otel)) = 1.2.0
Provides: bundled(golang(go.opentelemetry.io/otel/exporters/jaeger)) = 1.0.0
Provides: bundled(golang(go.opentelemetry.io/otel/sdk)) = 1.0.0
Provides: bundled(golang(go.opentelemetry.io/otel/trace)) = 1.2.0
Provides: bundled(golang(golang.org/x/crypto)) = 0.0.0-20210616213533.5ff15b29337e
Provides: bundled(golang(golang.org/x/net)) = 0.0.0-20210903162142.ad29c8ab022f
Provides: bundled(golang(golang.org/x/oauth2)) = 0.0.0-20210819190943.2bc19b11175f
Provides: bundled(golang(golang.org/x/sync)) = 0.0.0-20210220032951.036812b2e83c
Provides: bundled(golang(golang.org/x/time)) = 0.0.0-20210723032227.1f47c861a9ac
Provides: bundled(golang(golang.org/x/tools)) = 0.1.5
Provides: bundled(golang(gonum.org/v1/gonum)) = 0.9.3
Provides: bundled(golang(google.golang.org/api)) = 0.58.0
Provides: bundled(golang(google.golang.org/grpc)) = 1.41.0
Provides: bundled(golang(google.golang.org/protobuf)) = 1.27.1
Provides: bundled(golang(gopkg.in/ini.v1)) = 1.62.0
Provides: bundled(golang(gopkg.in/ldap.v3)) = 3.1.0
Provides: bundled(golang(gopkg.in/mail.v2)) = 2.3.1
Provides: bundled(golang(gopkg.in/square/go-jose.v2)) = 2.5.1
Provides: bundled(golang(gopkg.in/yaml.v2)) = 2.4.0
Provides: bundled(golang(gopkg.in/yaml.v3)) = 3.0.0-20210107192922.496545a6307b
Provides: bundled(golang(xorm.io/builder)) = 0.3.6
Provides: bundled(golang(xorm.io/core)) = 0.7.3
Provides: bundled(golang(xorm.io/xorm)) = 0.8.2
Provides: bundled(golang(github.com/andybalholm/brotli)) = 1.0.3
Provides: bundled(golang(github.com/go-kit/log)) = 0.1.0
Provides: bundled(golang(github.com/go-openapi/loads)) = 0.20.2
Provides: bundled(golang(github.com/go-openapi/spec)) = 0.20.4
Provides: bundled(golang(github.com/grafana/grafana-google-sdk-go)) = 0.0.0-20211104130251.b190293eaf58
Provides: bundled(golang(github.com/hashicorp/golang-lru)) = 0.5.4
Provides: bundled(golang(github.com/segmentio/encoding)) = 0.3.2
Provides: bundled(npm(@babel/core)) = 7.12.9
Provides: bundled(npm(@babel/plugin-proposal-nullish-coalescing-operator)) = 7.14.5
Provides: bundled(npm(@babel/plugin-proposal-object-rest-spread)) = 7.12.1
Provides: bundled(npm(@babel/plugin-proposal-optional-chaining)) = 7.14.5
Provides: bundled(npm(@babel/plugin-syntax-dynamic-import)) = 7.8.3
Provides: bundled(npm(@babel/plugin-transform-react-constant-elements)) = 7.16.7
Provides: bundled(npm(@babel/plugin-transform-runtime)) = 7.17.0
Provides: bundled(npm(@babel/plugin-transform-typescript)) = 7.15.8
Provides: bundled(npm(@babel/preset-env)) = 7.13.12
Provides: bundled(npm(@babel/preset-react)) = 7.14.5
Provides: bundled(npm(@babel/preset-typescript)) = 7.15.0
Provides: bundled(npm(@betterer/cli)) = 5.1.6
Provides: bundled(npm(@betterer/regexp)) = 5.1.6
Provides: bundled(npm(@emotion/css)) = 10.0.27
Provides: bundled(npm(@emotion/eslint-plugin)) = 11.7.0
Provides: bundled(npm(@emotion/react)) = 11.5.0
Provides: bundled(npm(@grafana/api-documenter)) = 7.11.2
Provides: bundled(npm(@grafana/aws-sdk)) = 0.0.33
Provides: bundled(npm(@grafana/data)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/e2e)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/e2e-selectors)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/eslint-config)) = 2.5.2
Provides: bundled(npm(@grafana/experimental)) = 0.0.2-canary.18
Provides: bundled(npm(@grafana/google-sdk)) = 0.0.2
Provides: bundled(npm(@grafana/runtime)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/schema)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/slate-react)) = 0.22.10-grafana
Provides: bundled(npm(@grafana/toolkit)) = 0.0.0-use.local
Provides: bundled(npm(@grafana/tsconfig)) = 1.0.0rc1
Provides: bundled(npm(@grafana/ui)) = 0.0.0-use.local
Provides: bundled(npm(@jaegertracing/jaeger-ui-components)) = 0.0.0-use.local
Provides: bundled(npm(@kusto/monaco-kusto)) = 4.1.3
Provides: bundled(npm(@lingui/cli)) = 3.13.2
Provides: bundled(npm(@lingui/core)) = 3.13.2
Provides: bundled(npm(@lingui/macro)) = 3.12.1
Provides: bundled(npm(@lingui/react)) = 3.13.2
Provides: bundled(npm(@microsoft/api-extractor)) = 7.19.4
Provides: bundled(npm(@opentelemetry/api)) = 1.1.0
Provides: bundled(npm(@opentelemetry/exporter-collector)) = 0.25.0
Provides: bundled(npm(@opentelemetry/semantic-conventions)) = 0.25.0
Provides: bundled(npm(@pmmmwh/react-refresh-webpack-plugin)) = 0.5.1
Provides: bundled(npm(@popperjs/core)) = 2.10.2
Provides: bundled(npm(@react-aria/button)) = 3.3.4
Provides: bundled(npm(@react-aria/dialog)) = 3.1.4
Provides: bundled(npm(@react-aria/focus)) = 3.5.0
Provides: bundled(npm(@react-aria/interactions)) = 3.6.0
Provides: bundled(npm(@react-aria/menu)) = 3.3.0
Provides: bundled(npm(@react-aria/overlays)) = 3.7.3
Provides: bundled(npm(@react-aria/utils)) = 3.9.0
Provides: bundled(npm(@react-stately/collections)) = 3.3.4
Provides: bundled(npm(@react-stately/menu)) = 3.2.3
Provides: bundled(npm(@react-stately/tree)) = 3.2.0
Provides: bundled(npm(@react-types/button)) = 3.4.1
Provides: bundled(npm(@react-types/menu)) = 3.4.1
Provides: bundled(npm(@react-types/overlays)) = 3.5.1
Provides: bundled(npm(@react-types/shared)) = 3.9.0
Provides: bundled(npm(@reduxjs/toolkit)) = 1.7.2
Provides: bundled(npm(@rtsao/plugin-proposal-class-properties)) = 7.0.1-patch.1
Provides: bundled(npm(@sentry/browser)) = 6.17.4
Provides: bundled(npm(@sentry/types)) = 6.17.4
Provides: bundled(npm(@sentry/utils)) = 6.17.4
Provides: bundled(npm(@swc/core)) = 1.2.136
Provides: bundled(npm(@swc/helpers)) = 0.3.2
Provides: bundled(npm(@testing-library/dom)) = 8.10.1
Provides: bundled(npm(@testing-library/jest-dom)) = 5.16.2
Provides: bundled(npm(@testing-library/react)) = 12.1.2
Provides: bundled(npm(@testing-library/react-hooks)) = 7.0.2
Provides: bundled(npm(@testing-library/user-event)) = 13.5.0
Provides: bundled(npm(@types/angular)) = 1.8.3
Provides: bundled(npm(@types/angular-route)) = 1.7.2
Provides: bundled(npm(@types/classnames)) = 2.3.0
Provides: bundled(npm(@types/common-tags)) = 1.8.1
Provides: bundled(npm(@types/d3)) = 7.1.0
Provides: bundled(npm(@types/d3-force)) = 2.1.4
Provides: bundled(npm(@types/d3-scale-chromatic)) = 1.3.1
Provides: bundled(npm(@types/debounce-promise)) = 3.1.4
Provides: bundled(npm(@types/enzyme)) = 3.10.10
Provides: bundled(npm(@types/enzyme-adapter-react-16)) = 1.0.6
Provides: bundled(npm(@types/eslint)) = 7.28.0
Provides: bundled(npm(@types/file-saver)) = 2.0.5
Provides: bundled(npm(@types/google.analytics)) = 0.0.42
Provides: bundled(npm(@types/grafana__slate-react)) = 0.22.5
Provides: bundled(npm(@types/history)) = 4.7.9
Provides: bundled(npm(@types/hoist-non-react-statics)) = 3.3.1
Provides: bundled(npm(@types/jest)) = 26.0.15
Provides: bundled(npm(@types/jquery)) = 3.5.13
Provides: bundled(npm(@types/jsurl)) = 1.2.30
Provides: bundled(npm(@types/lingui__macro)) = 3.0.0
Provides: bundled(npm(@types/lodash)) = 4.14.149
Provides: bundled(npm(@types/logfmt)) = 1.2.2
Provides: bundled(npm(@types/lru-cache)) = 5.1.1
Provides: bundled(npm(@types/mousetrap)) = 1.6.3
Provides: bundled(npm(@types/node)) = 12.20.24
Provides: bundled(npm(@types/papaparse)) = 5.3.2
Provides: bundled(npm(@types/pluralize)) = 0.0.29
Provides: bundled(npm(@types/prismjs)) = 1.26.0
Provides: bundled(npm(@types/rc-time-picker)) = 3.4.1
Provides: bundled(npm(@types/react)) = 17.0.30
Provides: bundled(npm(@types/react-beautiful-dnd)) = 13.1.2
Provides: bundled(npm(@types/react-dom)) = 17.0.10
Provides: bundled(npm(@types/react-grid-layout)) = 1.3.0
Provides: bundled(npm(@types/react-highlight-words)) = 0.16.4
Provides: bundled(npm(@types/react-loadable)) = 5.5.6
Provides: bundled(npm(@types/react-redux)) = 7.1.20
Provides: bundled(npm(@types/react-router-dom)) = 5.3.3
Provides: bundled(npm(@types/react-test-renderer)) = 17.0.1
Provides: bundled(npm(@types/react-transition-group)) = 4.4.4
Provides: bundled(npm(@types/react-virtualized-auto-sizer)) = 1.0.1
Provides: bundled(npm(@types/react-window)) = 1.8.5
Provides: bundled(npm(@types/redux-mock-store)) = 1.0.3
Provides: bundled(npm(@types/reselect)) = 2.2.0
Provides: bundled(npm(@types/semver)) = 7.3.9
Provides: bundled(npm(@types/slate)) = 0.47.2
Provides: bundled(npm(@types/slate-plain-serializer)) = 0.7.2
Provides: bundled(npm(@types/testing-library__jest-dom)) = 5.14.1
Provides: bundled(npm(@types/testing-library__react-hooks)) = 3.4.1
Provides: bundled(npm(@types/tinycolor2)) = 1.4.3
Provides: bundled(npm(@types/uuid)) = 8.3.3
Provides: bundled(npm(@typescript-eslint/eslint-plugin)) = 4.28.0
Provides: bundled(npm(@typescript-eslint/parser)) = 4.28.0
Provides: bundled(npm(@visx/event)) = 2.6.0
Provides: bundled(npm(@visx/gradient)) = 2.1.0
Provides: bundled(npm(@visx/group)) = 2.1.0
Provides: bundled(npm(@visx/scale)) = 2.2.2
Provides: bundled(npm(@visx/shape)) = 2.4.0
Provides: bundled(npm(@visx/tooltip)) = 2.8.0
Provides: bundled(npm(@welldone-software/why-did-you-render)) = 6.2.3
Provides: bundled(npm(@wojtekmaj/enzyme-adapter-react-17)) = 0.6.6
Provides: bundled(npm(angular)) = 1.8.2
Provides: bundled(npm(angular-bindonce)) = 0.3.1
Provides: bundled(npm(angular-route)) = 1.8.2
Provides: bundled(npm(angular-sanitize)) = 1.8.2
Provides: bundled(npm(app)) = 0.0.0-use.local
Provides: bundled(npm(autoprefixer)) = 9.8.8
Provides: bundled(npm(axios)) = 0.21.2
Provides: bundled(npm(babel-jest)) = 26.6.3
Provides: bundled(npm(babel-loader)) = 8.2.2
Provides: bundled(npm(babel-plugin-angularjs-annotate)) = 0.10.0
Provides: bundled(npm(babel-plugin-macros)) = 2.8.0
Provides: bundled(npm(baron)) = 3.0.3
Provides: bundled(npm(brace)) = 0.11.1
Provides: bundled(npm(calculate-size)) = 1.1.1
Provides: bundled(npm(centrifuge)) = 2.8.4
Provides: bundled(npm(classnames)) = 2.3.1
Provides: bundled(npm(comlink)) = 4.3.1
Provides: bundled(npm(common-tags)) = 1.8.0
Provides: bundled(npm(copy-webpack-plugin)) = 5.1.2
Provides: bundled(npm(core-js)) = 1.2.7
Provides: bundled(npm(css-loader)) = 3.4.2
Provides: bundled(npm(css-minimizer-webpack-plugin)) = 3.4.1
Provides: bundled(npm(cypress)) = 9.3.1
Provides: bundled(npm(d3)) = 5.15.0
Provides: bundled(npm(d3-force)) = 1.2.1
Provides: bundled(npm(d3-scale-chromatic)) = 1.5.0
Provides: bundled(npm(dangerously-set-html-content)) = 1.0.9
Provides: bundled(npm(date-fns)) = 2.25.0
Provides: bundled(npm(debounce-promise)) = 3.1.2
Provides: bundled(npm(emotion)) = 10.0.27
Provides: bundled(npm(enzyme)) = 3.11.0
Provides: bundled(npm(enzyme-to-json)) = 3.6.2
Provides: bundled(npm(eslint)) = 7.28.0
Provides: bundled(npm(eslint-config-prettier)) = 8.3.0
Provides: bundled(npm(eslint-plugin-jsdoc)) = 37.7.0
Provides: bundled(npm(eslint-plugin-lodash)) = 7.3.0
Provides: bundled(npm(eslint-plugin-no-only-tests)) = 2.6.0
Provides: bundled(npm(eslint-plugin-prettier)) = 4.0.0
Provides: bundled(npm(eslint-plugin-react)) = 7.28.0
Provides: bundled(npm(eslint-plugin-react-hooks)) = 4.3.0
Provides: bundled(npm(eslint-webpack-plugin)) = 3.1.1
Provides: bundled(npm(eventemitter3)) = 4.0.7
Provides: bundled(npm(expose-loader)) = 3.1.0
Provides: bundled(npm(fast-deep-equal)) = 3.1.3
Provides: bundled(npm(fast-json-patch)) = 3.1.0
Provides: bundled(npm(file-loader)) = 6.2.0
Provides: bundled(npm(file-saver)) = 2.0.5
Provides: bundled(npm(fork-ts-checker-webpack-plugin)) = 4.1.6
Provides: bundled(npm(fs-extra)) = 0.30.0
Provides: bundled(npm(glob)) = 7.2.0
Provides: bundled(npm(history)) = 4.10.1
Provides: bundled(npm(hoist-non-react-statics)) = 2.5.5
Provides: bundled(npm(html-loader)) = 0.5.5
Provides: bundled(npm(html-webpack-plugin)) = 3.2.0
Provides: bundled(npm(http-server)) = 14.1.0
Provides: bundled(npm(husky)) = 7.0.4
Provides: bundled(npm(iconscout-unicons-tarball)) = 1.0.0
Provides: bundled(npm(immer)) = 9.0.7
Provides: bundled(npm(immutable)) = 3.8.2
Provides: bundled(npm(jest)) = 26.6.3
Provides: bundled(npm(jest-canvas-mock)) = 2.3.0
Provides: bundled(npm(jest-date-mock)) = 1.0.8
Provides: bundled(npm(jest-junit)) = 13.0.0
Provides: bundled(npm(jest-matcher-utils)) = 26.6.2
Provides: bundled(npm(jest-mock-console)) = 1.2.3
Provides: bundled(npm(jquery)) = 3.5.1
Provides: bundled(npm(json-source-map)) = 0.6.1
Provides: bundled(npm(jsurl)) = 0.1.5
Provides: bundled(npm(lerna)) = 4.0.0
Provides: bundled(npm(lezer)) = 0.13.5
Provides: bundled(npm(lezer-promql)) = 0.20.0
Provides: bundled(npm(lezer-tree)) = 0.13.2
Provides: bundled(npm(lint-staged)) = 12.3.3
Provides: bundled(npm(lodash)) = 4.17.21
Provides: bundled(npm(logfmt)) = 1.3.2
Provides: bundled(npm(lru-cache)) = 5.1.1
Provides: bundled(npm(memoize-one)) = 4.0.3
Provides: bundled(npm(mini-css-extract-plugin)) = 0.7.0
Provides: bundled(npm(moment)) = 2.29.1
Provides: bundled(npm(moment-timezone)) = 0.5.34
Provides: bundled(npm(monaco-editor)) = 0.31.1
Provides: bundled(npm(monaco-promql)) = 1.7.2
Provides: bundled(npm(mousetrap)) = 1.6.5
Provides: bundled(npm(mousetrap-global-bind)) = 1.1.0
Provides: bundled(npm(moveable)) = 0.27.3
Provides: bundled(npm(mutationobserver-shim)) = 0.3.7
Provides: bundled(npm(ngtemplate-loader)) = 2.1.0
Provides: bundled(npm(node-notifier)) = 8.0.2
Provides: bundled(npm(nodemon)) = 2.0.15
Provides: bundled(npm(ol)) = 6.12.0
Provides: bundled(npm(papaparse)) = 5.3.1
Provides: bundled(npm(pluralize)) = 8.0.0
Provides: bundled(npm(postcss)) = 7.0.39
Provides: bundled(npm(postcss-loader)) = 3.0.0
Provides: bundled(npm(postcss-reporter)) = 7.0.5
Provides: bundled(npm(postcss-scss)) = 4.0.2
Provides: bundled(npm(prettier)) = 2.3.0
Provides: bundled(npm(prismjs)) = 1.25.0
Provides: bundled(npm(prop-types)) = 15.7.2
Provides: bundled(npm(raw-loader)) = 4.0.2
Provides: bundled(npm(rc-cascader)) = 3.2.1
Provides: bundled(npm(rc-drawer)) = 4.4.3
Provides: bundled(npm(rc-slider)) = 9.7.5
Provides: bundled(npm(rc-time-picker)) = 3.7.3
Provides: bundled(npm(re-resizable)) = 6.9.1
Provides: bundled(npm(react)) = 17.0.1
Provides: bundled(npm(react-beautiful-dnd)) = 13.1.0
Provides: bundled(npm(react-diff-viewer)) = 3.1.1
Provides: bundled(npm(react-dom)) = 17.0.1
Provides: bundled(npm(react-draggable)) = 4.4.4
Provides: bundled(npm(react-grid-layout)) = 1.3.3
Provides: bundled(npm(react-highlight-words)) = 0.17.0
Provides: bundled(npm(react-hook-form)) = 7.5.3
Provides: bundled(npm(react-inlinesvg)) = 2.3.0
Provides: bundled(npm(react-loadable)) = 5.5.0
Provides: bundled(npm(react-moveable)) = 0.30.3
Provides: bundled(npm(react-popper)) = 2.2.5
Provides: bundled(npm(react-popper-tooltip)) = 3.1.1
Provides: bundled(npm(react-redux)) = 7.2.6
Provides: bundled(npm(react-refresh)) = 0.11.0
Provides: bundled(npm(react-resizable)) = 3.0.4
Provides: bundled(npm(react-reverse-portal)) = 2.1.0
Provides: bundled(npm(react-router-dom)) = 5.3.0
Provides: bundled(npm(react-select)) = 3.2.0
Provides: bundled(npm(react-select-event)) = 5.3.0
Provides: bundled(npm(react-split-pane)) = 0.1.92
Provides: bundled(npm(react-test-renderer)) = 17.0.2
Provides: bundled(npm(react-transition-group)) = 4.4.2
Provides: bundled(npm(react-use)) = 17.3.2
Provides: bundled(npm(react-virtualized-auto-sizer)) = 1.0.6
Provides: bundled(npm(react-window)) = 1.8.6
Provides: bundled(npm(redux)) = 4.1.1
Provides: bundled(npm(redux-mock-store)) = 1.5.4
Provides: bundled(npm(redux-thunk)) = 2.4.1
Provides: bundled(npm(regenerator-runtime)) = 0.11.1
Provides: bundled(npm(reselect)) = 4.1.0
Provides: bundled(npm(rimraf)) = 2.7.1
Provides: bundled(npm(rst2html)) = 1.0.4
Provides: bundled(npm(rxjs)) = 6.6.7
Provides: bundled(npm(sass)) = 1.27.0
Provides: bundled(npm(sass)) = 1.27.0
Provides: bundled(npm(sass-loader)) = 8.0.2
Provides: bundled(npm(search-query-parser)) = 1.6.0
Provides: bundled(npm(selecto)) = 1.13.2
Provides: bundled(npm(semver)) = 5.7.1
Provides: bundled(npm(sinon)) = 13.0.1
Provides: bundled(npm(slate)) = 0.47.8
Provides: bundled(npm(slate-plain-serializer)) = 0.7.10
Provides: bundled(npm(style-loader)) = 1.1.3
Provides: bundled(npm(stylelint)) = 14.4.0
Provides: bundled(npm(stylelint-config-prettier)) = 9.0.3
Provides: bundled(npm(stylelint-config-sass-guidelines)) = 9.0.1
Provides: bundled(npm(symbol-observable)) = 1.2.0
Provides: bundled(npm(terser-webpack-plugin)) = 1.4.5
Provides: bundled(npm(test)) = 0.0.0-use.local
Provides: bundled(npm(testing-library-selector)) = 0.2.1
Provides: bundled(npm(tether-drop)) = 1.5.0
Provides: bundled(npm(tinycolor2)) = 1.4.2
Provides: bundled(npm(ts-jest)) = 26.4.4
Provides: bundled(npm(ts-loader)) = 6.2.1
Provides: bundled(npm(ts-node)) = 9.0.0
Provides: bundled(npm(tslib)) = 1.14.1
Provides: bundled(npm(typescript)) = 4.4.3
Provides: bundled(npm(uplot)) = 1.6.19
Provides: bundled(npm(uuid)) = 3.4.0
Provides: bundled(npm(vendor)) = 0.0.0-use.local
Provides: bundled(npm(visjs-network)) = 4.25.0
Provides: bundled(npm(wait-on)) = 6.0.0
Provides: bundled(npm(webpack)) = 4.41.5
Provides: bundled(npm(webpack-bundle-analyzer)) = 4.5.0
Provides: bundled(npm(webpack-cli)) = 4.9.2
Provides: bundled(npm(webpack-dev-server)) = 4.7.4
Provides: bundled(npm(webpack-merge)) = 5.8.0
Provides: bundled(npm(whatwg-fetch)) = 3.6.2


%description
Grafana is an open source, feature rich metrics dashboard and graph editor for
Graphite, InfluxDB & OpenTSDB.


%prep
%setup -q -T -D -b 0
%setup -q -T -D -b 1
%if %{compile_frontend} == 0
# remove bundled plugins source, otherwise they'll get merged
# with the compiled bundled plugins when extracting the webpack
rm -r plugins-bundled
%setup -q -T -D -b 2
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1
%ifarch s390x
%patch4 -p1
%endif
%patch5 -p1
%patch8 -p1
%patch9 -p1
%if %{enable_fips_mode}
%patch10 -p1
%endif
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1


%build
# Build the frontend
%if %{compile_frontend}
%{SOURCE4}
%endif

# Build the backend

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
install -p -m 640 conf/sample.ini %{buildroot}%{_sysconfdir}/%{name}/grafana.ini
install -p -m 640 conf/ldap.toml %{buildroot}%{_sysconfdir}/%{name}/ldap.toml
install -p -m 644 conf/defaults.ini %{buildroot}%{_datadir}/%{name}/conf/defaults.ini
install -p -m 644 conf/sample.ini %{buildroot}%{_datadir}/%{name}/conf/sample.ini
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
# Test frontend
%if %{compile_frontend}
node_modules/.bin/jest
%endif

# Test backend

# in setting_test.go there is a unit test which checks if 10 days are 240 hours
# which is usually true except if the dayligt saving time change falls into the last 10 days, then it's either 239 or 241 hours...
# let's set the time zone to a time zone without daylight saving time
export TZ=GMT

%gotest ./pkg/...

%if %{enable_fips_mode}
OPENSSL_FORCE_FIPS_MODE=1 GOLANG_FIPS=1 go test -v ./pkg/util -run TestEncryption
%endif

%files
# binaries and wrappers
%{_sbindir}/%{name}-server
%{_sbindir}/%{name}-cli
%{_libexecdir}/%{name}

# config files
%config(noreplace) %{_sysconfdir}/sysconfig/grafana-server
%dir %{_sysconfdir}/%{name}
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/dashboards
%attr(0750, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/datasources
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/notifiers
%attr(0755, root, %{GRAFANA_GROUP}) %dir %{_sysconfdir}/%{name}/provisioning/plugins
%attr(0640, root, %{GRAFANA_GROUP}) %config(noreplace) %{_sysconfdir}/%{name}/grafana.ini
%attr(0640, root, %{GRAFANA_GROUP}) %config(noreplace) %{_sysconfdir}/%{name}/ldap.toml

# config database directory and plugins
%attr(0750, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}
%attr(-,    %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_sharedstatedir}/%{name}/plugins

# shared directory and all files therein
%{_datadir}/%{name}
%attr(-, root, %{GRAFANA_GROUP}) %{_datadir}/%{name}/conf/*

# systemd service file
%{_unitdir}/grafana-server.service

# Grafana configuration to dynamically create /run/grafana/grafana.pid on tmpfs
%{_tmpfilesdir}/%{name}.conf

# log directory - grafana.log is created by grafana-server, and it does it's own log rotation
%attr(0755, %{GRAFANA_USER}, %{GRAFANA_GROUP}) %dir %{_localstatedir}/log/%{name}

# man pages for grafana binaries
%{_mandir}/man1/%{name}-server.1*
%{_mandir}/man1/%{name}-cli.1*

# other docs and license
%license LICENSE LICENSING.md
%doc CHANGELOG.md CODE_OF_CONDUCT.md CONTRIBUTING.md GOVERNANCE.md ISSUE_TRIAGE.md MAINTAINERS.md NOTICE.md
%doc PLUGIN_DEV.md README.md ROADMAP.md SECURITY.md SUPPORT.md UPGRADING_DEPENDENCIES.md WORKFLOW.md


%changelog
* Mon Feb 21 2022 Andreas Gerstmayr <agerstmayr@redhat.com> 8.4.1-1
- update to 8.4.1 tagged upstream community sources, see CHANGELOG
- place commented config file in /etc/grafana/grafana.ini
- enable Go modules in build process
- adapt Node.js bundling to yarn v3 and Zero Install feature

* Fri Jan 28 2022 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.13-1
- update to 7.5.13 tagged upstream community sources, see CHANGELOG
- support Go 1.18

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.11-3
- use HMAC-SHA-256 instead of SHA-1 to generate password reset tokens
- update FIPS tests in check phase

* Thu Dec 16 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.11-2
- resolve CVE-2021-44716 golang: net/http: limit growth of header canonicalization cache
- resolve CVE-2021-43813 grafana: directory traversal vulnerability for *.md files

* Mon Oct 11 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.11-1
- update to 7.5.11 tagged upstream community sources, see CHANGELOG
- resolve CVE-2021-39226

* Thu Sep 30 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.10-1
- update to 7.5.10 tagged upstream community sources, see CHANGELOG

* Mon Aug 16 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.9-4
- rebuild to resolve CVE-2021-34558

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.9-2
- remove unused dependency property-information
- always include FIPS patch in SRPM

* Fri Jun 25 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.9-1
- update to 7.5.9 tagged upstream community sources, see CHANGELOG

* Mon Jun 21 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.8-1
- update to 7.5.8 tagged upstream community sources, see CHANGELOG
- remove unused dependencies selfsigned, http-signature and gofpdf

* Fri Jun 11 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.7-2
- remove unused cryptographic implementations
- use cryptographic functions from OpenSSL if FIPS mode is enabled

* Tue May 25 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.5.7-1
- update to 7.5.7 tagged upstream community sources, see CHANGELOG

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.3.6-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Andreas Gerstmayr <agerstmayr@redhat.com> 7.3.6-2
- change working dir to $GRAFANA_HOME in grafana-cli wrapper (fixes Red Hat BZ #1916083)
- add pcp-redis-datasource to allow_loading_unsigned_plugins config option

* Mon Dec 21 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 7.3.6-1
- update to 7.3.6 tagged upstream community sources, see CHANGELOG
- remove dependency on SAML (not supported in the open source version of Grafana)

* Wed Nov 25 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 7.3.4-1
- update to 7.3.4 tagged upstream community sources, see CHANGELOG

* Tue Nov 10 2020 Andreas Gerstmayr <agerstmayr@redhat.com> 7.3.1-1
- update to 7.3.1 tagged upstream community sources, see CHANGELOG
- optionally bundle node.js dependencies and build and test frontend as part of the specfile
- change default provisioning path to /etc/grafana/provisioning (changed in version 7.1.1-1)
- resolve https://bugzilla.redhat.com/show_bug.cgi?id=1843170

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
