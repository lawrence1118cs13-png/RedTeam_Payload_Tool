import pytest
from payload_generator import PayloadGenerator

def test_boundary_length_truncation():
    """邊界值分析：測試 Payload 長度截斷機制"""
    generator = PayloadGenerator(max_length=50)
    
    # 測試長度 49 (應保留原樣)
    payload_49 = "A" * 49
    assert len(generator.process(payload_49)) == 49
    
    # 測試長度 50 (邊界值，應保留原樣)
    payload_50 = "A" * 50
    assert len(generator.process(payload_50)) == 50
    
    # 測試長度 51 (超出邊界，應截斷為 50)
    payload_51 = "A" * 51
    assert len(generator.process(payload_51)) == 50

def test_equivalence_sqli_encoding():
    """等價劃分：測試 SQL 注入特徵字元集的基礎編碼轉換"""
    generator = PayloadGenerator()
    payload = "' OR 1=1--"
    encoded_payload = generator.encode_sqli(payload)
    
    # 驗證單引號是否被成功轉換 (以簡單 URL 編碼為例)
    assert "'" not in encoded_payload
    assert "%27" in encoded_payload