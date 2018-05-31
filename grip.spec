%define build_id3 0
%{?_with_id3: %{expand: %%global build_id3 1}}
%{?_without_id3: %{expand: %%global build_id3 0}}
%define _disable_lto 1

Summary:	A CD player and ripper/MP3-encoder front-end
Name:		grip
Version:	3.8.1
Release:	1
License:	GPLv2+
Epoch:		1
Group:		Sound
URL:		http://sourceforge.net/projects/grip
Source0:	https://sourceforge.net/projects/grip/files/%{version}/%{name}-%{version}.tar.gz
Source2:	grip.1.bz2
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	vte-devel
BuildRequires:	imagemagick
Requires:	vorbis-tools
BuildRequires:	cdda-devel
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
#apply_patches

%build
#export CC=gcc

%configure \
%if %build_id3
    --enable-id3 \
%else
    --disable-id3 \
%endif
    --enable-shared-cdpar

%make

%install
%makeinstall_std
mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man1/

#mdk icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
ln -s %{_datadir}/pixmaps/gripicon.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 pixmaps/gripicon.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 pixmaps/gripicon.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

#menu - delete the included one and make our own, because the included one stinks
rm -f %{buildroot}%{_datadir}/applications/%{name}.desktop

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
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

%find_lang %{name}

%files -f %{name}.lang
%doc ABOUT-NLS AUTHORS CREDITS README ChangeLog TODO
%{_bindir}/*
%{_datadir}/gnome/help/%{name}/
%{_datadir}/pixmaps/gripicon.png
%{_datadir}/pixmaps/griptray.png
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
