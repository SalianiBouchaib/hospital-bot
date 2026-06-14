from setuptools import setup
from glob import glob
import os

package_name = "hospital_robot_description"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [os.path.join("resource", package_name)]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/launch", glob("launch/*.py")),
        (f"share/{package_name}/urdf", glob("urdf/*")),
        (f"share/{package_name}/meshes", glob("meshes/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Hospital Robotics",
    maintainer_email="robotics@example.com",
    description="Hospital robot description package.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={"console_scripts": []},
)
