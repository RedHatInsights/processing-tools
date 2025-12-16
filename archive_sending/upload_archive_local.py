#!/usr/bin/env python3
import io
import tarfile
import requests
import json

CLUSTER_ID = "18000000-c53b-4ea9-ae22-ac4415e2cf21"
LOCAL_INGRESS_UPLOAD = "http://localhost:3000/api/ingress/v1/upload"
IDENTITY_HEADER = "eyJpZGVudGl0eSI6IHsidHlwZSI6ICJVc2VyIiwgImFjY291bnRfbnVtYmVyIjogIjAwMDAwMDEiLCAib3JnX2lkIjogIjAwMDAwMSIsICJpbnRlcm5hbCI6IHsib3JnX2lkIjogIjAwMDAwMSJ9fX0="

def create_ols_archive():
    """Create a test OLS archive with openshift_lightspeed.json marker"""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w:gz') as tar:
        # Add cluster ID
        cluster_id_info = tarfile.TarInfo(name='config/id')
        cluster_id_info.size = len(CLUSTER_ID)
        tar.addfile(cluster_id_info, io.BytesIO(CLUSTER_ID.encode()))

        # Add OLS marker file
        ols_data = json.dumps({"some": "ols_data"}).encode()
        ols_info = tarfile.TarInfo(name='openshift_lightspeed.json')
        ols_info.size = len(ols_data)
        tar.addfile(ols_info, io.BytesIO(ols_data))

    buffer.seek(0)
    return buffer

def create_ocp_archive():
    """Create a test OCP archive"""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w:gz') as tar:
        # Add cluster ID
        cluster_id_info = tarfile.TarInfo(name='config/id')
        cluster_id_info.size = len(CLUSTER_ID)
        tar.addfile(cluster_id_info, io.BytesIO(CLUSTER_ID.encode()))

        # Add some generic OCP data
        ocp_data = b"ocp data"
        ocp_info = tarfile.TarInfo(name='data/metrics.json')
        ocp_info.size = len(ocp_data)
        tar.addfile(ocp_info, io.BytesIO(ocp_data))

    buffer.seek(0)
    return buffer

def upload_archive(archive_buffer, content_type='application/vnd.redhat.openshift.periodic+tar'):
    """Upload archive to local ingress"""
    files = {'file': ('archive.tar.gz', archive_buffer, content_type)}
    headers = {'x-rh-identity': IDENTITY_HEADER}

    response = requests.post(LOCAL_INGRESS_UPLOAD, files=files, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code != 202:
        print(f"Response Content: {response.text}")
    return response

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "ols":
        print("Sending OLS archive...")
        upload_archive(create_ols_archive())
    elif len(sys.argv) > 1 and sys.argv[1] == "ocp":
        print("Sending OCP archive...")
        upload_archive(create_ocp_archive())
    else:
        print("Usage: python send_archive_local.py [ols|ocp]")
        print("Example: python send_archive_local.py ols")
