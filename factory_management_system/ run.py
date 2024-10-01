from app import create_app

app = create_app('app.config.Config')

if __name__ == '__main__':
    with app.app_context():
        from app.models import db
        db.create_all()  # Create tables
    app.run(debug=True)
