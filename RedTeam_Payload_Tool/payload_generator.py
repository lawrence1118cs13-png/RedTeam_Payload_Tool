import urllib.parse

class PayloadGenerator:
    def __init__(self, max_length: int = 50):
        self.max_length = max_length

    def process(self, payload: str) -> str:
        """處理 Payload 長度限制"""
        if len(payload) > self.max_length:
            # 進行截斷處理
            return payload[:self.max_length]
        return payload

    def encode_sqli(self, payload: str) -> str:
        """模擬 WAF 繞過：基礎 SQLi 字元 URL 編碼"""
        # 實務上會有更複雜的混淆邏輯，此處先以 URL 編碼通過等價劃分測試
        return urllib.parse.quote(payload)