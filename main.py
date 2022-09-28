"""Application entry point."""
import os

# from dotenv import load_dotenv
from src import create_app

# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')  # Address of your .env file
# load_dotenv(dotenv_path)

app = create_app()  


if __name__ == "__main__":
    # https://stackoverflow.com/questions/55662222/container-failed-to-start-failed-to-start-and-then-listen-on-the-port-defined-b
    # below resolves the container failing to launch on cloud run (got from above)
    port = int(os.environ.get('PORT', 8000)) # For Cloud Run 
    # port = int(os.environ.get('PORT', 8080)) # For Cloud Run 
    app.run(debug=True, host='0.0.0.0', port=port) 
