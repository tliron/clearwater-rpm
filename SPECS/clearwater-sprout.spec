Name:          clearwater-sprout
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/sprout

Source0:       %{name}-%{version}.tar.bz2
BuildRequires: rsync make cmake libtool gcc-c++ bison flex
#rubygems
#BuildRequires: libevent-devel, boost-devel, boost-static, ncurses-devel, c-ares-devel
#BuildRequires: net-snmp-devel, zeromq-devel

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary: Clearwater - Sprout

%package plugin-scscf
Summary: Clearwater - Sprout S-CSCF Plugin

%package plugin-icscf
Summary: Clearwater - Sprout I-CSCF Plugin

%package plugin-bgcf
Summary: Clearwater - Sprout BGCF Plugin

%package as-plugin-mmtel
Summary: Clearwater - Sprout MMTEL Application Server Plugin

%package as-plugin-gemini
Summary: Clearwater - Sprout Gemini Application Server Plugin

%package as-plugin-memento
Summary: Clearwater - Sprout Memento Application Server Plugin

%package as-plugin-call-diversion
Summary: Clearwater - Sprout Call Diversion Application Server Plugin

%package as-plugin-mangelwurzel
Summary: Clearwater - Sprout Mangelwurzel Application Server Plugin

%package -n clearwater-bono
Summary: Clearwater - Bono 

%package -n clearwater-restund
Summary: Clearwater - restund

%package -n clearwater-sipp
Summary: Clearwater - SIPp

%package -n clearwater-sip-stress
Summary: Clearwater - SIP Stress Tests

%package -n clearwater-sip-stress-stats
Summary: Clearwater - SPI Stress Tests Statistics

%package -n clearwater-sip-perf
Summary: Clearwater - SIP Performance Tests

%description
SIP router

%description plugin-scscf
SIP router S-CSCF plugin

%description plugin-icscf
SIP router I-CSCF plugin

%description plugin-bgcf
SIP router BGCF plugin

%description as-plugin-mmtel
SIP router MMTEL application server plugin

%description as-plugin-gemini
Mobile twinning application server plugin

%description as-plugin-memento
Call list application server plugin

%description as-plugin-call-diversion
Call diversion application server plugin

%description as-plugin-mangelwurzel
B2BUA and SCC-AS emulator application server plugin

%description -n clearwater-bono
SIP edge proxy

%description -n clearwater-restund
STUN/TURN server

%description -n clearwater-sipp
Clearwater build of SIPp, used for running SIP stress and performance tests

%description -n clearwater-sip-stress
Runs SIP stress against Clearwater

%description -n clearwater-sip-stress-stats
Exposes SIP stress statistics over the Clearwater statistics interface.

%description -n clearwater-sip-perf
Runs SIP performance tests against Clearwater

%prep
%setup

%build
# Note: the modules must be built in order, so unfortunately we can't use --jobs/-J
make

