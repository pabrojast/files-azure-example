#!/usr/bin/env python3
"""
Script para subir un archivo individual a Azure Files
"""

import os
import sys
from azure.storage.fileshare import ShareServiceClient
from dotenv import load_dotenv

def upload_file(local_file_path, remote_file_name=None):
    load_dotenv()
    
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    share_name = os.getenv('AZURE_FILE_SHARE_NAME')
    
    if not connection_string or not share_name:
        print("Error: Configura AZURE_STORAGE_CONNECTION_STRING y AZURE_FILE_SHARE_NAME en el archivo .env")
        return False
    
    if not os.path.exists(local_file_path):
        print(f"Error: El archivo '{local_file_path}' no existe")
        return False
    
    if remote_file_name is None:
        remote_file_name = os.path.basename(local_file_path)
    
    try:
        service_client = ShareServiceClient.from_connection_string(connection_string)
        share_client = service_client.get_share_client(share_name)
        
        # Verificar si el share existe
        if not share_client.exists():
            print(f"Error: El share '{share_name}' no existe")
            return False
        
        file_client = share_client.get_file_client(remote_file_name)
        
        print(f"Subiendo archivo '{local_file_path}' como '{remote_file_name}'...")
        
        with open(local_file_path, 'rb') as file_data:
            file_client.upload_file(file_data, overwrite=True)
        
        file_size = os.path.getsize(local_file_path)
        print(f"✅ Archivo subido exitosamente: {remote_file_name} ({file_size} bytes)")
        return True
        
    except Exception as e:
        print(f"❌ Error al subir archivo: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python upload_file.py <ruta_archivo_local> [nombre_archivo_remoto]")
        print("Ejemplo: python upload_file.py data/employees.csv")
        print("Ejemplo: python upload_file.py data/sales.csv ventas_2023.csv")
        sys.exit(1)
    
    local_file_path = sys.argv[1]
    remote_file_name = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = upload_file(local_file_path, remote_file_name)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()