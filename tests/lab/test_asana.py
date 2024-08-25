from aiforge.lab.asana import load_asanas, print_asanas
import logging

def test_load_asanas():
    asanas = load_asanas()
    assert isinstance(asanas, list)
    assert len(asanas) > 0
    for asana in asanas:
        assert "id" in asana
        assert "name" in asana
        assert "sanskrit" in asana


def test_load_asanas_content():
    asanas = load_asanas()
    # Check for a few specific asanas that we know should be in the file
    asana_names = [asana["name"] for asana in asanas]
    assert "Mountain Pose" in asana_names
    assert "Downward-Facing Dog" in asana_names
    assert "Warrior I" in asana_names


def test_print_asanas(caplog):
    asanas = load_asanas()
    with caplog.at_level(logging.INFO):
        print_asanas(asanas)
        assert f"Loaded {len(asanas)} asanas: " in caplog.text
        assert "ID: 1, Name: Mountain Pose, Sanskrit: Tadasana" in caplog.text
        assert "..." in caplog.text


def test_print_asanas_empty_list(caplog):
    with caplog.at_level(logging.INFO):
        print_asanas([])
        assert "Loaded 0 asanas:" in caplog.text
        assert "..." in caplog.text