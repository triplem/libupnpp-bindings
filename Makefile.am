
SWIG_FLAGS = @SWIG_FLAGS@

AM_CPPFLAGS = -DDEBUG -g -Wall -I$(PYTHON_INC)
AM_CXXFLAGS = -std=c++11 $(SWIG_CXXFLAGS)

SWIG_sources = $(top_srcdir)/upcppy.i
SWIG_includes = -I$(top_srcdir)  -I/usr/include/libupnpp/control/

BUILT_SOURCES = upcppy_wrap.cxx

upcppy_wrap.cxx : $(SWIG_sources)
	$(SWIG) $(SWIG_FLAGS) $(SWIG_includes) -o $@ $<
         
lib_LTLIBRARIES = _upcppy.la

_upcppy_la_LDFLAGS = -avoid-version -module -no-undefined -shrext "$(PYTHON_SO)"
_upcppy_la_LIBADD = -lupnpp
_upcppy_la_SOURCES = upcppy_wrap.cxx
