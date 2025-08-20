import pytest
from machine import Machine
from sensor import Sensor
from factory_monitor import FactoryMonitor
from main import load_data_from_csv

# -------------------- Test Sensor --------------------
def test_sensor_creation():
    s = Sensor("S1", "Temperature", 25.5)
    assert s.id == "S1"
    assert s.type == "Temperature"
    assert s.reading == 25.5

# -------------------- Test Machine --------------------
def test_machine_add_sensor():
    m = Machine("M1")
    s = Sensor("S1", "Temperature", 25)
    m.add_sensor(s)
    assert len(m.sensors) == 1
    assert m.sensors["Temperature"].reading == 25

def test_machine_health_complete():
    m = Machine("M1")
    m.add_sensor(Sensor("S1", "Temperature", 60))
    m.add_sensor(Sensor("S2", "Pressure", 100))
    m.add_sensor(Sensor("S3", "Vibration", 2))
    health, warnings = m.compute_health()
    assert health == 20
    assert warnings == []

def test_machine_health_missing_sensor():
    m = Machine("M2")
    m.add_sensor(Sensor("S4", "Temperature", 70))
    m.add_sensor(Sensor("S5", "Pressure", 110))
    health, warnings = m.compute_health()
    assert health == 54.0
    assert any("Sensor Offline Warning" in w for w in warnings)

# -------------------- Test Factory Monitor --------------------
def test_factory_monitor_add_machine_and_check():
    m = Machine("M1")
    m.add_sensor(Sensor("S1", "Temperature", 90))
    m.add_sensor(Sensor("S2", "Pressure", 200))
    m.add_sensor(Sensor("S3", "Vibration", 3))
    fm = FactoryMonitor()
    fm.add_machine(m)
    results = fm.check_machines()
    health, alerts = results[m.id]
    assert health == -25.0  # 100 - (90/2 + 200/10 + 3*20) = 100 - (45 + 20 + 60) = -25
    assert any("Critical Machine Failure Risk" in a for a in alerts)

def test_factory_monitor_missing_sensor_alert():
    m = Machine("M2")
    m.add_sensor(Sensor("S4", "Temperature", 70))
    fm = FactoryMonitor()
    fm.add_machine(m)
    results = fm.check_machines()
    health, alerts = results[m.id]
    assert any("Sensor Offline Warning" in a for a in alerts)

# -------------------- Test CSV Loader --------------------
def test_load_data_from_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    # -------------------- Test Sensor --------------------
    def test_sensor_creation():
        s = Sensor("S1", "Temperature", 25.5)
        assert s.id == "S1"
        assert s.type == "Temperature"
        assert s.reading == 25.5

    # -------------------- Test Machine --------------------
    def test_machine_add_sensor():
        m = Machine("M1")
        s = Sensor("S1", "Temperature", 25)
        m.add_sensor(s)
        # sensors is a dict keyed by type or sensor id, not a list
        assert len(m.sensors) == 1
        # Access by type if that's how it's stored
        assert m.sensors["Temperature"].reading == 25

    def test_machine_health_complete():
        m = Machine("M1")
        m.add_sensor(Sensor("S1", "Temperature", 60))
        m.add_sensor(Sensor("S2", "Pressure", 100))
        m.add_sensor(Sensor("S3", "Vibration", 2))
        health, warnings = m.compute_health()
        assert health == 20.0  # 100 - (60/2 + 100/10 + 2*20) = 20
        assert warnings == []

    def test_machine_health_missing_sensor():
        m = Machine("M2")
        m.add_sensor(Sensor("S4", "Temperature", 70))
        m.add_sensor(Sensor("S5", "Pressure", 110))
        health, warnings = m.compute_health()
        # health should be computed with missing vibration as 0
        assert health == 54.0
        assert "Sensor Offline Warning" in warnings

    # -------------------- Test Factory Monitor --------------------
    def test_factory_monitor_add_machine_and_check():
        m = Machine("M1")
        m.add_sensor(Sensor("S1", "Temperature", 90))
        m.add_sensor(Sensor("S2", "Pressure", 200))
        m.add_sensor(Sensor("S3", "Vibration", 3))

        fm = FactoryMonitor()
        fm.add_machine(m)
        results = fm.check_machines()
        health, alerts = results[m.id]
        assert health == 9.0
        assert "Critical Machine Failure Risk" in alerts

    def test_factory_monitor_missing_sensor_alert():
        m = Machine("M2")
        m.add_sensor(Sensor("S4", "Temperature", 70))
        fm = FactoryMonitor()
        fm.add_machine(m)
        results = fm.check_machines()
        health, alerts = results[m.id]
        assert "Sensor Offline Warning" in alerts

    # -------------------- Test CSV Loader --------------------
    def test_load_data_from_csv(tmp_path):
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "machine_id,sensor_id,sensor_type,reading\n"
            "M1,S1,Temperature,60\n"
            "M1,S2,Pressure,100\n"
            "M1,S3,Vibration,2\n"
        )

        machines_dict = load_data_from_csv(str(csv_file))
        assert "M1" in machines_dict
        assert isinstance(machines_dict["M1"], Machine)
        assert len(machines_dict["M1"].sensors) == 3

    def test_load_data_from_csv_file_not_found():
        with pytest.raises(SystemExit):  # main.py exits with SystemExit
            load_data_from_csv("nonexistent.csv")

    # -------------------- Additional Tests --------------------
    def test_machine_health_all_missing():
        m = Machine("M3")
        health, warnings = m.compute_health()
        assert health == 100.0  # All zeros
        assert "Sensor Offline Warning" in warnings

    def test_factory_monitor_multiple_machines():
        m1 = Machine("M1")
        m1.add_sensor(Sensor("S1", "Temperature", 60))
        m1.add_sensor(Sensor("S2", "Pressure", 100))
        m1.add_sensor(Sensor("S3", "Vibration", 2))

        m2 = Machine("M2")
        m2.add_sensor(Sensor("S4", "Temperature", 70))
        m2.add_sensor(Sensor("S5", "Pressure", 110))

        fm = FactoryMonitor()
        fm.add_machine(m1)
        fm.add_machine(m2)
        results = fm.check_machines()
        assert results["M1"][0] == 20.0
        assert results["M2"][0] == 54.0
        assert "Sensor Offline Warning" in results["M2"][1]
