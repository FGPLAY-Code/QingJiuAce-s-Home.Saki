from flask import Flask, render_template, request, jsonify
import socket
import subprocess
import urllib.request
import os
import json
from datetime import datetime

app = Flask(__name__)

# 日志存储目录
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

tools = [
    {'name': '网络工具合集', 'description': 'IP查询、端口扫描等网络工具', 'url': '/network-tools'},
    {'name': '开发工具合集', 'description': '项目日志等开发工具', 'url': '/dev-tools'},
]

@app.route('/')
def index():
    return render_template('index.html', tools=tools)

@app.route('/network-tools')
def network_tools():
    network_tool_list = [
        {'name': 'IP查询', 'description': '查询本机和公网IP地址', 'url': '/ip-query'},
        {'name': 'Ping工具', 'description': '多种模式的网络连通性测试', 'url': '/ping-tool'},
        {'name': 'SSH连接', 'description': '通过OpenSSH连接远程服务器', 'url': '/ssh-tool'},
    ]
    return render_template('network-tools.html', tools=network_tool_list)

@app.route('/ip-query')
def ip_query():
    return render_template('ip-query.html')

@app.route('/api/get-local-ip')
def get_local_ip():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return jsonify({'success': True, 'ip': local_ip})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get-public-ip')
def get_public_ip():
    try:
        with urllib.request.urlopen('https://api.ipify.org?format=json', timeout=5) as response:
            data = response.read().decode()
            import json
            ip_data = json.loads(data)
            return jsonify({'success': True, 'ip': ip_data['ip']})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/ping-tool')
def ping_tool():
    return render_template('ping-tool.html')

@app.route('/api/ping', methods=['POST'])
def ping():
    data = request.json
    host = data.get('host', '')
    mode = data.get('mode', 'normal')
    
    if not host:
        return jsonify({'success': False, 'error': '请输入主机地址'})
    
    try:
        if mode == 'single':
            cmd = ['ping', '-n', '1', host]
            timeout = 5
        else:
            cmd = ['ping', '-n', '4', host]
            timeout = 10
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = result.stdout
        if result.stderr:
            output += '\n' + result.stderr
        return jsonify({'success': True, 'output': output})
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': '执行超时，请检查网络连接'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/ssh-tool')
def ssh_tool():
    return render_template('ssh-tool.html')

@app.route('/api/ssh-connect', methods=['POST'])
def ssh_connect():
    data = request.json
    host = data.get('host', '')
    port = data.get('port', '22')
    username = data.get('username', '')
    
    if not host or not username:
        return jsonify({'success': False, 'error': '请填写完整的连接信息'})
    
    try:
        ssh_cmd = f'start cmd /k "ssh {username}@{host} -p {port}"'
        subprocess.Popen(ssh_cmd, shell=True)
        return jsonify({'success': True, 'message': 'SSH连接窗口已打开，请在新窗口中操作'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/dev-tools')
def dev_tools():
    dev_tool_list = [
        {'name': '项目日志', 'description': '管理项目开发日志', 'url': '/project-logs'},
    ]
    return render_template('dev-tools.html', tools=dev_tool_list)

@app.route('/project-logs')
def project_logs():
    return render_template('project-logs.html')

def get_log_file(project_name):
    return os.path.join(LOGS_DIR, f'{project_name}.json')

def load_logs(project_name):
    log_file = get_log_file(project_name)
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_logs(project_name, logs):
    log_file = get_log_file(project_name)
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

@app.route('/api/get-projects')
def get_projects():
    projects = []
    for filename in os.listdir(LOGS_DIR):
        if filename.endswith('.json'):
            project_name = filename[:-5]
            logs = load_logs(project_name)
            projects.append({
                'name': project_name,
                'log_count': len(logs)
            })
    return jsonify({'success': True, 'projects': projects})

@app.route('/api/get-logs/<project_name>')
def get_logs(project_name):
    logs = load_logs(project_name)
    return jsonify({'success': True, 'logs': logs})

@app.route('/api/add-log', methods=['POST'])
def add_log():
    data = request.json
    project_name = data.get('project_name', '').strip()
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    
    if not project_name or not title:
        return jsonify({'success': False, 'error': '项目名和标题不能为空'})
    
    logs = load_logs(project_name)
    new_log = {
        'id': len(logs) + 1,
        'title': title,
        'content': content,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    logs.insert(0, new_log)
    save_logs(project_name, logs)
    return jsonify({'success': True, 'log': new_log})

@app.route('/api/update-log', methods=['POST'])
def update_log():
    data = request.json
    project_name = data.get('project_name', '').strip()
    log_id = data.get('log_id')
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    
    if not project_name or not log_id or not title:
        return jsonify({'success': False, 'error': '参数不完整'})
    
    logs = load_logs(project_name)
    for log in logs:
        if log['id'] == log_id:
            log['title'] = title
            log['content'] = content
            save_logs(project_name, logs)
            return jsonify({'success': True, 'log': log})
    
    return jsonify({'success': False, 'error': '日志不存在'})

@app.route('/api/delete-log', methods=['POST'])
def delete_log():
    data = request.json
    project_name = data.get('project_name', '').strip()
    log_id = data.get('log_id')
    
    if not project_name or not log_id:
        return jsonify({'success': False, 'error': '参数不完整'})
    
    logs = load_logs(project_name)
    logs = [log for log in logs if log['id'] != log_id]
    save_logs(project_name, logs)
    return jsonify({'success': True})

@app.route('/api/delete-project', methods=['POST'])
def delete_project():
    data = request.json
    project_name = data.get('project_name', '').strip()
    
    if not project_name:
        return jsonify({'success': False, 'error': '项目名不能为空'})
    
    log_file = get_log_file(project_name)
    if os.path.exists(log_file):
        os.remove(log_file)
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'error': '项目不存在'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1314)
