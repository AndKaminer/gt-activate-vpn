#!/bin/bash

import setuptools

install_requires = ['pexpect']

setuptools.setup(
        name="activate_vpn",
        version="1.1",
        packages=setuptools.find_packages(),
        install_requires=install_requires,
        entry_points={
            "console_scripts": [
                "activate_vpn = activate_vpn.activate_vpn:main"],
        },
        include_package_data=True)
