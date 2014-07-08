#define git 1

Name:		extra-cmake-modules5
Summary:	KDE Frameworks 5 cmake extra modules
Group:		Graphical desktop/KDE
Version:	1.0.0
Release:	1
License:	GPL
URL:		https://projects.kde.org/projects/kdesupport/extra-cmake-modules
# http://download.kde.org/unstable/frameworks/4.99.0/%{name}%{?!git:-%{version}}.tar.xz
Source0:	http://ftp5.gwdg.de/pub/linux/kde/stable/frameworks/5.0.0/extra-cmake-modules-%{version}.tar.xz
BuildArch:	noarch
BuildRequires:	cmake
Requires:	qt5-devel
Requires:	cmake
Requires:	qmake5
# Required by virtually all cmake modules shipped here
Requires:	cmake(Qt5LinguistTools)
Requires:	qt5-platformtheme-gtk2

%description
KDE Frameworks 5 cmake extra modules.

%files
%{_datadir}/ECM
%{_mandir}/man7/*
%doc %{_docdir}/ECM

#--------------------------------------------------------------------
%prep
%setup -qn extra-cmake-modules%{!?git:-%{version}}
%apply_patches

%build
%cmake
%make

%install
rm -fr %{buildroot}
%makeinstall_std -C build
