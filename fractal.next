%global commit0 bae327b4a5872a212965d04236bba6e675106f51
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:       fractal
Version:    5.0
Release:    1
Summary:    Matrix client
Group:      Applications/Internet
License:    GPLv3
URL:        https://gitlab.gnome.org/GNOME/fractal
Source:     https://gitlab.gnome.org/GNOME/fractal/-/archive/fractal-next/fractal-fractal-next.tar.gz
BuildRequires:  rustc 
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  libadwaita-dev
BuildRequires:  gtk4-dev
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
BuildRequires:  desktop-file-utils
BuildRequires:  openssl-dev
BuildRequires:  gobject-introspection-dev
BuildRequires:  cmake
BuildRequires:  gst-editing-services-dev
BuildRequires:  gmp-dev at-spi2-atk-dev
BuildRequires:  libsecret-dev pango-dev cairo-dev
BuildRequires:  Vulkan-Loader-dev Vulkan-Headers-dev Vulkan-ValidationLayers-dev
BuildRequires:  pcre2-dev gtksourceview5-dev
Requires:       gstreamer1-plugins-base-tools
Requires:       gstreamer1-plugins-base
Requires:       libappstream-glib
Requires:       sqlite-libs
Requires:       gstreamer1-plugins-bad-nonfree
Requires:       gstreamer1-libav

%description
Matrix client

%prep 
%setup -n fractal-fractal-next

# fix pkgdatadir
sed -i "s|@PKGDATADIR@|\"/opt/3rd-party/bundles/clearfraction/usr/share/fractal\"|" src/config.rs.in
sed -i "s|Cargo.toml -p|Cargo.toml --release -p|" build-aux/cargo.sh

%build
unset http_proxy
unset no_proxy 
unset https_proxy
meson --libdir=lib64 --prefix=/usr --buildtype=plain -Dprofile=default  builddir
ninja -v -C builddir

%install
DESTDIR=%{buildroot} ninja -C builddir install


%files
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/metainfo/*.xml
/usr/share/fractal/resources.gresource

%changelog
