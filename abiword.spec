# TODO:
#    - split into subpackages (plugins)
#    - use external wv library
Summary:	AbiWord - advanced wordprocessor
Summary(pl):	AbiWord - zaawansowany procesor tekstu
Summary(pt_BR):	Processador de textos completo
Summary(zh_CN):	跨平台的字处理程序
Name:		abiword
Version:	1.0.3
Release:	1
Epoch:		1
License:	GPL
Group:		X11/Applications
Source0:	http://download.sourceforge.net/abiword/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/abiword/%{name}-plugins.tar.gz
Source2:	%{name}.desktop
Patch0:		%{name}-oldmagick.patch
Patch1:		%{name}-fonts.patch
URL:		http://www.abisource.com/
BuildRequires:	Aiksaurus-devel
BuildRequires:	ImageMagick-c++-devel
BuildRequires:	autoconf
BuildRequires:	automake >= 1.5-8
BuildRequires:	bonobo-devel
BuildRequires:	gal-devel >= 0.5
BuildRequires:	gdk-pixbuf-gnome-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-libs-devel >= 1.2.0
BuildRequires:	gnome-vfs-devel
BuildRequires:	gtk+-devel >= 1.2.7
BuildRequires:	libglade-gnome-devel
BuildRequires:	libtool
BuildRequires:	libltdl-devel
BuildRequires:	libxml-devel
BuildRequires:	pspell-devel
BuildRequires:	readline-devel
BuildRequires:	zipios++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_sysconfdir	/etc/X11/GNOME

%description
AbiWord is a free word processing program similar to Microsoft Word.
It is suitable for typing papers, letters, reports, memos, and so
forth.

%description -l pl
AbiWord jest darmowym procesorem tekstu podobnym do Microsoft Word.
Jest idealnym narz阣ziem do pisania dokument體, list體, raport體 itp.

%description -l pt_BR
AbiWord � um processador de textos de livre distribui玢o para v醨ias
plataformas, com o objetivo de ser um aplicativo leve e completo.

%prep
%setup -q -a1
%patch1 -p1
cd abiword-plugins/abiword-plugins
%patch0 -p1

%build
cd abi
./autogen.sh
%{__gettextize}
if [ -f %{_pkgconfigdir}/libpng12.pc ] ; then
        CPPFLAGS="`pkg-config libpng12 --cflags`"
fi
%configure CPPFLAGS="$CPPFLAGS" \
	--enable-gnome \
	--enable-bidi \
	--with-pspell \
	--with-libjpeg \
	--with-libxml2
%{__make} -f GNUmakefile

cd ../abiword-plugins/abiword-plugins
find . -name autogen.sh -type f -exec /bin/sh -c "echo \"libtoolize --copy --force\" >> {}" ";"
./autogen.sh; ./autogen.sh
%configure CPPFLAGS="$CPPFLAGS `%{_bindir}/gtk-config --cflags`" \
	--prefix=%{_libdir}/AbiSuite \
	--enable-gnome \
	--with-bzip2 \
	--with-ImageMagick \
	--with-abiword=$PWD/../../abi/
%{__make} -f GNUmakefile

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_applnkdir}/Office/Wordprocessors,%{_pixmapsdir}}

%{__make} -C abi -f GNUmakefile install \
	DESTDIR=$RPM_BUILD_ROOT
%{__make} -C abiword-plugins/abiword-plugins -f GNUmakefile install \
	DESTDIR=$RPM_BUILD_ROOT

ln -sf %{_libdir}/AbiSuite/AbiWord/plugins  $RPM_BUILD_ROOT%{_datadir}/AbiSuite/AbiWord/plugins
ln -sf %{_bindir}/AbiWord $RPM_BUILD_ROOT%{_bindir}/abiword

install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Office/Wordprocessors
install $RPM_BUILD_ROOT%{_datadir}/AbiSuite/icons/abiword_48.png $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc abi/docs/*.abw abi/CREDITS.TXT
%attr(755,root,root) %{_bindir}/*
%{_datadir}/AbiSuite
%dir %{_libdir}/AbiSuite
%dir %{_libdir}/AbiSuite/AbiWord
%dir %{_libdir}/AbiSuite/AbiWord/plugins
%attr(755,root,root) %{_libdir}/AbiSuite/AbiWord/plugins/*.so
%{_libdir}/AbiSuite/AbiWord/plugins/*.la
%{_applnkdir}/Office/Wordprocessors/*
%{_pixmapsdir}/*.png
