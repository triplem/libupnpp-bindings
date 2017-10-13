%module upnpp
%{
/* upnpp-python.i: python-specific bits for the libupnpp swig interface
 *
 * Copyright (C) 2017 J.F.Dockes
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */
%}

%include ../upnpp-head.i

%include ../upnpp.i

%newobject installReporter;

%inline %{

// Utility class for event reporting. Wrapping the normal c++ looks too hard
class PythonReporter : public UPnPClient::VarEventReporter {
public:
    PythonReporter(UPnPClient::TypedService *s, PyObject *o)
        : m_service(s), m_o(o) {
        Py_XINCREF(m_o);
        if (!m_o || Py_None == m_o ||
            !PyObject_HasAttrString(m_o, "upnp_event")) {
            //fprintf(stderr, "PythonReporter: bad callback object\n");
            return;
        }
        m_service->installReporter(this);
    }
    PythonReporter(const PythonReporter& o)
        : m_service(o.m_service), m_o(o.m_o) {
        Py_XINCREF(m_o);
    }
    virtual ~PythonReporter() {
        //fprintf(stderr, "~PYTHONREPORTER\n");
        Py_XDECREF(m_o);
        m_service->installReporter(0);
    }

    virtual void changed(const char *nm, int val)  {
        char sv[20];
        sprintf(sv, "%d", val);
        reportEvent(nm, sv);
    }
    virtual void changed(const char *nm, const char *val) {
        reportEvent(nm, val);
    }
    virtual void changed(const char *nm, UPnPClient::UPnPDirObject *meta) {
        reportEvent(nm, meta->getdidl().c_str());
    }

    // Beware: other thread
    void reportEvent(const char *nm, const char *val) {
        PyGILState_STATE state = PyGILState_Ensure();
        if (!m_o || Py_None == m_o ||
            !PyObject_HasAttrString(m_o, "upnp_event")) {
            PyGILState_Release(state);
            return;
        }
        char method[20]{"upnp_event"};
        char format[10]{"(ss)"};
        PyObject *result = PyObject_CallMethod(m_o, method, format, nm, val);
        Py_XDECREF(result);
        PyGILState_Release(state);
    }

private:
    PythonReporter& operator=(const PythonReporter&);
    UPnPClient::TypedService *m_service{0};
    PyObject *m_o{0};
};

PythonReporter *installReporter(UPnPClient::TypedService *srv, PyObject *o)
{
    PythonReporter *reporter = new PythonReporter(srv, o);
    return reporter;
}
%}

%pythoncode %{
def _makeVS(l):
    ret = VectorString()
    for v in l:
        ret.append(v)
    return ret
def runaction(dev, action, args):
    '''Wrap runAction() method, using natural python types (list and dict).'''
    args = _makeVS(args)
    retdata = MapStringString()
    ret = dev.runAction(action, args, retdata)
    if ret:
        return None
    retdict = {}
    for nm, val in retdata.iteritems():
        retdict[nm] = val
    return retdict
%}

%init %{
if (! PyEval_ThreadsInitialized()) {
    PyEval_InitThreads();
}
%}

