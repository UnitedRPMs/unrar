#
# spec file for package unrar
#
# Copyright (c) 2020 UnitedRPMs.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://goo.gl/zqFJft
#

%define _legacy_common_support 1

%undefine _debugsource_packages


Name:           unrar
Version:        5.9.3
Release:        7%{?dist}
Summary:        Utility for extracting, testing and viewing RAR archives
License:        Freeware with further limitations
Group:          Applications/Archiving
URL:            http://www.rarlab.com/rar_add.htm
Source0:        http://www.rarlab.com/rar/unrarsrc-%{version}.tar.gz
# Man page from Debian
Source1:        unrar-nonfree.1
Source2:	com.rarlab.unrar.metainfo.xml

BuildRequires:  gcc-c++
Requires(post): chkconfig
Requires(preun): chkconfig


%description
The unrar utility is a freeware program for extracting, testing and
viewing the contents of archives created with the RAR archiver version
1.50 and above.


%package -n libunrar
Summary:        Decompress library for RAR v3 archives
Group:          System Environment/Libraries

# Packages using libunrar must Requires this:
#{?unrar_version:Requires: libunrar%%{_isa} = %%{unrar_version}}

%description -n libunrar
The libunrar library allows programs linking against it to decompress
existing RAR v3 archives.


%package -n libunrar-devel
Summary:        Development files for libunrar
Group:          Development/Libraries
Requires:       libunrar%{_isa} = %{version}-%{release}
Provides:       libunrar3-%{version}

%description -n libunrar-devel
The libunrar-devel package contains libraries and header files for
developing applications that use libunrar.


%prep
%setup -q -n %{name}
cp -p %SOURCE1 .
  sed -e '/CXXFLAGS=/d' -e '/LDFLAGS=/d' -i makefile 


%build

  cp -rf %{_builddir}/unrar %{_builddir}/libunrar
  export LDFLAGS+=' -pthread'
  make -C %{_builddir}/libunrar lib
  make -j1


%install
rm -rf %{buildroot}
install -Dpm 755 unrar %{buildroot}%{_bindir}/unrar-nonfree
install -Dpm 644 unrar-nonfree.1 %{buildroot}%{_mandir}/man1/unrar-nonfree.1
install -Dpm 755 %{_builddir}/libunrar/libunrar.so %{buildroot}%{_libdir}/libunrar.so
mkdir -p -m 755 %{buildroot}/%{_includedir}/unrar
for i in *.hpp; do
    install -Dpm 644 $i %{buildroot}/%{_includedir}/unrar
done

# handle alternatives
touch %{buildroot}%{_bindir}/unrar

# RPM Macros support
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat > %{buildroot}%{_sysconfdir}/rpm/macros.unrar << EOF
# unrar RPM Macros
%unrar_version    %{version}
EOF
touch -r license.txt %{buildroot}%{_sysconfdir}/rpm/macros.unrar

# Install AppData
  install -Dm 0644 %{S:2} %{buildroot}/%{_metainfodir}/com.rarlab.unrar.metainfo.xml


%post
%{_sbindir}/alternatives \
    --install %{_bindir}/unrar unrar %{_bindir}/unrar-nonfree 50 \
    --slave %{_mandir}/man1/unrar.1.gz unrar.1.gz \
    %{_mandir}/man1/unrar-nonfree.1.gz || :

%preun
if [ "$1" -eq 0 ]; then
  %{_sbindir}/alternatives \
      --remove unrar %{_bindir}/unrar-nonfree || :
fi

%post -n libunrar -p /sbin/ldconfig


%postun -n libunrar -p /sbin/ldconfig


%files
%doc readme.txt
%license license.txt
%ghost %{_bindir}/unrar
%{_bindir}/unrar-nonfree
%{_mandir}/man1/unrar-nonfree.1*
%{_metainfodir}/com.rarlab.unrar.metainfo.xml

