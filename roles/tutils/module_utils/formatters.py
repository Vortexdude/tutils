#  (C) Copyright 2024 Github (https://www.Github.com/).
#  This is unpublished proprietary source code of Github. All rights reserved.
#  Notice of copyright on this source code does not indicate publication.
#
#  Contributors:
#      Nitin Namdev <nitinnamdeo456@gmail.com>



import json

def request_formatter(data):
    _response_status = dict()

    if "\r\n\r\n" in data:
        for idx, data in enumerate(data.split("\r\n\r\n")):
            if idx == 0:
                for header in data.split("\r\n"):
                    if ":" in header.strip():
                        if "Date" in header:
                            _response_status['Date'] = header[6:]
                        else:
                            k, v = header.split(":")
                            _response_status[k] = v.strip()
                    else:
                        _response_status['Status-Code'] = header.strip().split("HTTP/1.1 ")[1][:3]

            elif idx == 1:
                if "\r\n" in data:
                    data = data.split("\r\n")[1]
                try:
                    _response_status['body'] = json.loads(data)
                except Exception:
                    _response_status['body'] = {}

    return _response_status

