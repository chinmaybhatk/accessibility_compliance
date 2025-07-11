from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="accessibility_compliance",
    version="1.0.0",
    description="AI-Powered Accessibility Compliance Scanner",
    author="Your Company",
    author_email="developer@yourcompany.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)