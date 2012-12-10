%define build_id3 0
%{?_with_id3: %{expand: %%global build_id3 1}}
%{?_without_id3: %{expand: %%global build_id3 0}}

Summary:	Grip, a CD player and ripper/MP3-encoder front-end
Name:		grip
Version:	3.3.1
Release:	%mkrel 15
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
Patch3:		grip-3.3.1-lame-flac-options.patch
Patch4:		grip-3.3.1-literal.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	libgnomeui2-devel
BuildRequires:	libcurl-devel
BuildRequires:	vte-devel
BuildRequires:	imagemagick
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
%patch4 -p1 -b .literal
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

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

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



%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.3.1-15mdv2011.0
+ Revision: 619255
- the mass rebuild of 2010.0 packages

* Thu Oct 08 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1:3.3.1-14mdv2010.0
+ Revision: 455850
- rebuild for new curl SSL backend

* Wed Jun 10 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1:3.3.1-13mdv2010.0
+ Revision: 384686
- rebuild for new vte

* Tue Jun 02 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1:3.3.1-12mdv2010.0
+ Revision: 382165
- rebuild for new libvte

* Thu Jan 08 2009 GÃ¶tz Waschk <waschk@mandriva.org> 1:3.3.1-11mdv2009.1
+ Revision: 327049
- disable stupid id3lib again
- always use id3v2 in lame options

* Wed Jan 07 2009 Adam Williamson <awilliamson@mandriva.org> 1:3.3.1-10mdv2009.1
+ Revision: 326760
- enable id3lib support, there's really no reason not to that I can see
- add literal.patch: fix a string literal error
- rediff lame-flac-options.patch

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 1:3.3.1-9mdv2009.0
+ Revision: 218421
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:3.3.1-9mdv2008.1
+ Revision: 178711
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Sep 21 2007 Adam Williamson <awilliamson@mandriva.org> 1:3.3.1-7mdv2008.0
+ Revision: 92088
- oops - fix icon directory creation
- rebuild for 2008
- don't package COPYING
- fd.o icons
- drop old menu, fix XDG menu (by dumping the included one and creating a new)
- new license policy
- spec clean


* Thu Nov 23 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.3.1-6mdv2007.0
+ Revision: 86771
- Import grip

* Thu Nov 23 2006 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.3.1-6mdv2007.1
- rebuild for new curl

* Tue Sep 19 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1:3.3.1-5mdv2007.0
- Rebuild

* Wed Aug 02 2006 Götz Waschk <waschk@mandriva.org> 3.3.1-4mdv2007.0
- xdg menu

* Sat Jul 08 2006 Thierry Vignaud <tvignaud@mandriva.com> 3.3.1-3mdv2007.0
- rebuild with new vte

* Thu Nov 17 2005 Thierry Vignaud <tvignaud@mandriva.com> 3.3.1-2mdk
- rebuild against openssl-0.9.8

* Mon Jun 27 2005 Götz Waschk <waschk@mandriva.org> 3.3.1-1mdk
- update source 3
- drop patch 2
- New release 3.3.1

* Wed Apr 06 2005 Götz Waschk <waschk@linux-mandrake.com> 1:3.3.0-2mdk
- fix MDKSA-2005:066 (bug #15172)

* Mon Jan 31 2005 Götz Waschk <waschk@linux-mandrake.com> 3.3.0-1mdk
- update the german translation
- new version

* Thu Jan 06 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 3.2.0-6mdk 
- Rebuild with latest howl

* Mon Nov 15 2004 Götz Waschk <waschk@linux-mandrake.com> 3.2.0-5mdk
- fix menu entry

* Sun Nov 14 2004 Götz Waschk <waschk@linux-mandrake.com> 3.2.0-4mdk
- use the official icon (thanks to Peter Adolphs)

* Thu Jul 01 2004 Götz Waschk <waschk@linux-mandrake.com> 3.2.0-3mdk
- rebuild for new curl

* Sat Jun 05 2004 <lmontel@n2.mandrakesoft.com> 3.2.0-2mdk
- Rebuild

* Wed Apr 28 2004 Goetz Waschk <waschk@linux-mandrake.com> 3.2.0-1mdk
- New release 3.2.0

* Thu Apr 22 2004 Götz Waschk <waschk@linux-mandrake.com> 3.1.10-1mdk
- fix URL
- New release 3.1.10

* Sat Apr 03 2004 Götz Waschk <waschk@linux-mandrake.com> 3.1.9-1mdk
- requires curl instead of ghttp
- drop patch 2
- rediff patches 0,3
- new version

* Mon Dec 22 2003 Götz Waschk <waschk@linux-mandrake.com> 3.1.4-1mdk
- add spec file support for id3lib
- patch3: add tagging to the default lame and flac encoder options
- patch2: fix header location of our cdparanoia libs
- new version

