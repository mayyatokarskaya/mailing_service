# 📧 Mailing Service

**Mailing Service** — это веб-приложение на Django для управления рассылками, получателями и сообщениями.  
Подходит для автоматической отправки писем по расписанию, управления базой клиентов и анализа статистики.

## 🚀 Функционал

- Регистрация и авторизация пользователей с подтверждением email.
- Личный кабинет пользователя.
- CRUD для:
  - Получателей рассылок
  - Сообщений
  - Самих рассылок
- Разделение доступа:
  - **Пользователи** — управляют только своими рассылками и получателями.
  - **Менеджеры** — видят все рассылки и получателей.
  - **Администраторы** — полный доступ.
- Автоматическая отправка писем через SMTP.
- Статистика отправок и отчёты.
- Кеширование списков рассылок (Redis).
- Планирование и выполнение рассылок через Celery.
- Группы пользователей и кастомные разрешения.
- Админ-панель Django для управления.

---

## 📂 Структура проекта

```
mailing_service/
│
├── mailing/               # Приложение рассылок
│   ├── models.py           # Модели (Mailing, Recipient, Message, MailingAttempt)
│   ├── views.py            # CRUD и бизнес-логика
│   ├── urls.py             # Маршруты
│   ├── management/         # Команды Django
│   │   ├── send_mailing.py # Отправка активных рассылок
│   │   ├── setup_groups.py # Создание группы "Менеджеры"
│   └── templates/mailing/  # HTML-шаблоны
│
├── users/                  # Приложение пользователей
│   ├── models.py           # Модель CustomUser
│   ├── forms.py            # Форма регистрации/редактирования профиля
│   ├── views.py            # Регистрация, вход, профиль
│   ├── urls.py             # Маршруты
│   └── templates/users/    # HTML-шаблоны
│
├── config/                 # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── static/                 # Статические файлы
├── templates/              # Общие шаблоны
├── .env                    # Переменные окружения
├── manage.py
```

---

## ⚙️ Установка

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/username/mailing_service.git
   cd mailing_service
   ```

2. **Создайте виртуальное окружение и активируйте его**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте .env файл**
   ```env
   SECRET_KEY=ваш_секретный_ключ
   DEBUG=True

   NAME=mailing_db
   USER=mailing_db_user
   PASSWORD=mailing_db_password
   HOST=localhost
   PORT=5432

   EMAIL_HOST=smtp.yandex.ru
   EMAIL_PORT=465
   EMAIL_USE_TLS=False
   EMAIL_USE_SSL=True
   EMAIL_HOST_USER=ваш_email
   EMAIL_HOST_PASSWORD=ваш_app_password
   DEFAULT_FROM_EMAIL=ваш_email
   ```

5. **Выполните миграции**
   ```bash
   python manage.py migrate
   ```

6. **Создайте суперпользователя**
   ```bash
   python manage.py createsuperuser
   ```

7. **Создайте группу "Менеджеры"**
   ```bash
   python manage.py setup_groups
   ```

---

## ▶️ Запуск проекта

### 1. Запуск сервера Django
```bash
python manage.py runserver
```

### 2. Запуск Redis (для кеша и Celery)
```bash
redis-server
```

### 3. Запуск Celery для задач рассылки
```bash
celery -A config worker -l info
celery -A config beat -l info
```

---

## 📜 Команды управления

- **Отправить все активные рассылки вручную**  
  ```bash
  python manage.py send_mailing
  ```

- **Создать группу "Менеджеры" и назначить права**  
  ```bash
  python manage.py setup_groups
  ```

---

## 👥 Роли пользователей

- **Пользователь**:
  - Управляет только своими рассылками, получателями и сообщениями.
- **Менеджер**:
  - Видит все рассылки и получателей.
- **Администратор**:
  - Полный доступ.

---

## 📊 Статистика

В разделе `/stats/` пользователь может просмотреть:
- Количество успешных отправок.
- Количество ошибок.
- Общее число попыток.

---

## 🛠 Используемые технологии

- **Backend**: Python, Django, Celery
- **База данных**: PostgreSQL
- **Кеш**: Redis
- **Email**: SMTP (Yandex, Gmail, др.)
- **Frontend**: HTML, CSS, Django Templates
- **Аутентификация**: Django Auth + подтверждение email
- **Разграничение прав**: Django Groups & Permissions

---

## 📄 Лицензия
Проект распространяется под лицензией MIT.
