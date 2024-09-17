FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -sfv /usr/share/zoneinfo/Europe/Istanbul /etc/localtime
RUN apt update -y && apt upgrade -y

EXPOSE 3389

RUN apt install -y ubuntu-desktop dbus dbus-user-session dbus-x11
RUN rm /run/reboot-required*

RUN apt install -y xrdp
RUN adduser xrdp ssl-cert

RUN echo "#!/bin/sh\\n\
if test -r /etc/profile; then\\n\
        . /etc/profile\\n\
fi\\n\
if test -r ~/.profile; then\\n\
        . ~/.profile\\n\
fi\\n\
export GNOME_SHELL_SESSION_MODE=ubuntu\\n\
export XDG_SESSION_TYPE=x11\\n\
export XDG_CURRENT_DESKTOP=ubuntu:GNOME\\n\
export XDG_CONFIG_DIRS=/etc/xdg/xdg-ubuntu:/etc/xdg\\n\
test -x /etc/X11/Xsession && exec /etc/X11/Xsession\\n\
exec /bin/sh /etc/X11/Xsession" > /etc/xrdp/startwm.sh

RUN apt install -y -qq libglu1-mesa-dev libx11-xcb-dev '^libxcb*' python3.12-venv sudo

RUN useradd -m testuser -p $(openssl passwd 1234)
RUN usermod -aG sudo testuser
USER testuser
WORKDIR /home/testuser/PlagiarismDetectionProject

ENV PYTHONUNBUFFERED=1

RUN python3 -m venv /home/testuser/PlagiarismDetectionProject/venv-docker
ENV PATH="/home/testuser/PlagiarismDetectionProject/venv-docker/bin:$PATH"
ENV VIRTUAL_ENV=/home/testuser/PlagiarismDetectionProject/venv-docker
COPY --chown=testuser:testuser requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY --chown=testuser:testuser . .

RUN echo "cd UI\\n\
../venv-docker/bin/python ./main.py\\n\
" > /home/testuser/PlagiarismDetectionProject/project-start.sh

USER root
CMD service dbus start; /usr/lib/systemd/systemd-logind & service xrdp start; bash;