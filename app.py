from flask import Flask, render_template, request
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)


def calculate_preparation_time(eat_time_str, work_minutes):
    eat_time = datetime.strptime(eat_time_str, '%H:%M')
    beijing_tz = pytz.timezone('Asia/Shanghai')
    current_time = datetime.now(beijing_tz)
    today_eat_time = beijing_tz.localize(datetime(current_time.year, current_time.month, current_time.day, eat_time.hour, eat_time.minute))
    if today_eat_time < current_time:
        eat_time = today_eat_time + timedelta(days=1)
    else:
        eat_time = today_eat_time
    preparation_time = eat_time - current_time - timedelta(minutes=work_minutes)
    total_minutes = int(preparation_time.total_seconds() // 60)
    if total_minutes < 0:
        return "输入的吃饭时间不合理，请重新输入"
    hours = total_minutes // 60
    hours = hours + 1
    minutes = total_minutes % 60
    return f"{hours}小时{minutes}分"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    eat_time = request.form.get('eat_time')
    work_minutes = request.form.get('work_minutes')
    if eat_time and work_minutes:
        try:
            work_minutes = int(work_minutes)
            result = calculate_preparation_time(eat_time, work_minutes)
            return render_template('result.html', result=result)
        except ValueError:
            return render_template('error.html', error="工作时间必须是有效的整数")
    else:
        return render_template('error.html', error="请输入吃饭时间和工作时间")


if __name__ == '__main__':
    app.run(debug = True)