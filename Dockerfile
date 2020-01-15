#Pulling the base image
FROM cameroncruz/flask-nginx-uwsgi-miniconda:python3.6

# Create conda env (base image is built on python 3.6 and will have to migrate to 3.7 later)
RUN conda create --name myenv python=3.6

# Install the required dependencies
RUN /bin/bash -c ". activate myenv && \
    conda config --add channels conda-forge && \
    conda install -y \
        scikit-learn \
        numpy \
        scipy \
	rdkit \
	wtforms \
	ipython \
        flask \
        uwsgi"

# Copy custom supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy application files

# The application to be served
COPY server/main.py /app/main.py

# Folder containing the styling
COPY server/static/ /app/static

# Folder containing the html
COPY server/templates/ /app/templates

# The trained machine learning model
copy server/model.pkl /app/model.pkl
