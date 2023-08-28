from dataclasses import dataclass

import pytest

from common import AnonMode, ScanMode, VerboseOptions
from pg_anon import Context, OutputFormat
from test.entities import CommonValues, DatabaseCredentials


@dataclass
class LocalValues:
    """Test values used during testing in this module."""

    PASSFILE: str = '/tmp/passfile.txt'
    SSL_KEY_FILE: str = '/tmp/.ssl_key_file'
    SSL_CERT_FILE: str = '/tmp/.ssl_cert_file'
    SSL_CA_FILE: str = '/tmp/.ssl_ca_file'
    MODE: AnonMode = AnonMode.DUMP
    COPY_OPTIONS: str = 'with binary'
    FORMAT: OutputFormat = OutputFormat.TEXT
    VERBOSE: VerboseOptions = VerboseOptions.ERROR
    DICT_FILE: str = './some_dict_file.py'
    THREADS: int = 5
    PG_DUMP: str = '/some/path/bin/pg_dump'
    PG_RESTORE: str = '/some/path/bin/pg_restore'
    OUTPUT_DIR: str = '/some/path/'
    INPUT_DIR: str = '/some/other/path/'
    SCAN_MODE: ScanMode = ScanMode.FULL
    OUTPUT_DICT_FILE: str = 'output_file.py'
    SCAN_PARTIAL_ROWS: int = 15


@pytest.fixture
def local_values() -> LocalValues:
    return LocalValues()


def test__all_args(
    db_creds: DatabaseCredentials,
    common_values: CommonValues,
    local_values: LocalValues,
) -> None:
    result = Context.get_arg_parser().parse_args(
        [
            f'--version',
            f'--debug',
            f'--db-host={db_creds.HOST}',
            f'--db-port={db_creds.PORT}',
            f'--db-name={common_values.INITIAL_DB}',
            f'--db-user={db_creds.USER}',
            f'--db-user-password={db_creds.PASSWORD}',
            f'--db-passfile={local_values.PASSFILE}',
            f'--db-ssl-key-file={local_values.SSL_KEY_FILE}',
            f'--db-ssl-cert-file={local_values.SSL_CERT_FILE}',
            f'--db-ssl-ca-file={local_values.SSL_CA_FILE}',
            f'--mode={local_values.MODE}',
            f'--copy-options={local_values.COPY_OPTIONS}',
            f'--format={local_values.FORMAT}',
            f'--verbose={local_values.VERBOSE}',
            f'--dict-file={local_values.DICT_FILE}',
            f'--threads={local_values.THREADS}',
            f'--pg-dump={local_values.PG_DUMP}',
            f'--pg-restore={local_values.PG_RESTORE}',
            f'--output-dir={local_values.OUTPUT_DIR}',
            f'--input-dir={local_values.INPUT_DIR}',
            '--validate-dict',
            '--validate-full',
            '--clear-output-dir',
            '--drop-custom-check-constr',
            '--seq-init-by-max-value',
            '--disable-checks',
            '--skip-data',
            f'--scan-mode={local_values.SCAN_MODE}',
            f'--output-dict-file={local_values.OUTPUT_DICT_FILE}',
            f'--scan-partial-rows={local_values.SCAN_PARTIAL_ROWS}',
        ]
    )

    assert result.version is True
    assert result.debug is True
    assert result.db_host == db_creds.HOST
    assert result.db_port == db_creds.PORT
    assert result.db_name == common_values.INITIAL_DB
    assert result.db_user == db_creds.USER
    assert result.db_user_password == db_creds.PASSWORD
    assert result.db_passfile == local_values.PASSFILE
    assert result.db_ssl_key_file == local_values.SSL_KEY_FILE
    assert result.db_ssl_cert_file == local_values.SSL_CERT_FILE
    assert result.db_ssl_ca_file == local_values.SSL_CA_FILE
    assert result.mode is AnonMode(local_values.MODE)
    assert result.copy_options == local_values.COPY_OPTIONS
    assert result.format is OutputFormat(local_values.FORMAT)
    assert result.verbose is VerboseOptions(local_values.VERBOSE)
    assert result.dict_file == local_values.DICT_FILE
    assert result.threads == local_values.THREADS
    assert result.pg_dump == local_values.PG_DUMP
    assert result.pg_restore == local_values.PG_RESTORE
    assert result.output_dir == local_values.OUTPUT_DIR
    assert result.input_dir == local_values.INPUT_DIR
    assert result.validate_dict is True
    assert result.validate_full is True
    assert result.clear_output_dir is True
    assert result.drop_custom_check_constr is True
    assert result.seq_init_by_max_value is True
    assert result.disable_checks is True
    assert result.skip_data is True
    assert result.scan_mode is ScanMode(local_values.SCAN_MODE)
    assert result.output_dict_file == local_values.OUTPUT_DICT_FILE
    assert result.scan_partial_rows == local_values.SCAN_PARTIAL_ROWS


def test__default_values(
    db_creds: DatabaseCredentials,
    common_values: CommonValues,
    local_values: LocalValues,
) -> None:
    result = Context.get_arg_parser().parse_args([f'--db-host=localhost'])

    assert result.version is False
    assert result.debug is False
    assert result.db_host == 'localhost'
    assert result.db_port == '5432'
    assert result.db_name == 'default'
    assert result.db_user == 'default'
    assert result.db_user_password == ''
    assert result.db_passfile == ''
    assert result.db_ssl_key_file == ''
    assert result.db_ssl_cert_file == ''
    assert result.db_ssl_ca_file == ''
    assert result.mode is AnonMode('init')
    assert result.copy_options == ''
    assert result.format is OutputFormat.BINARY
    assert result.verbose is VerboseOptions.INFO
    assert result.dict_file == ''
    assert result.threads == 4
    assert result.pg_dump == '/usr/bin/pg_dump'
    assert result.pg_restore == '/usr/bin/pg_restore'
    assert result.output_dir == ''
    assert result.input_dir == ''
    assert result.validate_dict is False
    assert result.validate_full is False
    assert result.clear_output_dir is False
    assert result.drop_custom_check_constr is False
    assert result.seq_init_by_max_value is False
    assert result.disable_checks is False
    assert result.skip_data is False
    assert result.scan_mode is ScanMode.PARTIAL
    assert result.output_dict_file == 'output-dict-file.py'
    assert result.scan_partial_rows == 10000
