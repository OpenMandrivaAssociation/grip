%define build_id3 1
%{?_with_id3: %{expand: %%global build_id3 1}}
%{?_without_id3: %{expand: %%global build_id3 0}}
%define _disable_lto 1

Summary:	A CD player and ripper/MP3-encoder front-end
Name:		grip
Version:	4.2.4
Release:	2
License:	GPLv2+
Epoch:		1
Group:		Sound
URL:		https://sourceforge.net/projects/grip/
Source0:	https://sourceforge.net/projects/grip/files/%{version}/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:  curl
BuildRequires:	imagemagick
Requires:	vorbis-tools
BuildRequires:	cdda-devel
%if %build_id3
BuildRequires:	id3lib-devel
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

%build

%configure \
    --disable-werror \
%if %build_id3
    --enable-id3 \
%else
    --disable-id3 \
%endif
    --enable-shared-cdpar

%make_build

%install
%make_install

#mdk icons
#mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
#ln -s %{_datadir}/pixmaps/gripicon.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
#convert -scale 32 pixmaps/gripicon.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
#convert -scale 16 pixmaps/gripicon.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%find_lang %{name}

%files -f %{name}.lang
%doc ABOUT-NLS AUTHORS CREDITS README ChangeLog TODO
%{_bindir}/*
%{_datadir}/gnome/help/%{name}/
#{_datadir}/pixmaps/gripicon.png
%{_datadir}/pixmaps/griptray.png
%{_datadir}/pixmaps/grip.png
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_mandir}/man1/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/apps/solid/actions/%{name}-audiocd.desktop
%{_datadir}/solid/actions/grip-audiocd.desktop
