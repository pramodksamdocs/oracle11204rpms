%define debug_packages  %{nil}
%define debug_package %{nil}
%define curloc 11.2.0.4
%define inventory /opt/app/oraInventory
%define base /opt/app/oracle
%define home /opt/app/oracle/product/11.2.0.4
%define LOG_FILE /var/opt/MFSoradb11204.log
%define oracle_stage /var//opt/dbinstall
%define RPM_BUILD_DIR /root/rpmbuild/BUILD
Name: oracle-db-112040
Version: 0.01
Release: 1.el7
Summary: Oracle Database 11.2.0.4 in a RPM
Vendor: Oracle Corp.
Group: Applications/Databases
License: Proprietary
URL: https://www.amdocs.com/
Source0: p13390677_112040_Linux-x86-64_1of7.zip
source1: p13390677_112040_Linux-x86-64_2of7.zip
Prefix: %{base}
AutoReqProv: no

BuildRequires: redhat-rpm-config

Conflicts:kernel-utils
Obsoletes:kernel-utils

%description
Oracle Database 11.2.0.4 Enterprise Edition is Oracle Flagship Database Server.
The release included in this RPM requires you have purchased the appropriate
License from Oracle.

%files


%prep

%setup -n oracle
mkdir -p /var/opt/dbinstall/
cp -rpf %{RPM_BUILD_DIR}/oracle /var/opt/dbinstall/
chown -R oracle:dba /var/opt/dbinstall/*
exit

%pre

DISPCHK=`printenv DISPLAY`

if [ ! -z "$DISPCHK" ]; then
  echo "*** Exiting the installation! ***" | tee -a $LOG_FILE
  echo "Ensure the DISPLAY enviroment variable is not set before installing" | tee -a $LOG_FILE
  echo "this package. The DISPLAY variable can be set automatically through" | tee -a $LOG_FILE
  echo "a program such as PUTTY through SSH X11 configuration." | tee -a $LOG_FILE
  exit 1;
fi

%build

%install
rm -rf $RPM_BUILD_ROOT

%post
cat /etc/passwd | grep oracle > /dev/null;
if [ $? -gt 0 ] ; then
  echo >> /var/opt/MFSoradb11204.log
  echo "Creating oracle unix account" >> /var/opt/MFSoradb11204.log
  # create user accounts and prompt for password
  mkdir -p /opt/app/oracle/product/11.2.0.4
  mkdir -p /opt/app/oracle
  groupadd -g 501 dba
  groupadd -g 500 oinstall
  useradd -g dba -G oinstall -d /opt/app/oracle -s /bin/bash -p $(echo mypasswd | openssl passwd -1 -stdin) oracle
  chown -R oracle:dba /opt/app/oracle
else
  echo >> /var/opt/MFSoradb11204.log
  echo "User oracle not created, it already exists" >> /var/opt/MFSoradb11204.log
fi

echo "inventory_loc=%{inventory}" >/etc/oraInst.loc;
echo "inst_group=dba" >>/etc/oraInst.loc;
mkdir -p %{inventory};
chown oracle:dba %{inventory}/..;
chown oracle:dba %{inventory};
chmod 664 /etc/oraInst.loc;
chown oracle:dba /etc/oraInst.loc;

ORACLE_HOME=/opt/app/oracle/product/11.2.0.4
ORACLE_BASE=/opt/app/oracle


/usr/bin/echo "Installing  the oracle database 11.2.0.4.0 home now to $ORACLE_HOME";
/usr/bin/mkdir -p $ORACLE_HOME;

su - oracle -c "/var/opt/dbinstall/db/runInstaller -silent -waitforcompletion -responseFile /stage/db_install.rsp -force" >> /var/opt/MFSoradb11204.log;

%clean

