#!/bin/bash

# Фиксим ovpn-файлы
/app/fix_ovpn.sh

# Перебор всех .ovpn конфигов
for CONFIG in /etc/openvpn/vpngate_*.ovpn; do
  echo "🔌 Пробуем подключиться к: $CONFIG"

  # Запуск OpenVPN и ожидание подключения
  openvpn --config "$CONFIG" &
  PID=$!

  # Даём 20 секунд на установку соединения
  sleep 20

  # Проверяем, подключён ли tun0
  if ip a | grep -q "tun0"; then
    echo "✅ Подключение успешно: $CONFIG"
    wait $PID  # Ждём завершения openvpn
    exit 0
  else
    echo "❌ Не удалось подключиться через $CONFIG, пробуем следующий..."
    kill $PID
    sleep 2
  fi
done

echo "🛑 Не удалось подключиться ни через один .ovpn конфиг"
exit 1
