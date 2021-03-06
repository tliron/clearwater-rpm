Name:          clearwater-etcd
Version:       129
Release:       1%{?dist}
License:       GPLv3+
URL:           https://github.com/Metaswitch/clearwater-etcd

Source0:       %{name}-%{version}.tar.bz2
Source1:       housekeeping.sh
Source2:       clearwater-etcd.service
Source3:       clearwater-etcd.sh
Source4:       clearwater-cluster-manager.service
Source5:       clearwater-cluster-manager.sh
Source6:       clearwater-cluster-manager.rules
Source7:       clearwater-queue-manager.service
Source8:       clearwater-queue-manager.sh
Source9:       clearwater-queue-manager.rules
Source10:      clearwater-config-manager.service
Source11:      clearwater-config-manager.sh
Source12:      clearwater-config-manager.rules

BuildRequires: make python-virtualenv gcc-c++ ccache
BuildRequires: libffi-devel
BuildRequires: systemd

%global debug_package %{nil}

Summary:       Clearwater - etcd
Requires:      nmap-ncat
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-infrastructure clearwater-monit clearwater-log-cleanup

%package -n clearwater-cluster-manager
Summary:       Clearwater - Cluster Manager
Requires:      python-virtualenv libffi
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-etcd clearwater-monit

%package -n clearwater-queue-manager
Summary:       Clearwater - Queue Manager
Requires:      python-virtualenv libffi
AutoReq:       no
%{?systemd_requires}
#Requires:      clearwater-etcd clearwater-monit

%package -n clearwater-config-manager
Summary:       Clearwater - Config Manager
Requires:      python-virtualenv libffi
AutoReq:       no
%{?systemd_requires}
#Requires:      python2-pip python2-requests python2-jsonschema
#Requires:      clearwater-etcd clearwater-queue-manager clearwater-monit

%package -n clearwater-clustering
Summary:       Clearwater - Clustering
Requires:      clearwater-etcd clearwater-cluster-manager clearwater-queue-manager
Requires:      clearwater-config-manager
AutoReq:       no

%description
etcd configured for Clearwater

%description -n clearwater-cluster-manager
cluster manager

%description -n clearwater-queue-manager
queue manager

%description -n clearwater-config-manager
config manager

%description -n clearwater-clustering
clustering

%prep
%setup -q

%build
make env MAKE="make --jobs=$(nproc)"

