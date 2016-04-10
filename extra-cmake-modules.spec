#define git 1
%define major %(echo %{version} |cut -d. -f1-2 |sed -e 's,^1,5,')
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

Name:		extra-cmake-modules
Summary:	KDE Frameworks 5 cmake extra modules
Group:		Graphical desktop/KDE
Version:	5.21.0
Release:	1
License:	GPL
URL:		https://projects.kde.org/projects/kdesupport/extra-cmake-modules
Source0:	http://download.kde.org/%{stable}/frameworks/%{major}/%{name}-%{version}.tar.xz
Source10:	kde5.macros
# We can't use -Wl,--fatal-warnings on ARM because of warnings
# about .GNU.stack
Patch0:		extra-cmake-modules-1.0.0-no-ld-fatal-warnings.patch
BuildArch:	noarch
BuildRequires:	cmake
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	qmake5
# For doc generation
BuildRequires:	python2-sphinx
BuildRequires:	python2-setuptools
BuildRequires:	ninja
Requires:	cmake
Requires:	qmake5
Requires:	ninja
# Required by virtually all cmake modules shipped here
Requires:	cmake(Qt5LinguistTools)
Requires:	qt5-qtbase-platformtheme-gtk2
%rename 	extra-cmake-modules5

%description
KDE Frameworks 5 cmake extra modules.

%files
%{_datadir}/ECM
%{_mandir}/man7/*
%{_sysconfdir}/rpm/macros.d/*
%doc %{_docdir}/ECM

#--------------------------------------------------------------------
%prep
%setup -qn extra-cmake-modules%{!?git:-%{version}}
%ifnarch %ix86 x86_64
%patch0 -p1 -b .ldfw~
%endif

%build
%cmake_qt5 \
    -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
    -DKDE_INSTALL_QTPLUGINDIR=%{_qt5_plugindir} \
    -DKDE_INSTALL_PLUGINDIR=%{_qt5_plugindir} \
    -DPLUGIN_INSTALL_DIR:PATH=%{_qt5_plugindir} \
    -DQT_PLUGIN_INSTALL_DIR:PATH=%{_qt5_plugindir} \
    -G Ninja

ninja

%install
DESTDIR="%{buildroot}" ninja install -C build

install -c -m 644 -D %{SOURCE10} "%{buildroot}"%{_sysconfdir}/rpm/macros.d/kde5.macros
