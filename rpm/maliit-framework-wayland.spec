# Out of tree builds are not default at the moment
# Remove this line when it is the default
%undefine __cmake_in_source_build

Name:       maliit-framework-wayland

Summary:    Core libraries of Maliit and server (Lipstick/Wayland environment)
Version:    2.2.1
Release:    1
License:    LGPL-2.0
URL:        https://github.com/sailfishos/maliit-framework
Source0:    %{name}-%{version}.tar.bz2
Requires:   maliit-framework-wayland-inputcontext
Requires:   qt5-qtdeclarative-import-qtquick2plugin
Requires:   systemd-user-session-targets
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(mce)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(qt5-boostable)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  cmake
Requires:   mapplauncherd-qt5
Provides:   maliit-framework

Source1: maliit-server.sh
Source2: maliit-server.service
Source3: tests.xml.in

Patch1: 0001-Install-unit-test-files.patch
Patch2: 0002-enable-systemd-activation.patch
Patch3: 0003-lipstick-platform.patch
Patch4: 0004-Use-invoker-to-launch.patch
Patch5: 0005-Use-mce-for-keyboard-state.-Fixes-JB-48910.patch
Patch6: 0006-Forward-arbitrary-extension-properties-to-QML-input-.patch
Patch7: 0007-Use-non-abstract-unix-domain-socket.-JB-52254.patch
Patch8: 0008-Allow-D-Bus-activation-only-through-systemd.-JB-5257.patch
Patch9: 0009-Fix-build-on-Qt-5.6.patch
Patch10: 0010-Revert-Fix-mapping-between-screen-orientations-and-r.patch
Patch11: 0011-Install-.prf-files-as-per-sailfish-setup.patch
Patch12: 0012-Fix-maliit-defines.prf-paths.patch

%description
Core libraries of Maliit and server


%package inputcontext
Summary:    Qt5 plugin for connecting to Maliit input method server
Requires:   %{name} = %{version}-%{release}

%description inputcontext
This package contains loadable plugin for Qt5 which allows to connect
to Maliit input method server


%package devel
Summary:    Maliit Framework Input Method Development Package
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-glib = %{version}-%{release}

%description devel
This package contains the files necessary to develop
input method plugins using Maliit


%package tests
Summary:    Maliit Framework Input Method Tests Package
Requires:   %{name} = %{version}-%{release}

%description tests
This package contains the files necessary to test
the Maliit input method framework


%package glib
Summary:    Maliit Framework Input Method Glib Package
Requires:   %{name} = %{version}-%{release}

%description glib
This package contains the files necessary to use
maliit keyboard via glib apis

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
%cmake \
      -Denable-docs=OFF \
      -Denable-glib=ON \
      -Denable-xcb=OFF \
      -Denable-wayland=OFF \
      -Denable-dbus-activation=ON \
      %{nil}
%cmake_build

%install
%cmake_install
install -D -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/profile.d/maliit-server.sh
install -D -m 0644 %{SOURCE2} %{buildroot}%{_userunitdir}/maliit-server.service
mkdir -p %{buildroot}%{_userunitdir}/user-session.target.wants
ln -s ../maliit-server.service %{buildroot}%{_userunitdir}/user-session.target.wants/
mkdir %{buildroot}%{_libdir}/maliit
mkdir %{buildroot}%{_datadir}/maliit
install -D -m 0644 %{SOURCE3} %{buildroot}/opt/tests/maliit-framework/tests.xml
sed -i -e 's:@PATH@:%{_libdir}/maliit-framework-tests:g' %{buildroot}/opt/tests/maliit-framework/tests.xml


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license LICENSE.LGPL
%{_bindir}/maliit-server
%{_libdir}/libmaliit-plugins.so.*
%{_datadir}/dbus-1/services/org.maliit.server.service
%config %{_sysconfdir}/profile.d/maliit-server.sh
%{_userunitdir}/maliit-server.service
%{_userunitdir}/user-session.target.wants/maliit-server.service
%dir %{_libdir}/maliit
%dir %{_datadir}/maliit
%exclude %{_docdir}/maliit-framework/

%files glib
%{_libdir}/libmaliit-glib.so.*

%files inputcontext
%defattr(-,root,root,-)
%{_libdir}/qt5/plugins/platforminputcontexts/*.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmaliit-plugins.so
%{_includedir}/maliit-2/
%{_libdir}/pkgconfig/*.pc
%{_datadir}/qt5/mkspecs/features/*
%{_libdir}/cmake/MaliitPlugins/
%{_libdir}/cmake/MaliitGLib/
%{_libdir}/libmaliit-glib.so

%files tests
%defattr(-,root,root,-)
%{_libdir}/maliit-framework-tests/
/opt/tests/maliit-framework/tests.xml
