%define api_version 1.0
%define lib_name %mklibname gnomecupsui- %{api_version} %{lib_major}
%define develname %mklibname -d gnomecupsui- %{api_version}
%define lib_major 1
%define libgnomecups_version 0.1.14
%define longtitle GNOME CUPS printer management tool

Summary: %{longtitle}
Name: gnome-cups-manager
Version: 0.33
Release: %mkrel 2
License: GPLv2+
Group: Graphical desktop/GNOME
URL: http://www.ximian.com
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
Patch1: 20_change-su-command.patch
Patch2: 23_options.patch
Patch3: 24_printer_properties_name_entry.patch
Patch4: 25_properties_on_add.patch
Patch5: 26_remove-no-cups-dialog.diff
Patch6: 27_dont-request-additional-attributes.patch
Patch8: 35_show_more_info_of_detected_printers.patch
Patch9: 37_transparent_notification_icon.patch
Patch10: 40_better_menu_text_for_tcp_socket_jetdirect_printers.patch
Patch11: 45_printer_driver_entry_cleanup.patch
Patch13: desktop-potfiles.patch
Patch17: ui_browse_share_ctl.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libgnomeui2-devel
BuildRequires: libglade2.0-devel
BuildRequires: libgnomecups-devel >= %{libgnomecups_version}
BuildRequires: perl-XML-Parser
Obsoletes: printman
Provides: printman
Requires: gksu

%description
GNOME Cups printer management tool

%package -n %{lib_name}
Summary: GNOME library for CUPS integration
Group: System/Libraries
Requires: %{name} = %{version}

%description -n %{lib_name}
GNOME library for CUPS integration

%package -n %develname
Summary: GNOME library for CUPS integration
Group: Development/GNOME and GTK+
Requires: %{lib_name} = %{version}
Provides: libgnomecupsui-devel = %{version}-%{release}
Provides: libgnomecupsui-%{api_version}-devel = %{version}-%{release}
Obsoletes: %mklibname -d gnomecupsui- %{api_version} %{lib_major}

%description -n %develname
GNOME library for CUPS integration


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p0
%patch5 -p0
%patch6 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1 -b .cleanup
%patch13 -p1
%patch17 -p1

%build

%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -p /sbin/ldconfig -n %{lib_name}
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig -n %{lib_name}
%endif

%if %mdkversion < 200900
%post
%{update_menus}
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%clean_icon_cache hicolor
%endif

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
%{_datadir}/applications/*

%files -n %{lib_name}
%defattr(-,root,root,-)
%{_libdir}/libgnomecupsui-%{api_version}.so.%{lib_major}*

%files -n %develname
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*
