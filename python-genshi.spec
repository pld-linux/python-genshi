# TODO:
# - do not enable tests before ensuring they do not lock up builders
#
# Conditional build:
%bcond_with	tests		# build without tests (lockup builders)

Summary:	Python toolkit for generation of output for the web
Name:		python-genshi
Version:	0.7
Release:	1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://ftp.edgewall.com/pub/genshi/Genshi-%{version}.tar.gz
# Source0-md5:	54e64dd69da3ec961f86e686e0848a82
URL:		https://genshi.edgewall.org/
BuildRequires:	python-devel
BuildRequires:	python-devel-tools
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%py_install
%py_postclean

%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/genshi/filters/tests
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/genshi/template/tests
%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/genshi/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog
%dir %{py_sitedir}/genshi
%{py_sitedir}/genshi/*.py[co]
%dir %{py_sitedir}/genshi/filters
%{py_sitedir}/genshi/filters/*.py[co]
%dir %{py_sitedir}/genshi/template
%{py_sitedir}/genshi/template/*.py[co]
%attr(755,root,root) %{py_sitedir}/genshi/_speedups.so
%{py_sitedir}/Genshi-*.egg-info