%install
# See: debian/clearwater-etcd.install
cp --recursive clearwater-etcd/* %{buildroot}/

# See: debian/clearwater-cluster-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/.wheelhouse/
cp cluster_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/.wheelhouse/
cp --recursive clearwater-cluster-manager.root/* %{buildroot}/

# See: debian/clearwater-queue-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/
cp queue_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-queue-manager/.wheelhouse/
cp --recursive clearwater-queue-manager.root/* %{buildroot}/
cp src/clearwater_etcd_plugins/clearwater_queue_manager/apply_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-queue-manager/plugins/

# See: debian/clearwater-config-manager.install
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/.wheelhouse/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
mkdir --parents %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp config_mgr_wheelhouse/* %{buildroot}/usr/share/clearwater/clearwater-config-manager/.wheelhouse/
cp --recursive clearwater-config-manager.root/* %{buildroot}/
cp src/clearwater_etcd_plugins/clearwater_config_manager/shared_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_manager/dns_json_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-manager/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_access/shared_config_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/
cp src/clearwater_etcd_plugins/clearwater_config_access/dns_json_config_plugin.py %{buildroot}/usr/share/clearwater/clearwater-config-access/plugins/

# Fix pid files
sed --in-place 's/\/var\/run\/clearwater-cluster-manager.pid/\/var\/run\/clearwater-cluster-manager\/clearwater-cluster-manager.pid/g' %{buildroot}/usr/share/clearwater/conf/clearwater-cluster-manager.monit 
sed --in-place 's/\/var\/run\/clearwater-config-manager.pid/\/var\/run\/clearwater-config-manager\/clearwater-config-manager.pid/g' %{buildroot}/usr/share/clearwater/conf/clearwater-config-manager.monit 
sed --in-place 's/\/var\/run\/clearwater-queue-manager.pid/\/var\/run\/clearwater-queue-manager\/clearwater-queue-manager.pid/g' %{buildroot}/usr/share/clearwater/conf/clearwater-queue-manager.monit 
sed --in-place 's/\/var\/run\/clearwater-queue-manager.pid/\/var\/run\/clearwater-queue-manager\/clearwater-queue-manager.pid/g' %{buildroot}/usr/share/clearwater/infrastructure/monit_uptime/check-queue-manager-uptime 

# systemd
mkdir --parents %{buildroot}%{_unitdir}/
mkdir --parents %{buildroot}/lib/systemd/scripts/
cp %{SOURCE2} %{buildroot}%{_unitdir}/clearwater-etcd.service
cp %{SOURCE3} %{buildroot}/lib/systemd/scripts/clearwater-etcd.sh
cp %{SOURCE4} %{buildroot}%{_unitdir}/clearwater-cluster-manager.service
cp %{SOURCE5} %{buildroot}/lib/systemd/scripts/clearwater-cluster-manager.sh
cp %{SOURCE7} %{buildroot}%{_unitdir}/clearwater-queue-manager.service
cp %{SOURCE8} %{buildroot}/lib/systemd/scripts/clearwater-queue-manager.sh
cp %{SOURCE10} %{buildroot}%{_unitdir}/clearwater-config-manager.service
cp %{SOURCE11} %{buildroot}/lib/systemd/scripts/clearwater-config-manager.sh

sed --in-place 's/\/etc\/init.d\/clearwater-etcd/service clearwater-etcd/g' %{buildroot}/usr/share/clearwater/conf/clearwater-etcd.monit
sed --in-place 's/\/etc\/init.d\/clearwater-cluster-manager/service clearwater-cluster-manager/g' %{buildroot}/usr/share/clearwater/conf/clearwater-cluster-manager.monit
sed --in-place 's/\/etc\/init.d\/clearwater-queue-manager/service clearwater-queue-manager/g' %{buildroot}/usr/share/clearwater/conf/clearwater-queue-manager.monit
sed --in-place 's/\/etc\/init.d\/clearwater-config-manager/service clearwater-config-manager/g' %{buildroot}/usr/share/clearwater/conf/clearwater-config-manager.monit
sed --in-place 's/\/etc\/init.d\/cassandra/\/lib\/systemd\/scripts\/clearwater-cassandra.sh/g' %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster.py
sed --in-place 's/\/etc\/init.d\/chronos/\/lib\/systemd\/scripts\/chronos.sh/g' %{buildroot}/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster.py
# TODO: this must be fixed when we fix clearwater-memcached
#%{buildroot}/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster.py

#mkdir --parents %{buildroot}%{_initrddir}/
#cp debian/clearwater-etcd.init.d %{buildroot}%{_initrddir}/clearwater-etcd
#cp debian/clearwater-cluster-manager.init.d %{buildroot}%{_initrddir}/clearwater-cluster-manager
#cp debian/clearwater-queue-manager.init.d %{buildroot}%{_initrddir}/clearwater-queue-manager
#cp debian/clearwater-config-manager.init.d %{buildroot}%{_initrddir}/clearwater-config-manager

# polkit
mkdir --parents %{buildroot}/etc/polkit-1/rules.d/
cp %{SOURCE6} %{buildroot}/etc/polkit-1/rules.d/99-clearwater-cluster-manager.rules
cp %{SOURCE9} %{buildroot}/etc/polkit-1/rules.d/99-clearwater-queue-manager.rules
cp %{SOURCE12} %{buildroot}/etc/polkit-1/rules.d/99-clearwater-config-manager.rules

%files
%attr(644,-,-) %{_unitdir}/clearwater-etcd.service
%attr(755,-,-) /lib/systemd/scripts/clearwater-etcd.sh
%attr(755,-,-) /usr/bin/clearwater-etcdctl
%attr(755,-,-) /usr/share/clearwater/bin/poll_etcd.sh
%attr(755,-,-) /usr/share/clearwater/bin/get_etcd_initial_cluster.py
%attr(755,-,-) /usr/share/clearwater/bin/poll_etcd_cluster.sh
%attr(755,-,-) /usr/share/clearwater/bin/raise_etcd_cluster_alarm.sh
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/scripts/save_etcd_config.py
/usr/share/clearwater/clearwater-etcd/scripts/save_etcd_config.pyc
/usr/share/clearwater/clearwater-etcd/scripts/save_etcd_config.pyo
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/scripts/wait_for_etcd
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/scripts/load_etcd_config.py
/usr/share/clearwater/clearwater-etcd/scripts/load_etcd_config.pyc
/usr/share/clearwater/clearwater-etcd/scripts/load_etcd_config.pyo
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/scripts/load_etcd_config
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/scripts/save_etcd_config
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/2.2.5/etcd-dump-logs
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/2.2.5/etcdctl
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/2.2.5/etcdwrapper
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/2.2.5/etcd
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/3.1.7/etcd-dump-logs
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/3.1.7/etcdctl
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/3.1.7/etcdwrapper
%attr(755,-,-) /usr/share/clearwater/clearwater-etcd/3.1.7/etcd
/usr/share/clearwater/infrastructure/alarms/clearwater_etcd_alarms.json
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_uptime/check-etcd-uptime
/usr/share/clearwater/conf/clearwater-etcd.monit
/etc/logrotate.d/clearwater-etcd
%ghost /var/lib/clearwater-etcd/
%ghost /etc/monit/conf.d/clearwater-etcd.monit

%files -n clearwater-cluster-manager
%attr(644,-,-) %{_unitdir}/clearwater-cluster-manager.service
%attr(644,-,-) /etc/polkit-1/rules.d/99-clearwater-cluster-manager.rules
%attr(755,-,-) /lib/systemd/scripts/clearwater-cluster-manager.sh
/usr/share/clearwater/clearwater-cluster-manager/.wheelhouse/
%attr(755,-,-) /usr/share/clearwater/bin/clearwater-cluster-manager
%attr(755,-,-) /usr/share/clearwater/infrastructure/scripts/restart/clearwater_cluster_manager_restart
/usr/share/clearwater/infrastructure/alarms/clearwater_cluster_manager_alarms.json
%attr(755,-,-) /usr/share/clearwater/clearwater-cluster-manager/scripts/recreate_homestead_cluster
%attr(755,-,-) /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_remote_node_failed
%attr(755,-,-) /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster
/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_chronos_cluster.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster.py*
%attr(755,-,-) /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed
%attr(755,-,-) /usr/share/clearwater/clearwater-cluster-manager/scripts/force_etcd_state
/usr/share/clearwater/clearwater-cluster-manager/scripts/recreate_cluster.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster.py*
%attr(755,-,-) /usr/share/clearwater/clearwater-cluster-manager/scripts/dump_etcd_state
%attr(755,-,-) /usr/share/clearwater/clearwater-cluster-manager/scripts/recreate_sprout_cluster
/usr/share/clearwater/clearwater-cluster-manager/scripts/dump_etcd_state.py*
%attr(755,-,-) /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_memcached_cluster
%attr(755,-,-) /usr/share/clearwater/clearwater-cluster-manager/scripts/load_from_cassandra_cluster
%attr(755,-,-) /usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state
/usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state.py*
/usr/share/clearwater/clearwater-cluster-manager/scripts/force_etcd_state.py*
/usr/share/clearwater/conf/clearwater-cluster-manager.monit
/etc/logrotate.d/clearwater-cluster-manager
%attr(755,-,-) /etc/cron.hourly/clearwater-cluster-manager-log-cleanup
%ghost /usr/share/clearwater/clearwater-cluster-manager/env/
%ghost /etc/monit/conf.d/clearwater-cluster-manager.monit

%files -n clearwater-queue-manager
%attr(644,-,-) %{_unitdir}/clearwater-queue-manager.service
%attr(755,-,-) /lib/systemd/scripts/clearwater-queue-manager.sh
%attr(644,-,-) /etc/polkit-1/rules.d/99-clearwater-queue-manager.rules
/usr/share/clearwater/clearwater-queue-manager/.wheelhouse/
/usr/share/clearwater/clearwater-queue-manager/plugins/apply_config_plugin.py*
%attr(755,-,-) /usr/share/clearwater/bin/clearwater-queue-manager
/usr/share/clearwater/infrastructure/alarms/clearwater_queue_manager_alarms.json
%attr(755,-,-) /usr/share/clearwater/infrastructure/monit_uptime/check-queue-manager-uptime
%attr(755,-,-) /usr/share/clearwater/clearwater-queue-manager/scripts/get_apply_config_key
%attr(755,-,-) /usr/share/clearwater/clearwater-queue-manager/scripts/modify_nodes_in_queue
%attr(755,-,-) /usr/share/clearwater/clearwater-queue-manager/scripts/check_restart_queue_state
%attr(755,-,-) /usr/share/clearwater/clearwater-queue-manager/scripts/force_restart_queue_state
/usr/share/clearwater/clearwater-queue-manager/scripts/force_queue_state.py*
/usr/share/clearwater/clearwater-queue-manager/scripts/check_node_health.py*
/usr/share/clearwater/clearwater-queue-manager/scripts/check_queue_state.py*
/usr/share/clearwater/clearwater-queue-manager/scripts/modify_nodes_in_queue.py*
/usr/share/clearwater/conf/clearwater-queue-manager.monit
%attr(755,-,-) /etc/cron.hourly/clearwater-queue-manager-log-cleanup
%ghost /usr/share/clearwater/clearwater-queue-manager/env/
%ghost /etc/monit/conf.d/clearwater-queue-manager.monit

%files -n clearwater-config-manager
%attr(644,-,-) %{_unitdir}/clearwater-config-manager.service
%attr(755,-,-) /lib/systemd/scripts/clearwater-config-manager.sh
%attr(644,-,-) /etc/polkit-1/rules.d/99-clearwater-config-manager.rules
/usr/share/clearwater/clearwater-config-manager/.wheelhouse/
/usr/share/clearwater/clearwater-config-manager/plugins/shared_config_plugin.py*
/usr/share/clearwater/clearwater-config-manager/plugins/dns_json_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/shared_config_config_plugin.py*
/usr/share/clearwater/clearwater-config-access/plugins/dns_json_config_plugin.py*
%attr(755,-,-) /usr/share/clearwater/bin/clearwater-config-manager
/usr/share/clearwater/infrastructure/alarms/clearwater_config_manager_alarms.json
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/print-dns-configuration
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/cw-config
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/upload_generic_json
/usr/share/clearwater/clearwater-config-manager/scripts/validate_json.py*
/usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync.py*
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/restore_config
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/backup_config
/usr/share/clearwater/clearwater-config-manager/scripts/config_validation/dns_schema.json
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/print-s-cscf-configuration
%attr(755,-,-) /usr/share/clearwater/clearwater-config-manager/scripts/print-enum-configuration
/usr/share/clearwater/conf/clearwater-config-manager.monit
/etc/rsyslog.d/35-config-manager.conf
/etc/logrotate.d/clearwater-config-manager
%attr(755,-,-) /etc/cron.hourly/clearwater-config-manager-log-cleanup
%ghost /usr/share/clearwater/clearwater-config-manager/env/
%ghost /etc/monit/conf.d/clearwater-config-manager.monit

%files -n clearwater-clustering

%post -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-etcd.postinst
cw_create_user clearwater-etcd
cw_create_log_dir clearwater-etcd
mkdir --parents /var/lib/clearwater-etcd/
chown --recursive clearwater-etcd /var/lib/clearwater-etcd/
%systemd_post clearwater-etcd.service
cw_activate clearwater-etcd

%preun -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-etcd.prerm
%systemd_preun clearwater-etcd.service
cw_deactivate clearwater-etcd
if [ "$1" = 0 ]; then # Uninstall
  cw_remove_user clearwater-etcd
  cw_remove_log_dir clearwater-etcd
fi

%postun
%systemd_postun_with_restart clearwater-etcd.service

%post -n clearwater-cluster-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-cluster-manager.links
ln --symbolic /usr/share/clearwater/clearwater-cluster-manager/scripts/check_cluster_state /usr/bin/cw-check_cluster_state
ln --symbolic /usr/share/clearwater/clearwater-cluster-manager/scripts/mark_node_failed /usr/sbin/cw-mark_node_failed

# See: debian/clearwater-cluster-manager.postinst
cw_create_user clearwater-cluster-manager
cw_create_log_dir clearwater-cluster-manager adm
cw_create_virtualenv clearwater-cluster-manager
%systemd_post clearwater-cluster-manager.service
cw_activate clearwater-cluster-manager

%preun -n clearwater-cluster-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-cluster-manager.prerm
%systemd_preun clearwater-cluster-manager.service
cw_deactivate clearwater-cluster-manager
cw_remove_virtualenv clearwater-cluster-manager
if [ "$1" = 0 ]; then # Uninstall
  cw_remove_user clearwater-cluster-manager
  cw_remove_log_dir clearwater-cluster-manager
fi

# See: debian/clearwater-cluster-manager.links
rm --force /usr/bin/cw-check_cluster_state
rm --force /usr/sbin/cw-mark_node_failed

%postun -n clearwater-cluster-manager
%systemd_postun_with_restart clearwater-cluster-manager.service

%post -n clearwater-queue-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-queue-manager.links
ln --symbolic /usr/share/clearwater/clearwater-queue-manager/scripts/check_restart_queue_state /usr/bin/cw-check_restart_queue_state

# See: debian/clearwater-queue-manager.postinst
cw_create_user clearwater-queue-manager
cw_create_log_dir clearwater-queue-manager adm
cw_create_virtualenv clearwater-queue-manager
%systemd_post clearwater-queue-manager.service
cw_activate clearwater-queue-manager

%preun -n clearwater-queue-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-queue-manager.prerm
%systemd_preun clearwater-queue-manager.service
cw_deactivate clearwater-queue-manager
cw_remove_virtualenv clearwater-queue-manager
if [ "$1" = 0 ]; then # Uninstall
  cw_remove_user clearwater-queue-manager
  cw_remove_log_dir clearwater-queue-manager
fi

# See: debian/clearwater-queue-manager.links
rm --force /usr/bin/cw-check_restart_queue_state

%postun -n clearwater-queue-manager
%systemd_postun_with_restart clearwater-queue-manager.service

%post -n clearwater-config-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-config-manager.links
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/cw-config /usr/bin/cw-config
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/restore_config /usr/bin/cw-restore_config
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/check_config_sync /usr/sbin/cw-check_config_sync
ln --symbolic /usr/share/clearwater/clearwater-config-manager/scripts/backup_config /usr/sbin/cw-backup_config

# See: debian/clearwater-config-manager.postinst
cw_create_user clearwater-config-manager
cw_create_log_dir clearwater-config-manager adm
cw_create_virtualenv clearwater-config-manager
%systemd_post clearwater-config-manager.service
cw_activate clearwater-config-manager

%preun -n clearwater-config-manager -p /bin/bash
%include %{SOURCE1}
# See: debian/clearwater-config-manager.prerm
%systemd_preun clearwater-config-manager.service
cw_deactivate clearwater-config-manager
cw_remove_virtualenv clearwater-config-manager
if [ "$1" = 0 ]; then # Uninstall
  cw_remove_user clearwater-config-manager
  cw_remove_log_dir clearwater-config-manager
fi

# See: debian/clearwater-config-manager.links
rm --force /usr/bin/cw-config
rm --force /usr/bin/cw-restore_config
rm --force /usr/sbin/cw-check_config_sync
rm --force /usr/sbin/cw-backup_config

%postun -n clearwater-config-manager
%systemd_postun_with_restart clearwater-config-manager.service
