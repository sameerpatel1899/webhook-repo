# Webhook Repo

This is a Flask-based application that acts as a GitHub webhook receiver. It listens for GitHub events such as **Push**, **Pull Request**, and **Merge**, stores the relevant data into **MongoDB**, and displays the events on a minimal frontend that auto-refreshes every 15 seconds.

---

## ⚙️ Tech Stack

- Python (Flask)
- MongoDB (NoSQL database)
- JavaScript (Vanilla JS polling)
- HTML/CSS
- GitHub Webhooks

---

## 🔥 Features

- Accepts GitHub Webhook Events via `/webhook`
- Stores parsed event messages in MongoDB
- Auto-refreshes and displays latest events every 15 seconds
- Handles:
  - Push
  - Pull Requests
  - Merges (bonus)

---

## 📦 Event Message Format

- **Push**  
  `"Sameer pushed to main on 3rd July 2025 - 6:34 PM UTC"`

- **Pull Request**  
  `"Sameer submitted a pull request from dev to main on 3rd July 2025 - 6:40 PM UTC"`

- **Merge**  
  `"Sameer merged branch dev to main on 3rd July 2025 - 6:45 PM UTC"`

---

## 🛠️ Setup Instructions

### 1. Clone the repository:
```bash
git clone https://github.com/your-username/webhook-repo.git
cd webhook-repo
````

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file:

```env
SECRET_KEY=your-secret-key
MONGO_URI=mongodb://localhost:27017/webhook_user
GITHUB_WEBHOOK_SECRET=your-github-secret-if-any
```

> You can also include `.env.example` to show required keys.

### 4. Run the app:

```bash
python run.py
```

Visit in browser:

```
http://localhost:5000
```

---

## 🧪 Testing with Postman

* Endpoint: `http://localhost:5000/webhook`
* Method: `POST`
* Headers:

  * `Content-Type: application/json`
  * `X-GitHub-Event: push`
* Body:

```json
{
  "pusher": { "name": "Sameer" },
  "ref": "refs/heads/main"
}
```

---

## 📊 MongoDB Schema

```json
{
  "type": "push",
  "message": "Sameer pushed to main on ...",
  "timestamp": "ISO Date"
}
```

---

## 🧠 Future Enhancements

* Deploy live using Render or Railway
* Add user authentication
* Improve frontend styling
* Add commit/message info in event logs

---

## 📄 License

MIT License

````

---

## 📗 `action-repo/README.md` (This is your GitHub trigger repo)

```markdown
# Action Repo

This repository is used to simulate GitHub actions for testing webhooks. It works together with the [`webhook-repo`](https://github.com/your-username/webhook-repo) which receives and displays these webhook events.

---

## 🎯 Purpose

To trigger GitHub Webhook Events such as:

- ✅ Push
- ✅ Pull Request
- ✅ Merge (via merged PR)

These events are sent to the `/webhook` endpoint of the `webhook-repo` Flask server using GitHub’s webhook system.

---

## ⚙️ How to Use

1. Make a commit in this repo → triggers **Push**
2. Create a pull request → triggers **Pull Request**
3. Merge the pull request → triggers **Merge**

GitHub automatically sends webhook payloads to the configured receiver (usually hosted locally via ngrok or deployed live).

---

## 🔗 How to Add a Webhook

1. Go to your repo → **Settings** → **Webhooks**
2. Click **"Add Webhook"**
3. Fill in:
   - **Payload URL:** `http://your-ngrok-url/webhook` (or deployed URL)
   - **Content type:** `application/json`
   - **Secret:** *(optional, from .env)*
4. Select **events to send**:
   - Just the ones you need: Push, Pull Request
5. Click **Save Webhook**

---

## 🧪 Sample Actions

### Push Test
```bash
git add .
git commit -m "Test push"
git push
````

### Pull Request Test

* Create a new branch
* Make changes and push
* Open a Pull Request on GitHub

### Merge Test

* Merge the PR on GitHub

---

## 🧠 Why Separate Repos?

Per the assignment:

* `action-repo` = Source of GitHub activity
* `webhook-repo` = Destination receiver that logs and displays activity
