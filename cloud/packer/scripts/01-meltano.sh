#!/bin/bash
#
# Scripts in this directory are run during the build process.
# each script will be uploaded to /tmp on your build droplet,
# given execute permissions and run.  The cleanup process will
# remove the scripts from your build system after they have run
# if you use the build_image task.
#
# fail on any error
set -e

MELTANO_USER=meltano
MELTANO_ROOT=/var/meltano
MELTANO_VENV=$MELTANO_ROOT/.venv

# setup the meltano root
mkdir -p $MELTANO_ROOT
chown $MELTANO_USER:$MELTANO_USER $MELTANO_ROOT

sudo -H -u $MELTANO_USER python3 -m venv $MELTANO_VENV
sudo -H -u $MELTANO_USER $MELTANO_VENV/bin/pip install --upgrade pip wheel
sudo -H -u $MELTANO_USER $MELTANO_VENV/bin/pip install meltano

# create the Meltano project
cd $MELTANO_ROOT
sudo -u $MELTANO_USER $MELTANO_VENV/bin/meltano --version

sudo -H -u $MELTANO_USER $MELTANO_VENV/bin/meltano init project
cd project

# remove the project id so a new one is generated
sudo -u $MELTANO_USER sed -i 's/project_id:.*$/project_id:/' meltano.yml

sudo -H -u $MELTANO_USER $MELTANO_VENV/bin/meltano add orchestrator airflow
sudo -H -u $MELTANO_USER $MELTANO_VENV/bin/meltano add transformer dbt
sudo -H -u $MELTANO_USER $MELTANO_VENV/bin/meltano add loader target-postgres

# start and enable Meltano
systemctl enable meltano
