import http.client
import urllib.parse
import time
import json

# Настройки
domain = "pin-up772.com"
slack_webhook_url = "https://hooks.slack.com/1234567890"
proxy = {
    "host": "11.22.33.44",
    "port": 8080,
    "auth": "olqIqKYvDD1xPQ87:",
    "mode": "mobile;",
    "geo": "tr;",
    "scheme": "http"
}
check_interval = 60  # время ожидания между блоками проверок
failures_limit = 3  # количество неудачных попыток подряд
attempts_delay = 1  # задержка между попытками (в секундах)


def send_slack_notification(message):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "text": message
    }

    conn = http.client.HTTPSConnection("hooks.slack.com")
    conn.request("POST", slack_webhook_url, body=json.dumps(payload), headers=headers)
    response = conn.getresponse()
    data = response.read()

    print(f"Sent notification to Slack. Response: {data.decode('utf-8')}")


def check_site():
    conn = http.client.HTTPConnection(proxy_host, proxy_port)
    headers = {
        "Proxy-Authorization": f"Basic {proxy.auth}",
        "Host": domain
    }

    conn.request("GET", f"https://{domain}", headers=headers)
    response = conn.getresponse()
    return response.status == 200

def main():
    while True:
        failures = 0

        for _ in range(failures_limit):
            if not check_site():
                failures += 1
            time.sleep(attempts_delay)

        if failures >= failures_limit:
            send_slack_notification(f"Site {domain} is down!")

        time.sleep(check_interval)


if __name__ == "__main__":
    main()
