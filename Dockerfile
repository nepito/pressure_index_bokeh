FROM islasgeci/base:latest
RUN pip install \
    black \
    bokeh \
    codecov \
    fastapi \
    flake8 \
    mutmut \
    pandas \
    pylint \
    pytest \
    pytest-cov \
    requests \
    uvicorn
RUN Rscript -e "install.packages(c('janitor'), repos='http://cran.rstudio.com')"
WORKDIR /workdir
COPY . .