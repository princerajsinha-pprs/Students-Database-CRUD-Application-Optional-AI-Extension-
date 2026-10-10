# EWB Students Database CRUD Application

**Internship Project Assignment — Python Backend Development**  
**Organization:** EWB Edu Tech Pvt. Ltd.  
**Prepared by:** Prince Raj  
**Email:** princerajsinha979@gmail.com

## 1. Project overview

This is a backend REST API for managing student records. It uses **Python**, **FastAPI**, and **SQLite**. It implements all mandatory CRUD operations and includes search/filtering, validation, duplicate-email handling, missing-record handling, automated tests, and an optional Ollama-based AI question endpoint.

## 2. Features

- Create a student record.
- List all students or filter by name, course, and date of birth.
- Retrieve a student by ID.
- Update all fields (`PUT`) or selected fields (`PATCH`).
- Delete a student.
- Persist records in SQLite.
- Validate request fields with Pydantic.
- Return clear HTTP errors for invalid input, duplicate email, and missing student.
- Interactive Swagger API documentation.
- Optional local Ollama extension (`POST /ai/ask`).

## 3. Project structure

```text
ewb_students_crud/
├── app/
│   ├── __init__.py
│   ├── ai.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_students.py
├── .gitignore
├── ASSIGNMENT_REPORT.md
├── README.md
└── requirements.txt
```

`students.db` is created automatically when the API starts. It is excluded from Git because it is a local runtime database.

## 4. Requirements

- Python 3.10 or newer
- pip
- Internet connection for initial dependency installation
- SQLite (usually included with Python)
- Optional: Ollama installed locally for the AI extension

## 5. Install and run

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/docs** for Swagger UI. Stop the server with `Ctrl+C`.

## 6. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/students` | Create a student |
| `GET` | `/students` | List/filter students |
| `GET` | `/students/{student_id}` | Retrieve one student |
| `PUT` | `/students/{student_id}` | Update student details |
| `PATCH` | `/students/{student_id}` | Update selected fields |
| `DELETE` | `/students/{student_id}` | Delete a student |
| `POST` | `/ai/ask` | Optional Ollama question answering |

### Filters

- `/students?name=Rahul`
- `/students?course=AIML`
- `/students?born_after=2005-12-31`

## 7. Try it in Swagger

1. Start the server using the command above.
2. Open `http://127.0.0.1:8000/docs`.
3. Expand `POST /students`, click **Try it out**, enter the example JSON below, and click **Execute**.
4. Copy the returned `student_id` and use it in the GET, PUT/PATCH, and DELETE routes.
5. Try `GET /students` to confirm that the record was saved.

Example request:

```json
{
  "name": "Aarav Sharma",
  "date_of_birth": "2006-04-15",
  "email": "aarav.demo@example.com",
  "phone": "9876543210",
  "course": "Computer Science (AIML)",
  "address": "Raipur, Chhattisgarh",
  "enrollment_date": "2026-07-01"
}
```

Use fictional data for demonstrations. The email must be unique. Dates use `YYYY-MM-DD` format.

## 8. cURL examples

Create:

```bash
curl -X POST http://127.0.0.1:8000/students -H 'Content-Type: application/json' -d '{"name":"Aarav Sharma","date_of_birth":"2006-04-15","email":"aarav.demo@example.com","course":"Computer Science (AIML)"}'
```

List:

```bash
curl http://127.0.0.1:8000/students
```

Get one (replace `1` with the returned ID):

```bash
curl http://127.0.0.1:8000/students/1
```

Patch:

```bash
curl -X PATCH http://127.0.0.1:8000/students/1 -H 'Content-Type: application/json' -d '{"course":"Artificial Intelligence and Machine Learning"}'
```

Delete:

```bash
curl -X DELETE http://127.0.0.1:8000/students/1
```

## 9. Run tests

```bash
pytest -q
```

Tests exercise the health check and the create/read/update/delete flow. Run tests in your local virtual environment after installing dependencies.

## 10. Optional AI extension (Ollama)

The AI extension is optional. Install and start Ollama separately, then download a local model, for example:

```bash
ollama pull llama3.2:1b
```

The API's `/ai/ask` endpoint prepares student records in backend code and sends those records as context to Ollama. The model is not allowed to execute unrestricted SQL. If Ollama is not running or the model is unavailable, the optional endpoint may return an error; the core CRUD API still works.

## 11. GitHub submission

1. Create a GitHub repository named `ewb-students-crud`.
2. In the project directory, run:

```bash
git init
git add .
git commit -m "Complete EWB student CRUD assignment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ewb-students-crud.git
git push -u origin main
```

3. Replace the sample repository URL with your own GitHub URL.
4. Submit the repository link using the channel announced by your trainer.

**Do not upload** `.venv`, `students.db`, secrets, passwords, or real student personal information. Capture your own screenshots from Swagger after running the project; do not claim screenshots or test results that you have not produced.

## 12. How the code works

- `models.py`: defines the SQLite student table.
- `schemas.py`: validates incoming request data and shapes API responses.
- `database.py`: creates the database connection/session.
- `crud.py`: contains database operations.
- `main.py`: defines API routes and HTTP responses.
- `ai.py`: optional Ollama integration.
- `tests/test_students.py`: automated checks.

## 13. Viva summary

**CRUD** means Create, Read, Update, and Delete. FastAPI exposes these operations as REST endpoints. SQLite stores the records in a local database file. Pydantic validates request data. The `student_id` is the primary key, and email is unique. A `404` response means the requested student was not found; duplicate email is reported as a conflict. The Ollama AI extension is optional and separate from the core CRUD functionality.
