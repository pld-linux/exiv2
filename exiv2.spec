#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests
#
Summary:	Exif and Iptc metadata manipulation tools
Name:		exiv2
Version:	0.7
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://home.arcor.de/ahuggel/exiv2/%{name}-%{version}.tar.gz
# Source0-md5:	540e720b77c05ca50d5005a140e38138
URL:		http://home.arcor.de/ahuggel/exiv2/
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Exif and Iptc metadata manipulation library and tools.

%package libs
Summary:	Exif and Iptc metadata manipulation library
Group:		Libraries

%description libs
Exif and Iptc metadata manipulation library.

%package devel
Summary:	Exif and Iptc metadata manipulation library development files
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description devel
Exif and Iptc metadata manipulation library development files.

%package static
Summary:	Exif and Iptc metadata manipulation static library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Exif and Iptc metadata manipulation static library.

%prep
%setup -q

%build
%configure
%{__make}

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
%attr(755,root,root) %{_libdir}/*so

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
%{_libdir}/*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
