#
# Conditional build:
%bcond_with	curl	# enable webready with HTTP support via curl
%bcond_with	libssh	# enable webready with SSH support via libssh

Summary:	EXIF and IPTC metadata manipulation tools
Summary(pl.UTF-8):	Narzędzia do obróbki metadanych EXIF i IPTC
Name:		exiv2
Version:	0.26
Release:	1
License:	GPL v2+
Group:		Applications/Graphics
#Source0Download: http://www.exiv2.org/download.html
Source0:	http://www.exiv2.org/builds/%{name}-%{version}-trunk.tar.gz
# Source0-md5:	5399e3b570d7f9205f0e76d47582da4c
Patch0:		%{name}-mkinstalldirs.patch
Patch1:		%{name}-png_support.patch
URL:		http://www.exiv2.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
%{?with_curl:BuildRequires:	curl-devel}
BuildRequires:	expat-devel
BuildRequires:	gettext-tools
%{?with_libssh:BuildRequires:	libssh-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.0
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
%setup -q -n %{name}-trunk
%patch0 -p0
%patch1 -p1

ln -s config/configure.ac .

# AX_CXX_CHECK_FLAG from old autoconf-archive, missing in acinclude or separate file
tail -n +10113 config/aclocal.m4 >> acinclude.m4

%build
%{__libtoolize} --install
%{__aclocal}
%{__autoconf}
# don't touch autoheader, config.h.in has been manually modified
%configure \
	--enable-video \
%if %{with curl} || %{with libssh}
	--enable-webready \
	%{!?with_curl:--without-curl} \
	%{!?with_libssh:--without-ssh}
%endif

%{__make} \
	CFLAGS="%{rpmcflags} -Wall" \
	CXXFLAGS="%{rpmcxxflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	incdir=%{_includedir}/exiv2 \
	libdir=%{_libdir} \
	bindir=%{_bindir} \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libexiv2.la
# let rpm autodetect dependencies
chmod 755 $RPM_BUILD_ROOT%{_libdir}/libexiv2.so*
# samples (exifprint, exiv2json) are not installed, so don't package man
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/exiv2samples.1

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/ChangeLog README
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/exiv2.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexiv2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libexiv2.so.26

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexiv2.so
%{_includedir}/%{name}
%{_pkgconfigdir}/exiv2.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libexiv2.a
