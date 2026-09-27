#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
alias grep='grep --color=auto'
# PS1='[\u@\h \W]\$ '
export EDITOR=vim
eval "$(starship init bash)"
export PATH=~/.cargo/bin:$PATH

[[ $PS1 &&
  ! ${BASH_COMPLETION_VERSINFO:-} &&
  -f /usr/share/bash-completion/bash_completion ]] &&
    . /usr/share/bash-completion/bash_completion

pyactivate(){
	if [ -z $1 ]; then
		echo "Empty venv name."
		[ -e ~/.pyvenvs ] && echo "Possible environments:" && ls ~/.pyvenvs
		return -1
	fi
	\. ~/.pyvenvs/$1/bin/activate
}

export VCPKG_ROOT=$HOME/vcpkg

alias gitam="git commit --amend -a --no-edit"
