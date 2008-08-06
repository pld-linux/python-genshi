# TODO
# - WARNING:
#   An optional C extension could not be compiled, speedups will not be
#   available:
# - /usr/include/python2.4/pyport.h:616:2: #error "LONG_BIT definition appears wrong for platform (bad gcc/glibc config?)."
#
# Conditional build:
%bcond_without	speedups	# skip optional C extension build
%bcond_without	tests		# build without tests
#
Summary:	Python toolkit for generation of output for the web
Name:		python-genshi
Version:	0.5.1
Release:	0.1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://ftp.edgewall.com/pub/genshi/Genshi-%{version}.tar.bz2
# Source0-md5:	822942bbc3109da9f6b472eb8ea4e3a4
URL:		http://genshi.edgewall.org/
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	python-setuptools-devel
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Genshi is a Python library that provides an integrated set of
components for parsing, generating, and processing HTML, XML or other
textual content for output generation on the web.

%prep
%setup -q -n Genshi-%{version}

%build
export CFLAGS="%{rpmcflags}"
%{__python} setup.py build
%{!?with_tests:%{__python} setup.py test}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--skip-build \
	%{!?with_speedups:--without-speedups} \
	--root=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog
%{py_sitedir}/genshi/*.py[co]
%dir %{py_sitedir}/genshi/filters
%{py_sitedir}/genshi/filters/*.py[co]
%dir %{py_sitedir}/genshi/template
%{py_sitedir}/genshi/template/*.py[co]

%if %{with speedups}
%attr(755,root,root) %{py_sitedir}/genshi/_speedups.so
%endif

# egg info is built with py 2.4 too
%{py_sitedir}/Genshi-*.egg-info
