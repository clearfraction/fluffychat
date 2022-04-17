%global flutter_version 2.10.1-stable
%global olm_version 3.2.10

Name     : fluffychat
Version  : 1.3.1
Release  : 1
URL      : https://fluffychat.im
Source0  : https://gitlab.com/famedly/fluffychat/-/archive/v%{version}/fluffychat-v%{version}.tar.gz
Source1  : https://gitlab.matrix.org/matrix-org/olm/-/archive/%{olm_version}/olm-%{olm_version}.tar.bz2
Summary  : Matrix. Chat with your friends.
Group    : Development/Tools
License  : AGPL-3.0
BuildRequires : glib-dev
BuildRequires : gtk3-dev
BuildRequires : libsecret-dev
BuildRequires : openssl-dev
BuildRequires : jsoncpp-dev
BuildRequires : libxdg-basedir-dev
BuildRequires : which
BuildRequires : cmake
BuildRequires : ninja
BuildRequires : llvm
BuildRequires : compat-webkitgtk-soname40-dev

%description
Matrix. Chat with your friends.

%prep
curl -LO https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_%{flutter_version}.tar.xz
tar xf flutter_linux_%{flutter_version}.tar.xz -C /
export PATH=/flutter/bin:"$PATH"

%setup -q -n fluffychat-v%{version} -a 1
dart --disable-analytics
flutter config --no-analytics
flutter config --enable-linux-desktop

%build
unset http_proxy
unset no_proxy 
unset https_proxy
export LANG=C.UTF-8
export GCC_IGNORE_WERROR=1
export PATH=/flutter/bin:"$PATH"
export CC=clang
export CXX=clang++
export LD=ld.gold
CFLAGS=${CFLAGS/ -Wa,/ -fno-integrated-as -Wa,}
CXXFLAGS=${CXXFLAGS/ -Wa,/ -fno-integrated-as -Wa,}
unset LDFLAGS
export CFLAGS="$CFLAGS -fno-lto "
export FCFLAGS="$FFLAGS -fno-lto "
export FFLAGS="$FFLAGS -fno-lto "
export CXXFLAGS="$CXXFLAGS -fno-lto "

export CXXFLAGS=`echo $CXXFLAGS| sed 's|-Wl,--enable-new-dtags||g'`
export CXXFLAGS=`echo $CXXFLAGS| sed 's|-Wl,--build-id=sha1||g'`
export CXXFLAGS=`echo $CXXFLAGS| sed 's|-Wl,-z,now,-z,relro,-z,max-page-size=0x1000,-z,separate-code||g'`
export CXXFLAGS=`echo $CXXFLAGS| sed 's|,--emit-relocs||g'`
export CXXFLAGS=`echo $CXXFLAGS| sed 's|,-mrelax-cmpxchg-loop||g'`

export CFLAGS=`echo $CFLAGS| sed 's|-Wl,--enable-new-dtags||g'`
export CFLAGS=`echo $CFLAGS| sed 's|-Wl,--build-id=sha1||g'`
export CFLAGS=`echo $CFLAGS| sed 's|-Wl,-z,now,-z,relro,-z,max-page-size=0x1000,-z,separate-code||g'`
export CFLAGS=`echo $CFLAGS| sed 's|,--emit-relocs||g'`
export CFLAGS=`echo $CFLAGS| sed 's|,-mrelax-cmpxchg-loop||g'`


pushd olm-%{olm_version}
cmake . -Bbuilddir -DCMAKE_BUILD_TYPE=Release
cmake --build builddir && cmake --install ./builddir --prefix /usr
  pushd ./builddir/tests/
    ctest .
  popd
popd

flutter clean
flutter build linux --release


%install
mkdir -p %{buildroot}/usr/share/{pixmaps,applications,fluffychat} %{buildroot}/usr/lib64
mv %{_builddir}/fluffychat-v%{version}/build/linux/x64/release/bundle/* %{buildroot}/usr/share/fluffychat
rm -rf %{buildroot}/usr/share/fluffychat/data/flutter_assets/fonts/{NotoEmoji,Roboto}
cp -r /usr/lib64/libolm* %{buildroot}/usr/lib64
mv %{buildroot}/usr/share/fluffychat/data/flutter_assets/assets/favicon.png %{buildroot}/usr/share/pixmaps/fluffychat.png
cat > %{buildroot}/usr/share/applications/fluffychat.desktop << EOF
[Desktop Entry]
Type=Application
Version=%{version}
Name=FluffyChat
Comment=Matrix Client. Chat with your friends
Exec=env GDK_GL=gles /opt/3rd-party/bundles/clearfraction/usr/share/fluffychat/fluffychat
Icon=fluffychat
Terminal=false
EOF

%files
%defattr(-,root,root,-)
/usr/share/fluffychat
/usr/lib64/libolm*
/usr/share/applications/fluffychat.desktop
/usr/share/pixmaps/fluffychat.png
