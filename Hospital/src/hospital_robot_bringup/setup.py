from setuptools import setup
from glob import glob
import os

package_name = "hospital_robot_bringup"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [os.path.join("resource", package_name)]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.py")),
        (f"share/{package_name}/worlds", glob("worlds/*")),
        (f"share/{package_name}/rviz", glob("rviz/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Hospital Robotics",
    maintainer_email="robotics@example.com",
    description="Bringup package for hospital robot.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "startup_cmd_vel_test = hospital_robot_bringup.startup_cmd_vel_test:main",
        ]
    },
)
