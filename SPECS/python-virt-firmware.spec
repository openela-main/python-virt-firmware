%global pypi_version 1.6

Name:           python-virt-firmware
Version:        %{pypi_version}
Release:        2%{?dist}
Summary:        Tools for virtual machine firmware volumes

License:        GPLv2
URL:            https://gitlab.com/kraxel/virt-firmware
Source0:        https://gitlab.com/kraxel/virt-firmware/-/archive/v%{pypi_version}/virt-firmware-v%{pypi_version}.tar.gz
Patch1:         0001-setup.cfg-drop-peutils.patch
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(cryptography)
BuildRequires:  python3dist(setuptools)
BuildRequires:  make

%description
Tools for ovmf / armvirt firmware volumes This is a small collection of tools
for edk2 firmware images. They support decoding and printing the content of
firmware volumes. Variable stores (OVMF_VARS.fd) can be modified, for example
to enroll secure boot certificates.

%package -n     python3-virt-firmware
Summary:        %{summary}
%{?python_provide:%python_provide python3-virt-firmware}
Provides:       virt-firmware
Requires:       python3dist(cryptography)
Requires:       python3dist(setuptools)
%description -n python3-virt-firmware
Tools for ovmf / armvirt firmware volumes This is a small collection of tools
for edk2 firmware images. They support decoding and printing the content of
firmware volumes. Variable stores (OVMF_VARS.fd) can be modified, for example
to enroll secure boot certificates.

%package -n     python3-virt-firmware-tests
Summary:        %{summary} - test cases
Requires:       python3-virt-firmware
Requires:       python3dist(pytest)
Requires:       edk2-ovmf
%description -n python3-virt-firmware-tests
test cases

%prep
%autosetup -n virt-firmware-v%{pypi_version}

%build
%py3_build

%install
%py3_install
# manpages
install -m 755 -d      %{buildroot}%{_mandir}/man1
install -m 644 man/*.1 %{buildroot}%{_mandir}/man1
# tests
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -ar tests %{buildroot}%{_datadir}/%{name}

%files -n python3-virt-firmware
%license LICENSE
%doc README.md
%{_bindir}/host-efi-vars
%{_bindir}/virt-fw-dump
%{_bindir}/virt-fw-vars
%{_bindir}/virt-fw-sigdb
%{_bindir}/migrate-vars
%{_mandir}/man1/virt-*.1*
%{python3_sitelib}/virt/firmware
%{python3_sitelib}/virt_firmware-%{pypi_version}-py%{python3_version}.egg-info

%files -n python3-virt-firmware-tests
%{_datadir}/%{name}/tests

%changelog
* Tue Nov 15 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.6-2
- add tests.yml

* Mon Nov 14 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.6-1
- update to version 1.6
- drop peutils
- add man-pages
- add tests sub-package
- resolves: rhbz#2142608

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.2-1
- update to version 1.2

* Fri Jul 01 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.1-1
- update to version 1.1

* Wed Jun 22 2022 Gerd Hoffmann <kraxel@redhat.com> - 1.0-1
- update to version 1.0

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.98-2
- Rebuilt for Python 3.11

* Tue May 24 2022 Gerd Hoffmann <kraxel@redhat.com> - 0.98-1
- update to version 0.98

* Mon Apr 11 2022 Gerd Hoffmann <kraxel@redhat.com> - 0.95-1
- Initial package.
