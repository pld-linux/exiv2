#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	curl		# enable webready with HTTP support via curl
%bcond_with	libssh		# enable webready with SSH support via libssh

Summary:	EXIF and IPTC metadata manipulation tools
Summary(pl.UTF-8):	Narzędzia do obróbki metadanych EXIF i IPTC
Name:		exiv2
Version:	0.27.6
Release:	1
License:	GPL v2+
Group:		Applications/Graphics
#Source0Download: https://exiv2.org/download.html
Source0:	https://github.com/Exiv2/exiv2/releases/download/v%{version}/%{name}-%{version}-Source.tar.gz
# Source0-md5:	837a469b0957df8b657151ffb9449771
Patch0:		%{name}-no-xmpsdk-install.patch
URL:		https://exiv2.org/
BuildRequires:	cmake >= 3.3.2
%{?with_curl:BuildRequires:	curl-devel}
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	expat-devel
BuildRequires:	gettext-tools
%{?with_libssh:BuildRequires:	libssh-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
EXIF and IPTC metadata manipulation tools.

%description -l pl.UTF-8
Narzędzia do obróbki metadanych EXIF i IPTC.

%package libs
Summary:	EXIF and IPTC metadata manipulation library
Summary(pl.UTF-8):	Biblioteka do obróbki metadanych EXIF i IPTC
Group:		Libraries

%description libs
EXIF and IPTC metadata manipulation library.

%description libs -l pl.UTF-8
Biblioteka do obróbki metadanych EXIF i IPTC.

%package devel
Summary:	EXIF and IPTC metadata manipulation library development files
Summary(pl.UTF-8):	Pliki programistyczne biblioteki do obróbki metadanych EXIF i IPTC
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
%{?with_curl:Requires:	curl-devel}
Requires:	expat-devel
%{?with_libssh:Requires:	libssh-devel}
Requires:	libstdc++-devel
Requires:	zlib-devel
Obsoletes:	exiv2-static < 0.27.0a-3

%description devel
EXIF and IPTC metadata manipulation library development files.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki do obróbki metadanych EXIF i IPTC.

%package apidocs
Summary:	API documentation for exiv2 library
Summary(pl.UTF-8):	Dokumentacja API biblioteki exiv2
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for exiv2 library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki exiv2.

%prep
%setup -q -n %{name}-%{version}-Source
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/exiv2 \
	%{?with_apidocs:-DEXIV2_BUILD_DOC=ON} \
	-DEXIV2_BUILD_SAMPLES=OFF \
	-DEXIV2_ENABLE_BMFF=ON \
	%{?with_curl:-DEXIV2_ENABLE_CURL=ON} \
	-DEXIV2_ENABLE_NLS=ON \
	%{?with_libssh:-DEXIV2_ENABLE_SSH=ON} \
	-DEXIV2_ENABLE_VIDEO=ON \
%if %{with curl} || %{with libssh}
	-DEXIV2_ENABLE_WEBREADY=ON
%endif

%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README.md doc/ChangeLog doc/cmd.txt
%attr(755,root,root) %{_bindir}/exiv2
%{_mandir}/man1/exiv2.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexiv2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexiv2.so.27

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexiv2.so
%{_includedir}/exiv2
%{_pkgconfigdir}/exiv2.pc
%{_libdir}/cmake/exiv2

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/exiv2
%endif
