#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

if [ -d /etc/X11/xinit/xinitrc.d ]; then
  for f in /etc/X11/xinit/xinitrc.d/*; do
    [ -x "$f" ] && . "$f"
  done
  unset f
fi

# load ~/.Xresources file
xrdb -merge ~/.Xresources
# set xcursor
xsetroot -cursor_name left_ptr

# set desktop background
# xloadimage -onroot -fullscreen -background black ~/pictures/wallpapers/earth.jpg

# Run clipboard manager
parcellite -n -d &

# Set font path
xset +fp /usr/share/fonts/local
xset fp rehash

# exec gnome-session
# exec startkde
# exec twm
# exec startxfce4
xmonad
# ...or the Window Manager of your choice
