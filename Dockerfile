#To install this image, execute command
# docker build -t python-tutorial-linux-img .
#run and access it in with
# docker run -it --memory=300m --cpus=0.5 python-tutorial-linux-img
# docker run -p 8080:8080 python-tutorial-linux-img
FROM alpine:3.14

# Install required packages (git and python)
RUN apk add git

RUN apk add --no-cache bash python3 py3-pip && \
    ln -s -f /usr/bin/python3 /usr/bin/python && \
    ln -s -f /usr/bin/pip3 /usr/bin/pip

# Create directory
RUN mkdir -p /usr/share/python-code
WORKDIR /usr/share/python-code

# Create user
RUN addgroup -g 10000 testers && \
    adduser -u 10000 -G testers -s /bin/sh -D userX
RUN chown -R userX:testers /usr/share/python-code
RUN chmod 777 /usr/share/python-code

# Get the app code
RUN git clone https://github.com/kdrzazga/python-tutorial.git
RUN chmod -R 777 /usr/share/python-code
WORKDIR /usr/share/python-code/python-tutorial
RUN git config --global --add safe.directory /usr/share/python-code/python-tutorial
RUN git status
RUN git checkout test-classification

# Install additional stuff
RUN pip install --no-cache-dir pytest

# Check installed programs
RUN git --version
RUN python --version
RUN pip --version
RUN pytest --version

USER userX

##Running tests
RUN pip install -r requirements.txt
#RUN pytest -m unit --junitxml=unittest-result.xml
