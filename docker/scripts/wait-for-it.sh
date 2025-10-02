#!/usr/bin/env bash
# wait-for-it.sh - Adaptado para uso em containers Docker
# Fonte: https://github.com/vishnubob/wait-for-it

set -e

hostport=(${1//:/ })
host=${hostport[0]}
port=${hostport[1]}
shift

for i in {1..60}; do
  nc -z "$host" "$port" && break
  echo "Aguardando $host:$port... ($i)"
  sleep 1
done
