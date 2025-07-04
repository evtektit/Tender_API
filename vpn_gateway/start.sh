#!/bin/bash
set -e

# Патчим конфиги
/fix_ovpn.sh

# Берём первый доступный конфиг
CONFIG=$(find /etc/openvpn -type f -name 'vpngate_*.ovpn' | head -n 1)

if [[ -z "$CONFIG" ]]; then
  echo "❌ .ovpn файл не найден в /etc/openvpn"
  exit 1

fi

echo "🚀 Запускаем OpenVPN с конфигом: $CONFIG"
exec openvpn --config "$CONFIG"
