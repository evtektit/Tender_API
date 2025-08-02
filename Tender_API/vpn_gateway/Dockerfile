FROM ubuntu:22.04

# Устанавливаем OpenVPN и curl
RUN apt-get update && \
    apt-get install -y openvpn curl

# Копируем VPN конфиги
COPY vpn_configs/ /etc/openvpn/

# Копируем скрипты
COPY start.sh /start.sh
COPY fix_ovpn.sh /fix_ovpn.sh

# Делаем их исполняемыми и применяем фиксы
RUN chmod +x /start.sh

# Запуск VPN с перебором конфигов
CMD ["/start.sh"]

