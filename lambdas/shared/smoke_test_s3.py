import tempfile

from .s3_io import (
    download_file,
    generate_presigned_url,
    read_json,
    upload_file,
    write_json,
)


def run_smoke_test(bucket: str, prefix: str = "smoke-test") -> None:
    payload = {"smoke": True, "message": "s3_io smoke test"}
    json_key = f"{prefix}/test.json"
    text_key = f"{prefix}/test.txt"

    write_json(json_key, payload, bucket=bucket)
    parsed = read_json(json_key, bucket=bucket)
    assert parsed == payload

    with tempfile.NamedTemporaryFile("w", delete=False) as source:
        source.write("hello")
        source_path = source.name

    upload_file(source_path, text_key, bucket=bucket, content_type="text/plain")

    with tempfile.NamedTemporaryFile("r", delete=False) as target:
        target_path = target.name

    download_file(text_key, target_path, bucket=bucket)
    with open(target_path, "r", encoding="utf-8") as downloaded:
        assert downloaded.read() == "hello"

    url = generate_presigned_url(json_key, bucket=bucket)
    print(url)
    print("S3 smoke test passed.")


if __name__ == "__main__":
    import sys

    run_smoke_test(sys.argv[1])
