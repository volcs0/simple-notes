from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
NOTES_FILE = "/app/data/notes.json"


def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return []


def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/notes", methods=["GET"])
def get_notes():
    return jsonify(load_notes())


@app.route("/api/notes", methods=["POST"])
def add_note():
    notes = load_notes()
    note = {
        "id": len(notes) + 1,
        "text": request.json["text"],
        "category": request.json.get("category", "General")
    }
    notes.append(note)
    save_notes(notes)
    return jsonify(note), 201


@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    notes = load_notes()
    notes = [n for n in notes if n["id"] != note_id]
    save_notes(notes)
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