%files -n libunrar
%doc readme.txt
%license license.txt
%{_libdir}/*.so

%files -n libunrar-devel
%doc readme.txt
%license license.txt
%config %{_sysconfdir}/rpm/macros.unrar
%{_includedir}/*


%changelog

* Mon Jun 08 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.9.3-7
- Updated to 5.9.3

* Tue Mar 31 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.9.2-7
- Updated to 5.9.2

* Fri Jan 31 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.9.1-7
- Updated to 5.9.1

* Fri Dec 13 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.8.5-7
- Updated to 5.8.5

* Mon Nov 25 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.8.4-7
- Updated to 5.8.4

* Mon Oct 21 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.8.3-7
- Updated to 5.8.3

* Fri Oct 04 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.8.2-7
- Updated to 5.8.2

* Fri Aug 30 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.8.1-7
- Updated to 5.8.1

* Sat May 11 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.7.5-7
- Updated to 5.7.5

* Sat Apr 06 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.7.4-7
- Updated to 5.7.4

* Fri Mar 01 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.7.3-2
- Updated to 5.7.3

* Fri Feb 22 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.7.2-2
- Updated to 5.7.2

* Tue Jan 29 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.7.1-2
- Updated to 5.7.1

* Thu Oct 04 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.6.8-2
- Updated to 5.6.8

* Mon Oct 01 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.6.7-2
- Updated to 5.6.7

* Fri Sep 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.6.6-2
- Updated to 5.6.6

* Tue Jun 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.6.5-2
- Updated to 5.6.5

* Mon May 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.6.4-2
- Updated to 5.6.4

* Mon Apr 23 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.6.3-2
- Updated to 5.6.3

* Sun Apr 01 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.6.2-2
- Updated to 5.6.2

* Sun Mar 11 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.6.1-2
- Updated to 5.6.1-2

* Tue Sep 26 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.5.8-2
- Updated to 5.5.8-2

* Sat Jun 24 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 5.5.5-2
- Updated to 5.5.5-2

* Sat Aug 27 2016 Pavlo Rudyi <paulcarroty at riseup.net> - 5.4.5-1
- Update to 5.4.5
- Import RF improvements

* Sat Dec 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 5.2.3-1
- Update to 5.2.3

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 5.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Dec 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 5.0.12-2
- Add isa dependency

* Fri Nov 8 2013 Conrad Meyer <cemeyer@uw.edu> - 5.0.12-1
- Bump to latest upstream
- Drop patch that doesn't apply anymore
- Makefile changed names

* Mon Oct 28 2013 Conrad Meyer <konrad@tylerc.org> - 4.2.4-4
- Remove unrar-4.2.3-fix-build.patch, add clean step to %%build
  per #2869

* Sun Dec 30 2012 Conrad Meyer <konrad@tylerc.org> - 4.2.4-3
- Try at #2357 again :). Instead of arbitrary date, use rpm %%version

* Sun Dec 30 2012 Conrad Meyer <konrad@tylerc.org> - 4.2.4-2
- Add RPM dependency check to ensure dependent packages break at install time
  rather than use time (#2357) (derived from live555 package)

* Sun Dec 30 2012 Conrad Meyer <konrad@tylerc.org> - 4.2.4-1
- Bump version (#2508)
- Fix unrar-4.2.3-fix-build.patch diff to have context

* Mon May 28 2012 Marcos Mello <marcosfrm AT gmail DOT com> - 4.2.3-1
- New version
- Include all header files in the -devel package (#1988)

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 4.0.7-3
- Rebuilt for c++ ABI breakage

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 4.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jul 9 2011 Conrad Meyer <konrad@tylerc.org> - 4.0.7-1
- Bump to new version.

* Tue Sep 28 2010 Conrad Meyer <konrad@tylerc.org> - 3.9.10-3
- Patch to fix unresolved symbol issues (#1385).

* Thu Sep 2 2010 Conrad Meyer <konrad@tylerc.org> - 3.9.10-1
- Bump to 3.9.10.

* Sun Feb 21 2010 Conrad Meyer <konrad@tylerc.org> - 3.9.9-1
- Bump to 3.9.9.

* Sun Dec 6 2009 Conrad Meyer <konrad@tylerc.org> - 3.8.5-5
- Fix post to use alternatives to manage unrar manpage as well.

* Mon Nov 30 2009 Conrad Meyer <konrad@tylerc.org> - 3.8.5-4
- Fix preun to refer to the correct alternatives files.

* Fri Nov 20 2009 Conrad Meyer <konrad@tylerc.org> - 3.8.5-3
- Add missing post/preun requires on chkconfig (#956).

* Fri Jul 17 2009 Conrad Meyer <konrad@tylerc.org> - 3.8.5-2
- Fix breakages introduced by dropping the versioned SONAME patch.

* Wed Jul 8 2009 Conrad Meyer <konrad@tylerc.org> - 3.8.5-1
- Bump to 3.8.5.

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.7.8-4
- rebuild for new F11 features

* Sat Oct 25 2008 Andreas Thienemann <andreas@bawue.net> - 3.7.8-3
- Added libunrar sub-packages
- Clarified license
- Added unrar robustness patches

* Thu Jul 24 2008 Conrad Meyer <konrad@tylerc.org> - 3.7.8-2
- Import into RPM Fusion.

* Sat Oct 13 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.8-1
- 3.7.8.

* Sat Sep  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.7-1
- 3.7.7, fixes CVE-2007-3726.

* Wed Aug 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.6-2
- Rebuild.

* Sun Jul  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.6-1
- 3.7.6.

* Fri May 18 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.5-1
- 3.7.5.

* Sat Mar 10 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.4-1
- 3.7.4.

* Wed Feb 14 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.3-1
- 3.7.3.

* Wed Jan 17 2007 Ville Skyttä <ville.skytta at iki.fi> - 3.7.2-1
- 3.7.2.

* Wed Sep 13 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.6.8-1
- 3.6.8.

* Wed Jul 12 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.6.6-1
- 3.6.6.

* Wed May 31 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.6.4-1
- 3.6.4.

* Sat May 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 3.6.3-1
- 3.6.3.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Tue Oct 11 2005 Ville Skyttä <ville.skytta at iki.fi> - 3.5.4-0.lvn.1
- 3.5.4.
- Drop zero Epoch.

* Wed Aug 10 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:3.5.3-0.lvn.1
- 3.5.3.

* Thu May 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:3.5.2-0.lvn.1
- 3.5.2.

* Thu Mar 31 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:3.5.1-0.lvn.1
- 3.5.1.

* Wed Nov 24 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.4.3-0.lvn.1
- Update to 3.4.3.

* Sun Sep  5 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.4.2-0.lvn.1
- Update to 3.4.2, nostrip patch no longer necessary.
- Update Debian patch URL.

* Sat Jul  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.4.1-0.lvn.1
- Update to 3.4.1 and Debian patch to 3.3.6-2.

* Thu May 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.6-0.lvn.2
- Update Debian patch to 3.3.6-1 (no real changes, just a working URL again).

* Sun Feb  8 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.6-0.lvn.1
- Update to 3.3.6.

* Mon Jan 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.4-0.lvn.1
- Update to 3.3.4.

* Sat Dec 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.3-0.lvn.1
- Update to 3.3.3.

* Sun Dec 21 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.2-0.lvn.1
- Update to 3.3.2.

* Wed Nov 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.3.1-0.lvn.1
- Update to 3.3.1.

* Sun Sep 14 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.2.3-0.fdr.1
- Update to 3.2.3.
- Sync with current Fedora spec template.

* Wed Apr 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.2.1-0.fdr.1
- Update to 3.2.1.

* Sat Apr  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:3.2.0-0.fdr.1
- Update to 3.2.0 and current Fedora guidelines.

* Sun Feb  9 2003 Ville Skyttä <ville.skytta at iki.fi> - 3.1.3-1.fedora.1
- First Fedora release, based on Matthias Saou's and PLD work.
