%define api_version 1.0
%define lib_name %mklibname gnomecupsui- %{api_version} %{lib_major}
%define lib_major 1
%define libgnomecups_version 0.1.14
%define longtitle GNOME CUPS printer management tool

Summary: %{longtitle}
Name: gnome-cups-manager
Version: 0.31
Release: %mkrel 4
License: GPL
Group: Graphical desktop/GNOME
URL: http://www.ximian.com
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libgnomeui2-devel
BuildRequires: libglade2.0-devel
BuildRequires: libgnomecups-devel >= %{libgnomecups_version}
BuildRequires: perl-XML-Parser
Obsoletes: printman
Provides: printman
Requires: gnomesu

%description
GNOME Cups printer management tool

%package -n %{lib_name}
Summary: GNOME library for CUPS integration
Group: System/Libraries
Requires: %{name} = %{version}

%description -n %{lib_name}
GNOME library for CUPS integration

%package -n %{lib_name}-devel
Summary: GNOME library for CUPS integration
Group: Development/GNOME and GTK+
Requires: %{lib_name} = %{version}
Provides: libgnomecupsui-devel = %{version}-%{release}
Provides: libgnomecupsui-%{api_version}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
GNOME library for CUPS integration


%prep
%setup -q

%build

%configure2_5x

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

%find_lang %{name}

# menu entry
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):  \
  needs="X11" \
  section="System/Configuration/Printing" \
  title="GNOME Cups Manager" \
  longtitle="Printer Management Tool"  \
  command="%{_bindir}/gnome-cups-manager" \
  icon="printing_section.png"  \
  startup_notify="true" xdg="true"
EOF

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{longtitle}
Exec=%{name}
Icon=printing_section.png
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Configuration-Printing;Settings;HardwareSettings;
EOF


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig -n %{lib_name}

%postun -p /sbin/ldconfig -n %{lib_name}

%post
%{update_menus}
gtk-update-icon-cache --force --quiet %{_datadir}/icons/hicolor

%postun
%{clean_menus}
if [ "$1" = "0" ]; then
  gtk-update-icon-cache --force --quiet %{_datadir}/icons/hicolor
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README ChangeLog NEWS
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_sbindir}/*
%{_datadir}/gnome-cups-manager
%{_datadir}/icons/hicolor/48x48/devices/*
%{_datadir}/icons/hicolor/48x48/stock/data/*
%{_datadir}/pixmaps/*
%{_menudir}/*
%{_datadir}/applications/*

%files -n %{lib_name}
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*
