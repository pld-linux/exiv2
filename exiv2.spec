Summary:	Exif and Iptc metadata manipulation tools
Summary(pl):	Narzêdzia do obróbki metadanych Exif i Iptc
Name:		exiv2
Version:	0.7
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://home.arcor.de/ahuggel/exiv2/%{name}-%{version}.tar.gz
# Source0-md5:	540e720b77c05ca50d5005a140e38138
URL:		http://home.arcor.de/ahuggel/exiv2/
BuildRequires:	libstdc++-devel
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Exif and Iptc metadata manipulation tools.

%description -l pl
Narzêdzia do obróbki metadanych Exif i Iptc.

%package libs
Summary:	Exif and Iptc metadata manipulation library
Summary(pl):	Biblioteka do obróbki metadanych Exif i Iptc
Group:		Libraries

%description libs
Exif and Iptc metadata manipulation library.

%description libs -l pl
Biblioteka do obróbki metadanych Exif i Iptc.

%package devel
Summary:	Exif and Iptc metadata manipulation library development files
Summary(pl):	Pliki programistyczne biblioteki do obróbki metadanych Exif i Iptc
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Exif and Iptc metadata manipulation library development files.

%description devel -l pl
Pliki programistyczne biblioteki do obróbki metadanych Exif i Iptc.

%package static
Summary:	Exif and Iptc metadata manipulation static library
Summary(pl):	Statyczna biblioteka do obróbki metadanych Exif i Iptc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Exif and Iptc metadata manipulation static library.

%description static -l pl
Statyczna biblioteka do obróbki metadanych Exif i Iptc.

%prep
%setup -q

%build
%configure
%{__make} \
	CFLAGS="%{rpmcflags} -Wall" \
	CXXFLAGS="%{rpmcxxflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	incdir=$RPM_BUILD_ROOT%{_includedir}/exiv2 \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/ChangeLog README
%attr(755,root,root) %{_bindir}/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexiv2-*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libexiv2.so
%{_libdir}/libexiv2.la
%{_includedir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/libexiv2.a
