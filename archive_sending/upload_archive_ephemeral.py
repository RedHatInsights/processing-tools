"""
Start a venv:

python3 -m venv venv        
source venv/bin/activate 

Install requirements:

pip install -r requirements.txt

You need to install molodec:

export PIP_INDEX_URL=https://repository.engineering.redhat.com/nexus/repository/insights-qe/simple
pip install -U molodec

upload with: python upload_archive_ephemeral.py upload <ephemeral-namespace> <options>
"""

import json
import tarfile
from io import BytesIO

import click
import requests
from bonfire.namespaces import describe_namespace
from molodec.archive_producer import ArchiveProducer
from molodec.crc import CONTENT_TYPE
from molodec.renderer import Renderer
from molodec.rules import RuleSet
from requests.auth import HTTPBasicAuth

CLUSTER_ID = "181862b9-c53b-4ea9-ae22-ac4415e2cf21"



def upload_ocp_recommendations(namespace):
    producer = ArchiveProducer(Renderer(*RuleSet("io").get_default_rules()))
    tario = producer.make_tar_io(CLUSTER_ID)

    ns_data = json.loads(describe_namespace(namespace, "json"))
    ingress_endpoint = f"{ns_data['gateway_route']}/api/ingress/v1/upload"
    requests.post(
        ingress_endpoint,
        files={"file": ("archive", tario.getvalue(), CONTENT_TYPE)},
        auth=HTTPBasicAuth(ns_data["default_username"], ns_data["default_password"])
    )


def upload_ols(namespace):
    ns_data = json.loads(describe_namespace(namespace, "json"))
    ingress_endpoint = f"{ns_data['gateway_route']}/api/ingress/v1/upload"

    tario = BytesIO()
    tar = tarfile.open(fileobj=tario, mode="w:gz")

    try:
        tar_info = tarfile.TarInfo("openshift_lightspeed.json")
        tar_info.size = 0
        tar.addfile(tar_info)

        tar_info = tarfile.TarInfo("config/id")
        content = bytes(CLUSTER_ID, "utf-8")
        tar_info.size = len(content)
        tar.addfile(tar_info, fileobj=BytesIO(content))

    except:  # noqa E722
        raise
    finally:
        tar.close()

    requests.post(
        ingress_endpoint,
        files={"file": ("archive", tario.getvalue(), CONTENT_TYPE)},
        auth=HTTPBasicAuth(ns_data["default_username"], ns_data["default_password"])
    )




@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    pass


@cli.command("upload")
@click.argument("namespace", envvar="NAMESPACE")
@click.option("--ols", default=False, is_flag=True)
def _upload(namespace, ols):
    if ols:
        upload_ols(namespace=namespace)
    else:
        upload_ocp_recommendations(namespace=namespace)


if __name__ == "__main__":
    cli()