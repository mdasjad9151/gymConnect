# GymConnect

**GymConnect** is a full-featured gym management and fitness engagement platform built with Django. It allows users to discover and join gyms, connect with trainers, purchase video courses, interact via blogs, and chat in real-time. Gym owners can manage their gyms, trainers can upload content and engage clients, and users can explore fitness options across cities.

---

## 🔍 Features

### 👥 User Roles

- **Gym Owner**: Manages gym, trainers, and membership analytics.
- **Trainer**: Creates video courses and blogs, manages user requests.
- **Gym User**: Finds nearby gyms, books memberships, buys courses, and chats.

### 🎯 Core Modules

- **Gym Membership System**

  - Location-based gym discovery
  - One-day, monthly, or yearly membership options
  - Digital ticket generation and rating system

- **Trainer & Course Management**

  - Course creation with video upload and quality settings
  - Pay-per-course system
  - Watch purchased courses in custom video player

- **Blog System**

  - Trainers post articles, users comment and follow trainers

- **Real-Time Chat**

  - Private messaging using Django Channels and WebSockets

- **📹 Custom Video Player Features** -
- Dynamic video quality switching (144p, 360p, 480p)

- Fullscreen, volume, and speed control

- Auto-hide controls on inactivity

- Secure access to purchased videos only

---

## ⚙️ Tech Stack

| Layer    | Technologies                             |
| -------- | ---------------------------------------- |
| Backend  | Django, Django REST Framework            |
| Frontend | HTML, CSS, JavaScript, jQuery, Bootstrap |
| Realtime | Django Channels, WebSockets              |
| Video    | FFmpeg for transcoding and streaming     |
| Database | PostgreSQL (or SQLite for dev)           |
| APIs     | Google Maps API                          |

---

## 🗂 Project Structure

```
gymconnect/
├── accounts/ # Authentication & profiles
├── blog/ # Blog system
├── core/ # Base utilities
├── course/ # Video course management
├── gymOwner/ # Gym owner dashboard
├── gymUser/ # Gym user dashboard
├── membership/ # Memberships & bookings
├── network/ # Real-time chat
├── trainer/ # Trainer dashboard
├── static/ # Static files (CSS/JS)
├── media/ # Uploaded content
└── manage.py
```

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
python -m venv env
source env/bin/activate     # On Windows: env\Scripts\activate

git clone https://github.com/yourusername/gymconnect.git
cd gymconnect

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

```

## Create a .env file or add the following in settings.py:

```
DEBUG = True
SECRET_KEY = 'your-secret-key'
GOOGLE_MAPS_API_KEY = 'your-google-maps-api-key'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 📝 License

This project is licensed under the [MIT License](LICENSE) — feel free to use, modify, and distribute with attribution.
