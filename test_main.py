import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_update_task():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        create_resp = await ac.post("/auth/createtask", json={"title": "Тестовая задача", "description": "dscr"})
        print(f"\nStatus Code: {create_resp.status_code}")
        print(f"Response Body: {create_resp.json()}")
         
        assert create_resp.status_code == 200, f"Ошибка при создании: {create_resp.text}"

        task_id = create_resp.json()["id"]

        patch_resp = await ac.patch(f"auth/tasks/{task_id}", params={"is_completed": True})
        
        assert patch_resp.status_code == 200
        assert patch_resp.json()["is_completed"] is True