from flask import Flask, request, redirect, url_for, render_template_string, session, flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = "secretkey123"

# Courses with categories
courses = {
    1: {"name": "Mathematics", "category": "Science"},
    2: {"name": "Physics", "category": "Science"},
    3: {"name": "Chemistry", "category": "Science"},
    4: {"name": "Biology", "category": "Science"},
    5: {"name": "Computer Science", "category": "Science"},
    6: {"name": "English", "category": "Arts"},
    7: {"name": "History", "category": "Arts"},
    8: {"name": "Geography", "category": "Arts"},
    9: {"name": "Philosophy", "category": "Arts"},
    10: {"name": "Economics", "category": "Commerce"},
    11: {"name": "Business Studies", "category": "Commerce"},
    12: {"name": "Accountancy", "category": "Commerce"}
}

registrations = []

# Login page
login_page = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Login</title>
<style>
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(to right, #6a11cb, #2575fc); height: 100vh; margin:0; display:flex; justify-content:center; align-items:center; }
.container { background:white; padding:30px; border-radius:15px; box-shadow:0 10px 25px rgba(0,0,0,0.3); width:350px; }
h2{text-align:center;color:#333;}
input[type=text], input[type=password] { padding:10px;width:100%;margin:10px 0;border-radius:8px;border:1px solid #ccc; }
input[type=submit] { padding:10px;width:100%;border:none;border-radius:8px;background:#2575fc;color:white;font-weight:bold;cursor:pointer;transition:0.3s; }
input[type=submit]:hover { background:#6a11cb; }
.error { color:red;text-align:center; }
</style>
</head>
<body>
<div class="container">
<h2>Login</h2>
{% if error %}<p class="error">{{ error }}</p>{% endif %}
<form method="POST">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <input type="submit" value="Login">
</form>
</div>
</body>
</html>
"""

# Main page with delete/update and flash messages
course_page = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Course Registration</title>
<style>
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f8; margin:0; padding:0; }
.container { width:90%; margin:auto; padding:20px; }
header { background:#2575fc; color:white; padding:20px; border-radius:10px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; }
header h1{ margin:0; font-size:28px; }
.logout { background:#ff4b5c; padding:10px 15px; border-radius:8px; text-decoration:none; color:white; font-weight:bold; transition:0.3s; }
.logout:hover { background:#ff2e3c; }
h2 { color:#333; margin-top:30px; }
.flash { background:#d4edda; color:#155724; padding:10px; border-radius:8px; margin-bottom:20px; border:1px solid #c3e6cb; }
.courses { display:grid; grid-template-columns: repeat(auto-fit, minmax(180px,1fr)); gap:15px; margin-bottom:30px; }
.card { background:white; padding:15px; border-radius:10px; box-shadow:0 6px 20px rgba(0,0,0,0.1); text-align:center; transition: transform 0.2s, box-shadow 0.2s; }
.card:hover { transform: translateY(-5px); box-shadow:0 12px 30px rgba(0,0,0,0.2); }
.science { background:#d0f0fd; }
.arts { background:#fde0f0; }
.commerce { background:#fdf4d0; }
form { background:white; padding:20px; border-radius:10px; max-width:500px; box-shadow:0 6px 20px rgba(0,0,0,0.1); margin-bottom:30px; }
input[type=text], select { padding:10px; width:100%; margin:10px 0; border-radius:8px; border:1px solid #ccc; }
input[type=submit], button { padding:12px; width:100%; border:none; border-radius:8px; background:#2575fc; color:white; font-weight:bold; cursor:pointer; transition:0.3s; margin-top:5px; }
input[type=submit]:hover, button:hover { background:#6a11cb; }
input[type=search] { padding:10px; width:50%; border-radius:8px; border:1px solid #ccc; margin-bottom:20px; }
table { width:100%; border-collapse: collapse; margin-top:20px; }
th, td { padding:12px; border:1px solid #ccc; text-align:left; }
th { background:#2575fc; color:white; }
tr:nth-child(even) { background:#f2f2f2; }
.action-btn { background:#ff4b5c; width:auto; padding:5px 10px; margin-left:5px; text-decoration:none; color:white; border-radius:5px; }
.action-btn:hover { background:#ff2e3c; }
</style>
<script>
function confirmDelete(url) {
    if(confirm('Are you sure you want to delete this registration?')) {
        window.location.href = url;
    }
}
</script>
</head>
<body>
<div class="container">
<header>
<h1>Course Registration System</h1>
<a class="logout" href="/logout">Logout</a>
</header>

{% with messages = get_flashed_messages() %}
  {% if messages %}
    {% for msg in messages %}
      <div class="flash">{{ msg }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}

<h2>Available Courses</h2>
<div class="courses">
{% for id, c in courses.items() %}
<div class="card {% if c['category']=='Science' %}science{% elif c['category']=='Arts' %}arts{% else %}commerce{% endif %}">
<h3>{{ c['name'] }}</h3>
<p>{{ c['category'] }}</p>
<p>Course ID: {{ id }}</p>
</div>
{% endfor %}
</div>

<h2>Register Student</h2>
<form method="POST">
<input type="hidden" name="editing_index" value="{{ edit_index if editing else '' }}">
<input type="text" name="student_name" placeholder="Student Name" value="{{ edit_name }}" required>
<select name="course_id" required>
{% for id, c in courses.items() %}
<option value="{{ id }}" {% if edit_course_id==id %}selected{% endif %}>{{ c['name'] }} ({{ c['category'] }})</option>
{% endfor %}
</select>
<input type="submit" value="{{ 'Update Registration' if editing else 'Register' }}">
{% if editing %}
<a href="{{ url_for('course_registration') }}">Cancel</a>
{% endif %}
</form>

<h2>Registered Students</h2>
<form method="GET">
<input type="search" name="search" placeholder="Search by student name" value="{{ search_query }}">
<input type="submit" value="Search">
</form>

<table>
<tr><th>Student Name</th><th>Course</th><th>Category</th><th>Actions</th></tr>
{% for idx, reg in registrations %}
{% if search_query.lower() in reg['name'].lower() %}
<tr>
<td>{{ reg['name'] }}</td>
<td>{{ reg['course'] }}</td>
<td>{{ reg['category'] }}</td>
<td>
<a class="action-btn" href="{{ url_for('edit_registration', index=idx) }}">Edit</a>
<a class="action-btn" href="javascript:confirmDelete('{{ url_for('delete_registration', index=idx) }}')">Delete</a>
</td>
</tr>
{% endif %}
{% endfor %}
{% if registrations|length == 0 or (search_query and not registrations|selectattr('name','search_query')|list) %}
<tr><td colspan="4">No registrations yet.</td></tr>
{% endif %}
</table>
</div>
</body>
</html>
"""

users = {"admin": "admin123", "student": "student123"}

@app.route("/", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("course_registration"))
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("course_registration"))
        else:
            error = "Invalid username or password"
    return render_template_string(login_page, error=error)

@app.route("/courses", methods=["GET", "POST"])
def course_registration():
    if "username" not in session:
        return redirect(url_for("login"))
    search_query = request.args.get("search", "")
    editing = False
    edit_name = ""
    edit_course_id = None
    edit_index = None
    if request.method == "POST":
        if request.form.get("editing_index"):
            idx = int(request.form["editing_index"])
            name = request.form.get("student_name")
            course_id = int(request.form.get("course_id"))
            registrations[idx] = {"name": name, "course": courses[course_id]['name'], "category": courses[course_id]['category']}
            flash("Registration updated successfully!")
        else:
            name = request.form.get("student_name")
            course_id = int(request.form.get("course_id"))
            registrations.append({"name": name, "course": courses[course_id]['name'], "category": courses[course_id]['category']})
            flash("Student registered successfully!")
        return redirect(url_for("course_registration"))
    return render_template_string(course_page, courses=courses, registrations=list(enumerate(registrations)), search_query=search_query, editing=editing, edit_name=edit_name, edit_course_id=edit_course_id, edit_index=edit_index)

@app.route("/edit/<int:index>", methods=["GET"])
def edit_registration(index):
    if "username" not in session:
        return redirect(url_for("login"))
    reg = registrations[index]
    search_query = request.args.get("search", "")
    edit_course_id = None
    # Get the key of the course based on name match
    for k, v in courses.items():
        if v['name'] == reg['course'] and v['category'] == reg['category']:
            edit_course_id = k
            break
    return render_template_string(course_page, courses=courses, registrations=list(enumerate(registrations)), search_query=search_query,
                                  editing=True, edit_name=reg['name'], edit_course_id=edit_course_id, edit_index=index)

@app.route("/delete/<int:index>")
def delete_registration(index):
    if "username" not in session:
        return redirect(url_for("login"))
    registrations.pop(index)
    flash("Registration deleted successfully!")
    return redirect(url_for("course_registration"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
