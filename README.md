# Recruiter Type Detector 🕵️‍♂️

![Recruiter Type Detector Screenshot](./path-to-your-screenshot.jpg)
A web application that uses a machine learning model to analyze job descriptions and classify them as being from a direct employer (**Real**) or a third-party staffing agency (**Consulting**).

---

## ## About The Project

Navigating the job market can be confusing. It's often difficult to tell if a job posting is from the company that's actually hiring or from a third-party recruiting firm. This tool aims to solve that problem by using a trained Scikit-learn model to analyze the text of a job description and provide an instant classification.

The application provides:
* A **classification** (Real vs. Consulting)
* An **explanation** of the result
* The key phrases or **evidence** that influenced the decision

### ### Built With

This project is a full-stack application built with modern web technologies.

* **Frontend:** [React.js](https://reactjs.org/)
* **Backend:** [Python 3](https://www.python.org/) with [FastAPI](https://fastapi.tiangolo.com/)
* **Machine Learning:** [Scikit-learn](https://scikit-learn.org/)
* **WSGI Server:** [Uvicorn](https://www.uvicorn.org/) & [Gunicorn](https://gunicorn.org/)

---

## ## Getting Started

To get a local copy up and running, follow these simple steps.

### ### Prerequisites

Make sure you have the following software installed on your machine:
* [Node.js](https://nodejs.org/en/) (which includes npm)
* [Python 3.8+](https://www.python.org/downloads/) and pip

### ### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/fake-job-detector.git](https://github.com/your-username/fake-job-detector.git)
    cd fake-job-detector
    ```

2.  **Set up the Backend:**
    * Navigate to the backend directory:
        ```sh
        cd backend
        ```
    * Create and activate a virtual environment (recommended):
        ```sh
        # For Mac/Linux
        python3 -m venv .venv
        source .venv/bin/activate

        # For Windows
        python -m venv .venv
        .venv\Scripts\activate
        ```
    * Install the required Python packages:
        ```sh
        pip install -r requirements.txt
        ```

3.  **Set up the Frontend:**
    * From the root directory, navigate to the frontend directory in a **new terminal**:
        ```sh
        cd frontend
        ```
    * Install the required npm packages:
        ```sh
        npm install
        ```

---

## ## Usage

To run the application, you need to have both the backend and frontend servers running simultaneously in separate terminals.

1.  **Run the Backend Server:**
    * In your backend terminal (with the virtual environment activated):
        ```sh
        uvicorn main:app --reload
        ```
    * The API will be available at `http://127.0.0.1:8000`. You can test it by visiting `http://127.0.0.1:8000/health` in your browser.

2.  **Run the Frontend Application:**
    * In your frontend terminal:
        ```sh
        npm start
        ```
    * The React application will open automatically in your browser at `http://localhost:3000`.

Now you can paste a job description into the app and see the results!

---

## ## License

Distributed under the MIT License. See `LICENSE` for more information.

---