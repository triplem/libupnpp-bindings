AC_PREREQ([2.63])

AC_INIT([upnpp], [0.1], [https://www.lesbonscomptes.com/upmpdcli])
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE([1.11.2 -Wportability tar-ustar no-dist-gzip dist-xz foreign])

AC_CONFIG_SRCDIR([upnpp.i])

LT_PREREQ([2.2.6])
LT_INIT([disable-static])

AC_PROG_CXX
AC_LANG_CPLUSPLUS

AX_PKG_SWIG([2.0.0])
AX_SWIG_ENABLE_CXX
AX_SWIG_MULTI_MODULE_SUPPORT
AX_SWIG_PYTHON
echo "AX_SWIG_PYTHON_CPPFLAGS" $AX_SWIG_PYTHON_CPPFLAGS \
     "AX_SWIG_PYTHON_OPT" $AX_SWIG_PYTHON_OPT

AC_PATH_PROGS(PYTHON, ["${PYTHON-python2 python}"], [])
if test -z "$PYTHON_LIB" ; then
  PYTHON_LIB=`$PYTHON -c 'import os,distutils.sysconfig;print(distutils.sysconfig.get_python_lib(1).replace(os.sep,"/"))'`
fi
AC_MSG_RESULT([$PYTHON_LIB])
AC_ARG_VAR(PYTHON_LIB, [Directory to install python bindings in])


AC_CONFIG_FILES([Makefile python/Makefile])
AC_OUTPUT

