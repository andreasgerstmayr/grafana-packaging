#!/bin/bash -eu
#
# create vendor and webpack bundles inside a container for reproducibility
# using a Go cache:
#   ./create_bundles_in_container.sh --security-opt label=disable -v $(pwd)/.gocache:/root/go
#

cat <<EOF | podman build -t grafana-build -f - .
FROM fedora:35

RUN dnf upgrade -y && \
    dnf install -y rpmdevtools python3-packaging python3-pyyaml make golang nodejs yarnpkg

# https://groups.google.com/g/golang-nuts/c/MVtHZUtZru4
ENV GOPROXY=https://proxy.golang.org,direct

WORKDIR /tmp/grafana-build
COPY Makefile grafana.spec *.patch build_frontend.sh list_bundled_nodejs_packages.py .
RUN mkdir bundles
CMD make && mv *.tar.* bundles
EOF

podman run --name grafana-build --replace "$@" grafana-build
podman cp grafana-build:bundles/. .
