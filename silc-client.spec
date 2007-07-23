# $Id: silc-client.spec 38507 2006-07-07 21:08:14Z nanardon $

%define name silc-client
%define version 1.1.2
%define release %mkrel 1

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
BuildRequires:	automake
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
#patch0 -p1 -b .glib-order

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
