from setuptools import setup, find_packages

setup(
    name="somakin_qr",
    version="0.0.3",
    description="QR utilities for ERPNext (payload -> QR image attachment)",
    author="Somakin",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "qrcode[pil]",
    ],
)
