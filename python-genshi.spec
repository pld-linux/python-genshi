# TODO:
# - fails to build --with speedups
#
# Conditional build:
%bcond_with	speedups	# skip optional C extension build
%bcond_without	tests		# build without tests
#
Summary:	Python toolkit for generation of output for the web
Name:		python-genshi
Version:	0.6
Release:	3
License:	BSD
Group:		Development/Languages/Python
Source0:	http://ftp.edgewall.com/pub/genshi/Genshi-%{version}.tar.gz
# Source0-md5:	604e8b23b4697655d36a69c2d8ef7187
URL:		http://genshi.edgewall.org/
BuildRequires:	python-devel
BuildRequires:	python-devel-tools
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
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
export CFLAGS="%{rpmcflags}"
%{__python} setup.py build
%{!?with_tests:%{__python} setup.py test}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py \
	%{?with_speedups:--with-speedups} \
	install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

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
