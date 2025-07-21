# Disease Prediction Web Application

A Django-based web application for predicting diseases based on user-input symptoms using machine learning models (Random Forest, Naive Bayes, SVM).

## Features

- User registration and login
- Disease prediction from symptoms
- Multiple ML models for prediction
- Confidence scores (can be added)
- Admin interface for user management

## Project Structure

```
django_HA/
├── AI/                  # Django project settings
├── healthadvisor/       # Main app: ML, views, models, etc.
│   ├── predictor.py
│   ├── train_models.py
│   └── ...
├── illnessnames/        # Data files (e.g., file2.csv)
├── db.sqlite3           # SQLite database
└── manage.py
```

## Setup Instructions

1. **Clone the repository**
   ```sh
   git clone https://github.com/HiAnand2004/Disease_Prediction.git
   cd Disease_Prediction/django_HA
   ```

2. **Install dependencies**
   ```sh
   pip install -r ../illnessnames/requirements.txt
   ```

3. **Prepare data**
   - Ensure `illnessnames/file2.csv` and `healthadvisor/processed_data.csv` are present.
   - If needed, run data preprocessing scripts.

4. **Train models**
   ```sh
   python healthadvisor/train_models.py
   ```

5. **Apply migrations**
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```sh
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```sh
   python manage.py runserver
   ```

8. **Access the app**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Notes

- Update `predictor.py` if you want to include confidence scores in predictions.
- Make sure all required data files are in the correct directories.

## License

This project is for educational purposes.
