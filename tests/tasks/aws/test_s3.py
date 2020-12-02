import gzip
from unittest.mock import MagicMock

import pytest

import prefect
from prefect.tasks.aws import S3Download, S3Upload, S3List
from prefect.utilities.configuration import set_temporary_config


class TestS3Download:
    def test_initialization(self):
        task = S3Download()

    def test_initialization_passes_to_task_constructor(self):
        task = S3Download(name="test", tags=["AWS"])
        assert task.name == "test"
        assert task.tags == {"AWS"}

    def test_raises_if_bucket_not_eventually_provided(self):
        task = S3Download()
        with pytest.raises(ValueError, match="bucket"):
            task.run(key="")

    def test_gzip_compression(self, monkeypatch):
        task = S3Download("bucket")
        byte_string = b"col1,col2,col3\nfake,data,1\nfalse,data,2\n"
        gzip_data = gzip.compress(byte_string)

        def modify_stream(Bucket=None, Key=None, Fileobj=None):
            Fileobj.write(gzip_data)

        client = MagicMock()
        boto3 = MagicMock(client=MagicMock(return_value=client))
        monkeypatch.setattr("prefect.utilities.aws.boto3", boto3)
        client.download_fileobj.side_effect = modify_stream

        returned_data = task.run("key", compression="gzip")
        assert returned_data == str(byte_string, "utf-8")

    def test_raises_on_invalid_compression_method(self, monkeypatch):
        task = S3Download("test")
        client = MagicMock()
        boto3 = MagicMock(client=MagicMock(return_value=client))
        monkeypatch.setattr("prefect.utilities.aws.boto3", boto3)

        with pytest.raises(ValueError, match="gz_fake"):
            task.run("key", compression="gz_fake")


class TestS3Upload:
    def test_initialization(self):
        task = S3Upload()

    def test_initialization_passes_to_task_constructor(self):
        task = S3Upload(name="test", tags=["AWS"])
        assert task.name == "test"
        assert task.tags == {"AWS"}

    def test_raises_if_bucket_not_eventually_provided(self):
        task = S3Upload()
        with pytest.raises(ValueError, match="bucket"):
            task.run(data="")

    def test_generated_key_is_str(self, monkeypatch):
        task = S3Upload(bucket="test")
        client = MagicMock()
        boto3 = MagicMock(client=MagicMock(return_value=client))
        monkeypatch.setattr("prefect.utilities.aws.boto3", boto3)
        with set_temporary_config({"cloud.use_local_secrets": True}):
            with prefect.context(
                secrets=dict(
                    AWS_CREDENTIALS={"ACCESS_KEY": "42", "SECRET_ACCESS_KEY": "99"}
                )
            ):
                task.run(data="")
        assert type(client.upload_fileobj.call_args[1]["Key"]) == str

    def test_gzip_compression(self, monkeypatch):
        task = S3Upload("bucket")
        byte_string = b"col1,col2,col3\nfake,data,1\nfalse,info,2\n"

        client = MagicMock()
        boto3 = MagicMock(client=MagicMock(return_value=client))
        monkeypatch.setattr("prefect.utilities.aws.boto3", boto3)

        task.run(byte_string, key="key", compression="gzip")
        args, kwargs = client.upload_fileobj.call_args_list[0]
        gzip_data_stream = args[0]
        assert gzip.decompress(gzip_data_stream.read()) == byte_string

    def test_raises_on_invalid_compression_method(self, monkeypatch):
        task = S3Upload("test")
        client = MagicMock()
        boto3 = MagicMock(client=MagicMock(return_value=client))
        monkeypatch.setattr("prefect.utilities.aws.boto3", boto3)

        with pytest.raises(ValueError, match="gz_fake"):
            task.run(b"data", compression="gz_fake")


class TestS3List:
    def test_initialization(self):
        task = S3List()

    def test_initialization_passes_to_task_constructor(self):
        task = S3List(name="test", tags=["AWS"])
        assert task.name == "test"
        assert task.tags == {"AWS"}

    def test_raises_if_bucket_not_eventually_provided(self):
        task = S3List()
        with pytest.raises(ValueError, match="bucket"):
            task.run(prefix="fake/path")
