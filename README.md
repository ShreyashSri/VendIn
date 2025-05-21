# VendIn

**VendIn** is a Django-based web platform that helps vendors increase their visibility by creating online profiles. Vendors can add details about their offerings, specify their location, and showcase the services or products they provide. The goal of VendIn is to give local vendors a digital presence and make it easier for users to discover hidden businesses and opportunities around them.

---

## 🚀 Features

- Vendor profile creation and management  
- Add and display available options/services  
- Location tagging to help users find nearby vendors  
- Organized and searchable vendor listings  
- Simple and user-friendly interface

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)  
- **Frontend**: HTML, CSS, JavaScript (Django Templates)  
- **Database**: SQLite  
- **Optional**: Bootstrap, Google Maps API

---

## 📦 Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/VendIn.git
    cd VendIn
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv env
    source env/bin/activate   # On Windows: env\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Start the development server:**

    ```bash
    python manage.py runserver
    ```

6. **Access the app at:**

    ```
    http://127.0.0.1:8000/
    ```

---

## 🧪 Development Notes

- Default database: `db.sqlite3` (included for demo purposes)  
- Main Django app: `VendInapp`  
- Templates located in `templates/VendInapp/`

---

## 📌 Future Enhancements

- User/vendor authentication  
- Geolocation-based vendor discovery  
- Vendor reviews and ratings  
- Integration with Google Maps API  
- Mobile-friendly design

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE)

---