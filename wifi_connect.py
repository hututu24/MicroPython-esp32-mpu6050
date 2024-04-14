import network
import machine
import time
import ujson as json
import usocket as socket
import ure
import ujson

# 设置AP模式的WiFi信息
AP_SSID = "ESP32_Setup"
AP_PASSWORD = "password"
HTTP_PORT = 80

# 保存WiFi账号密码的文件名
CREDENTIALS_FILE = "wifi_credentials.json"

# 创建热点并启动HTTP服务器
def create_ap_and_server():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=AP_SSID, password=AP_PASSWORD)

    addr = socket.getaddrinfo('0.0.0.0', HTTP_PORT)[0][-1]
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(addr)
    server_sock.listen(5)

    print('Access Point Created:', AP_SSID)
    print('Web Server Listening on', addr)

    return server_sock

# 保存WiFi账号密码到文件
def save_credentials_to_file(ssid, password):
    data = {'ssid': ssid, 'password': password}
    with open(CREDENTIALS_FILE, 'w') as file:
        file.write(json.dumps(data))

# 处理HTTP POST请求
def handle_post_request(data):
    try:
        json_data = json.loads(data)
        if 'ssid' in json_data and 'password' in json_data:
            save_credentials_to_file(json_data['ssid'], json_data['password'])
            return 'WiFi credentials saved successfully'
        else:
            return 'Invalid JSON data'
    except Exception as e:
        return 'Error processing JSON data: {}'.format(e)

# 主程序
def main():
    # 创建热点并启动HTTP服务器
    server_sock = create_ap_and_server()

    while True:
        conn, addr = server_sock.accept()
        print('Got a connection from', addr)
        request = conn.recv(1024).decode('utf-8')
        if request:
            print('Received HTTP Request:', request)
            if request.startswith('POST'):
                _, _, content = request.partition('\r\n\r\n')

                # 使用正则表达式匹配数据
                match = ure.search(r'ssid=(.*?)&password=(.*?)$', content)
                if match:
                    ssid = match.group(1)
                    password = match.group(2)
                    print('SSID:', ssid)
                    print('Password:', password)
                else:
                    print('Data format error')

                # 读取 JSON 文件内容
                with open('wifi_config.json', 'r') as file:
                    data = ujson.load(file)

                # 修改 JSON 数据
                data['ssid'] = ssid
                data['password'] = ssid

                # 将修改后的数据写回文件
                with open('wifi_config.json', 'w') as file:
                    ujson.dump(data, file)

                response = data
                conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{}'.format(response))
                print('receive_data_success,robot_now')
                machine.reset()
            else:
                with open('index.html', 'r') as file:
                    conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{}'.format(file.read()))
        conn.close()
        
# 连接WiFi
def connect_wifi():
    with open('wifi_config.json', 'r') as file:
        data = ujson.load(file)
    ssid = data['ssid']
    password = data['password']
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        time.sleep(10)
        
    connect_status = False
    if wlan.isconnected():
        connect_status = True
        print(wlan.ifconfig())
    print('WiFi Connected Status:',connect_status)
    return connect_status

def connect():
    if connect_wifi() == False:
        main()
    
    
    
if __name__ == '__main__':
    main()
