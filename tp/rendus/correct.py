#!/usr/bin/env python3

"""
Correction script.
"""

# TODO: detect type of key: RSA or EC
# TODO: check http to https redirect

import argparse
import json
from pathlib import Path
from shutil import rmtree
import subprocess
import sys
from typing import Optional
from zipfile import ZipFile

ZIP_DIR = Path(__file__).parent
BASE_DIR = ZIP_DIR.parent


class Correct:
    """Correction tests suite."""

    def __init__(
        self,
        zip_file: Path,
        keep: bool,
        keep_containers: bool,
        openssl_path: str,
        verbose: int,
    ) -> None:
        # initialize variables
        self.zip_file = zip_file
        self.workdir = ZIP_DIR / self.zip_file.stem
        if self.workdir.joinpath("docker-compose.yml").exists():
            self.dockercompose = self.workdir / "docker-compose.yml"
        else:
            self.dockercompose = BASE_DIR / "docker-compose.yml"
        print(self.dockercompose)
        self.points = 0
        self.points_totals = 22
        self.keep = keep
        self.keep_containers = keep_containers
        self.openssl = openssl_path
        self.verbose = verbose
        self.nginx_config_ok = False
        self.nginx_running = False
        self.docker_cmd = [
            "docker-compose",
            "--file",
            str(self.dockercompose),
            "--project-name",
            f"crypto-tp-{self.workdir.name.lower()}",
            "--project-directory",
            str(self.workdir),
        ]

        # extract zip file
        self.extract()

        self.test_required_files(1)

        # run openssl tests
        self.test_ca_privkey_valid(1)
        self.test_ca_cert_valid(1)
        self.test_ca_cert_match_privkey(2)
        self.test_web_privkey_valid(1)
        self.test_web_csr_valid(1)
        self.test_web_csr_match_privkey(1)
        self.test_web_csr_has_san(1)
        self.test_web_cert_valid(1)
        self.test_web_cert_match_privkey(2)
        self.test_web_cert_signed_by_ca(3)
        self.test_web_cert_has_san(1)

        # start docker environment
        self.docker_up()

        # remove existing testssl results
        self.workdir.joinpath("certs", "results.json").unlink(missing_ok=True)
        self.workdir.joinpath("certs", "output.log").unlink(missing_ok=True)

        # run docker tests
        self.test_nginx_config(1)
        self.test_testssl(5)

    def __del__(self) -> None:
        note = self.points * 20 / self.points_totals
        if self.verbose >= 1:
            print("\n")
        print(f"Note: {note:.2f}/20")

        # stop docker environment
        if not self.keep_containers:
            self.docker_down()

        # remove workdir
        if not self.keep:
            rmtree(self.workdir, ignore_errors=True)

    def docker_up(self, service: Optional[str] = None) -> None:
        """Start docker environment."""

        cmd = self.docker_cmd + [
            "up",
            "--detach",
        ]
        if service:
            cmd.append(service)
        if self.verbose >= 2:
            print(" ".join(cmd))
        try:
            subprocess.run(cmd, capture_output=not self.verbose, check=True)
        except subprocess.CalledProcessError as err:
            print(err.stderr.decode())
            self.docker_down()
            raise err

        if self.verbose >= 2:
            subprocess.run(self.docker_cmd + ["ps"])
            subprocess.run(self.docker_cmd + ["logs"])

    def docker_down(self) -> None:
        """Shutdown docker environment."""

        cmd = self.docker_cmd + [
            "down",
            "--volumes",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        subprocess.run(cmd, capture_output=True, check=True)

    def extract(self) -> None:
        """Extract if zip exists and not already extracted."""

        if self.zip_file.exists() and not self.workdir.is_dir():
            with ZipFile(self.zip_file) as zip_object:
                files_to_extract = [
                    x for x in zip_object.namelist() if x.startswith(self.zip_file.stem)
                ]
                zip_object.extractall(path=ZIP_DIR, members=files_to_extract)
        elif not self.zip_file.exists():
            print(f"error: {self.zip_file} does not exist")
            sys.exit(1)

    def test_required_files(self, points) -> bool:
        """> Check that all required file exist."""

        if self.verbose >= 1:
            print("\n" + str(self.test_required_files.__doc__))

        if not (
            self.workdir.is_dir()
            and self.workdir.joinpath("certs/").is_dir()
            and self.workdir.joinpath("certs/ca.cert.pem").is_file()
            and self.workdir.joinpath("certs/ca.privkey.pem").is_file()
            and self.workdir.joinpath("certs/web.cert.pem").is_file()
            and self.workdir.joinpath("certs/web.csr.pem").is_file()
            and self.workdir.joinpath("certs/web.privkey.pem").is_file()
            and self.workdir.joinpath("config/").is_dir()
            and self.workdir.joinpath("config/nginx.conf").is_file()
        ):
            if self.verbose >= 1:
                print("error: at least one of the required files is missing")
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_ca_privkey_valid(self, points) -> bool:
        """> Check that the CA private key is valid."""

        if self.verbose >= 1:
            print("\n" + str(self.test_ca_privkey_valid.__doc__))

        if not self.workdir.joinpath("certs/ca.privkey.pem").is_file():
            print("error: file does not exists")
            return False

        cmd = [
            self.openssl,
            "pkey",
            "-in",
            str(self.workdir.joinpath("certs/ca.privkey.pem")),
            "-noout",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        res = subprocess.run(cmd, capture_output=True)

        if res.returncode != 0:
            if self.verbose >= 1:
                print("error: " + res.stderr.decode())
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_ca_cert_valid(self, points) -> bool:
        """> Check that the CA certificate is valid."""

        if self.verbose >= 1:
            print("\n" + str(self.test_ca_cert_valid.__doc__))

        if not self.workdir.joinpath("certs/ca.cert.pem").is_file():
            print("error: file does not exists")
            return False

        cmd = [
            self.openssl,
            "x509",
            "-in",
            str(self.workdir.joinpath("certs/ca.cert.pem")),
            "-noout",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        res = subprocess.run(cmd, capture_output=True)

        if res.returncode != 0:
            if self.verbose >= 1:
                print("error: " + res.stderr.decode())
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_ca_cert_match_privkey(self, points) -> bool:
        """> Check that the CA certificate matches with its private key."""

        if self.verbose >= 1:
            print("\n" + str(self.test_ca_cert_match_privkey.__doc__))

        if (
            not self.workdir.joinpath("certs/ca.privkey.pem").is_file()
            or not self.workdir.joinpath("certs/ca.cert.pem").is_file()
        ):
            print("error: file does not exists")
            return False

        cmd_privkey = [
            self.openssl,
            "pkey",
            "-in",
            str(self.workdir.joinpath("certs/ca.privkey.pem")),
            "-pubout",
        ]
        cmd_cert = [
            self.openssl,
            "x509",
            "-in",
            str(self.workdir.joinpath("certs/ca.cert.pem")),
            "-noout",
            "-pubkey",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd_privkey))
        res_privkey = subprocess.run(cmd_privkey, capture_output=True)
        if self.verbose >= 2:
            print(" ".join(cmd_cert))
        res_cert = subprocess.run(cmd_cert, capture_output=True)

        if not res_privkey.stdout == res_cert.stdout:
            if self.verbose >= 1:
                print("error: does not match")
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_web_privkey_valid(self, points) -> bool:
        """> Check that the web private key is valid."""

        if self.verbose >= 1:
            print("\n" + str(self.test_web_privkey_valid.__doc__))

        if not self.workdir.joinpath("certs/web.privkey.pem").is_file():
            print("error: file does not exists")
            return False

        cmd = [
            self.openssl,
            "pkey",
            "-in",
            str(self.workdir.joinpath("certs/web.privkey.pem")),
            "-noout",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        res = subprocess.run(cmd, capture_output=True)

        if res.returncode != 0:
            if self.verbose >= 1:
                print("error: " + res.stderr.decode())
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_web_cert_valid(self, points) -> bool:
        """> Check that the web certificate is valid."""

        if self.verbose >= 1:
            print("\n" + str(self.test_web_cert_valid.__doc__))

        if not self.workdir.joinpath("certs/web.cert.pem").is_file():
            print("error: file does not exists")
            return False

        cmd = [
            self.openssl,
            "x509",
            "-in",
            str(self.workdir.joinpath("certs/web.cert.pem")),
            "-noout",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        res = subprocess.run(cmd, capture_output=True)

        if res.returncode != 0:
            if self.verbose >= 1:
                print("error: " + res.stderr.decode())
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_web_csr_valid(self, points) -> bool:
        """> Check that the web csr is valid."""

        if self.verbose >= 1:
            print("\n" + str(self.test_web_csr_valid.__doc__))

        if not self.workdir.joinpath("certs/web.csr.pem").is_file():
            print("error: file does not exists")
            return False

        cmd = [
            self.openssl,
            "req",
            "-in",
            str(self.workdir.joinpath("certs/web.csr.pem")),
            "-noout",
            "-verify",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        res = subprocess.run(cmd, capture_output=True)

        if res.returncode != 0:
            if self.verbose >= 1:
                print("error: " + res.stderr.decode())
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_web_csr_has_san(self, points) -> bool:
        """> Check that the web csr contains a subjectAltName field."""

        if self.verbose >= 1:
            print("\n" + str(self.test_web_csr_has_san.__doc__))

        if not self.workdir.joinpath("certs/web.csr.pem").is_file():
            print("error: file does not exists")
            return False

        cmd = [
            self.openssl,
            "req",
            "-in",
            str(self.workdir.joinpath("certs/web.csr.pem")),
            "-noout",
            "-text",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        res = subprocess.run(cmd, capture_output=True)

        if res.returncode != 0:
            if self.verbose >= 1:
                print("error: " + res.stderr.decode())
            return False

        if "Subject Alternative Name" not in res.stdout.decode():
            if self.verbose >= 1:
                print("error: subjectAltName is missing")
            return False

        if "DNS:assr.google.com" not in res.stdout.decode():
            if self.verbose >= 1:
                print("error: subjectAltName is missing or misconfigured")
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_web_csr_match_privkey(self, points) -> bool:
        """> Check that the web csr matches with its private key."""

        if self.verbose >= 1:
            print("\n" + str(self.test_web_csr_match_privkey.__doc__))

        if (
            not self.workdir.joinpath("certs/web.privkey.pem").is_file()
            or not self.workdir.joinpath("certs/web.csr.pem").is_file()
        ):
            print("error: file does not exists")
            return False

        cmd_privkey = [
            self.openssl,
            "pkey",
            "-in",
            str(self.workdir.joinpath("certs/web.privkey.pem")),
            "-pubout",
        ]
        cmd_csr = [
            self.openssl,
            "req",
            "-in",
            str(self.workdir.joinpath("certs/web.csr.pem")),
            "-noout",
            "-pubkey",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd_privkey))
        res_privkey = subprocess.run(cmd_privkey, capture_output=True)
        if self.verbose >= 2:
            print(" ".join(cmd_csr))
        res_csr = subprocess.run(cmd_csr, capture_output=True)

        if not res_privkey.stdout == res_csr.stdout:
            if self.verbose >= 1:
                print("error: does not match")
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_web_cert_match_privkey(self, points) -> bool:
        """> Check that the web certificate matches with its private key."""

        if self.verbose >= 1:
            print("\n" + str(self.test_web_cert_match_privkey.__doc__))

        if (
            not self.workdir.joinpath("certs/web.privkey.pem").is_file()
            or not self.workdir.joinpath("certs/web.cert.pem").is_file()
        ):
            print("error: file does not exists")
            return False

        cmd_privkey = [
            self.openssl,
            "pkey",
            "-in",
            str(self.workdir.joinpath("certs/web.privkey.pem")),
            "-pubout",
        ]
        cmd_cert = [
            self.openssl,
            "x509",
            "-in",
            str(self.workdir.joinpath("certs/web.cert.pem")),
            "-noout",
            "-pubkey",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd_privkey))
        res_privkey = subprocess.run(cmd_privkey, capture_output=True)
        if self.verbose >= 2:
            print(" ".join(cmd_cert))
        res_cert = subprocess.run(cmd_cert, capture_output=True)

        if not res_privkey.stdout == res_cert.stdout:
            if self.verbose >= 1:
                print("error: does not match")
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_web_cert_signed_by_ca(self, points) -> bool:
        """> Check that the web cert is signed by the CA."""

        if self.verbose >= 1:
            print("\n" + str(self.test_web_cert_signed_by_ca.__doc__))

        if (
            not self.workdir.joinpath("certs/ca.cert.pem").is_file()
            or not self.workdir.joinpath("certs/web.cert.pem").is_file()
        ):
            print("error: file does not exists")
            return False

        cmd = [
            self.openssl,
            "verify",
            "-CAfile",
            str(self.workdir.joinpath("certs/ca.cert.pem")),
            str(self.workdir.joinpath("certs/web.cert.pem")),
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        res = subprocess.run(cmd, capture_output=True)

        if res.returncode != 0:
            if self.verbose >= 1:
                print("error: " + res.stderr.decode())
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_web_cert_has_san(self, points) -> bool:
        """> Check that the web certificate contains a subjectAltName field."""

        if self.verbose >= 1:
            print("\n" + str(self.test_web_cert_has_san.__doc__))

        if not self.workdir.joinpath("certs/web.cert.pem").is_file():
            print("error: file does not exists")
            return False

        cmd = [
            self.openssl,
            "x509",
            "-in",
            str(self.workdir.joinpath("certs/web.cert.pem")),
            "-noout",
            "-text",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        res = subprocess.run(cmd, capture_output=True)

        if res.returncode != 0:
            if self.verbose >= 1:
                print("error: " + res.stderr.decode())
            return False

        if "Subject Alternative Name" not in res.stdout.decode():
            if self.verbose >= 1:
                print("error: subjectAltName is missing")
            return False

        if "DNS:assr.google.com" not in res.stdout.decode():
            if self.verbose >= 1:
                print("error: subjectAltName is missing or misconfigured")
            return False

        if self.verbose >= 1:
            print("success")
        self.points += points

        return True

    def test_nginx_config(self, points) -> bool:
        """> Check that the Nginx configuration is valid."""

        if self.verbose >= 1:
            print("\n" + str(self.test_nginx_config.__doc__))

        if not self.workdir.joinpath("config/nginx.conf").is_file():
            print("error: file does not exists")
            return False

        cmd = [
            "grep",
            "--quiet",
            "--extended-regexp",
            r"listen\s+443",
            str(self.workdir.joinpath("config/nginx.conf")),
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        res = subprocess.run(cmd, capture_output=True)

        if res.returncode != 0:
            if self.verbose >= 1:
                print("error: no tls configuration found in nginx")
            self.nginx_config_ok = False
            return False

        cmd = self.docker_cmd + [
            "exec",
            "nginx",
            "nginx",
            "-t",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        res = subprocess.run(cmd, capture_output=True)

        if res.returncode != 0:
            if self.verbose >= 1:
                print("error: " + res.stderr.decode())
            self.nginx_running = False
            return False

        if self.verbose >= 1:
            print("success")

        self.nginx_config_ok = True
        self.nginx_running = True
        self.points += points

        return True

    def test_testssl(self, points) -> bool:
        """> Check that the web server configuration is secure."""

        if self.verbose >= 1:
            print("\n" + str(self.test_testssl.__doc__))

        if not self.nginx_config_ok:
            if self.verbose >= 1:
                print("error: nginx is not configured")
            return False

        if not self.nginx_running:
            if self.verbose >= 1:
                print("error: nginx is not running")
            return False

        testssl_result = self.workdir / "certs" / "results.json"
        if testssl_result.exists():
            testssl_result.unlink()

        cmd = self.docker_cmd + [
            "exec",
            "client",
            "testssl.sh",
            "--add-ca",
            "/usr/local/share/ca-certificates/cacert.crt",
            "--quiet",
            "--warnings",
            "off",
            "--logfile",
            "/tmp/testssl/output.log",
            "--jsonfile",
            "/tmp/testssl/results.json",
            "--severity",
            "LOW",
            "assr.google.com",
        ]
        if self.verbose >= 2:
            print(" ".join(cmd))
        subprocess.run(cmd, capture_output=True)

        with open(testssl_result) as fp_results:
            results = json.load(fp_results)

        ignored_items = (
            "cert_revocation",
            "cert_expirationStatus",
            "cert_notAfter",
            "DNS_CAArecord",
            "grade",
            "security_headers",
        )
        for issue in results:
            if issue["id"] in ignored_items:
                continue
            if issue["severity"] == "CRITICAL":
                points -= 2
            elif issue["severity"] == "HIGH":
                points -= 1.5
            elif issue["severity"] == "MEDIUM":
                points -= 1
            elif issue["severity"] == "LOW":
                points -= 0.5
            if self.verbose >= 1:
                print(issue)

        # avoid negative score
        if points < 0:
            points = 0

        if points == 5 and self.verbose >= 1:
            print("success")

        self.points += points

        return True


def main():
    """Extract zip file and run test on extracted files."""

    # parse arguments.
    parser = argparse.ArgumentParser(description="Correction script.")
    parser.add_argument(
        "zip_file",
        help="path to the ZIP file containing your work",
        type=Path,
        nargs="+",
    )
    parser.add_argument(
        "-k",
        "--keep",
        help="keep extracted files for debugging purposes",
        action="store_true",
    )
    parser.add_argument(
        "-f",
        "--keep-containers",
        help="keep docker containers running for debugging purposes",
        action="store_true",
    )
    parser.add_argument(
        "--openssl-path",
        help="specify the path to openssl binary",
        default="openssl",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="add some verbosity",
        action="count",
        default=0,
    )
    args = parser.parse_args()

    for zip_file in args.zip_file:
        Correct(
            zip_file=zip_file,
            keep=args.keep,
            keep_containers=args.keep_containers,
            openssl_path=args.openssl_path,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    main()
