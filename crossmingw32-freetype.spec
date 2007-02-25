#
# Conditional build:
%bcond_without	bytecode	# without TT bytecode interpreter
#		 (patents pending in USA, Japan etc., but now it includes
#		  also patent-free hinting workaround)
%bcond_without	lcd             # disable filters reducing color fringes when
#                 subpixel rendering for LCD (only used with a new 2.3.0 API;
#                 patents pending)
%define		_realname   freetype
Summary:	TrueType font rasterizer - Mingw32 cross version
Summary(es.UTF-8):Biblioteca de render 3D de fuentes TrueType
Summary(ko.UTF-8):자유롭게 어디든 쓸 수 있는 트루타입 글꼴을 다루는 엔진
Summary(pl.UTF-8):Rasteryzer fontów TrueType - wersja skrośna dla Mingw32
Summary(pt_BR.UTF-8):Biblioteca de renderização de fontes TrueType
Summary(ru.UTF-8):Растеризатор шрифтов TrueType
Summary(uk.UTF-8):Растеризатор шрифтів TrueType
Name:		crossmingw32-%{_realname}
Version:	2.3.1
Release:	1
License:	GPL or FTL
Group:		Libraries
Source0:	http://savannah.nongnu.org/download/freetype/%{_realname}-%{version}.tar.bz2
# Source0-md5:	11e1186ca5520c5a284fa0a03f652035
URL:		http://www.freetype.org/
BuildRequires:	automake
BuildRequires:	crossmingw32-zlib
BuildRequires:	python
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	-fomit-frame-pointer
# see <freetype/internal/ftserv.h>, the real horror
%define		specflags	-fno-strict-aliasing

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_aclocaldir		%{_datadir}/aclocal
%define		_pkgconfigdir		%{_libdir}/pkgconfig
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

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

%description -l es.UTF-8
FreeType es una máquina libre y portátil para en render de fuentes
TrueType. Fue desarrollada para ofrecer soporte TrueType a una gran
variedad de plataformas y ambientes. Observa que FreeType es una
biblioteca y no una aplicación, a pesar de que algunos utilitarios se
incluyan en este paquete.

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

%description -l pt_BR.UTF-8
FreeType é uma máquina livre e portável para renderização de
fontes TrueType. Ela foi desenvolvida para fornecer suporte TrueType a
uma grande variedade de plataformas e ambientes. Note que FreeType é
uma biblioteca e não uma aplicação, apesar que alguns utilitários
são incluídos neste pacote.

%description -l ru.UTF-8
Библиотека FreeType - это свободная
переносимая библиотека для
рендеринга (растеризации) шрифтов
TrueType, доступная в исходных текстах на
ANSI C и Pascal. Она была разработана для
поддержки TT на разнообразных
платформах.

%description -l uk.UTF-8
Бібліотека FreeType - це вільна переносима
бібліотека для рендерингу
(растеризації) шрифтів TrueType, що
розповсюджується у вихідних текстах
на C та Pascal. Вона була розроблена для
підтримки TT на різних платформах.

%prep
%setup -q -n %{_realname}-%{version}

%build
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig
CFLAGS="%{rpmcflags} \
%{?with_bytecode:-DTT_CONFIG_OPTION_BYTECODE_INTERPRETER} \
%{?with_lcd:-DFT_CONFIG_OPTION_SUBPIXEL_RENDERING}" \
%configure \
	LDFLAGS="-shared %{rpmldflags}" \
	--target=%{target} \
	--build=i686-pc-linux-gnu \
	--host=%{target} \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/{CHANGES,FTL.TXT,LICENSE.TXT,PATENTS,TODO,formats.txt,raster.txt}
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_bindir}/*.dll
%{_includedir}/freetype2
%{_includedir}/*.h
%{_aclocaldir}/*.m4
%{_pkgconfigdir}/*.pc
