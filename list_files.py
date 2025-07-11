#!/usr/bin/env python3
"""
Script para listar archivos en Azure Files share
"""

import os
from azure.storage.fileshare import ShareServiceClient
from dotenv import load_dotenv

def list_files():
    load_dotenv()
    
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    share_name = os.getenv('AZURE_FILE_SHARE_NAME')
    
    if not connection_string or not share_name:
        print("Error: Configura AZURE_STORAGE_CONNECTION_STRING y AZURE_FILE_SHARE_NAME en el archivo .env")
        return
    
    try:
        service_client = ShareServiceClient.from_connection_string(connection_string)
        share_client = service_client.get_share_client(share_name)
        
        print(f"Archivos en el share '{share_name}':")
        print("-" * 50)
        
        files_found = False
        for item in share_client.list_directories_and_files():
            files_found = True
            if item.is_directory:
                print(f"📁 {item.name}/")
                # Listar archivos en el directorio
                directory_client = share_client.get_directory_client(item.name)
                for file_item in directory_client.list_directories_and_files():
                    if not file_item.is_directory:
                        print(f"   📄 {file_item.name} ({file_item.size} bytes)")
            else:
                print(f"📄 {item.name} ({item.size} bytes)")
        
        if not files_found:
            print("No se encontraron archivos en el share.")
            
    except Exception as e:
        print(f"Error al listar archivos: {e}")

if __name__ == "__main__":
    list_files()