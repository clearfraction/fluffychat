%global flutter_version 3.0.1-stable
%global olm_version 3.2.10
%global commit b2ba999c7288ffce7eab90c01e6fbe02f460f84e
%global shortcommit %(c=%{commit}; echo ${c:0:7})


Name     : fluffychat
Version  : 1.5.0
Release  : 1
URL      : https://fluffychat.im
Source0  : https://gitlab.com/famedly/fluffychat/-/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
#Source0 : https://gitlab.com/famedly/fluffychat/-/archive/v%%{version}/fluffychat-v%%{version}.tar.gz
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
git config --global --add safe.directory /flutter


%setup -q -n fluffychat-%{commit} -a 1
sed -i 's|2906e65ffaa96afbe6c72e8477d4dfcdfd06c2c3|a3d4020911860ff091d90638ab708604b71d2c5a|g' pubspec.lock
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
export CFLAGS="$CFLAGS -O3 -flto=auto "
export FCFLAGS="$FFLAGS -O3 -flto=auto "
export FFLAGS="$FFLAGS -O3 -flto=auto "
export CXXFLAGS="$CXXFLAGS -O3 -flto=auto "


pushd olm-%{olm_version}
cmake . -Bbuilddir -DCMAKE_BUILD_TYPE=Release
cmake --build builddir && cmake --install ./builddir --prefix /usr
  pushd ./builddir/tests/
    ctest .
  popd
popd

export CC=clang
export CXX=clang++
export LD=ld.gold
CFLAGS=${CFLAGS/ -Wa,/ -fno-integrated-as -Wa,}
CXXFLAGS=${CXXFLAGS/ -Wa,/ -fno-integrated-as -Wa,}
unset LDFLAGS
export CXXFLAGS=`echo $CXXFLAGS| sed 's|-Wl,--enable-new-dtags||g'`
export CXXFLAGS=`echo $CXXFLAGS| sed 's|-Wl,--build-id=sha1||g'`
export CXXFLAGS=`echo $CXXFLAGS| sed 's|-Wl,-z -Wl,now -Wl,-z -Wl,relro||g'`
export CXXFLAGS=`echo $CXXFLAGS| sed 's|-Wl,-z,now,-z,relro,-z,max-page-size=0x4000,-z,separate-code||g'`
export CXXFLAGS=`echo $CXXFLAGS| sed 's|,--emit-relocs||g'`
export CXXFLAGS=`echo $CXXFLAGS| sed 's|-mrelax-cmpxchg-loop|-enable-trivial-auto-var-init-zero-knowing-it-will-be-removed-from-clang|g'`
flutter clean
flutter build linux --release


%install
mkdir -p %{buildroot}/usr/share/{pixmaps,applications,fluffychat} %{buildroot}/usr/lib64
mv %{_builddir}/fluffychat-*/build/linux/x64/release/bundle/* %{buildroot}/usr/share/fluffychat
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
