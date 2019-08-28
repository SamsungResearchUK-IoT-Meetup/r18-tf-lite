#!/bin/bash
set -x

#DECODER=./OnDeviceE2EASR
DECODER=./OnDeviceE2EASR-arm

# ctrl-c trap
function ctrl_c() {
        echo "Finished recording."
}

trap  ctrl_c SIGINT



input=""

echo "Press Enter to start..."
read input

# 1. parecord
parecord --rate=16000 --channels=1 test_compressed/test.wav

# 2. decoder
$DECODER OnDeviceE2EASR_compressed.conf test_compressed/testfiles.txt out.compressed.log  2

# 3. output
cat out.compressed.log 
