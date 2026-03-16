async def test_create_facilities(ac):
    response_1 = await ac.post(
        "/facilities",
        json={
            "title": "Чайник"
        }
    )
    assert response_1.status_code == 200

    response_2 = await ac.post(
        "/facilities",
        json={
            "title": "Wi-Fi"
        }
    )
    assert response_2.status_code == 200


async def test_get_facilities(ac):
    response_1 = await ac.get(
        "/facilities",
    )
    assert len(response_1.json()) == 2
