%define _silcdatadir %{_datadir}/silc
%define _silcetcdir %{_sysconfdir}/silc

Summary:	Client for the secure Internet Live Conferencing (SILC) protocol
Name:		silc-client
Version:	1.1.8
Release:	5
License:	GPLv2+
Group:		Networking/Chat
URL:		https://www.silcnet.org/
Source0:	http://www.silcnet.org/download/client/sources/%{name}-%{version}.tar.gz
BuildRequires:	nasm
BuildRequires:	ncurses-devel
BuildRequires:	perl-devel
BuildRequires:	glib2-devel
BuildRequires:	gmp-devel
BuildRequires:	automake
BuildRequires:	silc-toolkit-devel >= 1.1.9
Conflicts:	irssi
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as IRC.
Other than that they are nothing alike.  Major differences are that SILC
is secure what IRC is not in any way.  The network model is also entirely
different compared to IRC.

%package -n perl-silc
Group:		Development/Perl
Summary:	Perl part of the SILC client

%description -n perl-silc
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as IRC.
Other than that they are nothing alike.  Major differences are that SILC
is secure what IRC is not in any way.  The network model is also entirely
different compared to IRC.

This contains the perl modules that come with SILC.

%prep
%setup -q
sed -i -e "s:-g -O2:${optflags}:g" configure
%ifarch x86_64
sed -i -e 's:felf\([^6]\):felf64\1:g' configure
%endif

%build
%configure2_5x \
	--with-etcdir=%{_silcetcdir} \
	--with-helpdir=%{_silcdatadir}/help \
	--with-logsdir=%{_var}/log/silc \
	--mandir=%{_mandir} \
	--enable-ipv6 \
	--with-silcd-pid-file=%{_var}/run/silcd.pid \
	--disable-shared \
	--enable-static \
	--with-perl=yes \
	--with-perl-lib=vendor \
	--with-gmp=%{_prefix} \
	--with-glib2 \
	--without-libtoolfix

make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc %{_datadir}/doc/%{name}
%config(noreplace) %{_sysconfdir}/silc.conf
%{_bindir}/silc
%{_datadir}/silc
%{_mandir}/man?/*

%files -n perl-silc
%{perl_vendorarch}/Irssi.pm
%{perl_vendorarch}/Irssi/
%{perl_vendorarch}/auto/Irssi


%changelog
* Wed Jan 25 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.1.8-4
+ Revision: 768358
- svn commit -m mass rebuild of perl extension against perl 5.14.2

* Sat Jul 24 2010 Jérôme Quelin <jquelin@mandriva.org> 1.1.8-3mdv2011.0
+ Revision: 558112
- perl 5.12 rebuild

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 1.1.8-2mdv2010.0
+ Revision: 445108
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - 1.1.8

* Sun Jan 11 2009 Funda Wang <fwang@mandriva.org> 1.1.7-1mdv2009.1
+ Revision: 328295
- bump BR
- New version 1.1.7

* Sun Oct 26 2008 Funda Wang <fwang@mandriva.org> 1.1.6-1mdv2009.1
+ Revision: 297322
- New version 1.1.6

* Sun Sep 07 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.5-1mdv2009.0
+ Revision: 282182
- update to new version 1.1.5

* Sun Jun 08 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.4-1mdv2009.0
+ Revision: 216771
- update to new version 1.1.4
- add buildrequires on nasm
- spec file clean

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag

* Mon Jan 21 2008 Thierry Vignaud <tv@mandriva.org> 1.1.3-2mdv2008.1
+ Revision: 155660
- rebuild for new perl
- kill re-definition of %%buildroot on Pixel's request

* Wed Nov 21 2007 Funda Wang <fwang@mandriva.org> 1.1.3-1mdv2008.1
+ Revision: 110863
- fix group
- BR silc-toolkit-devel
- New version 1.1.3
- add gentoo patch to have it build on x86_64
- clean up file list
- perl module is provided by silc-client now
- New version


* Fri Jul 07 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 2006-07-07 23:08:14 (38507)
- rebuild

* Fri Jul 07 2006 Olivier Thauvin <nanardon@mandriva.org>
+ 2006-07-07 22:49:37 (38506)
- import silc-client

* Tue Apr 19 2005 Tibor Pittich <Tibor.Pittich@mandriva.org> 1.0.2-1mdk
- 1.0.2

* Sun Nov 21 2004 Abel Cheung <deaddog@mandrake.org> 1.0.1-6mdk
- Fix BuildRequires

* Mon Nov 15 2004 Michael Scherer <misc@mandrake.org> 1.0.1-5mdk
- Rebuild for new perl

* Wed Oct 27 2004 Abel Cheung <deaddog@mandrake.org> 1.0.1-4mdk
- Conflicts with irssi

* Mon Oct 25 2004 Abel Cheung <deaddog@mandrake.org> 1.0.1-3mdk
- Redo spec file, to fix install issues
- Don't distribute any library, because this is the job of silc-toolkit;
  The library inside silc-client is older (despite having larger library
  major number and newer version number!)
- Link against gmp and glib2
- Patch0: Ugly fix for proper detection of glib2
- Merge perl stuff back to main client package, they are quite
  essential for proper usage of client (which is actually Irssi)

* Wed Jan 14 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 1.0.1-2mdk
- fixed glib BuildRequires

* Wed Jan 14 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 1.0.1-1mdk
- new bugfix release
- removed libtool hara-kiri

* Fri Nov 28 2003 Tibor Pittich <Tibor.Pittich@phuture.sk> 1.0-1mdk
- yes, yes; this is finally version 1.0 :)
- there is temporary fix for libtool problem, thanks to c0ffee

* Tue Nov 18 2003 Tibor Pittich <Tibor.Pittich@phuture.sk> 0.9.16-1mdk
- new bugfix release
- update Source link

* Fri Oct 31 2003 Tibor Pittich <Tibor.Pittich@phuture.sk> 0.9.15-1mdk
- new version

* Sun Oct 26 2003 Tibor Pittich <Tibor.Pittich@phuture.sk> 0.9.14-1mdk
- new version

* Thu Oct 16 2003 Tibor Pittich <Tibor.Pittich@phuture.sk> 0.9.13-1mdk
- new version
- removed mandir patch

* Wed Sep 24 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.9.12.1-1mdk
- 0.9.12.1
- Patch1 is now Patch0
- regenerate Patch1 which is Patch0 (you listening ?)

