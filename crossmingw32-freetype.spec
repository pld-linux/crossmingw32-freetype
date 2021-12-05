#
# Conditional build:
%bcond_without	lcd		# without LCD subpixel color filtering (Microsoft patents in USA)
%bcond_without	harfbuzz	# harfbuzz based autohinting
#
%define		realname   freetype
Summary:	TrueType font rasterizer - MinGW32 cross version
Summary(pl.UTF-8):	Rasteryzer fontów TrueType - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	2.11.1
Release:	1
License:	GPL v2 or FTL
Group:		Development/Libraries
Source0:	https://download.savannah.gnu.org/releases/freetype/%{realname}-%{version}.tar.xz
# Source0-md5:	24e79233d607ded439ef36ff1f3ab68f
URL:		https://freetype.org/
BuildRequires:	crossmingw32-bzip2
BuildRequires:	crossmingw32-gcc
%{?with_harfbuzz:BuildRequires:	crossmingw32-harfbuzz >= 2.0.0}
BuildRequires:	crossmingw32-libpng
BuildRequires:	crossmingw32-zlib >= 1.2.3-2
BuildRequires:	pkgconfig >= 1:0.24
BuildRequires:	python
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-bzip2
%{?with_harfbuzz:Requires:	crossmingw32-harfbuzz >= 2.0.0}
Requires:	crossmingw32-libpng
Requires:	crossmingw32-zlib >= 1.2.3-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	-fomit-frame-pointer
# see <freetype/internal/ftserv.h>, the real horror
%define		specflags	-fno-strict-aliasing

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
The FreeType engine is a free and portable TrueType font rendering
engine. It has been developed to provide TrueType support to a great
variety of platforms and environments.

Note that FreeType is a *library*. It is not a font server for your
favorite platform, even though it was designed to be used in many of
them. Note also that it is *not* a complete text-rendering library.
Its purpose is simply to open and manage font files, as well as load,
hint and render individual glyphs efficiently. You can also see it as
a "TrueType driver" for a higher-level library, though rendering text
with it is extremely easy, as demo-ed by the test programs.

This package contains the cross version for Win32.

%description -l pl.UTF-8
FreeType jest biblioteką służącą do rasteryzacji fontów
TrueType. Jest to jedynie biblioteka, a nie serwer fontów, chociaż
została ona zaprojektowana do używania także w takich serwerach.
Nie jest to też kompletna biblioteka do rasteryzacji tekstu. Jej
celem jest tylko odczytywanie i zarządzanie plikami z fontami oraz
wczytywanie i wykonywanie hintingu i rasteryzacji poszczególnych
glifów. Może być także uważana za "sterownik TrueType" dla
bibliotek wyższego poziomu, jednak użycie samej biblioteki FreeType
do rasteryzacji jest bardzo proste, co można zobaczyć w programach
demonstracyjnych.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static freetype library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka freetype (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static freetype library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka freetype (wersja skrośna MinGW32).

%package dll
Summary:	DLL freetype library for Windows
Summary(pl.UTF-8):	Biblioteka DLL freetype dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-bzip2-dll
%{?with_harfbuzz:Requires:	crossmingw32-harfbuzz-dll >= 2.0.0}
Requires:	crossmingw32-libpng-dll
Requires:	crossmingw32-zlib-dll
Requires:	wine

%description dll
DLL freetype library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL freetype dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
export PKG_CONFIG_LIBDIR=%{_pkgconfigdir}
CFLAGS="%{rpmcflags} \
%{?with_lcd:-DFT_CONFIG_OPTION_SUBPIXEL_RENDERING} \
-DTT_CONFIG_OPTION_SUBPIXEL_HINTING \
" \
%configure \
	LIBPNG_CFLAGS="$(pkg-config --cflags libpng)" \
	LIBPNG_LDFLAGS="$(pkg-config --libs libpng)" \
	--target=%{target} \
	--build=i686-pc-linux-gnu \
	--host=%{target} \
	--enable-shared \
	%{!?with_harfbuzz:--without-harfbuzz}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/aclocal

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.TXT docs/{CHANGES,FTL.TXT,TODO,formats.txt,raster.txt}
%{_libdir}/libfreetype.dll.a
%{_libdir}/libfreetype.la
%{_includedir}/freetype2
%{_pkgconfigdir}/freetype2.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libfreetype.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libfreetype-*.dll
