%define build_id3 0
%{?_with_id3: %{expand: %%global build_id3 1}}
%{?_without_id3: %{expand: %%global build_id3 0}}

Summary:	Grip, a CD player and ripper/MP3-encoder front-end
Name:		grip
Version:	3.3.1
Release:	%mkrel 7
License:	GPLv2+
Epoch:		1
Group:		Sound
URL:		http://www.nostatic.org/grip/
Source0:	http://prdownloads.sourceforge.net/grip/%{name}-%{version}.tar.bz2
Source2:	grip.1.bz2
Source3:	grip-3.3.1-de.po.bz2
Patch0:		grip-3.1.7-ogg.patch
Patch1:		grip-3.0.5-blind-write-fix.patch
Patch2:		grip-3.3.1-desktop.patch
Patch3:		grip-3.1.9-lame-flac-options.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	libgnomeui2-devel
BuildRequires:	libcurl-devel
BuildRequires:	vte-devel
BuildRequires:	ImageMagick
Requires:	vorbis-tools
BuildRequires:	libcdda-devel
%if %build_id3
BuildRequires:	libid3-devel
%endif

%description
Grip is a GTK+-based CD player and ripper. It has the ripping
capabilities of cdparanoia built in, but can also use external rippers
(such as cdda2wav). It also provides an automated frontend for various
encoders, letting you take a disc and transform it easily straight
into Vorbis, FLAC or MP3 format (MP3 only with a separate MP3 encoder).
The CDDB protocol is supported for retrieving track information from
disc database servers. Grip works with DigitalDJ to provide a unified
"computerized" version of your music collection.

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
rm -rf %{buildroot}
%makeinstall
mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 %SOURCE2 %{buildroot}%{_mandir}/man1/ 

#mdk icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
ln -s %{_datadir}/pixmaps/gripicon.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 pixmaps/gripicon.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 pixmaps/gripicon.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

#menu - delete the included one and make our own, because the included one stinks
rm -f %{buildroot}%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Grip
Comment=CD player and ripper
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;AudioVideo;Audio;Player;
EOF

%find_lang %{name}-2.2

%clean
rm -rf %{buildroot}

%post
%{update_menus}
%{update_icon_cache hicolor}

%postun
%{clean_menus}
%{clean_icon_cache hicolor}

%files -f %{name}-2.2.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS CREDITS README ChangeLog TODO  
%{_bindir}/*
%{_datadir}/gnome/help/%{name}/
%{_datadir}/pixmaps/gripicon.png
%{_datadir}/pixmaps/griptray.png
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop

