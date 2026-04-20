from fastapi import FastAPI
from pydantic import BaseModel
import time
import uuid
import hmac
import hashlib
import base64
import urllib.parse

app = FastAPI()

# =========================
# Request Model
# =========================
class OAuthRequest(BaseModel):
    account_id: str
    consumer_key: str
    consumer_secret: str
    token_id: str
    token_secret: str
    base_url: str
    http_method: str = "POST"


# =========================
# Helper: Percent Encode
# =========================
def percent_encode(val: str) -> str:
    return urllib.parse.quote(val, safe='~')


# =========================
# Generate OAuth Header
# =========================
@app.post("/generate-oauth")
def generate_oauth(req: OAuthRequest):

    # STEP 1 — OAuth params
    oauth_params = {
        "oauth_consumer_key": req.consumer_key,
        "oauth_token": req.token_id,
        "oauth_signature_method": "HMAC-SHA256",
        "oauth_timestamp": str(int(time.time())),
        "oauth_nonce": uuid.uuid4().hex,
        "oauth_version": "1.0"
    }

    # STEP 2 — Normalize params
    sorted_params = sorted(oauth_params.items())

    normalized_params = "&".join(
        f"{percent_encode(k)}={percent_encode(v)}"
        for k, v in sorted_params
    )

    # STEP 3 — Base string
    base_string = "&".join([
        req.http_method.upper(),
        percent_encode(req.base_url),
        percent_encode(normalized_params)
    ])

    # STEP 4 — Signing key
    signing_key = f"{req.consumer_secret}&{req.token_secret}"

    # STEP 5 — HMAC SHA256
    hashed = hmac.new(
        signing_key.encode("utf-8"),
        base_string.encode("utf-8"),
        hashlib.sha256
    )

    signature = base64.b64encode(hashed.digest()).decode()

    # STEP 6 — OAuth Header
    oauth_header = "OAuth " + ", ".join([
        f'realm="{req.account_id}"',
        f'oauth_consumer_key="{req.consumer_key}"',
        f'oauth_token="{req.token_id}"',
        f'oauth_signature_method="HMAC-SHA256"',
        f'oauth_timestamp="{oauth_params["oauth_timestamp"]}"',
        f'oauth_nonce="{oauth_params["oauth_nonce"]}"',
        f'oauth_version="1.0"',
        f'oauth_signature="{percent_encode(signature)}"'
    ])

    return {
        "oauth_header": oauth_header,
        "signature": signature,
        "base_string": base_string
    }
