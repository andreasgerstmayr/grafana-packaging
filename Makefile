all: grafana-vendor-go-$(VER).tar.gz \
     grafana-webpack-$(VER).tar.gz

grafana-$(VER).tar.gz grafana-$(VER)/:
	wget https://github.com/grafana/grafana/archive/v$(VER)/grafana-$(VER).tar.gz
	rm -rf grafana-$(VER)
	tar xfz grafana-$(VER).tar.gz
	cd grafana-$(VER) && \
	  for patch in ../*.patch; do patch -p1 < $$patch; done

grafana-vendor-go-$(VER).tar.gz: grafana-$(VER)/
	cd grafana-$(VER) && go mod vendor -v
	tar cfz $@ grafana-$(VER)/vendor
	awk '$$2~/^v/ && $$4 != "indirect" {print "Provides: bundled(golang(" $$1 ")) = " substr($$2, 2)}' grafana-$(VER)/go.mod | \
	sed -E 's/=(.*)-(.*)-(.*)/=\1-\2.\3/g' > $@.manifest

grafana-vendor-nodejs-$(VER).tar.gz: grafana-$(VER)/
	cd grafana-$(VER) && yarn install --pure-lockfile

	# Remove files with licensing issues
	find grafana-$(VER) -type d -name 'node-notifier' -prune -exec rm -r {} \;
	find grafana-$(VER) -name '*.exe' -delete

	tar cfz $@ $$(find grafana-$(VER) -type d -name "node_modules" -prune)
	./list_bundled_nodejs_packages.py grafana-$(VER)/ > $@.manifest

grafana-webpack-$(VER).tar.gz: grafana-$(VER)/
	cd grafana-$(VER) && \
	  yarn install --pure-lockfile && \
	  ../build_frontend.sh

	tar cfz $@ grafana-$(VER)/public/build grafana-$(VER)/public/views grafana-$(VER)/plugins-bundled
	./list_bundled_nodejs_packages.py grafana-$(VER)/ > $@.manifest

clean:
	rm -rf *.tar.gz *.manifest *.rpm grafana-*/
