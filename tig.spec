# Pass '--without docs' to rpmbuild if you don't want the documentation to be build
%define _without_docs	1

Summary:	Tig: text-mode interface for git
Name:		tig
Version:	2.5.0
Release:	1%{?dist}
License:	GPL
Group:		Development/Tools
Vendor:		Jonas Fonseca <jonas.fonseca@gmail.com>
URL:		https://jonas.github.io/tig
Source:		tig-%{version}.tar.gz
BuildRequires:	ncurses-devel%{!?_without_docs:, xmlto, asciidoc > 6.0.3}
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
Requires:	git-core
Requires:	ncurses

%description
Tig is a git repository browser that additionally can act as a pager
for output from various git commands.

When browsing repositories, it uses the underlying git commands to
present the user with various views, such as summarized revision log
and showing the commit with the log message, diffstat, and the diff.

Using it as a pager, it will display input from stdin and colorize it.

%prep
%setup -q

%build
./autogen.sh
%configure
CFLAGS="$RPM_OPT_FLAGS -DVERSION=tig-%{version}-%{release}"
%{__make} %{_smp_mflags} \
	prefix=%{_prefix} \
	all %{!?_without_docs: doc-man doc-html}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
CFLAGS="$RPM_OPT_FLAGS -DVERSION=tig-%{version}-%{release}"
%{__make} %{_smp_mflags} DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix} bindir=%{_bindir} mandir=%{_mandir} \
	install %{!?_without_docs: install-doc-man}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sysconfdir}/*
%doc README.adoc COPYING INSTALL.adoc NEWS.adoc contrib/tig-completion.bash contrib/tig-completion.zsh
%{!?_without_docs: %{_mandir}/man1/*.1*}
%{!?_without_docs: %{_mandir}/man5/*.5*}
%{!?_without_docs: %{_mandir}/man7/*.7*}
%{!?_without_docs: %doc doc/*.html}

%changelog
* Wed Mar 11 2020 Enrico Weigelt <info@metux.net>
- Packaging for SLES12

* Sun Feb 23 2014 Jonas Fonseca <jonas.fonseca@gmail.com>
- Add tigrc installed in /etc

* Tue Jan  8 2013 Joakim Sernbrant <serbaut@gmail.com>
- Added configure

* Thu Aug 16 2012 Victor Foitzik <vifo@cpan.org>
- Now also packaging man(7) pages

* Sat Jun 23 2007 Jonas Fonseca <jonas.fonseca@gmail.com>
- Include tig bash completion script

* Fri Jun  1 2007 Jakub Narebski <jnareb@gmail.com>
- Include documentation sources for --without docs
- Remove PDF version of manual from being build and installed

* Mon May 28 2007 Jakub Narebski <jnareb@gmail.com>
- Initial tig spec file
