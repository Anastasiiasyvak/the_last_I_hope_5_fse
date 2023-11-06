from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_report():
    response = client.get("/api/report/my_report?from=2023-01-01&to=2023-12-31")
    assert response.status_code == 200

    expected_report_data = [
        {
            "userId": "db58d6ab-73cb-40fe-819d-ef4f851c74b9",
            "metrics": [
                {"dailyAverage": 1475},
                {"total": 12345},
                {"weeklyAverage": 9800},
            ]
        },
        {
            "userId": "961038b5-3b9b-415b-9bae-cf0634ddcad8",
            "metrics": [
                {"dailyAverage": 1500},
                {"total": 13500},
                {"weeklyAverage": 10000},
            ]
        },
    ]

    assert response.json() == expected_report_data
