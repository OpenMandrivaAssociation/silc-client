%define name silc-client
%define version 1.1.3
%define release %mkrel 2

%define _silcdatadir %{_datadir}/silc
%define _silcetcdir %{_sysconfdir}/silc

Summary:	Client for the secure Internet Live Conferencing (SILC) protocol
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://www.silcnet.org/download/client/sources/%{name}-%{version}.tar.bz2
License:	GPLv2+
Group:		Networking/Chat
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.silcnet.org/
BuildRequires:	ncurses-devel
BuildRequires:	perl-devel
BuildRequires:	glib2-devel
BuildRequires:	gmp-devel
BuildRequires:	automake
BuildRequires:	silc-toolkit-devel
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

%package -n perl-silc
Group: Development/Perl
Summary: Perl part of the SILC client

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

# parallel make fails
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
