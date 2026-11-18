#!/usr/bin/env bash
# Usage (on the Ubuntu server, as root):  bash setup.sh yourdomain.com
set -euo pipefail
DOMAIN="${1:?Укажите домен: bash setup.sh yourdomain.com}"
APP=/srv/exam
REPO=https://github.com/Mans-techno/Exam.git

apt update
apt install -y python3 python3-venv python3-pip git nginx certbot python3-certbot-nginx

if [ -d "$APP/.git" ]; then git -C "$APP" pull; else git clone "$REPO" "$APP"; fi
cd "$APP"

python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

if [ ! -f .env ]; then
  SECRET=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')
  cat > .env <<ENV
DJANGO_SECRET_KEY=$SECRET
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN
ENV
  chmod 600 .env
fi

set -a; . ./.env; set +a
venv/bin/python manage.py migrate --noinput
venv/bin/python manage.py collectstatic --noinput
chown -R www-data:www-data "$APP"

cp deploy/gunicorn.service /etc/systemd/system/exam.service
systemctl daemon-reload
systemctl enable --now exam
systemctl restart exam

sed "s/DOMAIN/$DOMAIN/g" deploy/nginx.conf > /etc/nginx/sites-available/exam
ln -sf /etc/nginx/sites-available/exam /etc/nginx/sites-enabled/exam
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

ufw allow 'Nginx Full' >/dev/null 2>&1 || true

CERT_DOMAINS=(-d "$DOMAIN")
getent hosts "www.$DOMAIN" >/dev/null && CERT_DOMAINS+=(-d "www.$DOMAIN")
# No --redirect: if Cloudflare SSL mode is "Flexible", a redirect here would loop.
certbot --nginx "${CERT_DOMAINS[@]}" --non-interactive --agree-tos --register-unsafely-without-email --no-redirect   || echo "ВНИМАНИЕ: сертификат не выпущен (проверьте DNS/Cloudflare). Сайт работает по HTTP."

echo "Готово: https://$DOMAIN/admin/"
