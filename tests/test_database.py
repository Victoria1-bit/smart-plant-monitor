def test_empty_database_gets_a_week_of_simulated_readings(signed_in):
    readings = signed_in.get("/api/readings?hours=200").json()
    assert len(readings) == 7 * 24
    assert all(r["simulated"] for r in readings)


def test_new_reading_is_saved(signed_in):
    before = len(signed_in.get("/api/readings?hours=200").json())
    reading = signed_in.get("/api/reading").json()
    after = signed_in.get("/api/readings?hours=200").json()
    assert len(after) == before + 1
    assert after[0]["timestamp"] == reading["timestamp"]


def test_readings_are_newest_first(signed_in):
    times = [r["timestamp"] for r in signed_in.get("/api/readings?limit=10").json()]
    assert len(times) == 10
    assert times == sorted(times, reverse=True)


def test_settings_start_at_30_and_70(signed_in):
    assert signed_in.get("/api/settings").json() == {"dry_threshold": 30, "wet_threshold": 70}


def test_settings_are_saved(signed_in):
    response = signed_in.put("/api/settings", json={"dry_threshold": 20, "wet_threshold": 80})
    assert response.status_code == 200
    assert signed_in.get("/api/settings").json() == {"dry_threshold": 20, "wet_threshold": 80}


def test_dry_level_must_be_below_wet_level(signed_in):
    response = signed_in.put("/api/settings", json={"dry_threshold": 60, "wet_threshold": 40})
    assert response.status_code == 400


def test_status_follows_the_saved_levels(signed_in):
    moisture = signed_in.get("/api/status").json()["reading"]["moisture"]
    # Put the dry level above the reading: it must now count as dry and the light is on
    signed_in.put("/api/settings", json={"dry_threshold": 60, "wet_threshold": 95})
    status = signed_in.get("/api/status").json()
    if moisture < 60:
        assert status["reading"]["status"] == "Dry"
        assert status["light"] == "On"
