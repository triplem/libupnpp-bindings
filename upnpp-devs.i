%{
/* upnpp-devs.i: libupnpp description and discovery swig interface
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

/* We have a hard time with discovery and description because of all the
   embedded classes. Needs a lot of glue code */

%warnfilter(325) UPnPClient::UPnPServiceDesc::Argument;
%warnfilter(325) UPnPClient::UPnPServiceDesc::Action;
%warnfilter(325) UPnPClient::UPnPServiceDesc::StateVariable;
%warnfilter(325) UPnPClient::UPnPServiceDesc::Parsed;

%include <libupnpp/control/description.hxx>
%include <libupnpp/control/discovery.hxx>

%inline %{

struct CUPnPServiceArgument {
    CUPnPServiceArgument() {}
    CUPnPServiceArgument(const UPnPClient::UPnPServiceDesc::Argument& r)
        : name(r.name), todevice(r.todevice), relatedVariable(r.relatedVariable)
        {}
        
    std::string name;
    bool todevice;
    std::string relatedVariable;
};
%}

namespace std {
%template(VectorCUPnPServiceArgument) vector<CUPnPServiceArgument>;
}

%inline %{
struct CUPnPServiceAction {
    CUPnPServiceAction() {}
    CUPnPServiceAction(const UPnPClient::UPnPServiceDesc::Action& r)
        : name(r.name), argList(r.argList.begin(), r.argList.end()) {}

    std::string name;
    std::vector<CUPnPServiceArgument> argList;
};

struct CUPnPServiceVariable {
    CUPnPServiceVariable() {}
    CUPnPServiceVariable(const UPnPClient::UPnPServiceDesc::StateVariable& r)
        : name(r.name), sendEvents(r.sendEvents), dataType(r.dataType),
          hasValueRange(r.hasValueRange), minimum(r.minimum), maximum(r.maximum),
          step(r.step) {}

    std::string name;
    bool sendEvents;
    std::string dataType;
    bool hasValueRange;
    int minimum;
    int maximum;
    int step;
};

%}

namespace std {
%template(UMapCUPnPServiceAction)  map<string, CUPnPServiceAction>;
%template(UMapCUPnPServiceVariable)  map<string, CUPnPServiceVariable>;
}

%inline %{
struct CUPnPServiceDesc {
    CUPnPServiceDesc() {}
    CUPnPServiceDesc(const UPnPClient::UPnPServiceDesc& r)
        : serviceType(r.serviceType), serviceId(r.serviceId),
          SCPDURL(r.SCPDURL), controlURL(r.controlURL),
          eventSubURL(r.eventSubURL), m_libservice(r) {}
    
    /// Service Type e.g. urn:schemas-upnp-org:service:ConnectionManager:1
    std::string serviceType;
    /// Service Id inside device: e.g. urn:upnp-org:serviceId:ConnectionManager
    std::string serviceId; 
    /// Service description URL.
    std::string SCPDURL;
    /// Service control URL.
    std::string controlURL; 
    /// Service event URL.
    std::string eventSubURL;

    // actionList and stateTable are only valid after a successful
    // call to fetchAndParseDesc()
    bool fetchAndParseDesc(const std::string& urlbase) {
        UPnPClient::UPnPServiceDesc::Parsed parsed;
        if (!m_libservice.fetchAndParseDesc(urlbase, parsed, 0)) {
            return false;
        }
        for (const auto& entry : parsed.actionList) {
            actionList.insert(
                std::pair<std::string, CUPnPServiceAction>
                (entry.first, entry.second));
        }
        for (const auto& entry : parsed.stateTable) {
            stateTable.insert(
                std::pair<std::string, CUPnPServiceVariable>
                (entry.first, entry.second));
        }
        return true;
    }
    std::map<std::string, CUPnPServiceAction> actionList;
    std::map<std::string, CUPnPServiceVariable> stateTable;
private:
    // fetchAndParseDesc is a UPnPServiceDesc member, so we have to keep a copy
    // of the libupnpp object if we want to be able to call it.
    UPnPClient::UPnPServiceDesc m_libservice;
};
%}

namespace std {
%template(VectorCUPnPServiceDesc)  vector<CUPnPServiceDesc>;
}

%inline %{
struct CUPnPDeviceDesc {
    CUPnPDeviceDesc() {}
    CUPnPDeviceDesc(const UPnPClient::UPnPDeviceDesc& r)
        : deviceType(r.deviceType), friendlyName(r.friendlyName), UDN(r.UDN),
          URLBase(r.URLBase), manufacturer(r.manufacturer), modelName(r.modelName),
          XMLText(r.XMLText), services(r.services.begin(), r.services.end()) {}

    /// Device Type: e.g. urn:schemas-upnp-org:device:MediaServer:1
    std::string deviceType;
    /// User-configurable name (usually), e.g. Lounge-streamer
    std::string friendlyName;
    /// Unique Device Number. This is the same as the deviceID in the
    /// discovery message. e.g. uuid:a7bdcd12-e6c1-4c7e-b588-3bbc959eda8d
    std::string UDN;
    /// Base for all relative URLs. e.g. http://192.168.4.4:49152/
    std::string URLBase;
    /// Manufacturer: e.g. D-Link, PacketVideo
    std::string manufacturer;
    /// Model name: e.g. MediaTomb, DNS-327L
    std::string modelName;

    /// Raw description text
    std::string XMLText;

    std::vector<CUPnPServiceDesc> services;
};

%}

namespace std {
%template(VectorCUPnPDeviceDesc)  vector<CUPnPDeviceDesc>;
}

%newobject getDevices;

%inline %{
std::vector<CUPnPDeviceDesc> getDevices() {
    auto superdir = UPnPClient::UPnPDeviceDirectory::getTheDir(1);
    if (nullptr == superdir) {
        return std::vector<CUPnPDeviceDesc>();
    }
    std::unordered_map<std::string, CUPnPDeviceDesc> devmap;
    superdir->traverse(
        [&devmap](const UPnPClient::UPnPDeviceDesc& dev,
                  const UPnPClient::UPnPServiceDesc& serv)->bool {
            if (devmap.find(dev.UDN) == devmap.end()) {
                devmap.insert(std::pair<std::string, CUPnPDeviceDesc>(
                                  dev.UDN, CUPnPDeviceDesc(dev)));
            }
            return true;
        });

    std::vector<CUPnPDeviceDesc> devs;
    for (const auto& entry: devmap) {
        devs.push_back(entry.second);
    }
    return devs;
}

%}
