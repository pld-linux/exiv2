#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	curl		# enable webready with HTTP support via curl

Summary:	EXIF and IPTC metadata manipulation tools
Summary(pl.UTF-8):	Narzędzia do obróbki metadanych EXIF i IPTC
Name:		exiv2
Version:	0.28.1
Release:	1
License:	GPL v2+
Group:		Applications/Graphics
#Source0Download: https://exiv2.org/download.html
Source0:	https://github.com/Exiv2/exiv2/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c4d05b86bda11c15163903822d0eebfb
URL:		https://exiv2.org/
BuildRequires:	cmake >= 3.11.0
%{?with_curl:BuildRequires:	curl-devel}
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	expat-devel
BuildRequires:	gettext-tools
BuildRequires:	inih-c++-devel
BuildRequires:	libbrotli-devel
BuildRequires:	libstdc++-devel >= 6:8
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
Requires:	inih-c++-devel
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
%setup -q

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
	-DEXIV2_ENABLE_VIDEO=ON \
	%{?with_curl:-DEXIV2_ENABLE_WEBREADY=ON}

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
%attr(755,root,root) %ghost %{_libdir}/libexiv2.so.28

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexiv2.so
%{_includedir}/exiv2
%{_pkgconfigdir}/exiv2.pc
%{_datadir}/cmake/exiv2

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/exiv2
%endif
