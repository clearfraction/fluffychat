%global debug_package %{nil}
%global commit0 7a97d2a880dc574457e1db0be5c3c7d4b2225b2c
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:       fractal
Version:    4.4.0
Release:    1
Summary:    Matrix client
Group:      Applications/Internet
License:    GPLv3
URL:        https://gitlab.gnome.org/GNOME/fractal
Source0:    https://gitlab.gnome.org/GNOME/fractal/-/archive/%{commit0}/fractal-%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildRequires:  rustc 
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  libhandy-dev
BuildRequires:  gtk3-dev
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires:  intltool desktop-file-utils
BuildRequires:  appstream-glib-dev
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  gettext
BuildRequires:  libdazzle-dev
BuildRequires:  desktop-file-utils
BuildRequires:  openssl-dev
BuildRequires:  gobject-introspection-dev
BuildRequires:  cmake
BuildRequires:  gtksourceview-dev
BuildRequires:  gspell-dev
BuildRequires:  gst-editing-services-dev
Requires:       gstreamer1-plugins-base-tools
Requires:       gstreamer1-plugins-base
Requires:       libappstream-glib
Requires:       sqlite-libs
Requires:       gstreamer1-plugins-bad-nonfree
Requires:       gstreamer1-libav

%description
Matrix client

%prep 
%setup -n fractal-%{commit0}

# fix pkgdatadir
sed -i "s|@PKGDATADIR@|\"/opt/3rd-party/bundles/clearfraction/usr/share/fractal\"|" fractal-gtk/src/config.rs.in


%build
unset http_proxy
unset no_proxy 
unset https_proxy
meson --libdir=lib64 --prefix=/usr --buildtype=plain  builddir
ninja -v -C builddir

%install
DESTDIR=%{buildroot} ninja -C builddir install
%find_lang %{name}


%files -f %{name}.lang
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/metainfo/*.xml


%changelog
# based on https://github.com/UnitedRPMs/shortwave
