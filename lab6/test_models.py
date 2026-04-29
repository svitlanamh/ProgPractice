import csv
import pytest
from pydantic import ValidationError
from models import Block, Person, Source, Vote

def test_valid_block():
    b = Block(block_id="a1b2c3d4", view=150, desc="Genesis block")
    assert b.block_id == "a1b2c3d4"
    assert b.view == 150
    assert b.desc == "Genesis block"

def test_block_invalid_id_format():
    with pytest.raises(ValidationError):
        Block(block_id="abc", view=10)

def test_block_negative_view():
    with pytest.raises(ValidationError):
        Block(block_id="a1b2c3d4", view=-5)

def test_valid_person():
    p = Person(name="Ivan Meyhes", addr="Kyiv, Ukraine")
    assert p.name == "Ivan Meyhes"
    assert p.addr == "Kyiv, Ukraine"

def test_person_empty_name():
    with pytest.raises(ValidationError):
        Person(name="", addr="Kyiv, Ukraine")

def test_valid_source():
    s = Source(ip_addr="192.168.0.1", country_code="UA")
    assert s.ip_addr == "192.168.0."
    assert s.country_code == "UA"

def test_source_invalid_ip():
    with pytest.raises(ValidationError):
        Source(ip_addr="not-an-ip-address", country_code="US")

def test_source_invalid_country_code():
    with pytest.raises(ValidationError):
        Source(ip_addr="10.0.0.1", country_code="UKR")

def test_valid_vote():
    v = Vote(voter_id=1, block_id="ff00ff00", source_id=42)
    assert v.voter_id == 1
    assert v.block_id == "ff00ff00"

def test_vote_invalid_voter_id():
    with pytest.raises(ValidationError):
        Vote(voter_id=0, block_id="ff00ff00", source_id=42)

def test_vote_invalid_block_id():
    with pytest.raises(ValidationError):
        Vote(voter_id=1, block_id="wrong_id", source_id=42)

def test_blocks_from_csv():
    with open("lab6/data.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            Block(
                block_id=row["id"],
                view=int(row["view"])
            )

