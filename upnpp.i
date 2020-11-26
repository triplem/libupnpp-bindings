%{
/* upnpp.i: libupnpp swig interface
 *
 * Copyright (C) 2017 J.F.Dockes
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Lesser General Public License as published by
 *   the Free Software Foundation; either version 2.1 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU Lesser General Public License for more details.
 *
 *   You should have received a copy of the GNU Lesser General Public License
 *   along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */
%}

/**************************************
 * Wrapper for the TypedService class, which has a string-based interface
 * and was actually created for ease of use from swig.
 * cdircontent is needed because of the VarEventReporter method which takes
 * an UPnPDirObject value argument.
 */
%include <libupnpp/upnppexports.hxx>
%include <libupnpp/control/cdircontent.hxx>
%include <libupnpp/control/service.hxx>

%newobject findTypedService;
%include <libupnpp/control/typedservice.hxx>

namespace std {
%template(VectorString)  vector<string>;
%template(MapStringString) map<string,string>;
}   

%include <libupnpp/log.h>

/* Description and discovery */
%include upnpp-devs.i

/*************************************************************************
 * Incomplete wrappers for avtransport and renderingcontrol. Not very
 * useful, code kept around for reference.
 * Because there is no factory function, these need to deal explicitely
 * with discovery and description.
 */

%include <libupnpp/control/renderingcontrol.hxx>

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
