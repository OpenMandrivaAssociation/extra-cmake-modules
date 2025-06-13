%define major %(echo %{version} |cut -d. -f1-2 |sed -e 's,^1,5,')
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
#define git 20240217
%undefine _debugsource_packages

Name:		extra-cmake-modules
Summary:	KDE Frameworks 5 cmake extra modules
Group:		Graphical desktop/KDE
Version:	6.15.0
Release:	%{?git:0.%{git}.}1
License:	GPL
URL:		https://projects.kde.org/projects/kdesupport/extra-cmake-modules
%if 0%{?git:1}
Source0:	https://invent.kde.org/frameworks/extra-cmake-modules/-/archive/master/extra-cmake-modules-master.tar.bz2#/extra-cmake-modules-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/frameworks/%{major}/%{name}-%{version}.tar.xz
%endif
Source10:	kde5.macros
BuildArch:	noarch
# Version dependency is to make sure we have the current version
# of the cmake dependency generators
BuildRequires:	cmake >= 3.11.2-1
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	qmake5
# For doc generation
BuildRequires:	python-sphinx
BuildRequires:	python-setuptools
BuildRequires:	ninja
Requires:	cmake >= 3.11.2-1
# For Qt 5 detection
Requires:	qmake5
# For Qt 6 detection
Requires:	qt6-qtbase-tools
Requires:	cmake(Qt6CoreTools)
Requires:	ninja
%rename 	extra-cmake-modules5
Obsoletes:	%{name}-python < %{EVRD}

%patchlist
# We can't use -Wl,--fatal-warnings on ARM because of warnings
# about .GNU.stack
extra-cmake-modules-1.0.0-no-ld-fatal-warnings.patch

%description
KDE Frameworks cmake extra modules.

%files
%{_datadir}/ECM
%{_mandir}/man7/*
%{_sysconfdir}/rpm/macros.d/*
%doc %{_docdir}/ECM

#--------------------------------------------------------------------
%prep
%autosetup -p1 -n extra-cmake-modules%{!?git:-%{version}}%{?git:-master}

%build
%cmake \
    -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
    -DKDE_INSTALL_QTPLUGINDIR=%{_qt5_plugindir} \
    -DKDE_INSTALL_PLUGINDIR=%{_qt5_plugindir} \
    -DPLUGIN_INSTALL_DIR:PATH=%{_qt5_plugindir} \
    -DQT_PLUGIN_INSTALL_DIR:PATH=%{_qt5_plugindir} \
    -G Ninja

%ninja_build

%install
%ninja_install -C build

install -c -m 644 -D %{SOURCE10} "%{buildroot}"%{_sysconfdir}/rpm/macros.d/kde5.macros
