#!/bin/bash

set -o errexit

SPARK_DL_URL="http://ftp.jaist.ac.jp/pub/apache/spark/spark-2.2.0/spark-2.2.0-bin-hadoop2.7.tgz"
SPARK_DL_FILENAME="spark-2.2.0-bin-hadoop2.7"
SPARK_INSTALL_DIR="/opt/spark-2.2.0"
BASHRC="${HOME}/.bashrc"


wget "$SPARK_DL_URL" -P /tmp/ && tar -zxvf /tmp/${SPARK_DL_FILENAME}.tgz && rm /tmp/${SPARK_DL_FILENAME}.tgz
sudo mv /tmp/${SPARK_DL_FILENAME} ${SPARK_INSTALL_DIR}

for cmd in "chown" "chgrp"
do
	sudo "$cmd" -R vagrant "$SPARK_INSTALL_DIR"
done

sed -i -e "/^export SPARK_HOME=.*/d" "$BASHRC" && echo "export SPARK_HOME=${SPARK_INSTALL_DIR}" >> "$BASHRC"

echo "Successfully installed to -> ${SPARK_INSTALL_DIR}"

exit 0