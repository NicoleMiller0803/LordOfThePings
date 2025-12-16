
from flask import Flask, render_template, request
import subprocess
import json
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        street = request.form['street']
        zip_code = request.form['zip_code']
        state = request.form['state']
        coverage_type = request.form['coverage_type']
        project_id = "ccibt-hack25ww7-738" # Hardcoded project ID

        try:
            command = [
                "python3", "OrchestrationAgent/main.py",
                "--street", street,
                "--zip_code", zip_code,
                "--state", state,
                "--coverage_type", coverage_type,
                "--project_id", project_id
            ]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            deal_memo_raw = result.stdout
            
            # Extract relevant info for indicators
            recommendation_match = re.search(r"Investment Recommendation\s*\*\*(.*?)\*\*", deal_memo_raw)
            recommendation = recommendation_match.group(1).strip() if recommendation_match else "N/A"

            loss_risk_match = re.search(r"State-Level Financial Loss Risk:\*\* (.*)", deal_memo_raw)
            loss_risk = loss_risk_match.group(1).strip() if loss_risk_match else "N/A"

            return render_template('deal_memo.html', deal_memo=deal_memo_raw, recommendation=recommendation, loss_risk=loss_risk)
        except subprocess.CalledProcessError as e:
            error_message = f"Error running OrchestrationAgent: {e.stderr}"
            return render_template('index.html', error=error_message)
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
