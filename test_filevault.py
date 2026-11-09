from app import app

client = app.test_client()

response = client.get(
    "/download",
    query_string={"file_path": "readme.txt"}
)
blocked = client.get("/download", query_string={"file_path": "../private/demo-secret.txt"})
body = blocked.get_data(as_text=True)
assert blocked.status_code == 403
assert "FILEVAULT_TEST_SECRET_42" not in body
print("[PASS] Private file is blocked")
assert response.status_code == 200
assert response.get_data(as_text=True).strip() == "Public readme from FileVault"
print("[PASS] Public file returns the expected text")
missing_client = client.get("/download", query_string={"file_path": "nonexistent.txt"})
assert missing_client.status_code == 404
assert missing_client.get_data(as_text=True).strip() == "File not found"
print("[PASS] File not found")
