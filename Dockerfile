FROM python:3

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
  && unzip -q awscliv2.zip \
  && ./aws/install

RUN apt-get update \
  && apt-get install -y jq

COPY entrypoint.sh /entrypoint.sh
COPY src/format_json_to_html.py /format_json_to_html.py

ENTRYPOINT ["/entrypoint.sh"]
