%{
/* upnpp-head.i: libupnpp includes for the swig files
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


%{
#include <libupnpp/control/description.hxx>
#include <libupnpp/control/cdircontent.hxx>
#include <libupnpp/control/typedservice.hxx>
#include <libupnpp/control/discovery.hxx>
#include <libupnpp/control/renderingcontrol.hxx>
#include <libupnpp/control/avtransport.hxx>
%}

%include stl.i

%template(VectorUPnPDirContent)  std::vector<UPnPClient::UPnPDirObject>;
%template(VectorUPnPResource)  std::vector<UPnPClient::UPnPResource>;
