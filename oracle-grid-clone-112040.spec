%define curloc 11.2.0.4
%define inventory /opt/app/oracle/oraInventory
%define base /opt/app/oracle
%define home oragrid/11.2.0.4
Name: oracle-grid-clone-112040
Version: 0.1
Release: 1.ol7
Summary: Oracle Database 11.2.0.4 in a RPM
Vendor: Oracle Corp.
Group: Applications/Databases
License: Proprietary
URL: https://www.amdocs.com/
Source0: 11.2.0.4_grid.tar.gz
Prefix: %{base}
AutoReqProv: no
%description
Oracle Database 11.2.0.4 Enterprise Edition is Oracle Flagship Database Server.
The release included in this RPM requires you have purchased the appropriate
License from Oracle.

%files
%defattr(-,root,root,-)

%post
ORACLE_HOME=/opt/app/oragrid/11.2.0.4
ORACLE_BASE=/opt/app/oracle

if [ -d "$ORACLE_HOME" ]; then
        /usr/bin/echo "ORACLE_HOME directory $ORACLE_HOME exists-aborting";
        exit 127
fi

/usr/bin/echo "cloning the oracle grid  home now to $ORACLE_HOME"
/usr/bin/mkdir -p $ORACLE_HOME



/usr/bin/tar --gzip -xf /stage/11.2.0.4_grid.tar.gz -C /opt/app/oragrid/

/usr/bin/chown -R oracle:dba /opt

/usr/bin/su - oracle -c "cd $ORACLE_HOME/clone/bin && ./clone.pl ORACLE_HOME=$ORACLE_HOME ORACLE_BASE=$ORACLE_BASE -defaultHomeName"

$ORACLE_HOME/root.sh
