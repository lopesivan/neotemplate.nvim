" $Id$
" Name Of File: neotemplate.vim
"
"  Description: Vim plugin
"
"       Author: Ivan Carlos S. Lopes <lopesivan (at) poli (dot) com (dot) br>
"   Maintainer: Ivan Carlos S. Lopes <lopesivan (at) poli (dot) com (dot) br>
"
"  Last Change: Qua 24 Out 2018 01:05:59 -03
"      Version: |Revision|
"
"    Copyright: This script is released under the Vim License.
"

if &cp || exists("g:loaded_neotemplate")
	finish
endif

let g:loaded_neotemplate = "v01"
let s:keepcpo     = &cpo
set cpo&vim

"-----------------------------------------------------------------------------
function! s:split_filetypes(filetype) abort
    if a:filetype == ''
        return ''
    endif
    return split(a:filetype, '\.')[0]
endfunction

function! s:get_enabled_templates(filetype) abort
    return systemlist("find ".expand("$NDE_APP_CONFIG")."/cheetah/tmpl/".a:filetype."/ -name \*.cheetah -printf '%P\n'| sed 's/\.cheetah$//'")
endfunction

function! CompleteTemplates(ArgLead, CmdLine, CursorPos) abort
    let filetype = s:split_filetypes(&filetype)
    return filter(s:get_enabled_templates(filetype),
                \ "v:val =~? '^" . a:ArgLead ."'")
endfunction
" ////////////////////////////////////////////////////////////////////////////

"command -nargs=? -bar -range=% -complete=customlist,CompleteTemplates Template :call Neotemplate(<q-args>, <line1>, <line2>)

"command! -nargs=? -bar -range=% -bang -complete=customlist,neotemplate#CompleteTemplates Neotemplate
"            \ call neotemplate#Neotemplate(<bang>0, <q-args>, <line1>, <line2>)
"-----------------------------------------------------------------------------
let &cpo= s:keepcpo
unlet s:keepcpo

" vim: ts=3
