import requests
from requests_ratelimiter import LimiterSession
import argparse
import sys
import json

base_url = "https://data.sec.gov/api/xbrl/companyfacts/"

ratelimit_calls = 10
ratelimit_period = 1

parser = argparse.ArgumentParser()

parser.add_argument("user_agent", type=str, help="The user agent header required by the sec website to accept http requests.  Should be <Full Name> <Email>.")
parser.add_argument("tickers_file", type=str, help="The location of the file which contains the company tickers.")

args = parser.parse_args()

if not args.user_agent:
    print(f"Invalid user agent arg: {args.user_agent}")
    sys.exit()

if not args.tickers_file:
    print(f"Invalid tickers file arg: {args.tickers_file}")
    sys.exit()

session = LimiterSession(per_second=10)

session.headers.update({
    "User-Agent": args.user_agent,
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate"
})

with open(args.tickers_file, "r", encoding="utf-8") as in_file:

    for line in in_file:
        if "\"cik\":" in line:
            str_split = line.split(':')

            if len(str_split) == 2:
                cik_num = str_split[1]
                str_mapping = str.maketrans({'"': '', ' ': '', ',': '', '\n': ''})
                trimmed_cik = cik_num.translate(str_mapping)
                
                response = session.get(f"{base_url}{trimmed_cik}.json")
                
                if response.status_code == 200:
                    data = response.json()

                    with open(f"output/xbrl_facts/{trimmed_cik}_xbrl.json", "w", encoding="utf-8") as out_file:
                        json.dump(data, out_file, indent=4, ensure_ascii=False)
                        out_file.close()

                else:
                    print(f"status code {response.status_code} for {base_url}{trimmed_cik}.json")

            else:
                print(f"Invalid format for line: {line}")

    