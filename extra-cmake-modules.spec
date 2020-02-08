#define git 1
%define major %(echo %{version} |cut -d. -f1-2 |sed -e 's,^1,5,')
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)

Name:		extra-cmake-modules
Summary:	KDE Frameworks 5 cmake extra modules
Group:		Graphical desktop/KDE
Version:	5.67.0
Release:	1
License:	GPL
URL:		https://projects.kde.org/projects/kdesupport/extra-cmake-modules
Source0:	http://download.kde.org/%{stable}/frameworks/%{major}/%{name}-%{version}.tar.xz
Source10:	kde5.macros
# We can't use -Wl,--fatal-warnings on ARM because of warnings
# about .GNU.stack
Patch0:		extra-cmake-modules-1.0.0-no-ld-fatal-warnings.patch
Patch1:		extra-cmake-modules-5.57.0-support-newer-clang.patch
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
Requires:	qmake5
Requires:	ninja
# Required by virtually all cmake modules shipped here
Requires:	pkgconfig(Qt5Core)
Requires:	pkgconfig(Qt5Quick)
Requires:	cmake(Qt5LinguistTools)
%rename 	extra-cmake-modules5

%description
KDE Frameworks 5 cmake extra modules.

%files
%{_datadir}/ECM
%exclude %{_datadir}/ECM/find-modules/FindPythonModuleGeneration.cmake
%exclude %{_datadir}/ECM/find-modules/run-sip.py
%exclude %{_datadir}/ECM/find-modules/sip_generator.py
%{_mandir}/man7/*
%{_sysconfdir}/rpm/macros.d/*
%doc %{_docdir}/ECM

# We split the python bits into a separate package because of the
# large number of dependencies for cmake(PythonModuleGeneration)
# to be useful...
%package python
Summary:	extra-cmake-modules components needed for Python module generation
Group:		Graphical desktop/KDE
Requires:	%{name} = %{EVRD}
Requires:	python-sip
Requires:	python-clang
Requires:	clang-devel
Requires:	pkgconfig(python3)
Requires:	python-qt5-core

%description python
extra-cmake-modules components needed for Python module generation

%files python
%{_datadir}/ECM/find-modules/FindPythonModuleGeneration.cmake
%{_datadir}/ECM/find-modules/run-sip.py
%{_datadir}/ECM/find-modules/sip_generator.py

#--------------------------------------------------------------------
%prep
%setup -qn extra-cmake-modules%{!?git:-%{version}}
%ifnarch %ix86 %{x86_64}
%patch0 -p1 -b .ldfw~
%endif
%patch1 -p1 -b .clang~

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
