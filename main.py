from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# Set the secret key for session management and CSRF protection
app.config['SECRET_KEY'] = 'your_secret_key_here'

def calculate_required_grades(prelim_grade):
    # Convert the preliminary grade to a float
    prelim_grade = float(prelim_grade)

    # Define constants for the passing grade and the weight of each grading component
    passing_grade = 75.0
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50
    grade_range = (0.0, 100.0)

    # Check if the prelim grade is within the acceptable range
    if not (grade_range[0] <= prelim_grade <= grade_range[1]):
        return "Error: Preliminary grade must be between 0 and 100."

    # Calculate the current contribution of the prelim grade
    current_total = prelim_grade * prelim_weight
    
    # Determine the required total score needed from midterms and finals to pass
    required_total = passing_grade - current_total
    
    # Calculate the minimum average required for midterms and finals
    min_required_average = required_total / (midterm_weight + final_weight)

    # If the prelim grade already meets or exceeds the passing grade, inform the user
    if prelim_grade >= passing_grade:
        return f"Stay focused and keep going. Grades needed for midterms and finals.: {min_required_average:.2f}%"

    # Check if it's impossible to achieve the passing grade with the given prelim score
    if min_required_average > grade_range[1]:
        return "Error: You can’t reach a passing grade with this initial score.."

    # Ensure that the minimum average does not fall below the grade range
    if min_required_average < grade_range[0]:
        min_required_average = grade_range[0]
    
    # Return average grade for midterms and finals
    return f"Required Grade for Midterms and Finals: {min_required_average:.2f}%"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            # Extract and convert the prelim grade from the form data
            prelim_grade = float(request.form['prelim_grade'])
            result = calculate_required_grades(prelim_grade)
        except ValueError:
            # Handle invalid input by user
            result = "Error: Invalid input. Please enter a valid number."

    # Render the HTML template then pass the result to it
    return render_template('index.html', result=result)

if __name__ == '__main__':
    # Run application in debug mode
    app.run(debug=True)
