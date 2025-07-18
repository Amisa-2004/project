# StudyBank
#### Video Demo: [https://youtu.be/MYmiYodFhJ4?feature=shared](https://youtu.be/MYmiYodFhJ4?feature=shared)
#### Description:
**StudyBank** is a web-based application developed using Flask that serves as a centralized, searchable repository for university question papers. The purpose of this project is to simplify the process of accessing past exam papers, allowing students to revise effectively while also contributing to a verified and organized database for future learners.

This project was created as my final submission for **CS50x 2025** and is inspired by the real-world challenges students face in discovering authentic and relevant exam preparation materials. Institutions often lack a unified archive for past year papers, and unofficial sources are incomplete or unreliable. StudyBank aims to solve that by encouraging both accessibility and community-driven contribution, while ensuring content verification and input validation throughout.

---

## 🧩 Functionality Overview

StudyBank allows users to do the following:
- **Search** for question papers based on department, semester, subject, year, and exam type (midsem/endsem).
- **Upload** new question papers to the archive, subject to validation and CAPTCHA verification.
- **Filter by Verification**, enabling users to prioritize officially validated documents.

The homepage features a carousel-style display of verified documents, offering prominent visibility to the most trusted contributions. The system distinguishes between verified and unverified files, ensuring transparency regarding the source and reliability of uploaded content.

---

## 📁 File Structure and What Each File Does

├── app.py # Main Flask application<br />
├── helpers.py # Input validation and utility functions<br />
├── schema.sql # SQL schema for SQLite DB<br />
├── init_db.py # Script to initialize the database<br />
├── requirements.txt # Dependencies<br />
├── templates/ # Jinja2 HTML templates<br />
│ ├── layout.html<br />
│ ├── index.html<br />
│ ├── search.html<br />
│ ├── results.html<br />
│ └── upload.html<br />
├── static/<br />
│ └── style.css # Styling for the front-end<br />
├── uploads/ # Directory for uploaded .pdf files<br />
├── .env # Environment variables (to be created by user)<br />
└── README.md # Project documentation<br />

Below is an explanation of each file created or configured for this project:

- **app.py**: The central logic of the Flask web application. It handles routing, form submissions, search logic, upload functionality, database interactions, and template rendering. All major features such as `/`, `/search`, `/upload`, and file validation logic are managed here.

- **helpers.py**: Contains utility functions used across the app, including comprehensive validations for form inputs (ensuring correct semester, exam types, year range, and file type restrictions). This modular design keeps the main application logic in `app.py` clean and readable.

- **init_db.py**: A standalone Python script used to initialize the SQLite database using the schema defined in `schema.sql`. Running this script prepares the application to store and retrieve question paper metadata and filenames.

- **schema.sql**: Defines the SQL schema for the SQLite database. It outlines a table named `papers` with fields such as `id`, `department`, `subject`, `semester`, `exam`, `year`, `verified`, and `filename`. The schema supports indexing and retrieval of multiple entry types efficiently.

- **templates/**: Contains all the HTML files used with Flask’s Jinja templating engine:
    - `layout.html`: A base layout shared across all pages for consistency of UI.
    - `index.html`: The homepage containing a selection of verified question papers.
    - `search.html`: The form interface where users can query based on multiple filters.
    - `results.html`: Displays search results, cleanly separating verified and unverified docs.
    - `upload.html`: A secure form with validation and reCAPTCHA to submit new papers.

- **static/style.css**: Adds basic visual styling to pages, forms, and the homepage. Maintains a responsive and minimalistic UI to ensure usability on both desktop and mobile.

- **uploads/**: A directory that securely stores uploaded PDF files after validation. File names are sanitized using Werkzeug’s `secure_filename()` to prevent unsafe paths.

- **.env**: Stores environment variables such as the Flask `SECRET_KEY` and API key for Google reCAPTCHA, loaded using `python-dotenv`. This ensures clean separation of secrets from production code.
> [!NOTE]:
> This project uses environment variables to store sensitive keys. The `.env` file is excluded from thr repository for security. See `.env.example` for required variables.

---

## 💡 Design Decisions and Justifications

Several design considerations were debated during the development process:

- **Framework Choice — Flask**: I chose Flask for its simplicity and flexibility, especially suitable for relatively small-scale but dynamic applications. Compared to Django, Flask provides more control for introducing custom validations and lightweight routing.

- **Database — SQLite**: SQLite was selected for local persistence due to its lightweight nature and ease of use without installing a separate DBMS. For production deployment in a shared or cloud environment, transitioning to PostgreSQL would be straightforward.

- **File Validation & Security**: One of the most important concerns was avoiding malicious uploads. To address this, uploaded files undergo a strict validation process:
    - Accepted only if they are PDFs (`.pdf`).
    - File size limited to 5 MB.
    - Filenames sanitized before saving.
    - Inputs (e.g., semester, year, exam type) validated to avoid SQL injection or form abuse.
    - Google reCAPTCHA is used to block bots or script-based uploads.

- **Verified vs. Unverified Designation**: The application allows papers to be flagged as "verified" for authenticity (potentially by admin input). I intentionally separated search results into verified/unverified lists, so users can make informed decisions on trustworthiness. This feature enhances long-term credibility and usability.

---

## ⚙️ How to Run

To run StudyBank locally:

1. Clone the repository
    ```
    git clone https://github.com/Amisa-2004/project.git
    cd studybank
    ```
2. Set up a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate  # Use `venv\Scripts\activate` for Windows
    pip install -r requirements.txt
    ```
3. Create a `.env` file with:
    ```
    RECAPTCHA_SECRET=your_recaptcha_secret
    ```
    Use `.env.example` for reference.
4. Initialize the database:
    ```
    python init_db.py
    ```
5. Run the Flask application:
    ```
    python app.py
    ```

Access the web app at [http://localhost:5000](http://localhost:5000).

---

## 🤝 Contributing and Future Improvements

Currently, the system supports manual uploads and review. In the future, I plan to add:
- Admin interface for verification
- Search history and file downloads tracking
- Department-specific analytics
- Google Drive/Cloud storage integration

---

## 📜 License

This project is created for educational purposes under CS50x guidelines. You are free to adapt or reuse ideas from it in your own academic or portfolio projects.

---

Thank you for checking out StudyBank — a place where education meets collaboration.
