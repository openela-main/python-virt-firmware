%global pypi_version 24.2

Name:           python-virt-firmware
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        Tools for virtual machine firmware volumes

License:        GPLv2
URL:            https://pypi.org/project/virt-firmware/
Source0:        virt-firmware-%{pypi_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(cryptography)
BuildRequires:  python3dist(setuptools)
BuildRequires:  make
BuildRequires:  systemd systemd-rpm-macros

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
Requires:       python3dist(pefile)
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

%package -n     uki-direct
Provides:       ukidirect
Summary:        %{summary} - manage UKI kernels.
Requires:       python3-virt-firmware
Conflicts:      systemd < 252-21
Obsoletes:      rhel-cvm-update-tool
%description -n uki-direct
kernel-install plugin and systemd unit to manage automatic
UKI (unified kernel image) updates.

%prep
%autosetup -n virt-firmware-%{pypi_version}

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
# uki-direct
install -m 755 -d  %{buildroot}%{_unitdir}
install -m 755 -d  %{buildroot}%{_libdir}/kernel/install.d
install -m 644 systemd/kernel-bootcfg-boot-successful.service %{buildroot}%{_unitdir}
install -m 755 systemd/99-uki-uefi-setup.install %{buildroot}%{_libdir}/kernel/install.d

%post -n uki-direct
%systemd_post kernel-bootcfg-boot-successful.service

%preun -n uki-direct
%systemd_preun kernel-bootcfg-boot-successful.service

%postun -n uki-direct
%systemd_postun kernel-bootcfg-boot-successful.service

%files -n python3-virt-firmware
%license LICENSE
%doc README.md experimental
%{_bindir}/host-efi-vars
%{_bindir}/virt-fw-dump
%{_bindir}/virt-fw-vars
%{_bindir}/virt-fw-sigdb
%{_bindir}/kernel-bootcfg
%{_bindir}/uefi-boot-menu
%{_bindir}/migrate-vars
%{_bindir}/pe-dumpinfo
%{_bindir}/pe-listsigs
%{_bindir}/pe-addsigs
%{_bindir}/pe-inspect
%{_mandir}/man1/virt-*.1*
%{_mandir}/man1/kernel-bootcfg.1*
%{_mandir}/man1/uefi-boot-menu.1*
%{_mandir}/man1/pe-*.1*
%{python3_sitelib}/virt/firmware
%{python3_sitelib}/virt/peutils
%{python3_sitelib}/virt_firmware-%{pypi_version}-py%{python3_version}.egg-info

%files -n python3-virt-firmware-tests
%{_datadir}/%{name}/tests

%files -n uki-direct
%{_unitdir}/kernel-bootcfg-boot-successful.service
%{_libdir}/kernel/install.d/99-uki-uefi-setup.install

%changelog
* Fri Feb 16 2024 Gerd Hoffmann <kraxel@redhat.com> - 24.2-1
- update to version 24.2

* Thu Jan 11 2024 Gerd Hoffmann <kraxel@redhat.com> - 24.1.1-1
- update to version 24.1.1

* Tue Jan 09 2024 Gerd Hoffmann <kraxel@redhat.com> - 24.1-1
- update to version 24.1
- Resolves: RHEL-21090

* Wed Jan 03 2024 Gerd Hoffmann <kraxel@redhat.com> - 23.11-3
- add "obsoletes: rhel-cvm-update-tool" to uki-direct

* Tue Jan 02 2024 Gerd Hoffmann <kraxel@redhat.com> - 23.11-2
- add uki-direct subpackage
- Resolves: RHEL-19383

* Wed Dec 13 2023 Gerd Hoffmann <kraxel@redhat.com> - 23.11-1
- update to version 23.11

* Thu Oct 12 2023 Gerd Hoffmann <kraxel@redhat.com> - 23.10-2
- drop uki-direct subpackage for now (wait for systemd update)

* Wed Oct 11 2023 Gerd Hoffmann <kraxel@redhat.com> - 23.10-1
- update to version 23.10
- add uki-direct subpackage

* Tue Jun 27 2023 Gerd Hoffmann <kraxel@redhat.com> - 23.6-2
- drop -peutils subpackage

* Tue Jun 20 2023 Gerd Hoffmann <kraxel@redhat.com> - 23.6-1
- update to version 23.6
- resolves: rhbz#2216102

* Thu May 04 2023 Gerd Hoffmann <kraxel@redhat.com> - 23.5-1
- update to version 23.5
- resolves: rhbz#2193089

* Fri Apr 14 2023 Gerd Hoffmann <kraxel@redhat.com> - 23.4-1
- update to version 23.4
- resolves: rhbz#2186770
- resolves: rhbz#2143566

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
