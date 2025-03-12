from setuptools import setup, find_packages

setup(
    name="open-webui-extensions",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.95.0",
        "pydantic>=2.0.0",
        "jinja2>=3.0.0",
        "aiofiles>=0.8.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "openwebui-ext=open_webui_extensions.cli:main",
        ],
    },
    python_requires=">=3.8",
)
