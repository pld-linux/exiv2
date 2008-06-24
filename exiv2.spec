Summary:	Exif and Iptc metadata manipulation tools
Summary(pl.UTF-8):	Narzędzia do obróbki metadanych Exif i Iptc
Name:		exiv2
Version:	0.17.1
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://www.exiv2.org/%{name}-%{version}.tar.gz
# Source0-md5:	52a602f4f0d9e89b7084ac795b7547ac
Patch0:		%{name}-mkinstalldirs.patch
URL:		http://www.exiv2.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Exif and Iptc metadata manipulation tools.

%description -l pl.UTF-8
Narzędzia do obróbki metadanych Exif i Iptc.

%package libs
Summary:	Exif and Iptc metadata manipulation library
Summary(pl.UTF-8):	Biblioteka do obróbki metadanych Exif i Iptc
Group:		Libraries

%description libs
Exif and Iptc metadata manipulation library.

%description libs -l pl.UTF-8
Biblioteka do obróbki metadanych Exif i Iptc.

%package devel
Summary:	Exif and Iptc metadata manipulation library development files
Summary(pl.UTF-8):	Pliki programistyczne biblioteki do obróbki metadanych Exif i Iptc
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	zlib-devel

%description devel
Exif and Iptc metadata manipulation library development files.

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki do obróbki metadanych Exif i Iptc.

%package static
Summary:	Exif and Iptc metadata manipulation static library
Summary(pl.UTF-8):	Statyczna biblioteka do obróbki metadanych Exif i Iptc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Exif and Iptc metadata manipulation static library.

%description static -l pl.UTF-8
Statyczna biblioteka do obróbki metadanych Exif i Iptc.

%prep
%setup -q
%patch0 -p0

ln -s config/configure.ac .

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
# don't touch autoheader, config.h.in has been manually modified
%configure

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

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/ChangeLog README
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/exiv2.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexiv2.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexiv2.so
%{_libdir}/libexiv2.la
%{_includedir}/%{name}
%{_pkgconfigdir}/exiv2.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libexiv2.a
