%define build_id3 0
%{?_with_id3: %{expand: %%global build_id3 1}}
%{?_without_id3: %{expand: %%global build_id3 0}}

Summary: Grip, a CD player and ripper/MP3-encoder front-end
Name:	 grip
Version: 3.3.1
Release: %mkrel 6
License: GPL
Epoch:   1
Group: Sound
URL: http://www.nostatic.org/grip/
Source0: http://prdownloads.sourceforge.net/grip/%name-%version.tar.bz2
Source2: grip.1.bz2
Source3: grip-3.3.1-de.po.bz2
Patch0: grip-3.1.7-ogg.patch
Patch1: grip-3.0.5-blind-write-fix.patch
Patch2: grip-3.3.1-desktop.patch
Patch3: grip-3.1.9-lame-flac-options.patch
Buildroot: %_tmppath/%name-%version-%release-root
BuildRequires: libgnomeui2-devel
BuildRequires: libcurl-devel
BuildRequires: vte-devel
BuildRequires: ImageMagick
Requires: vorbis-tools
%ifarch %ix86
BuildRequires: libcdda-devel
%endif
%if %build_id3
BuildRequires: libid3-devel
%endif

%description
Grip is a gtk-based cd-player and cd-ripper. It has the ripping capabilities
of cdparanoia builtin, but can also use external rippers (such as
cdda2wav). It also provides an automated frontend for MP3 encoders, letting
you take a disc and transform it easily straight into MP3s. The CDDB
protocol is supported for retrieving track information from disc database
servers. Grip works with DigitalDJ to provide a unified "computerized"
version of your music collection.

%prep

%setup -q
%patch0 -p1 -b .tv
%patch1 -p1 -b .blind-write-fix
%patch2 -p1 -b .desktop
%patch3 -p1 -b .options
bzcat %SOURCE3 > po/de.po

%build
%configure2_5x \
%if %build_id3
  --enable-id3 \
%else
  --disable-id3 \
%endif
%ifarch alpha ppc
  --disable-cdpar
%endif

%make

%install
rm -rf %buildroot
%makeinstall
mkdir -p $RPM_BUILD_ROOT%_mandir/man1
install -m 644 %SOURCE2 $RPM_BUILD_ROOT%_mandir/man1/ 

#mdk menu entry
mkdir -p $RPM_BUILD_ROOT/%_menudir
cat > $RPM_BUILD_ROOT%_menudir/%name <<EOF
?package(%name):\
command="%_bindir/%name" icon="%name.png" title="Grip"\
longtitle="A gtk-based cd-player and cd-ripper"\
needs="x11"	section="Multimedia/Sound" xdg="true"
EOF

#mdk icons
install -d %buildroot{%_liconsdir,%_miconsdir}
ln -s %_datadir/pixmaps/gripicon.png %buildroot%_liconsdir/%name.png
convert -scale 32 pixmaps/gripicon.png %buildroot%_iconsdir/%name.png
convert -scale 16 pixmaps/gripicon.png %buildroot%_miconsdir/%name.png

%find_lang %name-2.2

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

%postun
%clean_menus

%files -f %name-2.2.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS COPYING CREDITS README ChangeLog TODO  
%_bindir/*
%_datadir/gnome/help/%name/
%_datadir/pixmaps/gripicon.png
%_datadir/pixmaps/griptray.png
%_iconsdir/%name.png
%_liconsdir/%name.png
%_miconsdir/%name.png
%_mandir/man1/*
%_menudir/%name
%_datadir/applications/%name.desktop


