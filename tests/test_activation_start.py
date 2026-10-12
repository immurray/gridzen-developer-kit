import json
import sys
from gridzen_developer.cli import main


def test_start_is_local_and_preserves_language(monkeypatch,capsys):
    import socket
    monkeypatch.setattr(socket,"create_connection",lambda *a,**k: (_ for _ in ()).throw(AssertionError("unexpected network")))
    for lang in ("en","es","zh"):
        monkeypatch.setattr(sys,"argv",["gridzen","start","--lang",lang])
        main();data=json.loads(capsys.readouterr().out)
        assert data["network_calls"]==0 and not data["verified"] and not data["real_payments_enabled"]
        assert "source=developer_kit" in data["account"]
        assert all("lang="+lang in data[k] for k in ("trial","account","assistant","tutorials"))
