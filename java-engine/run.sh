#!/usr/bin/env bash
set -euo pipefail
"$(dirname "$0")/build.sh"
java -cp out com.example.tileengine.app.Main
