%define version 20121022
%define release 1

%define enable_3d 1
%{?_without_3d: %define enable_3d 0}

Summary:	GNU Backgammon
Name:		gnubg
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Games/Boards
URL:		http://www.gnubg.org

Source0:	http://gnubg.org/media/sources/%{name}-source-SNAPSHOT-%{version}.tar.gz

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	readline-devel
BuildRequires:	gdbm-devel
BuildRequires:	gettext-devel
BuildRequires:	termcap-devel
BuildRequires:	gmp-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libxml2-devel
BuildRequires:	python-devel
BuildRequires:	png-devel
BuildRequires:	esound-devel

%if %enable_3d
BuildRequires:	ftgl-devel
BuildRequires:	gtkglext-devel >= 1.0
BuildRequires:	pkgconfig(glu)
%endif

%description
GNU Backgammon (gnubg) plays and analyses backgammon games and matches.
Some of its features include:

* Tournament match and money session cube handling
* Can play using graphical board (using GTK+ interface) with 2D/3D
  graphics, or command line interface
* Functions to generate legal moves and evaluate positions at
  varying search depths
* Neural  net functions for giving cubeless evaluations of all other
  contact and race positions
* Support for both 1-sided and 2-sided bearoff databases, and allows
  storing optional larger databases on disks
* Automated  rollouts of positions, with lookahead and race variance
  reduction where appropriate. Rollouts may also be extended.
* Both TD(0) and supervised training of neural net weights
* Optional position databases for supervised training
* Loading and saving .sgf games and matches, and export to various
  other formats
* Scripting ability
* Automatic and manual annotation (analysis and commentary) of games
  and matches.
* Record keeping of statistics of players in games and matches

%prep
%setup -q -n %{name}

%build
./autogen.sh
%configure2_5x \
	--with-gtk \
	--with-python \
	--bindir=%{_gamesbindir} \
%if %enable_3d
	--with-board3d \
%else
	--without-board3d \
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std bindir=%{_gamesbindir}

# XDG menu entry
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=GNU Backgammon
Comment=GNU Backgammon
Exec=%{_gamesbindir}/%{name} -b -w
Icon=strategy_section
Terminal=false
Type=Application
Categories=Game;BoardGame;
EOF

# remove unwanted files
rm -rf %{buildroot}%{_datadir}/locale/en@quot

%find_lang %{name}

%post

%preun


%files -f %{name}.lang
%defattr(-, root, root)
%{_gamesbindir}/*
%{_datadir}/%{name}
%{_mandir}/man6/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_docdir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.*



%changelog
* Sat Mar 12 2011 Funda Wang <fwang@mandriva.org> 1:0.9.0-3mdv2011.0
+ Revision: 643963
- fix desktop launcher (bug#62761)

* Wed Feb 10 2010 Funda Wang <fwang@mandriva.org> 1:0.9.0-2mdv2011.0
+ Revision: 503622
- fix version
- rebuild for new gmp

  + Sandro Cazzaniga <kharec@mandriva.org>
    - fix licence and version

* Thu Dec 31 2009 Crispin Boylan <crisb@mandriva.org> 1:0.9.0-1mdv2010.1
+ Revision: 484504
- New(er) release 0.9.0
- Clean up spec file

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sat Feb 28 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.15-5mdv2009.1
+ Revision: 346063
- builtfor latest readline
- fix some (not all) format errors
- fix linking order

  + Adam Williamson <awilliamson@mandriva.org>
    - rebuild for new ftgl major

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.15-1mdv2008.1
+ Revision: 136454
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - do not harcode icon extension
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Sun Mar 04 2007 Emmanuel Andry <eandry@mandriva.org> 0.15-1mdv2007.0
+ Revision: 132148
- buildrequires ghostscript
- drop source 1
- New version 0.15

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Fix BuildRequires
    - Use mkrel
    - Fix BuildRequires
    - Add menu entry
    - Import gnubg

* Tue Feb 08 2005 Abel Cheung <deaddog@mandrake.org> 0.14.3-4mdk
- Rebuild against new readline

* Sun Dec 26 2004 Abel Cheung <deaddog@mandrake.org> 0.14.3-3mdk
- Rebuild against new python

* Thu Dec 02 2004 Abel Cheung <deaddog@mandrake.org> 0.14.3-2mdk
- Fix BuildRequires

* Thu Nov 04 2004 Abel Cheung <deaddog@mandrake.org> 0.14.3-1mdk
- First Mandrakelinux package
- If you try to play without -b option, it will encounter
  assertion fail and quit during bearoff

