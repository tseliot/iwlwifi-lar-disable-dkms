%global dkms_name iwlwifi-lar-disable
%global dkms_version 7.1.5-202

Name:           iwlwifi-lar-disable-dkms
Version:        7.1.5
Release:        202%{?dist}
Summary:        Experimental iwlwifi LARI-disable DKMS workaround
License:        GPL-2.0-only
URL:            https://github.com/tseliot/iwlwifi-lar-disable-dkms
Source0:        %{dkms_name}-%{dkms_version}.tar.xz
BuildArch:      noarch
BuildRequires:  make
Requires:       dkms
Requires:       kernel-devel

%description
An experimental Intel iwlwifi DKMS build which adds the opt-in lar_disable
parameter. With lar_disable=1, iwlwifi skips the BIOS LARI regulatory command
for systems whose firmware reports an incorrect 6 GHz authorization.

%prep
%setup -q -n %{dkms_name}-%{dkms_version}

%build

%install
install -d %{buildroot}/usr/src/%{dkms_name}-%{dkms_version}
cp -a . %{buildroot}/usr/src/%{dkms_name}-%{dkms_version}/

%post
/usr/sbin/dkms add -m %{dkms_name} -v %{dkms_version} || :
/usr/sbin/dkms autoinstall -m %{dkms_name} -v %{dkms_version} || :

%preun
if [ "$1" -eq 0 ]; then
    /usr/sbin/dkms remove -m %{dkms_name} -v %{dkms_version} --all || :
fi

%files
/usr/src/%{dkms_name}-%{dkms_version}

%changelog
* Tue Aug 04 2026 Alberto Milone <albertomilone@gmail.com> - 7.1.5-202
- Initial package
