FROM ubuntu:22.04

WORKDIR /app

# Установка зависимостей
RUN apt update && apt install -y openvpn curl unzip

# Копируем скрипты
COPY start.sh /app/start.sh
COPY fix_ovpn.sh /app/fix_ovpn.sh

# Даём права на выполнение
RUN chmod +x /app/start.sh /app/fix_ovpn.sh

# Запуск
CMD ["/app/start.sh"]
