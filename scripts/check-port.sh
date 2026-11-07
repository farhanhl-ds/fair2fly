#!/usr/bin/env bash
set -euo pipefail

port="${1:?usage: check-port.sh PORT NAME [VARIABLE]}"
name="${2:-service}"
variable="${3:-port}"

if (exec 3<>"/dev/tcp/127.0.0.1/${port}") 2>/dev/null; then
    printf 'error: %s port %s is already in use; set %s in .env to a free port\n' \
        "$name" "$port" "$variable" >&2
    exit 1
fi
