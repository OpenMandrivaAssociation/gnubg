%define version 0.15
%define release %mkrel 6
# can't get rid of
# renderprefs.c:672: error: format not a string literal and no format arguments
%define Werror_cflags %nil

%define enable_3d 1
%{?_without_3d: %define enable_3d 0}

Summary:	GNU Backgammon
Name:		gnubg
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Boards
URL:		http://www.gnu.org/software/gnubg/

Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
#Source1:	%{SOURCE0}.sig
Source2:	ftp://ftp.gnu.org/gnu/%{name}/gnubg.weights-0.14.gz
Source3:	%{SOURCE2}.sig
Source4:	ftp://ftp.gnu.org/gnu/%{name}/gnubg_os0.bd.gz
Source5:	%{SOURCE4}.sig
Source6:	ftp://ftp.gnu.org/gnu/%{name}/gnubg_ts0.bd.gz
Source7:	%{SOURCE6}.sig
Source8:	gnubg-textures.txt.bz2
Patch0:     gnubg-0.15-fix-format-errors.patch
Patch1:     gnubg-0.15-fix-linking-order.patch

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	gnuplot
BuildRequires:	netpbm
BuildRequires:	readline-devel
BuildRequires:	gdbm-devel
BuildRequires:	gettext-devel
BuildRequires:	termcap-devel
BuildRequires:	gmp-devel
BuildRequires:	gtk+2-devel
BuildRequires:	guile-devel
BuildRequires:	libxml2-devel
BuildRequires:	python-devel
BuildRequires:	arts-devel
BuildRequires:	esound-devel
BuildRequires:	audiofile-devel
BuildRequires:	nas-devel
BuildRequires:	png-devel
BuildRequires:	gettext-devel
BuildRequires:	ghostscript

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
%patch0 -p 1
%patch1 -p 1

# (Abel) Let it be. Adding proper detection of nas library is tedious
perl -pi -e 's#-laudio#-L/usr/X11R6/%{_lib} -laudio#' configure.in
#ACLOCAL=aclocal-1.9 AUTOMAKE=automake-1.9 autoreconf -I m4

gzip -dc %{SOURCE2} > gnubg.weights
gzip -dc %{SOURCE4} > gnubg_ts0.bd
gzip -dc %{SOURCE6} > gnubg_os0.bd
bzip2 -dc %{SOURCE8} > textures.txt

%build
./autogen.sh
%configure2_5x \
	--with-readline \
	--with-gtk2 \
	--with-python \
	--with-sound \
	--with-timecontrol \
	--enable-nas \
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
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%files -f %{name}.lang
%defattr(-, root, root)
%{_gamesbindir}/*
%{_datadir}/%{name}
%{_infodir}/*
%{_mandir}/man6/*
%{_datadir}/applications/mandriva-%{name}.desktop


