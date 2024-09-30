from app import create_app

app = create_app('config.py')  # Adjust config file as necessary

if __name__ == '__main__':
    app.run(debug=True)
