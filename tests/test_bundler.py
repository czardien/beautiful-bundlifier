import pytest
import tempfile

from src import bundler
from lib.config import Config
from lib.models.notification_manager import NotificationManager


@pytest.fixture
def tmp_file():
    tmp_file = tempfile.NamedTemporaryFile()
    content = "2017-08-01 00:06:47,F62712701E7AF6588B69A44235A6FC,06D188F4064E0D47BD760EEFEB7AAD,Geir\n" \
        "2017-08-01 00:31:05,DF5BB50FAD220C8D2A8FF9A0DBAA47,588C89FCADD0DBA0E722822513A267,Antim\n" \
        "2017-08-01 00:35:24,8473CCCE79294CB494D1B42E2B1BAA,EDBB3D240ADBCF6CF175B192630ABB,Σωτήριος"
    tmp_file.write(bytes(content, encoding="utf-8"))
    tmp_file.seek(0)

    yield tmp_file
    tmp_file.close()


def test_capture_output_naive(tmp_file, capsys):
    NotificationManager.from_config(Config.MAX_NOTIFICATIONS_PER_DAY, Config.ANALYSIS, Config.INITIAL_TS)
    bundler.bundle(tmp_file.name, Config.CSV_HEADERS, Config.CSV_DELIMITER)
    captured = capsys.readouterr()

    expected_out = "\n".join([
        "2017-08-01 00:06:47,2017-08-01 00:06:47,1,F62712701E7AF6588B69A44235A6FC,Geir went on a tour",
        "2017-08-01 00:31:05,2017-08-01 00:31:05,1,DF5BB50FAD220C8D2A8FF9A0DBAA47,Antim went on a tour",
        "2017-08-01 00:35:24,2017-08-01 00:35:24,1,8473CCCE79294CB494D1B42E2B1BAA,Σωτήριος went on a tour",
        "",
    ])

    assert captured.out == expected_out
