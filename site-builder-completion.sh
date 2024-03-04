#!/bin/bash

_site-builder() {
  local cur prev words cword
  _get_comp_words_by_ref -n : cur prev words cword

  # Generate completion options based on the current word
  case $cword in
    1)
      COMPREPLY=( $(compgen -W "build publish help" -- $cur) )
      ;;
    2)
      # Generate completion options based on the previous word
      case $prev in
        build)
          COMPREPLY=( $(compgen -W "clean normal" -- $cur) )
          ;;
        *)
          ;;
      esac
      ;;
  esac
}
complete -F _site-builder site-builder