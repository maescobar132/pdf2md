# pdf2md

Convierte documentos a Markdown desde la línea de comandos.

- **PDF** → PyMuPDF. Respeta bien los espacios en maquetas académicas densas (el motor pdfminer de markitdown los estropea). El texto se normaliza (NFKC): las ligaduras `fi`/`fl` pasan a letras normales y se conservan los acentos.
- **DOCX, PPTX, XLSX, HTML/HTM, EPUB, CSV** → [markitdown](https://github.com/microsoft/markitdown).

El resultado se guarda como `.md` junto al archivo original.

## Requisitos

Solo [uv](https://docs.astral.sh/uv/). `uv` lee las dependencias del encabezado de `convert.py` (PyMuPDF y markitdown, con versión fija), las instala en un entorno aislado la primera vez y descarga Python 3.11 o superior si no lo tienes. No hay que crear un entorno virtual ni correr `pip install`.

## Instalación en Windows 11 (PowerShell)

1. Instala uv y **cierra y vuelve a abrir** PowerShell:

   ```powershell
   winget install --id=astral-sh.uv -e
   ```

2. Descarga el repositorio (o baja el ZIP de GitHub y descomprímelo en esa carpeta):

   ```powershell
   git clone https://github.com/maescobar132/pdf2md $HOME\tools\pdf2md
   ```

3. Prueba con un archivo:

   ```powershell
   uv run --script $HOME\tools\pdf2md\convert.py "C:\ruta\archivo.pdf"
   ```

   La primera ejecución tarda un poco porque descarga las dependencias.

4. (Opcional) Crea el comando `pdf2md`:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   New-Item -Path $PROFILE -Type File -Force
   notepad $PROFILE
   ```

   Pega esta línea en el archivo que se abre, guarda y reabre PowerShell:

   ```powershell
   function pdf2md { uv run --script $HOME\tools\pdf2md\convert.py @args }
   ```

   Sin perfil también puedes usar el envoltorio del repo: `.\pdf2md.ps1 archivo.pdf`. Ambas opciones requieren que PowerShell permita ejecutar scripts locales (el comando `Set-ExecutionPolicy` de arriba). Si descargaste el ZIP en lugar de clonar, ejecuta antes `Unblock-File .\pdf2md.ps1`.

## Instalación en Ubuntu

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/maescobar132/pdf2md ~/tools/pdf2md
mkdir -p ~/bin && ln -s ~/tools/pdf2md/pdf2md.sh ~/bin/pdf2md
```

## Uso

```text
pdf2md archivo.pdf                    -> archivo.md junto al original
pdf2md --no-images diapositivas.pptx  -> sin imágenes (solo formatos no PDF)
pdf2md carpeta\                       -> convierte todo lo soportado, recorriendo subcarpetas
pdf2md uno.pdf dos.docx tres.xlsx     -> varios archivos
```

Al terminar, cada archivo imprime su tamaño de entrada y de salida. El código de salida es 1 si algún archivo falló.

### Lotes en Windows

PowerShell y cmd no expanden comodines como `*.pdf` antes de llamar al programa, así que el script recibe el texto literal y responde `no existe`. En Windows usa una carpeta o una lista:

```powershell
pdf2md .\documentos
pdf2md (Get-ChildItem *.pdf).FullName
```

En Ubuntu `pdf2md *.pdf` funciona porque bash lo expande.

## Limitaciones

- **PDF escaneados:** no hay OCR. Si el PDF es una imagen, el `.md` sale vacío y el script avisa con `ADVERTENCIA: salida vacia`.
- **Archivos con el mismo nombre:** `informe.pdf` e `informe.docx` en la misma carpeta producen ambos `informe.md`, y el segundo sobrescribe al primero. Un `.md` existente con ese nombre también se sobrescribe sin preguntar.
- `--no-images` no afecta a los PDF, porque PyMuPDF solo extrae texto.
- Los PDF se convierten a texto plano con saltos de página, sin encabezados ni tablas de Markdown.

## Contenido del repositorio

| Archivo | Para qué sirve |
|---|---|
| `convert.py` | El conversor. Declara sus dependencias en el encabezado (formato PEP 723). |
| `pdf2md.ps1` | Envoltorio para Windows (PowerShell). |
| `pdf2md.sh` | Envoltorio para Ubuntu (bash). |
