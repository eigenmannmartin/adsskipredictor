FROM mcr.microsoft.com/devcontainers/base:focal

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends git zsh vim wget firefox \
    #&& wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    #&& apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && apt-get clean autoclean \
    && apt-get autoremove --yes

RUN chsh -s /usr/bin/zsh vscode
RUN echo "DONE"