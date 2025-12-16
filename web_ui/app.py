
from flask import Flask, render_template, request
import subprocess
import json
import re

app = Flask(__name__)

def to_formatted_currency(value):
    try:
        # Ensure value is a number before formatting
        num_value = float(value)
        return f"{num_value:,.2f}"
    except (ValueError, TypeError):
        return value # Return original value if it can't be formatted

app.jinja_env.filters['to_formatted_currency'] = to_formatted_currency

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
            deal_memo_json_str = result.stdout
            
            deal_memo_data = json.loads(deal_memo_json_str)

            if "error" in deal_memo_data:
                error_message = deal_memo_data["error"]
                return render_template('index.html', error=error_message)

            recommendation = deal_memo_data['executive_summary']['recommendation']
            loss_risk = deal_memo_data['financial_loss_risk']['status']

            return render_template('deal_memo.html', deal_memo_data=deal_memo_data, recommendation=recommendation, loss_risk=loss_risk)
        except subprocess.CalledProcessError as e:
            error_message = f"Error running OrchestrationAgent: {e.stderr}"
            return render_template('index.html', error=error_message)
        except json.JSONDecodeError as e:
            error_message = f"Error parsing JSON from OrchestrationAgent output: {e}. Output: {deal_memo_json_str}"
            return render_template('index.html', error=error_message)
        except Exception as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
