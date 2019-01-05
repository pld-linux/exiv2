#
# Conditional build:
%bcond_with	curl		# enable webready with HTTP support via curl
%bcond_with	libssh		# enable webready with SSH support via libssh
%bcond_without	static_libs	# static library

Summary:	EXIF and IPTC metadata manipulation tools
Summary(pl.UTF-8):	Narzędzia do obróbki metadanych EXIF i IPTC
Name:		exiv2
Version:	0.27.0a
Release:	1
License:	GPL v2+
Group:		Applications/Graphics
#Source0Download: http://www.exiv2.org/download.html
Source0:	http://www.exiv2.org/builds/%{name}-%{version}-Source.tar.gz
# Source0-md5:	b7f49949deafa96a9e6a22d42bd91031
URL:		http://www.exiv2.org/
BuildRequires:	cmake >= 3.3.2
%{?with_curl:BuildRequires:	curl-devel}
BuildRequires:	expat-devel
BuildRequires:	gettext-tools
%{?with_libssh:BuildRequires:	libssh-devel}
BuildRequires:	libstdc++-devel
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

%description devel
EXIF and IPTC metadata manipulation library development files.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki do obróbki metadanych EXIF i IPTC.

%package static
Summary:	EXIF and IPTC metadata manipulation static library
Summary(pl.UTF-8):	Statyczna biblioteka do obróbki metadanych EXIF i IPTC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
EXIF and IPTC metadata manipulation static library.

%description static -l pl.UTF-8
Statyczna biblioteka do obróbki metadanych EXIF i IPTC.

%prep
%setup -q -n %{name}-0.27.0-Source

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF \
	-DEXIV2_BUILD_PO=ON \
	-DEXIV2_BUILD_SAMPLES=OFF \
	%{?with_curl:-DEXIV2_ENABLE_CURL=ON} \
	%{?with_libssh:-DEXIV2_ENABLE_SSH=ON} \
	-DEXIV2_ENABLE_VIDEO=ON \
%if %{with curl} || %{with libssh}
	-DEXIV2_ENABLE_WEBREADY=ON
%endif

%{__make}
cd ..
%endif

install -d build
cd build
%cmake .. \
	-DEXIV2_BUILD_PO=ON \
	-DEXIV2_BUILD_SAMPLES=OFF \
	%{?with_curl:-DEXIV2_ENABLE_CURL=ON} \
	%{?with_libssh:-DEXIV2_ENABLE_SSH=ON} \
	-DEXIV2_ENABLE_VIDEO=ON \
%if %{with curl} || %{with libssh}
	-DEXIV2_ENABLE_WEBREADY=ON
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# internally used Adobe XMP SDK
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libxmp.a

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
%dir %{_datadir}/exiv2
%{_datadir}/exiv2/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libexiv2.a
%endif
