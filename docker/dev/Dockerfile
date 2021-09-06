FROM internetofus/profile-diversity-manager:latest

ENV LOG_LEVEL=debug
ENV MAX_EXECUTOR_WORKERS=4
ENV HOST=0.0.0.0
ENV PORT=9000
ENV MAX_COMB_NO_BACKGROUND=1000
ENV PYTEST_HTTPSERVER_HOST=0.0.0.0


COPY . /app/.
WORKDIR /app
RUN pip install -r docker/dev/requirements.txt

RUN echo "PS1='\[\033[01;32m\]profile-diversity-manager@dev\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\] \$ '" >> /root/.bashrc
RUN echo "export PATH=/:\$PATH" >> /root/.bashrc
RUN echo "export PYTHONPATH=\"\$PYTHONPATH:/app/app\"" >> /root/.bashrc


CMD ["bash"]