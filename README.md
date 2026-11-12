# Flask & MongoDB Assignment

A Flask application with:
- `GET /api`: reads a list from `data.json` and returns JSON.
- `GET /`: displays an HTML form.
- `POST /submit`: validates form input and inserts it into MongoDB Atlas.
- `GET /success`: displays **Data submitted successfully** after a successful insert.

## 1. Requirements
- Python 3.10+
- A MongoDB Atlas account and database user
- Network access configured in Atlas for the machine running this application

## 2. Setup

```bash
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD**
```cmd
.venv\Scripts\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install packages:

```bash
pip install -r requirements.txt
```

## 3. Configure MongoDB Atlas

1. In MongoDB Atlas, create a free/shared cluster if you do not already have one.
2. Create a database user with a username and strong password.
3. In Network Access, allow your current public IP address. Avoid leaving `0.0.0.0/0` enabled after testing.
4. Select Connect > Drivers > Python and copy the connection string.
5. Copy `.env.example` to `.env`.
6. Replace the URI placeholders with your actual Atlas username, password and cluster hostname. URL-encode special characters in the password.
7. Keep `.env` private. It is excluded by `.gitignore`; never commit database credentials.

The database and collection are selected through the environment variables in `.env`.

## 4. Run the application

```bash
python app.py
```

Open `http://127.0.0.1:5000/` in your browser.

## 5. Test Task 1

Open:

```text
http://127.0.0.1:5000/api
```

Expected result: a JSON array containing the records in `data.json`.

You can also test from a terminal:

```bash
curl http://127.0.0.1:5000/api
```

## 6. Test Task 2

1. Open `http://127.0.0.1:5000/`.
2. Enter a name, valid email address and message.
3. Submit the form.
4. If MongoDB insert succeeds, Flask redirects to `/success` and displays `Data submitted successfully`.
5. To test an error, stop MongoDB access temporarily or use an invalid/unreachable URI, restart the app and submit. The form page should display an error without redirecting. Restore the correct URI afterwards.

After a successful submission, open MongoDB Atlas > Browse Collections and inspect the `flask_assignment.submissions` collection (or the database/collection names configured in `.env`).

## 7. Routes summary

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Display form |
| GET | `/api` | Return JSON list from `data.json` |
| POST | `/submit` | Validate and insert submitted form data |
| GET | `/success` | Display success message |

## 8. Submission checklist

- [ ] Add your name to the project folder name.
- [ ] Configure `.env` locally; do not include it in the ZIP or GitHub.
- [ ] Run and test `/api`.
- [ ] Test successful form submission and verify the MongoDB document.
- [ ] Test an error and capture the form error without redirect.
- [ ] Add genuine screenshots to `documentation/Flask_MongoDB_Assignment.docx`.
- [ ] Create a GitHub repository and add its URL to the documentation and below.
- [ ] Zip the complete project folder and upload that ZIP.
