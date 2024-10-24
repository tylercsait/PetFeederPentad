#!/bin/bash
azcopy copy "path/to/image.jpg" "https://<your_storage_account_name>.blob.core.windows.net/<container_name>/<blob_name>.jpg" --sas-token "<your_sas_token>"
