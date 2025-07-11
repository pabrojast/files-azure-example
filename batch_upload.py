#!/usr/bin/env python3
"""
Script para subir todos los archivos CSV de una carpeta a Azure Files en lote
"""

import os
import sys
import glob
from azure.storage.fileshare import ShareServiceClient
from dotenv import load_dotenv

def batch_upload_folder(folder_path, file_pattern="*.csv", remote_folder=None):
    load_dotenv()
    
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    share_name = os.getenv('AZURE_FILE_SHARE_NAME')
    
    if not connection_string or not share_name:
        print("Error: Configura AZURE_STORAGE_CONNECTION_STRING y AZURE_FILE_SHARE_NAME en el archivo .env")
        return False
    
    if not os.path.exists(folder_path):
        print(f"Error: La carpeta '{folder_path}' no existe")
        return False
    
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' no es una carpeta")
        return False
    
    # Buscar archivos que coincidan con el patrón
    search_pattern = os.path.join(folder_path, file_pattern)
    files_to_upload = glob.glob(search_pattern)
    
    if not files_to_upload:
        print(f"No se encontraron archivos con el patrón '{file_pattern}' en '{folder_path}'")
        return False
    
    try:
        service_client = ShareServiceClient.from_connection_string(connection_string)
        share_client = service_client.get_share_client(share_name)
        
        # Verificar si el share existe
        if not share_client.exists():
            print(f"Error: El share '{share_name}' no existe")
            return False
        
        # Crear directorio remoto si se especifica
        if remote_folder:
            try:
                directory_client = share_client.get_directory_client(remote_folder)
                directory_client.create_directory()
                print(f"📁 Directorio creado: {remote_folder}")
            except Exception as e:
                if "DirectoryAlreadyExists" not in str(e):
                    print(f"Error al crear directorio '{remote_folder}': {e}")
                    return False
        
        print(f"Subiendo {len(files_to_upload)} archivos...")
        print("-" * 50)
        
        uploaded_count = 0
        failed_count = 0
        
        for local_file_path in files_to_upload:
            try:
                file_name = os.path.basename(local_file_path)
                
                # Determinar la ruta remota
                if remote_folder:
                    remote_file_path = f"{remote_folder}/{file_name}"
                else:
                    remote_file_path = file_name
                
                file_client = share_client.get_file_client(remote_file_path)
                
                print(f"📤 Subiendo: {file_name}...", end=" ")
                
                with open(local_file_path, 'rb') as file_data:
                    file_client.upload_file(file_data, overwrite=True)
                
                file_size = os.path.getsize(local_file_path)
                print(f"✅ ({file_size} bytes)")
                uploaded_count += 1
                
            except Exception as e:
                print(f"❌ Error: {e}")
                failed_count += 1
        
        print("-" * 50)
        print(f"Resumen: {uploaded_count} archivos subidos, {failed_count} fallidos")
        return failed_count == 0
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python batch_upload.py <carpeta> [patrón] [carpeta_remota]")
        print("Ejemplos:")
        print("  python batch_upload.py data/")
        print("  python batch_upload.py data/ *.csv")
        print("  python batch_upload.py data/ *.csv backup_2023")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    file_pattern = sys.argv[2] if len(sys.argv) > 2 else "*.csv"
    remote_folder = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"Carpeta local: {folder_path}")
    print(f"Patrón de archivos: {file_pattern}")
    if remote_folder:
        print(f"Carpeta remota: {remote_folder}")
    print()
    
    success = batch_upload_folder(folder_path, file_pattern, remote_folder)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()