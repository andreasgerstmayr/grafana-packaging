#!/bin/bash -eu
#
# create vendor and webpack tarballs inside a container for reproducibility
#

cat <<EOF | podman build -t grafana-build -f - .
FROM fedora:35

RUN dnf install -y rpmdevtools time python3-packaging make golang nodejs yarnpkg

RUN useradd builder
USER builder
WORKDIR /home/builder

COPY Makefile grafana.spec *.patch build_frontend.sh list_bundled_nodejs_packages.py .
CMD make
EOF

podman run -v $(pwd)/cache_go:/home/builder/go:z grafana-build
