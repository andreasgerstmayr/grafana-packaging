all: grafana-$(VER).tar.gz \
	 grafana-vendor-$(VER).tar.xz \
	 grafana-webpack-$(VER).tar.gz

grafana-$(VER).tar.gz:
	wget https://github.com/grafana/grafana/archive/v$(VER)/grafana-$(VER).tar.gz

ALL_PATCHES := $(wildcard *.patch)
PATCHES_TO_APPLY := $(filter-out 009-patch-unused-backend-crypto.patch 010-fips.patch,$(ALL_PATCHES))

grafana-vendor-$(VER).tar.xz: grafana-$(VER).tar.gz
	rm -rf grafana-$(VER)
	tar xfz grafana-$(VER).tar.gz

	# patches can affect Go or Node.js dependencies, or the webpack
	for patch in $(PATCHES_TO_APPLY); do patch -d grafana-$(VER) -p1 --fuzz=0 < $$patch; done

	# Go
	cd grafana-$(VER) && go mod vendor -v
	# Remove unused crypto
	rm grafana-$(VER)/vendor/golang.org/x/crypto/cast5/cast5.go
	rm grafana-$(VER)/vendor/golang.org/x/crypto/ed25519/ed25519.go
	rm grafana-$(VER)/vendor/golang.org/x/crypto/ed25519/internal/edwards25519/const.go
	rm grafana-$(VER)/vendor/golang.org/x/crypto/ed25519/internal/edwards25519/edwards25519.go
	rm grafana-$(VER)/vendor/golang.org/x/crypto/openpgp/elgamal/elgamal.go
	rm grafana-$(VER)/vendor/golang.org/x/crypto/openpgp/packet/ocfb.go
	awk '$$2~/^v/ && $$4 != "indirect" {print "Provides: bundled(golang(" $$1 ")) = " substr($$2, 2)}' grafana-$(VER)/go.mod | \
		sed -E 's/=(.*)-(.*)-(.*)/=\1-\2.\3/g' > $@.manifest

	# Node.js
	cd grafana-$(VER) && yarn install --pure-lockfile
	# Remove files with licensing issues
	find grafana-$(VER) -type d -name 'node-notifier' -prune -exec rm -r {} \;
	find grafana-$(VER) -type f -name '*.exe' -delete
	./list_bundled_nodejs_packages.py grafana-$(VER)/ >> $@.manifest

	# Create tarball
	XZ_OPT=-9 tar cfJ $@ \
		grafana-$(VER)/vendor \
		$$(find grafana-$(VER) -type d -name "node_modules" -prune)

grafana-webpack-$(VER).tar.gz: grafana-vendor-$(VER).tar.xz
	cd grafana-$(VER) && \
		../build_frontend.sh

	tar cfz $@ grafana-$(VER)/public/build grafana-$(VER)/public/views grafana-$(VER)/plugins-bundled

clean:
	rm -rf *.tar.gz *.tar.xz *.manifest *.rpm grafana-*/
