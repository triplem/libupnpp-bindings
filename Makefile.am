ACLOCAL_AMFLAGS = -I m4

EXTRA_DIST = upnpp-head.i  upnpp.i upnpp-devs.i

SUBDIRS = . python

dist-hook:
	test -z "`git status -s | egrep -v '?? libupnpp-bindings-'`" 
	git tag -a libupnpp-bindings-v$(VERSION) -m 'version $(VERSION)'
