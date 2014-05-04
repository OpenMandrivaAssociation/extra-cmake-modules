#define git 1

Name:		extra-cmake-modules5
Summary:	KDE Frameworks 5 cmake extra modules
Group:		Graphical desktop/KDE
Version:	0.0.12
Release:	1
License:	GPL
URL:		https://projects.kde.org/projects/kdesupport/extra-cmake-modules
# http://download.kde.org/unstable/frameworks/4.98.0/%{name}%{?!git:-%{version}}.tar.xz
Source0:	http://ftp5.gwdg.de/pub/linux/kde/unstable/frameworks/4.98.0/extra-cmake-modules-%{version}.tar.xz
BuildArch:	noarch
BuildRequires:	cmake
Requires:	qt5-devel

%description
KDE Frameworks 5 cmake extra modules.

%files
%{_datadir}/ECM

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
