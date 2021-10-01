VERSION := $(shell rpm --specfile *.spec --qf '%{VERSION}\n' | head -1)
RELEASE := $(shell rpm --specfile *.spec --qf '%{RELEASE}\n' | head -1 | cut -d. -f1)

NAME       := grafana
RPM_NAME   := $(NAME)
SOURCE_DIR := $(NAME)-$(VERSION)
SOURCE_TAR := $(NAME)-$(VERSION).tar.gz
VENDOR_TAR := $(RPM_NAME)-vendor-$(VERSION)-$(RELEASE).tar.xz
WEBPACK_TAR := $(RPM_NAME)-webpack-$(VERSION)-$(RELEASE).tar.gz

ALL_PATCHES     := $(sort $(wildcard *.patch))
VENDOR_PATCHES  := $(sort $(wildcard *.vendor.patch))
COND_PATCHES    := $(sort $(wildcard *.cond.patch))
REGULAR_PATCHES := $(filter-out $(VENDOR_PATCHES) $(COND_PATCHES),$(ALL_PATCHES))

all: $(SOURCE_TAR) $(VENDOR_TAR) $(WEBPACK_TAR)

$(SOURCE_TAR):
	spectool -g $(RPM_NAME).spec

$(VENDOR_TAR): $(SOURCE_TAR)
	rm -rf $(SOURCE_DIR)
	tar xf $(SOURCE_TAR)

	# Patches to apply before vendoring
	for patch in $(REGULAR_PATCHES); do echo applying $$patch ...; patch -d $(SOURCE_DIR) -p1 --fuzz=0 < $$patch; done

	# Go
	cd $(SOURCE_DIR) && go mod vendor -v
	# Remove unused crypto
	rm $(SOURCE_DIR)/vendor/golang.org/x/crypto/cast5/cast5.go
	rm $(SOURCE_DIR)/vendor/golang.org/x/crypto/ed25519/ed25519.go
	rm $(SOURCE_DIR)/vendor/golang.org/x/crypto/ed25519/internal/edwards25519/const.go
	rm $(SOURCE_DIR)/vendor/golang.org/x/crypto/ed25519/internal/edwards25519/edwards25519.go
	rm $(SOURCE_DIR)/vendor/golang.org/x/crypto/openpgp/elgamal/elgamal.go
	rm $(SOURCE_DIR)/vendor/golang.org/x/crypto/openpgp/packet/ocfb.go
	awk '$$2~/^v/ && $$4 != "indirect" {print "Provides: bundled(golang(" $$1 ")) = " substr($$2, 2)}' $(SOURCE_DIR)/go.mod | \
		sed -E 's/=(.*)-(.*)-(.*)/=\1-\2.\3/g' > $@.manifest

	# Node.js
	cd $(SOURCE_DIR) && yarn install --pure-lockfile
	# Remove files with licensing issues
	find $(SOURCE_DIR) -type d -name 'node-notifier' -prune -exec rm -r {} \;
	find $(SOURCE_DIR) -type d -name 'property-information' -prune -exec rm -r {} \;
	find $(SOURCE_DIR) -type f -name '*.exe' -delete
	rm -r $(SOURCE_DIR)/node_modules/visjs-network/examples
	./list_bundled_nodejs_packages.py $(SOURCE_DIR) >> $@.manifest

	# Patches to apply after vendoring
	for patch in $(VENDOR_PATCHES); do echo applying $$patch ...; patch -d $(SOURCE_DIR) -p1 --fuzz=0 < $$patch; done

	# Create tarball
	XZ_OPT=-9 time -p tar cJf $@ \
		$(SOURCE_DIR)/vendor \
		$$(find $(SOURCE_DIR) -type d -name "node_modules" -prune)

$(WEBPACK_TAR): $(VENDOR_TAR)
	cd $(SOURCE_DIR) && \
		../build_frontend.sh

	tar cfz $@ $(SOURCE_DIR)/public/build $(SOURCE_DIR)/public/views $(SOURCE_DIR)/plugins-bundled

clean:
	rm -rf *.tar.gz *.tar.xz *.manifest *.rpm $(NAME)-*/
