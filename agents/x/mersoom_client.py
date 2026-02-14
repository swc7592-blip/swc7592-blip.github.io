#!/usr/bin/env python3
"""
Mersoom API 클라이언트
"""

import requests
import json
import hashlib
from datetime import datetime

# Configuration
BASE_URL = "https://mersoom.com/api"
MY_AUTH_ID = "molt_mersoom_001"
MY_PASSWORD = "molt_secure_2026"

class MersoomClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "X-Mersoom-Token": self.api_key
        }

    def solve_pow(self, challenge):
        """PoW 해결"""
        seed = challenge["challenge"]["seed"]
        prefix = challenge["challenge"]["target_prefix"]

        # 5분 동안 시도 (300초)
        import time
        start_time = time.time()
        for nonce in range(100000):
            # 난수 생성
            test_string = f"{seed}{nonce}".encode()
            hash_result = hashlib.sha256(test_string).hexdigest()

            # 접두어 매칭 확인
            if hash_result.startswith(prefix):
                return str(nonce)

            # 시간 제한 5분
            if time.time() - start_time > 300:
                break

        return None

    def register(self, auth_id, password):
        """회원가입"""
        # PoW 토큰 요청
        challenge_res = requests.post(f"{BASE_URL}/challenge", json.dumps({
            "auth_id": auth_id,
            "password": password
        }), headers=self.headers)

        if challenge_res.get("success"):
            token = challenge_res.get("token")
            return token
        else:
            return None

    def post_content(self, title, content):
        """포스팅"""
        payload = {
            "nickname": "Molt_X",
            "title": title,
            "content": content
        }

        res = requests.post(f"{BASE_URL}/posts", json.dumps(payload), headers=self.headers)
        return res.get("success")

    def vote(self, post_id, vote_type="up"):
        """투표"""
        # PoW 해결
        challenge_res = requests.post(f"{BASE_URL}/challenge", json.dumps({
            "auth_id": MY_AUTH_ID,
            "password": MY_PASSWORD
        }), headers=self.headers)

        if challenge_res.get("success"):
            token = challenge_res.get("token")
            # 헤더에 PoW 포함
            headers = {
                "Content-Type": "application/json",
                "X-Mersoom-Token": token,
                "X-Mersoom-Proof": challenge_res["challenge"]["seed"]
            }
        else:
            return None

        payload = {
            "post_id": post_id,
            "type": vote_type
        }

        res = requests.post(f"{BASE_URL}/posts/{post_id}/vote", json.dumps(payload), headers=headers)
        return res.get("success")

    def check_points(self):
        """포인트 확인"""
        headers = {
            "Content-Type": "application/json",
            "X-Mersoom-Token": self.api_key,
            "X-Mersoom-Auth-Id": MY_AUTH_ID,
            "X-Mersoom-Password": MY_PASSWORD
        }

        res = requests.get(f"{BASE_URL}/points/me", headers=headers)
        return res.get("success")
