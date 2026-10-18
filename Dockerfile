FROM basemax/salam:latest
WORKDIR /workspace
COPY . /workspace
ENTRYPOINT ["salam", "exec", "salam.salam"]
