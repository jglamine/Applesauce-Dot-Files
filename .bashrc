#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

##Add ~/bin to path variable
PATH=$PATH:~/bin

alias ls='ls --color=auto -h'
# PS1='[\u@\h \W]\$ '
PS1='\[\e[1;32m\][\u@\h \W]\$\[\e[0m\] '

## Custom aliases for color and ease of use
alias diff='colordiff'
alias df='df -h'
alias du='du -h -c'
alias nano='nano -w'
export GREP_COLOR="1;33"
alias grep='grep --color=auto'
alias cp='cp -v'
alias wicd-client='wicd-client -n'

## Aliases for shtdown and suspend
alias shutdown='sudo poweroff'
alias poweroff='sudo poweroff'
alias reboot='sudo reboot'
alias suspend='sudo pm-suspend'
alias pm-suspend='sudo pm-suspend'

## Aliases for programs
alias image='sxiv'
alias images='sxiv -t'
alias music='cmus'
