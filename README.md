# iwlwifi LARI-disable DKMS workaround

An experimental out-of-tree build of Intel `iwlwifi`/`iwlmvm` for systems whose
firmware-provided LARI configuration incorrectly disables Wi-Fi 6E.

The package adds an opt-in module parameter:

```text
iwlwifi.lar_disable=1
```

When enabled, the driver skips the BIOS `LARI_CONFIG_CHANGE` command. It does
not change Linux's global regulatory domain; use it only where 6 GHz operation
is permitted and only for diagnosing a broken platform firmware policy.

## Fedora RPM installation

Install the RPM built for your Fedora release, then enable the workaround and
rebuild the initramfs:

```sh
sudo dnf install ./iwlwifi-lar-disable-dkms-*.noarch.rpm
printf 'options iwlwifi lar_disable=1\n' | sudo tee /etc/modprobe.d/iwlwifi-lar-disable.conf
sudo dracut --force --kver "$(uname -r)"
sudo reboot
```

Verify after boot:

```sh
cat /sys/module/iwlwifi/parameters/lar_disable
journalctl -kb | grep 'skipping BIOS LARI'
```

## Removal

```sh
sudo rm /etc/modprobe.d/iwlwifi-lar-disable.conf
sudo dnf remove iwlwifi-lar-disable-dkms
sudo dracut --force --kver "$(uname -r)"
sudo reboot
```

## Build scope

The source archive is based on Fedora kernel `7.1.5-201.fc44`, and the GitHub
workflow produces an installable noarch DKMS RPM and SRPM. DKMS rebuilds the
modules for installed kernels with their matching `kernel-devel` packages.
