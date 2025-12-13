%define major %(echo %{version} |cut -d. -f1-2 |sed -e 's,^1,5,')
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
#define git 20240217
%undefine _debugsource_packages

Name:		extra-cmake-modules
Summary:	KDE Frameworks 5 cmake extra modules
Group:		Graphical desktop/KDE
Version:	6.21.0
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
BuildSystem:	cmake
BuildOption:    -DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON
# For doc generation
BuildRequires:	python-sphinx
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	ninja
Requires:	cmake >= 3.11.2-1
# For Qt 6 detection
Requires:	qt6-qtbase-tools
Requires:	cmake(Qt6CoreTools)
Requires:	ninja
%rename 	extra-cmake-modules5
Obsoletes:	%{name}-python < %{EVRD}

%package plasma5
Summary:	Support for outdated Plasma 5.x in extra-cmake-modules
Requires:	%{name} = %{EVRD}
# For Qt 5 detection
Requires:	qmake5

%description plasma5
Support for outdated Plasma 5.x in extra-cmake-modules

%patchlist
# We can't use -Wl,--fatal-warnings on ARM because of warnings
# about .GNU.stack
extra-cmake-modules-1.0.0-no-ld-fatal-warnings.patch

%description
KDE Frameworks cmake extra modules.

%files
%{_datadir}/ECM
%{_mandir}/man7/*
%doc %{_docdir}/ECM

%files plasma5
%{_sysconfdir}/rpm/macros.d/kde5.macros

%install -a
install -c -m 644 -D %{SOURCE10} "%{buildroot}"%{_sysconfdir}/rpm/macros.d/kde5.macros
