
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


def test_homepage():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200

from unittest.mock import patch, MagicMock


def test_get_employees():
    mock_connection = MagicMock()
    mock_cursor = mock_connection.__enter__.return_value.cursor.return_value.__enter__.return_value

    mock_cursor.fetchall.return_value = [
        (1, "Arun", "IT"),
        (2, "Priya", "HR")
    ]

    with patch("app.get_db_connection", return_value=mock_connection):
        client = app.test_client()
        response = client.get("/employees")

    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "name": "Arun", "department": "IT"},
        {"id": 2, "name": "Priya", "department": "HR"}
    ]

def test_add_employee_without_name():
    client = app.test_client()

    response = client.post(
        "/employees",
        json={
            "name": "",
            "department": "IT"
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Employee name is required"
    }

def test_update_employee_without_department():
    client = app.test_client()

    response = client.put(
        "/employees/1",
        json={
            "name": "Arun",
            "department": ""
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Department is required"
    }

def test_delete_employee_not_found():
    mock_connection = MagicMock()
    mock_cursor = (
        mock_connection.__enter__.return_value
        .cursor.return_value.__enter__.return_value
    )

    mock_cursor.fetchone.return_value = None

    with patch("app.get_db_connection", return_value=mock_connection):
        client = app.test_client()
        response = client.delete("/employees/999999")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "Employee not found"
    }
