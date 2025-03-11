from setuptools import setup, find_packages

setup(
    name="open-webui-extensions",
    version="0.1.0",
    description="Extension Manager and Framework for Open WebUI",
    author="Open WebUI Team",
    author_email="info@openwebui.example",
    url="https://github.com/open-webui/extensions",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.68.0",
        "pydantic>=1.8.2",
        "starlette>=0.14.2",
        "python-multipart>=0.0.5",
        "aiohttp>=3.7.4",
        "requests>=2.25.1",
    ],
    entry_points={
        'console_scripts': [
            'openwebui-extensions=open_webui_extensions.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    python_requires=">=3.7",
)
