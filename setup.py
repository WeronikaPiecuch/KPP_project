import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
 long_description = fh.read()
setuptools.setup(
 name="public_transport_project_wp439938",
 version="0.0.1",
 author="Weronika Piecuch",
 author_email="wp439938@students.mimuw.edu.pl",
 description="Project for the course 'Programming in Python' at the University of Warsaw.",
 long_description=long_description,
 long_description_content_type="text/markdown",
 url="",
 packages=setuptools.find_packages(),
 classifiers=[
 "Programming Language :: Python :: 3",
 "License :: OSI Approved :: MIT License",
 "Operating System :: OS Independent",
 ],
 python_requires='>=3.6',
)