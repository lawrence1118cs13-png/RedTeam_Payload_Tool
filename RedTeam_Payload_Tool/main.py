from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from payload_generator import PayloadGenerator

app = FastAPI(title="Red Team Payload Generator API")

# 定義 API 請求格式 (加入基礎的輸入檢查)
class PayloadRequest(BaseModel):
    # 限定 payload 不能為空，且最少要 1 個字元
    payload: str = Field(..., min_length=1, description="原始 Payload")
    max_length: int = Field(50, gt=0, description="最大長度限制")
    encode_type: str = Field("none", description="編碼類型: none 或 sqli")

@app.post("/api/v1/generate")
def generate_payload(request: PayloadRequest):
    try:
        # 1. 檢查編碼類型是否合法 (例外處理示範)
        if request.encode_type not in ["none", "sqli"]:
            raise ValueError(f"不支援的編碼類型: {request.encode_type}")

        # 2. 實例化生成器並處理
        generator = PayloadGenerator(max_length=request.max_length)
        processed_payload = generator.process(request.payload)
        
        if request.encode_type == "sqli":
            processed_payload = generator.encode_sqli(processed_payload)
            
        return {
            "status": "success",
            "original_payload": request.payload,
            "generated_payload": processed_payload,
            "final_length": len(processed_payload)
        }
        
    except ValueError as e:
        # 捕捉我們自定義的錯誤，回傳 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 捕捉其他未知的系統錯誤，回傳 500 Internal Server Error
        raise HTTPException(status_code=500, detail="伺服器內部發生錯誤")