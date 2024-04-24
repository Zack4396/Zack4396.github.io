#!/usr/bin/env python3
# Author: Zack4396(zokkkki)
# Date: 2024-04-22
# Description: This is a Python script for subscribe convert


def base64_decode(data):
    import base64

    return base64.urlsafe_b64decode(data + "=" * (4 - len(data) % 4)).decode("utf-8")


def is_base64(s):
    try:
        base64_decode(s)
        return True
    except:
        return False


class protocol(object):
    def __init__(self, name, link) -> None:
        self._name = name
        self._link = link
        pass

    def decode(self):
        raise NotImplementedError("decode() method must be implemented")


class protocolA:
    # S-S-:-/-/
    name = b"\x73\x73\x3a\x2f\x2f".decode()
    # S-H-A-D-O-W-S-O-C-K-S
    protocol = b"\x73\x68\x61\x64\x6f\x77\x73\x6f\x63\x6b\x73".decode()

    def decode(self, link):
        import urllib.parse

        body = link.replace(self.name, "").replace("\r", "")
        header, footer = body.split("#")

        if is_base64(header):
            import re

            """
                 [base64]
                    |
                  (dec)
                    |
                    v
                 [method]:[uuid]@[addr]:[port]
            """
            method, uuid, addr, port = re.split(r"[:@]", base64_decode(header))
            note = footer
        else:
            import re

            """
                 [base64]@[addr]:[port]
                    |
                  (dec)
                    |
                    v
                 [method]:[uuid]
            """
            method_uuid, addr, port = re.split(r"[:@]", header)
            method, uuid = base64_decode(method_uuid).split(":")
            note = urllib.parse.unquote(footer.split("%20")[1])
        return {
            "uuid": uuid,
            "port": port,
            "addr": addr,
            "protocol": self.protocol,
            "method": method,
            "note": note,
        }


class protocolB:
    # V-M-E-S-S-:-/-/
    name = b"\x76\x6d\x65\x73\x73\x3a\x2f\x2f".decode()
    # V-M-E-S-S
    protocol = b"\x76\x6d\x65\x73\x73".decode()

    def decode(self, link):
        body = link.replace(self.name, "")
        decoded_body = base64_decode(body)
        decoded_body = eval(decoded_body)

        return {
            "uuid": decoded_body["id"],
            "port": decoded_body["port"],
            "addr": decoded_body["add"],
            "protocol": self.protocol,
            "note": decoded_body["ps"].split(" ")[1],
        }


def fetch_subscribe_content(url):
    try:
        import requests
    except ImportError:
        print(f"requests is not install, please run")
        print(f"$ pip install requests")
        exit(1)

    try:
        req = requests.get(url, timeout=(10, 10), verify=False)
    except Exception:
        print(
            "\nFailed to fetch subscribe content: \033[1;31m(please check subscribe URL or network)\033[0m"
        )
        exit(1)

    return req.content


def decode_subscribe_content(content):
    import base64

    try:
        decoded_content = base64.b64decode(content).decode("utf-8") if content else None
    except Exception:
        print(
            "\nFailed to decode subscribe content: \033[1;31m(the subscription token is wrong, please check it again)\033[0m"
        )
        exit(1)

    if content == b"":
        print(
            "\nFailed to decode subscribe content: \033[1;31m(the subscription is expired, please renewal it)\033[0m"
        )
        exit(1)

    return decoded_content.strip().split("\n") if decoded_content else []


def decode_protocol_links(links):
    data = []

    protocols = {
        protocolA.name: protocolA(),
        protocolB.name: protocolB(),
    }

    for link in links:
        for protocol_name, protocol_obj in protocols.items():
            if link.startswith(protocol_name):
                data.append(protocol_obj.decode(link))

    return data


def args_parse():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Subscribe Convert Tool")

    parser.add_argument(
        "-s", "--subscribe", metavar="URL", required=True, help="URL to subscribe"
    )
    parser.add_argument(
        "-o", "--outdir", metavar="DIR", required=True, help="Path to outdir"
    )

    debug = parser.add_argument_group("test options")
    debug.add_argument("--fakecontent", help="fake content")

    return parser.parse_args()


def main():
    import os
    import json

    args = args_parse()

    if args.fakecontent:
        content = open(args.fakecontent, "rb").read()
    else:
        content = fetch_subscribe_content(args.subscribe)

    links = decode_subscribe_content(content)

    data = decode_protocol_links(links)

    count = 0
    for item in data:
        count += 1
        filename = os.path.join(args.outdir, f"server{count:02d}.conf")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(item, f, indent=4, ensure_ascii=False)
            print(
                f"Output file saved at \033[1;32m{os.path.realpath(f.name)}\033[0m ({count:02d}: {item['note']})"
            )
    print("Subscribe conversion: \033[1;32mCompleted\033[0m")


if __name__ == "__main__":
    main()
