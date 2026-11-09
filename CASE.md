# FileVault: Reading a private file through the download endpoint

## Finding

FileVault lets users choose which file to download. The app did not check
whether the requested path stayed inside the `public` folder. A user could
put `../` in the path to move up one folder and reach a private file.

## Proof

I sent this request to my local Flask app:

```bash
curl -i 'http://127.0.0.1:5001/download?file_path=../private/demo-secret.txt'
```

Before the fix, the app returned `200 OK` and showed
`FILEVAULT_TEST_SECRET_42`. This was a fake secret created for the lab.

## Impact

Someone using the download endpoint could read files outside `public`
if they knew or guessed the path and the app had permission to read them.
I confirmed this with the private test file.

## Fix

The app now resolves the requested path and checks that it stays inside
`public` before reading the file. If the path points outside `public`,
the app returns `403 Forbidden`.

## Verification

After the fix, the same request returned `403 Forbidden` without the test
secret. `python test_filevault.py` checks that the private file is blocked,
the public file still opens, and a missing file returns `404`.
All three checks passed locally and in GitHub Actions.

Semgrep flagged the file read in both versions. The rule could see that
the path came from the request, but it did not account for the folder check
