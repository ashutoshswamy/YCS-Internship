from flask import Flask, request, jsonify

app = Flask(__name__)

todos = [
    {
        "id": 1,
        "title": "Learn Python",
        "description": "Learn Python programming language",
        "completed": False
    }
]

def find_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return None

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = find_todo(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo)

@app.route('/create_todo', methods=['POST'])
def create_todo():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Title is required"}), 400
    
    new_id = max([todo["id"] for todo in todos]) + 1 if todos else 1
    
    todo = {
        "id": new_id,
        "title": request.json["title"],
        "description": request.json.get("description", ""),
        "completed": request.json.get("completed", False)
    }
    
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/update_todo/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = find_todo(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    
    if not request.json:
        return jsonify({"error": "No data provided"}), 400
    
    if 'title' in request.json:
        todo['title'] = request.json['title']
    if 'description' in request.json:
        todo['description'] = request.json['description']
    if 'completed' in request.json:
        todo['completed'] = request.json['completed']
    
    return jsonify(todo)

@app.route('/delete_todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = find_todo(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    
    todos.remove(todo)
    return jsonify({"message": f"Todo {todo_id} deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)