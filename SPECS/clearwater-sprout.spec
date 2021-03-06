Name:          clearwater-sprout
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/sprout

Source0:       %{name}-%{version}.tar.bz2
Source1:       housekeeping.sh
Source2:       sprout.service
Source3:       sprout.sh
Source4:       bono.service
Source5:       bono.sh
Source6:       restund.service
Source7:       restund.sh
Source8:       clearwater-sip-stress.service
Source9:       clearwater-sip-stress.sh
Source10:      clearwater-sip-stress-stats.service
Source11:      clearwater-sip-stress-stats.sh
Source12:      clearwater-sip-perf.service
Source13:      clearwater-sip-perf.sh

BuildRequires: make cmake libtool gcc-c++ ccache bison flex rubygems rsync
BuildRequires: libevent-devel boost-devel boost-static ncurses-devel zeromq-devel
BuildRequires: net-snmp-devel
BuildRequires: systemd

# Note: zeromq-devel requires epel-release

%global debug_package %{nil}

Summary:       Clearwater - Sprout
Requires:      clearwater-sprout-libs
AutoReq:       no
%{?systemd_requires}

%package libs
Summary:       Clearwater - Sprout Libraries
Requires:      libevent ncurses zeromq net-snmp-libs net-snmp-agent-libs
AutoReq:       no

%package -n clearwater-bono
Summary:       Clearwater - Bono
Requires:      clearwater-sprout-libs
AutoReq:       no
%{?systemd_requires}

%package -n clearwater-restund
Summary:       Clearwater - restund
AutoReq:       no
%{?systemd_requires}

%package plugin-scscf
Summary:       Clearwater - Sprout S-CSCF Plugin
AutoReq:       no

%package plugin-icscf
Summary:       Clearwater - Sprout I-CSCF Plugin
AutoReq:       no

%package plugin-bgcf
Summary:       Clearwater - Sprout BGCF Plugin
AutoReq:       no

%package as-plugin-mmtel
Summary:       Clearwater - Sprout MMTEL Application Server Plugin
AutoReq:       no

%package as-plugin-gemini
Summary:       Clearwater - Sprout Gemini Application Server Plugin
AutoReq:       no

%package as-plugin-memento
Summary:       Clearwater - Sprout Memento Application Server Plugin
AutoReq:       no

%package as-plugin-call-diversion
Summary:       Clearwater - Sprout Call Diversion Application Server Plugin
AutoReq:       no

%package as-plugin-mangelwurzel
Summary:       Clearwater - Sprout Mangelwurzel Application Server Plugin
AutoReq:       no

%package -n clearwater-sipp
Summary:       Clearwater - SIPp
AutoReq:       no

%package -n clearwater-sip-stress
Summary:       Clearwater - SIP Stress Tests
AutoReq:       no
%{?systemd_requires}

%package -n clearwater-sip-stress-stats
Summary:       Clearwater - SPI Stress Tests Statistics
AutoReq:       no
%{?systemd_requires}

%package -n clearwater-sip-perf
Summary:       Clearwater - SIP Performance Tests
AutoReq:       no
%{?systemd_requires}

%package -n clearwater-node-sprout
Summary:       Clearwater Node - Sprout
Requires:      clearwater-sprout clearwater-infrastructure
AutoReq:       no

%package -n clearwater-node-bono
Summary:       Clearwater Node - Bono
Requires:      clearwater-bono clearwater-infrastructure
AutoReq:       no

%description
SIP router

%description libs
Sprout libraries

%description -n clearwater-bono
SIP edge proxy

%description -n clearwater-restund
STUN/TURN server

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

%description -n clearwater-sipp
Clearwater build of SIPp, used for running SIP stress and performance tests

%description -n clearwater-sip-stress
Runs SIP stress against Clearwater

%description -n clearwater-sip-stress-stats
Exposes SIP stress statistics over the Clearwater statistics interface.

%description -n clearwater-sip-perf
Runs SIP performance tests against Clearwater

%description -n clearwater-node-sprout
Clearwater Sprout node