%install
# See: debian/sprout-base.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
rsync build/bin/sprout %{buildroot}/usr/share/clearwater/bin/
rsync --recursive sprout-base.root/* %{buildroot}/
rsync scripts/sprout-log-cleanup %{buildroot}/etc/cron.hourly/
rsync modules/clearwater-etcd-plugins/sprout/sprout_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
rsync modules/clearwater-etcd-plugins/sprout/sprout_scscf_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
rsync modules/clearwater-etcd-plugins/sprout/sprout_enum_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
rsync modules/clearwater-etcd-plugins/sprout/sprout_rph_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
rsync modules/clearwater-etcd-plugins/clearwater_config_access/scscf_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
rsync modules/clearwater-etcd-plugins/clearwater_config_access/enum_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
rsync modules/clearwater-etcd-plugins/clearwater_config_access/rph_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

# See: debian/sprout-scscf.install
mkdir --parents %{buildroot}/usr/share/clearwater/sprout/plugins
rsync build/bin/sprout_scscf.so %{buildroot}/usr/share/clearwater/sprout/plugins/
rsync modules/clearwater-etcd-plugins/clearwater_config_manager/shared_ifcs_xml_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
rsync modules/clearwater-etcd-plugins/clearwater_config_manager/fallback_ifcs_xml_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
rsync modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/remove_shared_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
rsync modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/remove_fallback_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
rsync modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/validate_shared_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
rsync modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/validate_fallback_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
rsync modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/display_shared_ifcs %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
rsync modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/display_fallback_ifcs %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
rsync modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/config_validation/* %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/
rsync modules/clearwater-etcd-plugins/clearwater_config_access/shared_ifcs_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
rsync modules/clearwater-etcd-plugins/clearwater_config_access/fallback_ifcs_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

# See: debian/sprout-icscf.install
rsync build/bin/sprout_icscf.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/sprout-bgcf.install
rsync build/bin/sprout_bgcf.so %{buildroot}/usr/share/clearwater/sprout/plugins/
rsync --recursive sprout-bgcf.root/* %{buildroot}/
rsync modules/clearwater-etcd-plugins/sprout/sprout_bgcf_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
rsync modules/clearwater-etcd-plugins/clearwater_config_access/bgcf_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

# See: debian/sprout-mmtel-as.install
rsync build/bin/sprout_mmtel_as.so %{buildroot}/usr/share/clearwater/sprout/plugins/
rsync --recursive sprout-mmtel-as.root/* %{buildroot}/

# See: debian/gemini-as.install
rsync build/bin/gemini-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/memento-as.install
rsync build/bin/memento-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/
rsync --recursive memento-as.root/* %{buildroot}/

# See: debian/call-diversion-as.install
rsync build/bin/call-diversion-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/mangelwurzel-as.install
rsync build/bin/mangelwurzel-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/bono.install
mkdir --parents %{buildroot}%{_initrddir}/
rsync build/bin/sprout %{buildroot}/usr/share/clearwater/bin/bono
rsync debian/bono.init.d %{buildroot}%{_initrddir}/bono
rsync --recursive bono.root/* %{buildroot}/
rsync scripts/bono-log-cleanup %{buildroot}/etc/cron.hourly/

# See: debian/restund.install
mkdir --parents %{buildroot}/usr/share/clearwater/restund/lib/
rsync debian/restund.init.d %{buildroot}%{_initrddir}/restund
rsync usr/sbin/restund %{buildroot}/usr/share/clearwater/bin/
rsync usr/lib/libre.* %{buildroot}/usr/share/clearwater/restund/lib/
rsync usr/lib/restund/modules/* %{buildroot}/usr/share/clearwater/restund/lib/
rsync --recursive restund.root/* %{buildroot}/

# See: debian/clearwater-sipp.install
rsync --recursive clearwater-sipp.root/* %{buildroot}/
rsync modules/sipp/sipp %{buildroot}/usr/share/clearwater/bin/

# See: debian/clearwater-sip-stress.install
rsync debian/clearwater-sip-stress.init.d %{buildroot}%{_initrddir}/clearwater-sip-stress
rsync --recursive clearwater-sip-stress.root/* %{buildroot}/

# See: debian/clearwater-sip-stress-stats.install
rsync debian/clearwater-sip-stress-stats.init.d %{buildroot}%{_initrddir}/clearwater-sip-stress-stats
rsync scripts/sipp-stats/clearwater-sipp-stats-*.gem %{buildroot}/usr/share/clearwater/gems/

# See: debian/clearwater-sip-perf.install
rsync debian/clearwater-sip-perf.init.d %{buildroot}%{_initrddir}/clearwater-sip-perf
rsync --recursive clearwater-sip-perf.root/* %{buildroot}/

%files
/usr/share/clearwater/bin/sprout
/usr/share/clearwater/bin/poll_sprout_http.sh
/usr/share/clearwater/bin/poll_sprout_sip.sh
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/enum_schema.json
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/rph_schema.json
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/rph_validation.py*
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/scscf_schema.json
/usr/share/clearwater/clearwater-diags-monitor/scripts/sprout_base_diags
/usr/share/clearwater/infrastructure/alarms/sprout_alarms.json
/usr/share/clearwater/infrastructure/monit_stability/sprout-stability
/usr/share/clearwater/infrastructure/monit_uptime/check-sprout-uptime
/usr/share/clearwater/infrastructure/scripts/reload/fallback_ifcs_xml/sprout_reload
/usr/share/clearwater/infrastructure/scripts/reload/memcached/sprout_reload
/usr/share/clearwater/infrastructure/scripts/reload/shared_ifcs_xml/sprout_reload
/usr/share/clearwater/infrastructure/scripts/restart/sprout_restart
/usr/share/clearwater/infrastructure/scripts/create-analytics-syslog-config
/usr/share/clearwater/infrastructure/scripts/create-sprout-nginx-config
/usr/share/clearwater/infrastructure/scripts/sprout.monit
/usr/share/clearwater/node_type.d/20_sprout
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_json_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_scscf_json_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_enum_json_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_rph_json_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/scscf_json_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/enum_json_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/rph_json_config_plugin.py*
%config /etc/clearwater/logging/sprout
%config /etc/init.d/sprout
%config /etc/logrotate.d/sproutanalytics
%config /etc/security/limits.conf.sprout
%config /etc/cron.hourly/sprout-log-cleanup

%files plugin-scscf
/usr/share/clearwater/sprout/plugins/sprout_scscf.so
/usr/share/clearwater/clearwater-config-manager/plugins/shared_ifcs_xml_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/fallback_ifcs_xml_plugin.py*
/usr/share/clearwater/clearwater-config-manager/scripts/remove_shared_ifcs_xml
/usr/share/clearwater/clearwater-config-manager/scripts/remove_fallback_ifcs_xml
/usr/share/clearwater/clearwater-config-manager/scripts/validate_shared_ifcs_xml
/usr/share/clearwater/clearwater-config-manager/scripts/validate_fallback_ifcs_xml
/usr/share/clearwater/clearwater-config-manager/scripts/display_shared_ifcs
/usr/share/clearwater/clearwater-config-manager/scripts/display_fallback_ifcs
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/
/usr/share/clearwater/clearwater-config-access/plugins/shared_ifcs_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/fallback_ifcs_config_plugin.py*

%files plugin-icscf
/usr/share/clearwater/sprout/plugins/sprout_icscf.so

%files plugin-bgcf
/usr/share/clearwater/sprout/plugins/sprout_bgcf.so
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/bgcf_schema.json
/usr/share/clearwater/clearwater-config-manager/scripts/print-bgcf-configuration
/usr/share/clearwater/clearwater-config-manager/scripts/upload_bgcf_json
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_bgcf_json_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/bgcf_json_config_plugin.py*

%files as-plugin-mmtel
/usr/share/clearwater/sprout/plugins/sprout_mmtel_as.so
/usr/share/clearwater/clearwater-diags-monitor/scripts/sprout_mmtel_as_diags

%files as-plugin-gemini
/usr/share/clearwater/sprout/plugins/gemini-as.so

%files as-plugin-memento
/usr/share/clearwater/sprout/plugins/memento-as.so
/usr/share/clearwater/infrastructure/alarms/memento_as_alarms.json

%files as-plugin-call-diversion
/usr/share/clearwater/sprout/plugins/call-diversion-as.so

%files as-plugin-mangelwurzel
/usr/share/clearwater/sprout/plugins/mangelwurzel-as.so

%files -n clearwater-bono
%{_initrddir}/bono
/usr/share/clearwater/bin/bono
/usr/share/clearwater/bin/poll_bono.sh
/usr/share/clearwater/clearwater-diags-monitor/scripts/bono_diags
/usr/share/clearwater/infrastructure/scripts/restart/bono_restart
/usr/share/clearwater/infrastructure/scripts/bono.monit
/usr/share/clearwater/node_type.d/20_bono
%config /etc/clearwater/logging/bono
%config /etc/security/limits.conf.bono
%config /etc/cron.hourly/bono-log-cleanup

%files -n clearwater-restund
%{_initrddir}/restund
/usr/share/clearwater/bin/restund
/usr/share/clearwater/restund/lib/
/usr/share/clearwater/bin/poll_restund.sh
/usr/share/clearwater/infrastructure/scripts/restund
%config /etc/security/limits.conf.restund

%files -n clearwater-sipp
/etc/sysctl.conf.clearwater-sipp
/usr/share/clearwater/bin/sipp

%files -n clearwater-sip-stress
%{_initrddir}/clearwater-sip-stress
/etc/cron.hourly/clearwater-sip-stress-log-cleanup
/usr/share/clearwater/bin/sip-stress
/usr/share/clearwater/infrastructure/scripts/sip-stress
/usr/share/clearwater/sip-stress/sip-stress.xml

%files -n clearwater-sip-stress-stats
%{_initrddir}/clearwater-sip-stress-stats
/usr/share/clearwater/gems/clearwater-sipp-stats-*.gem

%files -n clearwater-sip-perf
%{_initrddir}/clearwater-sip-perf
/usr/share/clearwater/bin/sip-perf
/usr/share/clearwater/infrastructure/scripts/sip-perf
/usr/share/clearwater/sip-perf/sip-perf.xml

%post plugin-scscf
# See: debian/scsf-bgcf.links
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/validate_shared_ifcs_xml /usr/bin/cw-validate_shared_ifcs_xml
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/validate_fallback_ifcs_xml /usr/bin/cw-validate_fallback_ifcs_xml
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/display_shared_ifcs /usr/bin/cw-display_shared_ifcs
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/display_fallback_ifcs /usr/bin/cw-display_fallback_ifcs
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/remove_shared_ifcs_xml /usr/sbin/cw-remove_shared_ifcs_xml
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/remove_fallback_ifcs_xml /usr/sbin/cw-remove_fallback_ifcs_xml

%preun plugin-scscf
rm --force /usr/bin/cw-validate_shared_ifcs_xml
rm --force /usr/bin/cw-validate_fallback_ifcs_xml
rm --force /usr/bin/cw-display_shared_ifcs
rm --force /usr/bin/cw-display_fallback_ifcs
rm --force /usr/sbin/cw-remove_shared_ifcs_xml
rm --force /usr/sbin/cw-remove_fallback_ifcs_xml

%post plugin-bgcf
# See: debian/sprout-bgcf.links
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/upload_bgcf_json /usr/bin/cw-upload_bgcf_json

%preun plugin-bgcf
rm --force /usr/bin/cw-upload_bgcf_json