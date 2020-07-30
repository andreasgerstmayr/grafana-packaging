all: grafana-vendor-$(VER).tar.gz \
     grafana-vendor-$(VER).tar.gz.manifest \
     grafana-webpack-$(VER).tar.gz \
     grafana-webpack-$(VER).tar.gz.manifest

grafana-$(VER).tar.gz grafana-$(VER):
	wget https://github.com/grafana/grafana/archive/v$(VER)/grafana-$(VER).tar.gz
	tar xfz grafana-$(VER).tar.gz

grafana-vendor-$(VER).tar.gz: grafana-$(VER).tar.gz
	cd grafana-$(VER) && go mod vendor -v
	tar cfz $@ grafana-$(VER)/vendor

grafana-vendor-$(VER).tar.gz.manifest: grafana-$(VER).tar.gz
	awk '$$2~/^v/ && $$4 != "indirect" {print "Provides: bundled(golang(" $$1 ")) = " substr($$2, 2)}' grafana-$(VER)/go.mod | \
	sed -E 's/=(.*)-(.*)-(.*)/=\1-\2.\3/g' > $@

grafana-webpack-$(VER).tar.gz: grafana-$(VER).tar.gz
	cd grafana-$(VER) && yarn install --pure-lockfile && yarn run build
	cd grafana-$(VER) && \
		mkdir plugins-bundled/external && yarn run plugins:build-bundled && \
		for plugin in plugins-bundled/internal/*; do mv $$plugin $$plugin.tmp; mv $$plugin.tmp/dist $$plugin; rm -rf $$plugin.tmp; done && \
		rm plugins-bundled/README.md plugins-bundled/.gitignore plugins-bundled/external.json
	tar cfz $@ grafana-$(VER)/public/build grafana-$(VER)/public/views grafana-$(VER)/plugins-bundled

grafana-webpack-$(VER).tar.gz.manifest: grafana-$(VER).tar.gz
	./create_webpack_manifest.py grafana-$(VER)/ > $@

clean:
	rm -rf *.tar.gz grafana-*/
