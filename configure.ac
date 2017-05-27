AC_PREREQ([2.63])

AC_INIT([upcppy], [0.1], [https://www.lesbonscomptes.com/upmpdcli])

AM_INIT_AUTOMAKE([1.11.2 -Wportability tar-ustar no-dist-gzip dist-xz foreign])
AC_CONFIG_SRCDIR([upcppy.i])

LT_PREREQ([2.2.6])
LT_INIT([disable-static])

AC_CONFIG_MACRO_DIR([m4])

AC_PROG_CXX
AC_LANG_CPLUSPLUS

swigoverridden=${SWIG+yes}
AC_PATH_PROGS(SWIG, ["${SWIG-swig}"], [])
AC_ARG_VAR(SWIG, [SWIG interface generator (only needed by Xapian developers)])
if test -z "$SWIG" ; then
    AC_MSG_ERROR([Can't find SWIG utility])
fi
SWIG_FLAGS="-python -c++"
AC_SUBST(SWIG_FLAGS)

AC_PATH_PROGS(PYTHON, ["${PYTHON-python2 python}"], [])
AC_ARG_VAR(PYTHON, [Python interpreter])
if test -n "$PYTHON" ; then
  dnl Require Python 2.3 or newer.  It's now > 4.5 years since the last
  dnl 2.2.x release, so 2.2 is essentially unsupported upstream.
  AC_MSG_CHECKING([$PYTHON version])
  version=`$PYTHON -c 'import sys;print("%d.%d" % sys.version_info[[:2]])' 2>/dev/null`
  case $version in
  [2.[3-9]*|2.[12][0-9][0-9]*])
    AC_MSG_RESULT([$version])
    ;;
  [[3-9].*])
    AC_MSG_RESULT([$version (too new - only Python 2 is supported by Xapian 1.2.x)])
    if test yes = "$with_python" ; then
      AC_MSG_ERROR([Only Python 2 is supported by Xapian 1.2.x ($python is $version)])
    fi
    PYTHON=
    ;;
  *)
    AC_MSG_RESULT([$version (too old)])
    if test yes = "$with_python" ; then
      AC_MSG_ERROR([Only python 2.3 or newer is supported ($python is $version)])
    fi
    PYTHON=
    ;;
  esac
  if test -n "$PYTHON" ; then
    if $PYTHON -c 'import distutils.sysconfig' 2>/dev/null ; then
      PYTHON_INC=`$PYTHON -c 'import os,distutils.sysconfig;print(distutils.sysconfig.get_python_inc().replace(os.sep,"/"))'`
      AC_SUBST(PYTHON_INC)
    else
      if test yes = "$with_python" ; then
        AC_MSG_ERROR([Couldn't import Python module distutils.sysconfig - you probably need to install a python-dev or python-devel package])
      else
        AC_MSG_WARN([Couldn't import Python module distutils.sysconfig - you probably don't have a python-dev or python-devel package installed])
        PYTHON=
      fi
    fi
  fi
  if test -n "$PYTHON" ; then
    dnl Check that Python.h is there, which is a good way to check that
    dnl the appropriate python-dev package has been installed.
    AC_MSG_CHECKING([for $PYTHON_INC/Python.h])
    if test -f "$PYTHON_INC/Python.h" ; then
      AC_MSG_RESULT(yes)
      AC_MSG_CHECKING([for directory to install python bindings in])
      if test -z "$PYTHON_LIB" ; then
        PYTHON_LIB=`$PYTHON -c 'import os,distutils.sysconfig;print(distutils.sysconfig.get_python_lib(1).replace(os.sep,"/"))'`
      fi
      AC_MSG_RESULT([$PYTHON_LIB])
      AC_ARG_VAR(PYTHON_LIB, [Directory to install python bindings in])

      AC_MSG_CHECKING([for python libraries to link against])
      case $host_os in
      mingw* | pw32*)
        PYTHON_LIBS=`$PYTHON -c 'import os,sys;print("-L"+os.path.join(sys.prefix,"libs").replace(os.sep,"/")+" -lpython"+sys.version[[:3]].replace(".",""))'` ;;
      cygwin*)
        PYTHON_LIBS=`$PYTHON -c 'import os,sys;print("-L"+os.path.join(sys.path[[3]],"config")+" -lpython"+sys.version[[:3]])'` ;;
      *)
        PYTHON_LIBS= ;;
      esac
      AC_SUBST(PYTHON_LIBS)
      AC_MSG_RESULT([$PYTHON_LIBS])

      AC_MSG_CHECKING([for python module extension])
      dnl Usually ".so", but for example, Mac OS X uses ".dylib".
      PYTHON_SO=`$PYTHON -c 'import distutils.sysconfig;print(distutils.sysconfig.get_config_vars("SO")[[0]])'`
      AC_SUBST(PYTHON_SO)
      AC_MSG_RESULT([$PYTHON_SO])

      BINDINGS="$BINDINGS python"
    else
      AC_MSG_RESULT([no (install python-dev or python-devel package or similar)])
      if test yes = "$with_python" ; then
        AC_MSG_ERROR([Python.h not found])
      fi
    fi
  fi
fi

AC_SUBST(BINDINGS)

AC_CONFIG_FILES([Makefile])
AC_OUTPUT

