
import toml

from quickette.repo import Repository

def test_setup(tmpdir):
    root = tmpdir / "repo"
    r = Repository(root, create=True)

    for file in root, root / ".config", root / ".config" / "main":
        assert file.exists()

    assert r.allocate_ticket_id() == "1"
    assert r.allocate_ticket_id() == "2"
    assert r.allocate_ticket_id() == "3"

    for file in root / ".config" / "last_id", :
        assert file.exists()

def test_id_format(tmpdir):
    root = tmpdir / "repo"
    r = Repository(root, create=True)

    r.config["id-format"] = "MJD-{:03d}"
    assert r.format_ticket_id(1) == "MJD-001"

def test_reconfigure(tmpdir):
    root = tmpdir / "repo"
    r = Repository(root, create=True)

    conf = r.default_config()
    conf["id-format"] = "TICKET{:02d}"

    with open(r.main_config_file(), "w") as fh:
        toml.dump(conf, fh)

    assert r.format_ticket_id(1) == "1"
    r.reload_configuration()
    assert r.format_ticket_id(2) == "TICKET02"
