AX_SWIG_PYTHON_CPPFLAGS = @AX_SWIG_PYTHON_CPPFLAGS@
AX_SWIG_PYTHON_OPT = @AX_SWIG_PYTHON_OPT@

AM_CPPFLAGS = -DDEBUG -g -Wall -I$(AX_SWIG_PYTHON_CPPFLAGS)
AM_CXXFLAGS = -std=c++11 $(AX_SWIG_PYTHON_CPPFLAGS)

SWIG_sources = $(top_srcdir)/python/upnpp-python.i \
             $(top_srcdir)/upnpp-head.i \
             $(top_srcdir)/upnpp-devs.i \
             $(top_srcdir)/upnpp.i 
SWIG_includes = -I$(top_srcdir) @CPPFLAGS@ -I/usr/include

EXTRA_DIST = upnpp-python.i upnpp.py upnpp/__init__.py

BUILT_SOURCES = upnpp_wrap.cxx upnpp.py

pkgpylibdir = @PYTHON_SITE_PKG@/upnpp
pkgpylib_DATA = upnpp/__init__.py upnpp/upnpp.py
pkgpylib_LTLIBRARIES = _upnpp.la

upnpp/upnpp.py: $(top_srcdir)/python/upnpp.py
	mkdir -p upnpp
	cp -p $(top_srcdir)/python/upnpp.py upnpp/upnpp.py

_upnpp_la_LDFLAGS = -avoid-version -module -no-undefined -shrext .so
_upnpp_la_LIBADD = -lupnpp
_upnpp_la_SOURCES = upnpp_wrap.cxx

upnpp_wrap.cxx : $(SWIG_sources)
	$(SWIG) $(AX_SWIG_PYTHON_OPT) $(SWIG_includes) -o $@ $<
         
CLEANFILES = \
    upnpp/_upnpp.so \
    upnpp/upnpp.py upnpp/__init__.pyc upnpp/__init__.pyo \
    $(srcdir)/*.pyc

clean-local:
	-rmdir upnpp
