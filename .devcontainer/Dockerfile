FROM mcr.microsoft.com/devcontainers/base:focal

RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - 

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends git zsh vim wget firefox locales postgresql-15 \
    #&& cp /usr/share/i18n/SUPPORTED /etc/locale.gen \
    #&& dpkg-reconfigure --frontend=noninteractive locales \
    #&& locale-gen \
    #&& wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    #&& apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && apt-get clean autoclean \
    && apt-get autoremove --yes

RUN chsh -s /usr/bin/zsh vscode
RUN echo "DONE"