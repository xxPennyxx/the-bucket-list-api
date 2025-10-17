
# The Bucket List API

**The Bucket List** is a Flask web application that lets you create, view, update, and delete destinations on your personal travel bucket list. The app provides a **RESTful API** for managing places and a simple front-end using Flask and Bootstrap.

---

## Features

* **Add Places**: Add new destinations with fields like name, city, country, Google Maps URL, opening/closing hours, rating, and review.
* **View Places**: Retrieve all destinations or a specific one by ID.
* **Update Places**: Update existing destinations using PUT (full) or PATCH (partial).
* **Delete Places**: Remove destinations from your bucket list.
* **Web Interface**: Simple pages for adding and viewing places.
* **Persistent Storage**: Uses SQLite (`places.db`) for storing data.

---

## API Routes

### 1. Get all places

**GET** `/all_places`

**Response**:

```json
{
  "places": [
    {
      "id": 1,
      "name": "Eiffel Tower",
      "city": "Paris",
      "country": "France",
      "location": "https://maps.google.com/...",
      "open": "9:00 AM",
      "close": "11:00 PM",
      "rating": "⭐⭐⭐⭐",
      "review": "Amazing views of the city!"
    }
  ]
}
```

---

### 2. Get a single place by ID

**GET** `/places/<place_id>`

**Response**:

```json
{
  "place": {
    "id": 1,
    "name": "Eiffel Tower",
    "city": "Paris",
    "country": "France",
    "location": "https://maps.google.com/...",
    "open": "9:00 AM",
    "close": "11:00 PM",
    "rating": "⭐⭐⭐⭐",
    "review": "Amazing views of the city!"
  }
}
```

**Error**:

```json
{
  "error": "404 Not Found"
}
```

---

### 3. Get a random place

**GET** `/random`

**Response**:

```json
{
  "place": {
    "id": 3,
    "name": "Grand Canyon",
    "city": "Arizona",
    "country": "USA",
    "location": "https://maps.google.com/...",
    "open": "6:00 AM",
    "close": "8:00 PM",
    "rating": "⭐⭐⭐⭐⭐",
    "review": "Breathtaking natural wonder!"
  }
}
```

---

### 4. Add a new place

**POST** `/add_place`

**Request**:

```json
{
  "name": "Eiffel Tower",
  "city": "Paris",
  "country": "France",
  "location": "https://maps.google.com/...",
  "open": "9:00 AM",
  "close": "11:00 PM",
  "rating": "⭐⭐⭐⭐",
  "review": "Amazing views of the city!"
}
```

**Response**:

```json
{
  "message": "Successfully added new place",
  "place": { ... }
}
```

---

### 5. Update a place (full)

**PUT** `/places/<place_id>`

**Request** (all fields required):

```json
{
  "name": "Eiffel Tower",
  "city": "Paris",
  "country": "France",
  "location": "https://maps.google.com/...",
  "open": "9:00 AM",
  "close": "11:00 PM",
  "rating": "⭐⭐⭐⭐",
  "review": "Updated review"
}
```

**Response**:

```json
{
  "message": "Place updated successfully (PUT)",
  "place": { ... }
}
```

---

### 6. Update a place (partial)

**PATCH** `/places/<place_id>`

**Request** (only fields to update):

```json
{
  "rating": "⭐⭐⭐⭐⭐",
  "review": "Even better after sunset!"
}
```

**Response**:

```json
{
  "message": "Place updated successfully (PATCH)",
  "place": { ... }
}
```

---

### 7. Delete a place

**DELETE** `/places/<place_id>`

**Response**:

```json
{
  "message": "Place with ID 1 deleted successfully"
}
```

---

## Web Interface

* **Landing Page**: `/`
* **View all places**: `/places` – displays all destinations in a table with Edit/Delete buttons.
* **Add or Edit a Place**: `/add` – form page for adding new places or editing existing ones. Pre-fills data when editing using query parameter `?id=<place_id>`.

---

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/xxPennyxx/the-bucket-list.git
cd the-bucket-list
```

2. **Create a virtual environment**:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install Flask Flask-Bootstrap SQLAlchemy
```

4. **Run the app**:

```bash
python main.py
```

5. **Open your browser**:

```
http://127.0.0.1:5002/
```

---

## Notes

* The app uses **SQLite (`places.db`)** for data storage, created automatically if it doesn’t exist.
* All API responses are **JSON formatted**.
* The web interface interacts with the API, so adding/editing/deleting places uses the same endpoints.
* The `add.html` form can handle both adding a new place and editing an existing place via `?id=<place_id>` in the URL.
