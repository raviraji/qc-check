#!/bin/bash
cd /home/dt/
sleep 1
if [ ! -f QC_Test.py ]; then
    curl -O https://raw.githubusercontent.com/raviraji/qc-check/main/QC_Test.py
fi
python3 QC_Test.py