%description -n clearwater-node-bono
Clearwater Bono node

%prep
%setup -q

%build
# Disable concurrent builds for some modules
sed --in-place '1ioverride MAKE = make' modules/pjsip/Makefile
sed --in-place '1ioverride MAKE = make' modules/openssl/Makefile.org

# Make sure that we don't run bison for libmemached
# (in CentOS it is too new and will generate broken source)
# (also note that using byacc instead introduces problems with other moduels)
sed --in-place 's/include libmemcached\/csl\/parser.am//' modules/libmemcached/libmemcached/csl/include.am

make MAKE="make --jobs=$(nproc)"

%install
# See: debian/sprout-base.install
mkdir --parents %{buildroot}/usr/share/clearwater/bin/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
mkdir --parents %{buildroot}/etc/cron.hourly/
cp build/bin/sprout %{buildroot}/usr/share/clearwater/bin/
cp --recursive sprout-base.root/* %{buildroot}/
rm %{buildroot}/etc/init.d/sprout
cp scripts/sprout-log-cleanup %{buildroot}/etc/cron.hourly/
cp modules/clearwater-etcd-plugins/sprout/sprout_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/sprout/sprout_scscf_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/sprout/sprout_enum_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/sprout/sprout_rph_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_access/scscf_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_access/enum_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_access/rph_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

# See: debian/sprout-libs.install
mkdir --parents %{buildroot}/usr/share/clearwater/sprout/lib/
cp usr/lib/*.so %{buildroot}/usr/share/clearwater/sprout/lib/
cp usr/lib/*.so.* %{buildroot}/usr/share/clearwater/sprout/lib/

# See: debian/bono.install
cp build/bin/sprout %{buildroot}/usr/share/clearwater/bin/bono
cp --recursive bono.root/* %{buildroot}/
cp scripts/bono-log-cleanup %{buildroot}/etc/cron.hourly/

# See: debian/restund.install
mkdir --parents %{buildroot}/usr/share/clearwater/restund/lib/
cp usr/sbin/restund %{buildroot}/usr/share/clearwater/bin/
cp usr/lib/libre.* %{buildroot}/usr/share/clearwater/restund/lib/
cp usr/lib/restund/modules/* %{buildroot}/usr/share/clearwater/restund/lib/
cp --recursive restund.root/* %{buildroot}/

# See: debian/sprout-scscf.install
mkdir --parents %{buildroot}/usr/share/clearwater/sprout/plugins
cp build/bin/sprout_scscf.so %{buildroot}/usr/share/clearwater/sprout/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/shared_ifcs_xml_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/fallback_ifcs_xml_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/remove_shared_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/remove_fallback_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/validate_shared_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/validate_fallback_ifcs_xml %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/display_shared_ifcs %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/display_fallback_ifcs %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/
cp modules/clearwater-etcd-plugins/clearwater_config_manager/scripts/config_validation/* %{buildroot}/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/
cp modules/clearwater-etcd-plugins/clearwater_config_access/shared_ifcs_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_access/fallback_ifcs_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

# See: debian/sprout-icscf.install
cp build/bin/sprout_icscf.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/sprout-bgcf.install
cp build/bin/sprout_bgcf.so %{buildroot}/usr/share/clearwater/sprout/plugins/
cp --recursive sprout-bgcf.root/* %{buildroot}/
cp modules/clearwater-etcd-plugins/sprout/sprout_bgcf_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp modules/clearwater-etcd-plugins/clearwater_config_access/bgcf_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

# See: debian/sprout-mmtel-as.install
cp build/bin/sprout_mmtel_as.so %{buildroot}/usr/share/clearwater/sprout/plugins/
cp --recursive sprout-mmtel-as.root/* %{buildroot}/

# See: debian/gemini-as.install
cp build/bin/gemini-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/memento-as.install
cp build/bin/memento-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/
cp --recursive memento-as.root/* %{buildroot}/

# See: debian/call-diversion-as.install
cp build/bin/call-diversion-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/mangelwurzel-as.install
cp build/bin/mangelwurzel-as.so %{buildroot}/usr/share/clearwater/sprout/plugins/

# See: debian/clearwater-sipp.install
cp --recursive clearwater-sipp.root/* %{buildroot}/
cp modules/sipp/sipp %{buildroot}/usr/share/clearwater/bin/

# See: debian/clearwater-sip-stress.install
cp --recursive clearwater-sip-stress.root/* %{buildroot}/

# See: debian/clearwater-sip-stress-stats.install
mkdir --parents %{buildroot}/usr/share/clearwater/gems/
cp scripts/sipp-stats/clearwater-sipp-stats-*.gem %{buildroot}/usr/share/clearwater/gems/

# See: debian/clearwater-sip-perf.install
cp --recursive clearwater-sip-perf.root/* %{buildroot}/

# systemd
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
cp %{SOURCE2} %{buildroot}%{_unitdir}/sprout.service
cp %{SOURCE3} %{buildroot}/lib/systemd/scripts/sprout.sh
cp %{SOURCE4} %{buildroot}%{_unitdir}/bono.service
cp %{SOURCE5} %{buildroot}/lib/systemd/scripts/bono.sh
cp %{SOURCE6} %{buildroot}%{_unitdir}/restund.service
cp %{SOURCE7} %{buildroot}/lib/systemd/scripts/restund.sh
cp %{SOURCE8} %{buildroot}%{_unitdir}/clearwater-sip-stress.service
cp %{SOURCE9} %{buildroot}/lib/systemd/scripts/clearwater-sip-stress.sh
cp %{SOURCE10} %{buildroot}%{_unitdir}/clearwater-sip-stress-stats.service
cp %{SOURCE11} %{buildroot}/lib/systemd/scripts/clearwater-sip-stress-stats.sh
cp %{SOURCE12} %{buildroot}%{_unitdir}/clearwater-sip-perf.service
cp %{SOURCE13} %{buildroot}/lib/systemd/scripts/clearwater-sip-perf.sh

sed --in-place 's/\/etc\/init.d\/sprout/service sprout/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/sprout.monit
sed --in-place 's/reload clearwater-monit/service reload clearwater-monit/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/sprout.monit
sed --in-place 's/\/etc\/init.d\/bono/service bono/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/bono.monit
sed --in-place 's/reload clearwater-monit/service reload clearwater-monit/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/bono.monit
sed --in-place 's/\/etc\/init.d\/restund/service restund/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/restund
sed --in-place 's/reload clearwater-monit/service reload clearwater-monit/g' %{buildroot}/usr/share/clearwater/infrastructure/scripts/restund

#mkdir --parents %{buildroot}%{_initrddir}/
#cp debian/bono.init.d %{buildroot}%{_initrddir}/bono
#cp debian/restund.init.d %{buildroot}%{_initrddir}/restund
#cp debian/clearwater-sip-stress.init.d %{buildroot}%{_initrddir}/clearwater-sip-stress
#cp debian/clearwater-sip-stress-stats.init.d %{buildroot}%{_initrddir}/clearwater-sip-stress-stats
#cp debian/clearwater-sip-perf.init.d %{buildroot}%{_initrddir}/clearwater-sip-perf

%files
%attr(644,-,-) %{_unitdir}/sprout.service
%attr(755,-,-) /lib/systemd/scripts/sprout.sh
%attr(755,-,-) /usr/share/clearwater/bin/sprout
%attr(755,-,-) /usr/share/clearwater/bin/poll_sprout_http.sh
%attr(755,-,-) /usr/share/clearwater/bin/poll_sprout_sip.sh
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/enum_schema.json
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/rph_schema.json
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/rph_validation.py
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/scscf_schema.json
%attr(755,-,-) /usr/share/clearwater/clearwater-diags-monitor/scripts/sprout_base_diags
/usr/share/clearwater/infrastructure/alarms/sprout_alarms.json
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_stability/sprout-stability
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_uptime/check-sprout-uptime
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/reload/fallback_ifcs_xml/sprout_reload
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/reload/memcached/sprout_reload
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/reload/shared_ifcs_xml/sprout_reload
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/sprout_restart
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/create-analytics-syslog-config
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/create-sprout-nginx-config
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/sprout.monit
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_json_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_scscf_json_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_enum_json_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_rph_json_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/scscf_json_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/enum_json_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/rph_json_config_plugin.py*
/etc/clearwater/logging/sprout
/etc/logrotate.d/sproutanalytics
/etc/security/limits.conf.sprout
%attr(755,-,-) /etc/cron.hourly/sprout-log-cleanup
%ghost /etc/monit/conf.d/sprout.monit

%files libs
/usr/share/clearwater/sprout/lib/

%files -n clearwater-bono
%attr(644,-,-) %{_unitdir}/bono.service
%attr(755,-,-) /lib/systemd/scripts/bono.sh
%attr(755,-,-) /usr/share/clearwater/bin/bono
%attr(755,-,-) /usr/share/clearwater/bin/poll_bono.sh
%attr(755,-,-) /usr/share/clearwater/clearwater-diags-monitor/scripts/bono_diags
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/bono_restart
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/bono.monit
/etc/clearwater/logging/bono
/etc/security/limits.conf.bono
%attr(755,-,-) /etc/cron.hourly/bono-log-cleanup
%ghost /etc/monit/conf.d/bono.monit

%files -n clearwater-restund
%attr(644,-,-) %{_unitdir}/restund.service
%attr(755,-,-) /lib/systemd/scripts/restund.sh
%attr(755,-,-) /usr/share/clearwater/bin/restund
/usr/share/clearwater/restund/lib/
%attr(755,-,-) /usr/share/clearwater/bin/poll_restund.sh
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restund
/etc/security/limits.conf.restund
%ghost /etc/monit/conf.d/restund.monit

%files plugin-scscf
/usr/share/clearwater/sprout/plugins/sprout_scscf.so
/usr/share/clearwater/clearwater-config-manager/plugins/shared_ifcs_xml_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/fallback_ifcs_xml_plugin.py*
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/remove_shared_ifcs_xml
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/remove_fallback_ifcs_xml
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/validate_shared_ifcs_xml
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/validate_fallback_ifcs_xml
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/display_shared_ifcs
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/display_fallback_ifcs
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/config_validation/
/usr/share/clearwater/clearwater-config-access/plugins/shared_ifcs_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/fallback_ifcs_config_plugin.py*

%files plugin-icscf
/usr/share/clearwater/sprout/plugins/sprout_icscf.so

%files plugin-bgcf
/usr/share/clearwater/sprout/plugins/sprout_bgcf.so
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/bgcf_schema.json
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/print-bgcf-configuration
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/upload_bgcf_json
/usr/share/clearwater/clearwater-config-manager/plugins/sprout_bgcf_json_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/bgcf_json_config_plugin.py*

%files as-plugin-mmtel
/usr/share/clearwater/sprout/plugins/sprout_mmtel_as.so
%attr(755,-,-) /usr/share/clearwater/clearwater-diags-monitor/scripts/sprout_mmtel_as_diags

%files as-plugin-gemini
/usr/share/clearwater/sprout/plugins/gemini-as.so

%files as-plugin-memento
/usr/share/clearwater/sprout/plugins/memento-as.so
/usr/share/clearwater/infrastructure/alarms/memento_as_alarms.json

%files as-plugin-call-diversion
/usr/share/clearwater/sprout/plugins/call-diversion-as.so

%files as-plugin-mangelwurzel
/usr/share/clearwater/sprout/plugins/mangelwurzel-as.so

%files -n clearwater-sipp
/etc/sysctl.conf.clearwater-sipp
%attr(755,-,-) /usr/share/clearwater/bin/sipp

%files -n clearwater-sip-stress
%attr(644,-,-) %{_unitdir}/clearwater-sip-stress.service
%attr(755,-,-) /lib/systemd/scripts/clearwater-sip-stress.sh
%attr(755,-,-) /usr/share/clearwater/bin/sip-stress
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/sip-stress
/usr/share/clearwater/sip-stress/sip-stress.xml
%attr(755,-,-) /etc/cron.hourly/clearwater-sip-stress-log-cleanup

%files -n clearwater-sip-stress-stats
%attr(644,-,-) %{_unitdir}/clearwater-sip-stress-stats.service
%attr(755,-,-) /lib/systemd/scripts/clearwater-sip-stress-stats.sh
/usr/share/clearwater/gems/clearwater-sipp-stats-*.gem

%files -n clearwater-sip-perf
%attr(644,-,-) %{_unitdir}/clearwater-sip-perf.service
%attr(755,-,-) /lib/systemd/scripts/clearwater-sip-perf.sh
%attr(755,-,-) /usr/share/clearwater/bin/sip-perf
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/sip-perf
/usr/share/clearwater/sip-perf/sip-perf.xml

%files -n clearwater-node-sprout
/usr/share/clearwater/node_type.d/20_sprout

%files -n clearwater-node-bono
/usr/share/clearwater/node_type.d/20_bono

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/sprout-base.postinst
cw_create_user sprout
cw_create_log_dir sprout
cw_add_security_limits sprout
%systemd_post sprout.service
cw_activate sprout

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/sprout-base.prerm
%systemd_preun sprout.service
cw_deactivate sprout
if [ "$1" = 0 ]; then # Uninstall
  cw_remove_user sprout
  cw_remove_log_dir sprout
fi
cw_remove_security_limits sprout

%postun
%systemd_postun_with_restart sprout.service

%post -n clearwater-bono -p /bin/bash
%include %{SOURCE1}
# See: debian/bono.postinst
cw_create_user bono
cw_create_log_dir bono
cw_add_security_limits bono
%systemd_post bono.service
cw_activate bono

%preun -n clearwater-bono -p /bin/bash
%include %{SOURCE1}
# See: debian/bono.prerm
%systemd_preun bono.service
cw_deactivate bono
if [ "$1" = 0 ]; then # Uninstall
  cw_remove_user bono
  cw_remove_log_dir bono
fi
cw_remove_security_limits bono

%postun -n clearwater-bono
%systemd_postun_with_restart bono.service

%post -n clearwater-restund -p /bin/bash
%include %{SOURCE1}
# See: debian/restund.postinst
cw_create_user restund
cw_create_log_dir restund
cw_add_security_limits restund
%systemd_post restund.service
cw_activate restund

%preun -n clearwater-restund -p /bin/bash
%include %{SOURCE1}
# See: debian/restund.prerm
%systemd_preun restund.service
cw_deactivate restund
if [ "$1" = 0 ]; then # Uninstall
  cw_remove_user restund
  cw_remove_log_dir restund
fi
cw_remove_security_limits restund

%postun -n clearwater-restund
%systemd_postun_with_restart restund.service

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

%post -n clearwater-sip-stress -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-sip-stress.postinst
/usr/share/clearwater/infrastructure/scripts/sip-stress
service_action clearwater-sip-stress start
%systemd_post clearwater-sip-stress.service

%preun -n clearwater-sip-stress
%systemd_preun clearwater-sip-stress.service

%postun -n clearwater-sip-stress
%systemd_postun_with_restart clearwater-sip-stress.service

%post -n clearwater-sip-stress-stats -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-sip-stress-stats.postinst
gem install /usr/share/clearwater/gems/clearwater-sipp-stats-1.0.0.gem --no-ri --no-rdoc
service_action clearwater-sip-stress-stats start
%systemd_post clearwater-sip-stress-stats.service

%preun -n clearwater-sip-stress-stats
%systemd_preun clearwater-sip-stress-stats.service

%postun -n clearwater-sip-stress-stats
%systemd_postun_with_restart clearwater-sip-stress-stats.service

%post -n clearwater-sip-perf -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-sip-perf.postinst
/usr/share/clearwater/infrastructure/scripts/sip-perf
%systemd_post clearwater-sip-perf.service

%preun -n clearwater-sip-perf
%systemd_preun clearwater-sip-perf.service

%postun -n clearwater-sip-perf
%systemd_postun_with_restart clearwater-sip-perf.service
