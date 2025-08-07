#!/bin/bash

EXTRA_CONF="remote-cert-tls server
data-ciphers AES-256-GCM:AES-128-CBC
cipher AES-128-CBC
auth SHA1"

for file in /etc/openvpn/*.ovpn; do
    echo "📄 Обрабатываю $file"
    echo -e "\n# 🔧 Auto-patched settings\n$EXTRA_CONF" >> "$file"
done

echo "✅ Все .ovpn файлы дополнены."
