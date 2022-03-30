# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		bitstring
%define		egg_name	bitstring
%define		pypi_name	bitstring
Summary:	A Python module to help you manage your bits
Name:		python-%{pypi_name}
Version:	3.1.5
Release:	6
License:	MIT
Group:		Libraries/Python
Source0:	https://github.com/scott-griffiths/bitstring/archive/bitstring-%{version}.tar.gz
# Source0-md5:	ba96be1d2ae5ad35e4263c6a1c8bc310
URL:		https://github.com/scott-griffiths/bitstring
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
bitstring is a pure Python module designed to help make the creation
and analysis of binary data as simple and natural as possible.

Bitstrings can be constructed from integers (big and little endian),
hex, octal, binary, strings or files. They can be sliced, joined,
reversed, inserted into, overwritten, etc. with simple functions or
slice notation. They can also be read from, searched and replaced, and
navigated in, similar to a file or stream.

%package -n python3-%{pypi_name}
Summary:	A Python module to help you manage your bits
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{pypi_name}
bitstring is a pure Python module designed to help make the creation
and analysis of binary data as simple and natural as possible.

Bitstrings can be constructed from integers (big and little endian),
hex, octal, binary, strings or files. They can be sliced, joined,
reversed, inserted into, overwritten, etc. with simple functions or
slice notation. They can also be read from, searched and replaced, and
navigated in, similar to a file or stream.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{pypi_name}-%{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd doc
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/%{module}.py[co]
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}.py
%{py3_sitescriptdir}/__pycache__/%{module}.*.py[co]
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
