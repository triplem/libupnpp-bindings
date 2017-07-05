%module upcppy

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
#include <iostream>
#include <libupnpp/control/description.hxx>
#include <libupnpp/control/discovery.hxx>
#include <libupnpp/control/cdircontent.hxx>
#include <libupnpp/control/avtransport.hxx>
#include <libupnpp/control/renderingcontrol.hxx>
%}


%include stl.i
%include typemaps.i

%include "description.hxx"
%include "discovery.hxx"
%include "cdircontent.hxx"
%include "service.hxx"
%include "renderingcontrol.hxx"

/* Helper for finding a service description specified by service type inside a
 * device description, then used to call the service constructor.
 * C++ code would use the device directory traverse()
 * method to do this, but I'm not too sure how to do it from Python. 
 * sobj is typically an empty object (default constructor) just used to call
 * the appropriate virtual method, which avoids having to use templates.
 * Usage was:
 *   rdrdesc = upcppy.findServiceDesc(emptyrdr, desc)
 *   if rdrdesc:
 *       rdrc = upcppy.RenderingControl(desc, rdrdesc)
 *
 * This has been replaced by the initFromDescription() call on an empty object
 */
%{
UPnPClient::UPnPServiceDesc *
findServiceDesc(UPnPClient::Service *sobj, UPnPClient::UPnPDeviceDesc *dev)
{
    for (auto& serv : dev->services) {
        if (sobj->serviceTypeMatch(serv.serviceType)) {
           return &serv;
        }
    }
    return 0;
}
%}

UPnPClient::UPnPServiceDesc *findServiceDesc(UPnPClient::Service *,
                                             UPnPClient::UPnPDeviceDesc *);


%include "avtransport.hxx"

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


namespace std {
%template(VectorString)  vector<string>;
%template(MapStringString) map<string,string>;
}   

%{
#include <libupnpp/control/typedservice.hxx>
%}

%newobject findTypedService;
%include "typedservice.hxx"

