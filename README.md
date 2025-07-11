# Azure Files Python Example

Este proyecto demuestra cómo subir archivos directamente a Azure Files usando Python. Incluye scripts para listar archivos en contenedores y subir archivos individuales o en lotes.

## Requisitos

- Python 3.7+
- Cuenta de Azure Storage
- Azure Files share configurado

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/files-azure-example.git
cd files-azure-example
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales de Azure:
```
AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
AZURE_STORAGE_ACCOUNT_KEY=your_storage_account_key
AZURE_FILE_SHARE_NAME=your_file_share_name
```

## Scripts incluidos

### 1. Listar archivos (`list_files.py`)
Lista todos los archivos en el Azure Files share:
```bash
python list_files.py
```

### 2. Subir archivo individual (`upload_file.py`)
Sube un archivo específico a Azure Files:
```bash
python upload_file.py path/to/local/file.csv
```

### 3. Subir lote de archivos (`batch_upload.py`)
Sube todos los archivos CSV de una carpeta a Azure Files:
```bash
python batch_upload.py data/
```

## Archivos de ejemplo

El proyecto incluye archivos CSV de ejemplo en la carpeta `data/`:
- `employees.csv` - Datos de empleados
- `sales.csv` - Datos de ventas
- `inventory.csv` - Datos de inventario

## Estructura del proyecto

```
files-azure-example/
├── README.md
├── requirements.txt
├── .env.example
├── list_files.py
├── upload_file.py
├── batch_upload.py
└── data/
    ├── employees.csv
    ├── sales.csv
    └── inventory.csv
```

## Uso

1. **Listar archivos existentes:**
   ```bash
   python list_files.py
   ```

2. **Subir un archivo individual:**
   ```bash
   python upload_file.py data/employees.csv
   ```

3. **Subir todos los archivos CSV de una carpeta:**
   ```bash
   python batch_upload.py data/
   ```

## Configuración de Azure

Para usar este proyecto necesitas:

1. Una cuenta de Azure Storage
2. Un File Share creado en tu cuenta de storage
3. Las credenciales de acceso (connection string o account name + key)

### Obtener el connection string

1. Ve a tu Storage Account en Azure Portal
2. En el menú izquierdo, selecciona "Access keys"
3. Copia el "Connection string" de key1 o key2

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.