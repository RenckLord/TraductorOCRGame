"""
Configuración de instalación del paquete
"""
from setuptools import setup, find_packages

setup(
    name="traductorocr",
    version="1.0.0",
    description="Traductor OCR en tiempo real para juegos",
    author="RenckLord",
    author_email="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "altgraph>=0.17.4",
        "deep-translator>=1.11.4",
        "mss>=10.1.0",
        "numpy>=2.2.6",
        "opencv-python>=4.12.0.88",
        "pillow>=12.0.0",
        "pytesseract>=0.3.13"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "traductorocr=traductorocr.__main__:main"
        ]
    }
)