from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient

# Helper to get Azure credentials and clients (fill in your subscription ID)
def get_azure_clients():
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID", "<your-subscription-id>")
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, subscription_id)
    resource_client = ResourceManagementClient(credential, subscription_id)
    return compute_client, resource_client
def handle_create_vm(prompt: str):
    # User-friendly, approval-based output for VM creation
    yield "[APPROVAL REQUIRED] You requested to create a new Virtual Machine.\n"
    yield "This action requires admin approval. Please confirm to proceed.\n"
    # Example stub for real Azure VM creation
    # compute_client, resource_client = get_azure_clients()
    # TODO: Parse VM parameters from prompt and call compute_client.virtual_machines.begin_create_or_update(...)
    yield "(Stub: Here you would call Azure SDK to create a VM.)\n"

def handle_get_vm_details(prompt: str):
    # User-friendly, super view output for VM details
    yield "[SUPER VIEW] Here are the details for your requested Virtual Machine.\n"
    # Example stub for real Azure VM details
    # compute_client, _ = get_azure_clients()
    # TODO: Parse VM name/resource group from prompt and call compute_client.virtual_machines.get(...)
    yield "(Stub: Here you would call Azure SDK to get VM details.)\n"

def handle_list_vms(prompt: str):
    # User-friendly, super view output for listing VMs
    yield "[SUPER VIEW] Here is a list of all created Virtual Machines.\n"
    # Example stub for real Azure VM listing
    # compute_client, _ = get_azure_clients()
    # vms = compute_client.virtual_machines.list_all()
    # for vm in vms:
    #     yield f"VM: {vm.name}\n"
    yield "(Stub: Here you would call Azure SDK to list VMs.)\n"

def handle_list_deleted_vms(prompt: str):
    # User-friendly, super view output for deleted VMs
    yield "[SUPER VIEW] Here is a list of all deleted Virtual Machines.\n"
    # Example stub for deleted VMs (Azure does not keep deleted VMs by default)
    # You may need to track deletions or use Activity Logs
    yield "(Stub: Here you would implement logic to list deleted VMs, e.g., from logs.)\n"

def handle_export_vms(prompt: str):
    # User-friendly, approval-based output for export
    yield "[APPROVAL REQUIRED] You requested to export VM data.\n"
    yield "Please select your preferred format: doc, pdf, or excel.\n"
    yield "This action requires admin approval. Please confirm to proceed.\n"
    yield "(Stub: Export logic for doc/pdf/excel would be implemented here.)\n"
if __name__ == "__main__":
    # Example usage: Fetch and print sample data from Azure Blob Storage
    try:
        sample_data = get_agenticai_sample_data()
        print("Sample data from Azure Blob Storage:")
        print(sample_data)
    except Exception as e:
        print(f"Failed to fetch sample data: {e}")
from azure.storage.blob import BlobServiceClient

def get_agenticai_sample_data() -> str:
    """
    Fetches sample data from Azure Blob Storage for agentic AI demo.
    Returns the blob content as a string.
    """
    const_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not const_string:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set.")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(const_string)
        container_client = blob_service_client.get_container_client('agenticai-demo-data')
        blob_client = container_client.get_blob_client('agentic ai demo prep work.txt')
        data = blob_client.download_blob().readall()
        return data.decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Error accessing Azure Blob Storage: {e}")
import os
import time
from typing import Generator

def azure_fetch_realtime_data(prompt: str) -> Generator[str, None, None]:
    """
    If the prompt requests storage account sample data, fetch it from Azure Blob Storage.
    Otherwise, stream tokens from Azure OpenAI if credentials are set, or return a mock stream.
    """
    # Check if the prompt is asking for storage account sample data

    # Keywords for storage account
    storage_keywords = [
        "storage account sample data", "fetch storage data", "get storage data", "blob storage sample",
        "agentic ai demo data", "agentic ai demo prep work", "fetch the storage account details",
        "fetch storage account details", "get storage account details", "fetch storage account info",
        "get storage account info", "fetch azure storage", "get azure storage", "fetch storage from azure",
        "get storage from azure", "fetch storage details from azure", "get storage details from azure"
    ]
    # Keywords for VM management
    vm_create_keywords = ["create a vm", "provision vm", "new virtual machine", "deploy vm"]
    vm_get_keywords = ["get existing vm details", "get vm details", "show vm details", "vm info"]
    vm_list_keywords = ["list of vms", "list vms", "show all vms", "get all vms"]
    vm_deleted_keywords = ["deleted vms", "list deleted vms", "show deleted vms"]
    output_doc_keywords = ["doc", "word", "document"]
    output_pdf_keywords = ["pdf"]
    output_excel_keywords = ["excel", "xlsx", "spreadsheet"]

    prompt_lower = prompt.lower()
    # Storage account logic (unchanged)
    if any(keyword in prompt_lower for keyword in storage_keywords):
        try:
            data = get_agenticai_sample_data()
            for line in data.splitlines(keepends=True):
                yield line
        except Exception as e:
            yield f"[Error fetching storage data: {e}]\n"
        return

    # VM management logic
    if any(keyword in prompt_lower for keyword in vm_create_keywords):
        yield from handle_create_vm(prompt)
        return
    if any(keyword in prompt_lower for keyword in vm_get_keywords):
        yield from handle_get_vm_details(prompt)
        return
    if any(keyword in prompt_lower for keyword in vm_list_keywords):
        yield from handle_list_vms(prompt)
        return
    if any(keyword in prompt_lower for keyword in vm_deleted_keywords):
        yield from handle_list_deleted_vms(prompt)
        return
    if any(keyword in prompt_lower for keyword in output_doc_keywords + output_pdf_keywords + output_excel_keywords):
        yield from handle_export_vms(prompt)
        return

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    key = os.getenv("AZURE_OPENAI_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")
    promtData = ("Gathering the storage account details from Azure Blob Storage.\n""Login success to Azure Blob Storage.\n""Fetching the storage account details.\n""Storage account details fetched successfully.\n""Here are the storage account details:\n"f"{prompt}\n")
    if endpoint and key:
        try:
            try:
                from azure.ai.openai import OpenAIClient
                from azure.core.credentials import AzureKeyCredential
            except ImportError:
                yield ("correctte the prompt.\n")
                return
            client = OpenAIClient(endpoint, AzureKeyCredential(key))

            # Use streaming completion
            response = client.chat.completions.create(
                model=deployment,
                messages=[{"role": "user", "content": promtData}, {"role": "system", "content": 'Testing the Azure OpenAI streaming response.'}],
                stream=True
            )
            for chunk in response:
                # Each chunk may have choices with delta content
                for choice in getattr(chunk, "choices", []):
                    delta = getattr(choice, "delta", None)
                    if delta and getattr(delta, "content", None):
                        yield delta.content
        except Exception as e:
            yield f"[Azure OpenAI error: {e}] "
    else:
        # Fallback: mock streaming
        for word in (prompt + ' (mocked response)').split():
            yield word + ' '
            time.sleep(0.2)