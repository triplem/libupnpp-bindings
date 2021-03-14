# Set PYTHON_VERSION in the environment or command line to change the
# Python version.  e.g. ./configure PYTHON_VERSION=3

AC_PREREQ([2.63])

AC_INIT([libupnpp-bindings], [0.21.0],[https://www.lesbonscomptes.com/upmpdcli])
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE([1.11.2 -Wportability foreign])

AC_CONFIG_SRCDIR([upnpp.i])

LT_PREREQ([2.2.6])
LT_INIT([disable-static])

AC_PROG_CXX
AC_LANG_CPLUSPLUS

AX_PKG_SWIG([2.0.0])
AX_SWIG_ENABLE_CXX
AX_SWIG_MULTI_MODULE_SUPPORT
AX_SWIG_PYTHON

AC_MSG_NOTICE([AX_SWIG_PYTHON_CPPFLAGS => $AX_SWIG_PYTHON_CPPFLAGS
     AX_SWIG_PYTHON_OPT => $AX_SWIG_PYTHON_OPT
     PYTHON_SITE_PKG => $PYTHON_SITE_PKG])

AC_CONFIG_FILES([Makefile python/Makefile])
AC_OUTPUT

