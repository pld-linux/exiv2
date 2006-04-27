Summary:	Exif and Iptc metadata manipulation tools
Summary(pl):	Narzêdzia do obróbki metadanych Exif i Iptc
Name:		exiv2
Version:	0.9.1
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://www.exiv2.org/%{name}-%{version}.tar.gz
# Source0-md5:	4c6593751368f5e9235d85e0d4058e67
URL:		http://www.exiv2.org/
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
	incdir=%{_includedir}/exiv2 \
	libdir=%{_libdir} \
	bindir=%{_bindir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/ChangeLog README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

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
