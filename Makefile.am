
AM_CPPFLAGS = -DDEBUG -g -Wall -I$(PYTHON_INC)
AM_CXXFLAGS = -std=c++11 $(SWIG_CXXFLAGS)

SWIG_sources = $(srcdir)/upcppy.i
SWIG_includes = -I$(srcdir) 

BUILT_SOURCES = upcppy_wrap.cxx

lib_LTLIBRARIES = _upcppy.la

# Curiously, -no-undefined seems to do nothing?? -Wl,-zdefs works though.
# automake 1.14.1
_upcppy_la_LDFLAGS = -avoid-version -module -no-undefined -shrext "$(PYTHON_SO)"

_upcppy_la_LIBADD = -lupnpp
_upcppy_la_SOURCES = upcppy_wrap.cxx
