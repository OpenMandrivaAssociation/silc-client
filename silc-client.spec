# $Id: silc-client.spec 38507 2006-07-07 21:08:14Z nanardon $

%define name silc-client
%define version 1.0.2
%define release %mkrel 2

%define _silcdatadir %{_datadir}/silc
%define _silcetcdir %{_sysconfdir}/silc

Summary:	Client for the secure Internet Live Conferencing (SILC) protocol
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://www.silcnet.org/download/client/sources/%{name}-%{version}.tar.bz2
Patch0:		%{name}-1.0.1-glib-check-order.patch
License:	GPL
Group:		Networking/Chat
URL:		http://www.silcnet.org/
BuildRequires:	ncurses-devel
BuildRequires:	perl-devel
BuildRequires:	glib2-devel
BuildRequires:	gmp-devel
BuildRequires:	automake1.8
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Conflicts:	irssi

%description
SILC (Secure Internet Live Conferencing) is a protocol which provides
secure conferencing services on the Internet over insecure channel.
SILC is IRC-like software although internally they are very different.
The biggest similarity between SILC and IRC is that they both provide
conferencing services and that SILC has almost the same commands as IRC.
Other than that they are nothing alike.  Major differences are that SILC
is secure what IRC is not in any way.  The network model is also entirely
different compared to IRC.

%prep
%setup -q
%patch0 -p1 -b .glib-order

find -type f | xargs file | grep -v script | cut -d: -f1 | xargs chmod -x

pushd irssi
aclocal-1.8 -I .
automake-1.8 -a -c
autoconf
popd

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

# parallel make fails
make

%install
rm -rf "%{buildroot}"
%makeinstall_std

# install conf file, makeinstall don't do it (it really sucks)
cp ./doc/silcalgs.conf %{buildroot}/%{_silcetcdir}
cp ./irssi/silc.conf %{buildroot}/%{_silcetcdir}

# let rpm macros handle documents
rm -rf package-doc
mv %{buildroot}%{_prefix}/doc package-doc/
mkdir -p package-doc/irssi
install -m 644 irssi/docs/*.{txt,html} package-doc/irssi/
find package-doc -size 0 -type f -print0 | xargs -0 -r rm -f

# remove all unwanted files
rm -f %{buildroot}%{_prefix}/*.{a,la}


%clean
rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%doc package-doc/*

%config(noreplace) %{_silcetcdir}
%{_bindir}/silc
%{_silcdatadir}
%{_mandir}/man?/*
%{perl_vendorarch}/Irssi*
%{perl_vendorarch}/auto/Irssi



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

* Sun Apr 27 2003 Tibor Pittich <Tibor.Pittich@phuture.sk> 0.9.12-3mdk
- add missing dir into files section (mr. distlint)

* Sat Apr 26 2003 Tibor Pittich <Tibor.Pittich@phuture.sk> 0.9.12-2mdk
- fixed Requires and Builrequires section (thnx. to Stefan's robot)
- cleanup spec file (remove old non-mdk-contrib records)
- fixed permissions of source files
- add mklibname macro into definition of libname and libclient

* Tue Mar 18 2003 Tibor Pittich <Tibor.Pittich@phuture.sk> 0.9.12-1mdk
- 0.9.12 - bugfix release
	- Fixed RESOLVING flag handling in JOIN notify
	- Fixed incorrect connection deletion
- mandir patch synced with cvs

* Fri Jan 10 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.9.11-1mdk
- 0.9.11

* Mon Dec 30 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.9.10.1-1mdk
- 0.9.10.1
- fix install of lib and perl module
- By Tibor Pittich <Tibor.Pittich@phuture.sk>
	- SILC protocol version 1.2
		- add mandir dirty patch (thanks to johnny)
		- provide this hot package, because silc protocol changed, and it is
		  incompatibille with old silc-client ..

* Sun Nov 17 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.9.8-3mdk
- add _silclibdir in ld.so.conf
- libsilcclient requires libsilc
- split perl module into silc-perl
- silc-perl conflicts with irssi
- remove _silclibdir/perl5 (seems to be unused)

* Wed Nov 13 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.9.8-2mdk
- Add missing lib
- split into libsilc, libsilc-client

* Sun Nov 10 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.9.8-1mdk
- By Tibor Pittich <Tibor.Pittich@phuture.sk>
	- new version
		- a lots of fixes and some new stuff
		- added manual page silc(1)
		- topics are now UTF-8
		- support for encrypted private key files is added
		- included latest fixes from irssi.org CVS
	- man page added into spec, define mandir
	- some changes dedicated to rpmlint (unmark default.theme as config,
	  update my .rpmmacros file)

* Tue Oct 22 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.9.7-1mdk
- Excellent spec By Tibor Pittich <Tibor.Pittich@phuture.sk>
	- new version
		- totally new Irssi base from the irssi.org CVS
		- stabilisation
		- fixes several bugs with the new ATTR command
	- add silc-client into Mandrake menu system
	- add png icons

* Mon Oct 21 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.9.6-1mdk 
- By Tibor Pittich <Tibor.Pittich@phuture.sk>
	- new version
	- remove previous patches

* Tue Sep 17 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.9.5-1mdk 
- By Tibor Pittich <Tibor.Pittich@phuture.sk>
	- Added some user-friendly aliases
	- Removed some unsafe code from the original client
	- Also fixed temporarily the /detach bug [#24]
	- new version 0.9.5
	- Added a temporary fix for the "(null)" hostname bug

* Sat Jul 06 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.9.4-2mdk
- Fix summary (Tibor Pittich <Tibor.Pittich@phuture.sk>)

* Fri Jul 05 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.9.4-1mdk 
- From Tibor Pittich <Tibor.Pittich@phuture.sk>
	- First mdk package
- fix non %config

