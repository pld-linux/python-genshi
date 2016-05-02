# TODO:
# - fails to build --with speedups
# - --with speedups broken with new python macros
# - do not enable tests before ensuring they do not lock up builders
#
# Conditional build:
%bcond_with	speedups	# skip optional C extension build
%bcond_with	tests		# build without tests (lockup builders)

Summary:	Python toolkit for generation of output for the web
Name:		python-genshi
Version:	0.7
Release:	0.1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://ftp.edgewall.com/pub/genshi/Genshi-0.7.tar.gz
# Source0-md5:	54e64dd69da3ec961f86e686e0848a82
URL:		https://genshi.edgewall.org/
BuildRequires:	python-devel
BuildRequires:	python-devel-tools
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%{!?with_speedups:BuildArch:	noarch}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%{!?with_speedups:%{expand:%%global py_sitedir %{py_sitescriptdir}}}

%description
Genshi is a Python library that provides an integrated set of
components for parsing, generating, and processing HTML, XML or other
textual content for output generation on the web.

%prep
%setup -q -n Genshi-%{version}

%build
%py_build

%{?with_tests:%{__python} setup.py test}

%install
rm -rf $RPM_BUILD_ROOT
%py_install \
	%{?with_speedups:--with-speedups}

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog
%dir %{py_sitescriptdir}/genshi
%{py_sitescriptdir}/genshi/*.py[co]
%dir %{py_sitescriptdir}/genshi/filters
%{py_sitescriptdir}/genshi/filters/*.py[co]
%dir %{py_sitescriptdir}/genshi/template
%{py_sitescriptdir}/genshi/template/*.py[co]

%if %{with speedups}
%attr(755,root,root) %{py_sitescriptdir}/genshi/_speedups.so
%endif

# egg-info is built with setuptools under py 2.4 too
%{py_sitescriptdir}/Genshi-*.egg-info
