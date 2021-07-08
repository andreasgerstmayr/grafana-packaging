ifndef VER
  $(error VER is undefined)
endif
ifndef REL
  $(error REL is undefined)
endif

NAME       := grafana
RPM_NAME   := $(NAME)
SOURCE_DIR := $(NAME)-$(VER)
SOURCE_TAR := $(NAME)-$(VER).tar.gz
VENDOR_TAR := $(RPM_NAME)-vendor-$(VER)-$(REL).tar.xz
WEBPACK_TAR := $(RPM_NAME)-webpack-$(VER)-$(REL).tar.gz

ALL_PATCHES := $(wildcard *.patch)
PATCHES_TO_APPLY := $(filter-out 009-patch-unused-backend-crypto.patch 010-fips.patch,$(ALL_PATCHES))

all: $(SOURCE_TAR) $(VENDOR_TAR) $(WEBPACK_TAR)

$(SOURCE_TAR):
	spectool -g $(RPM_NAME).spec

$(VENDOR_TAR): $(SOURCE_TAR)
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
	find grafana-$(VER) -type d -name 'property-information' -prune -exec rm -r {} \;
	find grafana-$(VER) -type f -name '*.exe' -delete
	rm -r grafana-$(VER)/node_modules/visjs-network/examples
	./list_bundled_nodejs_packages.py grafana-$(VER)/ >> $@.manifest

	# Create tarball
	XZ_OPT=-9 tar cfJ $@ \
		grafana-$(VER)/vendor \
		$$(find grafana-$(VER) -type d -name "node_modules" -prune)

$(WEBPACK_TAR): $(VENDOR_TAR)
	cd grafana-$(VER) && \
		../build_frontend.sh

	tar cfz $@ grafana-$(VER)/public/build grafana-$(VER)/public/views grafana-$(VER)/plugins-bundled

clean:
	rm -rf *.tar.gz *.tar.xz *.manifest *.rpm $(NAME)-*/
