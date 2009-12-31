%define version 0.9.0
%define release %mkrel 1

%define enable_3d 1
%{?_without_3d: %define enable_3d 0}

Summary:	GNU Backgammon
Name:		gnubg
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	GPL
Group:		Games/Boards
URL:		http://www.gnubg.org

Source0:	http://www.gnubg.org/media/sources/%{name}/%{name}-%{version}-1.tar.gz
Patch0:		gnubg-0.9.0-strfmt.patch

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
BuildRequires:	mesaglut-devel
%endif
Buildroot:	%{_tmppath}/%{name}-%{version}

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
%patch0 -p0 -b .strfmt

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
Exec=%{_gamesbindir}/%{name} -b 
Icon=strategy_section
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Games-Boards;Game;BoardGame;
EOF

# remove unwanted files
rm -rf %{buildroot}%{_datadir}/locale/en@quot

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post

%preun


%files -f %{name}.lang
%defattr(-, root, root)
%{_gamesbindir}/*
%{_datadir}/%{name}
%{_mandir}/man6/*
%{_datadir}/applications/mandriva-%{name}.desktop


