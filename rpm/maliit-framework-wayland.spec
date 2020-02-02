Name:       maliit-framework-wayland

Summary:    Core libraries of Maliit and server (Lipstick/Wayland environment)
Version:    0.99.1
Release:    1
License:    LGPLv2
URL:        https://github.com/maliit/framework
Source0:    %{name}-%{version}.tar.bz2
Requires:   maliit-framework-wayland-inputcontext
Requires:   qt5-qtdeclarative-import-qtquick2plugin
Requires:   systemd-user-session-targets
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  pkgconfig(Qt5Test)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  fdupes
BuildRequires:  pkgconfig(qt5-boostable)
BuildRequires:  pkgconfig(contextkit-statefs)
Requires:   mapplauncherd-qt5
Provides:   maliit-framework
Conflicts:   maliit-framework-x11
Obsoletes:   libmaliit-quick

%description
Core libraries of Maliit and server


%package inputcontext
Summary:    Qt5 plugin for connecting to Maliit input method server
Requires:   %{name} = %{version}-%{release}
Provides:   qt5-plugin-platform-inputcontext-maliit
Obsoletes:  qt5-plugin-platform-inputcontext-maliit

%description inputcontext
This package contains loadable plugin for Qt5 which allows to connect
to Maliit input method server


%package devel
Summary:    Maliit Framework Input Method Development Package
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the files necessary to develop
input method plugins using Maliit


%package doc
Summary:    Maliit Framework Documentation
Requires:   %{name} = %{version}-%{release}

%description doc
Documentation for the Maliit Input Method Framework

%package examples
Summary:    Maliit Framework Input Method Examples
Requires:   %{name} = %{version}-%{release}

%description examples
This package contains examples applications for
the Maliit input method framework


%package tests
Summary:    Maliit Framework Input Method Tests Package
Requires:   %{name} = %{version}-%{release}

%description tests
This package contains the files necessary to test
the Maliit input method framework


%prep
%setup -q -n %{name}-%{version}

pushd maliit-framework
popd

%build
pushd maliit-framework
%qmake5  \
    CONFIG+=enable-dbus-activation \
    CONFIG+=qt5-inputcontext \
    CONFIG+=lipstick \
    CONFIG+=noxcb \
    CONFIG+=enable-contextkit

make %{?jobs:-j%jobs}
popd

%install
rm -rf %{buildroot}
pushd maliit-framework
%qmake_install
popd
install -D -m 0644 maliit-server.sh %{buildroot}%{_sysconfdir}/profile.d/maliit-server.sh
install -D -m 0644 maliit-server.service %{buildroot}%{_libdir}/systemd/user/maliit-server.service
mkdir -p %{buildroot}%{_libdir}/systemd/user/user-session.target.wants
ln -s ../maliit-server.service %{buildroot}%{_libdir}/systemd/user/user-session.target.wants/
mkdir %{buildroot}%{_libdir}/maliit
mkdir %{buildroot}%{_datadir}/maliit


%fdupes  %{buildroot}/%{_libdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license maliit-framework/LICENSE.LGPL
%{_bindir}/maliit-server
%{_libdir}/libmaliit-plugins.so*
%{_datadir}/dbus-1/services/org.maliit.server.service
%config %{_sysconfdir}/profile.d/maliit-server.sh
%{_libdir}/systemd/user/maliit-server.service
%{_libdir}/systemd/user/user-session.target.wants/maliit-server.service
%dir %{_libdir}/maliit
%dir %{_datadir}/maliit

%files inputcontext
%defattr(-,root,root,-)
%{_libdir}/qt5/plugins/platforminputcontexts/*.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/maliit/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/qt5/mkspecs/features/*

%files doc
%defattr(-,root,root,-)
%{_docdir}/maliit-framework/html

%files examples
%defattr(-,root,root,-)
%{_bindir}/maliit-exampleapp-plainqt

%files tests
%defattr(-,root,root,-)
%{_libdir}/maliit-framework-tests/
/opt/tests/maliit-framework/tests.xml
