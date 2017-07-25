%module upnpp

%{
/* upcppy.i: libupnpp swig interface
 *
 * Copyright (C) 2016 J.F.Dockes
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

%include stl.i

/**************************************
 * Wrapper for the TypedService class, which has a string-based interface
 * and was actually created for ease of use from swig.
 * cdircontent is needed because of the VarEventReporter method which takes
 * an UPnPDirObject value argument.
 */
%{
#include <libupnpp/control/description.hxx>
#include <libupnpp/control/cdircontent.hxx>
#include <libupnpp/control/typedservice.hxx>

%}
%include <libupnpp/control/cdircontent.hxx>
%include <libupnpp/control/service.hxx>
%newobject findTypedService;
%include <libupnpp/control/typedservice.hxx>

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
%}

%newobject installReporter;
%inline %{
PythonReporter *installReporter(UPnPClient::TypedService *srv, PyObject *o)
{
    PythonReporter *reporter = new PythonReporter(srv, o);
    return reporter;
}
%}

%init %{
if (! PyEval_ThreadsInitialized()) {
    PyEval_InitThreads();
}
%}

namespace std {
%template(VectorString)  vector<string>;
%template(MapStringString) map<string,string>;
}   



/*************************************************************************
 * Incomplete wrappers for avtransport and renderingcontrol. Not very
 * useful, code kept around for reference.
 * Because there is no factory function, these need to deal explicitely
 * with discovery and description.
 */
%{
#include <libupnpp/control/discovery.hxx>
%}
%warnfilter(325) UPnPClient::UPnPServiceDesc::Argument;
%warnfilter(325) UPnPClient::UPnPServiceDesc::Action;
%warnfilter(325) UPnPClient::UPnPServiceDesc::StateVariable;
%warnfilter(325) UPnPClient::UPnPServiceDesc::Parsed;
%include <libupnpp/control/description.hxx>
%include <libupnpp/control/discovery.hxx>
%{
#include <libupnpp/control/renderingcontrol.hxx>
%}
%include <libupnpp/control/renderingcontrol.hxx>
%{
#include <libupnpp/control/avtransport.hxx>
%}
%warnfilter(325) UPnPClient::AVTransport::MediaInfo;
%warnfilter(325) UPnPClient::AVTransport::TransportInfo;
%warnfilter(325) UPnPClient::AVTransport::PositionInfo;
%warnfilter(325) UPnPClient::AVTransport::DeviceCapabilities;
%warnfilter(325) UPnPClient::AVTransport::TransportSettings;
%include <libupnpp/control/avtransport.hxx>
/* Manage the nested PositionInfo class by defining another top level class
   and using a helper function. No need for the new class to be identical
   to the old one, as opposed to what would happen with typedefs */
%inline %{
struct AVTPositionInfo {
    int track;
    int trackduration; // secs
//    UPnPClient::UPnPDirObject trackmeta;
    std::string trackuri;
    int reltime;
    int abstime;
    int relcount;
    int abscount;
};
int AVTGetPositionInfo(UPnPClient::AVTransport *tp, AVTPositionInfo *inf)
{
    UPnPClient::AVTransport::PositionInfo avinf;
    int ret= tp->getPositionInfo(avinf);
    if (ret == 0) {
        inf->track = avinf.track;
        inf->trackduration = avinf.trackduration;
        inf->trackuri = avinf.trackuri;
        inf->reltime = avinf.reltime;
        inf->abstime = avinf.abstime;
        inf->relcount = avinf.relcount;
        inf->abscount = avinf.abscount;
    }
    return ret;
}
%}
